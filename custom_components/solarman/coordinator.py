from __future__ import annotations

from logging import getLogger
from itertools import count
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import *
from .common import *
from .device import Device
from .provider import ConfigurationProvider

_LOGGER = getLogger(__name__)

class Coordinator(DataUpdateCoordinator[dict[str, tuple[int | float | str | list, int | float | None]]]):
    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry[Coordinator]):
        self.device = Device(ConfigurationProvider(hass, config_entry))
        self._deferred_validations = []
        super().__init__(hass, _LOGGER, config_entry = config_entry, name = "", update_interval = TIMINGS_UPDATE_INTERVAL, always_update = False)

    @DataUpdateCoordinator.update_interval.setter
    def update_interval(self, value: timedelta | None):
        DataUpdateCoordinator.update_interval.fset(self, value)
        self.counter = self._update_interval_seconds

    @property
    def name(self):
        return self.device.config.name

    @name.setter
    def name(self, _: str):
        pass

    @property
    def counter(self):
        return self._counter_value

    @counter.setter
    def counter(self, value: int | float):
        self._counter = count(0, int(value))
        self._counter_value = next(self._counter)

    async def _async_setup(self):
        await super()._async_setup()
        try:
            await self.device.setup()
        except TimeoutError:
            raise
        except Exception as e:
            raise UpdateFailed(strepr(e)) from e

    async def _async_update_data(self):
        try:
            return await self.device.get(self.counter)
        except TimeoutError:
            raise
        except Exception as e:
            raise UpdateFailed(strepr(e)) from e

    def _async_refresh_finished(self):
        super()._async_refresh_finished()
        if self.data:
            if self.device.profile.undetected:
                # Set up offline with the selected profile instead of the autodetected one: reload to run the autodetection now
                self.device.profile.undetected = False
                self.hass.config_entries.async_schedule_reload(self.config_entry.entry_id)
            if self._deferred_validations:
                # First data after an offline setup: apply the validation limits that need a read value (e.g. rated power)
                self._deferred_validations = [v for v in self._deferred_validations if not postprocess_validation(self, v)]
            self._counter_value = next(self._counter)
        elif not self.last_update_success:
            self.counter = self._update_interval_seconds

    async def init(self):
        try:
            await super().async_config_entry_first_refresh()
        except ConfigEntryNotReady as e:
            # Device offline at startup (e.g. a micro-inverter at night): with a fixed profile the entities can be built without data,
            # so set up anyway - offline_value and persistent sensors then show 0 W or their last value instead of unavailable
            # Unreachable at the first connect is a ConnectionError wrapped in UpdateFailed, a silent device is a TimeoutError
            cause = e.__cause__.__cause__ if isinstance(e.__cause__, UpdateFailed) else e.__cause__
            if not isinstance(cause, (TimeoutError, ConnectionError)) or self.device.profile is None or self.device.profile.parser is None or requires_data(self.device.profile.parser.get_entity_descriptions()):
                raise
            _LOGGER.debug(f"[{self.device.endpoint.host}] {self.name} is offline, setting up without initial data")
            self.data = {}
        serial_number, _ = self.data.get(slugify("device", "serial", "number", "sensor"), (str(self.device.modbus.serial) if self.device.modbus.serial > 0 else None, None))
        if serial_number is None and (device := next((d for d in dr.async_entries_for_config_entry(dr.async_get(self.hass), self.config_entry.entry_id) if (DOMAIN, self.config_entry.entry_id) in d.identifiers), None)):
            # Keep the known serial number in the device registry while the device is offline
            serial_number = device.serial_number
        device_info = build_device_info(self.config_entry.entry_id, serial_number, self.device.endpoint.mac, self.device.endpoint.host, self.device.profile.info, self.device.config.name)
        self.device.info[self.config_entry.entry_id] = device_info
        self._deferred_validations = postprocess_descriptions(self)
        _LOGGER.debug(device_info)
        return self

    async def async_shutdown(self):
        await super().async_shutdown()
        try:
            await self.device.shutdown()
        except Exception as e:
            _LOGGER.exception(f"Unexpected error shutting down {self.name}")
