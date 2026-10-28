# Changelog

Changes in this fork on top of [davidrapan/ha-solarman](https://github.com/davidrapan/ha-solarman) `main`
(based on upstream `ac1d88b`, 2026-05-03). For upstream history see its
[releases](https://github.com/davidrapan/ha-solarman/releases).

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Issue numbers like
davidrapan#1186 refer to upstream issues and pull requests.

## [Unreleased]

## [v26.10.28] - 2026-10-28

### Added
- This changelog.

## [v26.10.25_2] - 2026-10-25

Ported from open upstream pull requests.

### Added
- Russian translation (davidrapan#1067), including the fork-only *Minimum poll interval* option.
- `category: diagnostic` in profiles creates diagnostic entities (davidrapan#938).
- `reverse_bytes` option for string registers (davidrapan#931).

### Fixed
- Entities disabled by the profile can be enabled from the UI (davidrapan#939).
- `deye_p3`: byte-swapped battery BMS serial numbers (davidrapan#931, davidrapan#1099).
- `deye_hybrid`, `deye_p3`: signed Zero Export power (davidrapan#1048).
- `deye_p3`: larger export surplus limit (davidrapan#1150).
- `deye_hybrid`: TOU program power limits raised from 12000 to 16000 (davidrapan#1033).
- `deye_p3`: battery power sums BMS1 and BMS2 in dual BMS parallel mode (davidrapan#1061).

## [v26.10.25_1] - 2026-10-25

### Added
- Translations: Spanish and Galician (davidrapan#1194), Slovak (davidrapan#1164), including the fork-only
  *Minimum poll interval* option.

## [v26.10.25] - 2026-10-25

### Changed
- Setup works while the device is offline (e.g. after an HA restart at night): the selected profile is used
  instead of autodetection (the entry reloads once the device answers), validation lookups are applied on the
  first data, and `offline_value`/`persistent` sensors show `0 W` / their last value instead of `unavailable`.
- `deye_micro`: Device State reports *Offline* while the inverter is offline.

## [v26.10.23_7] - 2026-10-23

### Added
- New option *Additional options → Minimum poll interval* (seconds, `0` = profile default): registers are read
  no more often than this; slower profile intervals (e.g. hourly device info) are kept. Rounded up to a multiple
  of 5 s.

## [v26.10.23_6] - 2026-10-23

### Fixed
- pysolarman: logger serials below 2^31 are accepted in the V5 frame (old LSW-3 `17xxxxxxxx` loggers never
  answer a placeholder serial), fixes davidrapan#1186.
- `deye_p3`: HV raw range minimum `[3800, 380]` so battery voltages below 380 V are not rejected,
  fixes davidrapan#1180.
- Number entities round before truncating (`160.1 / 0.1` → `1601`, not `1600`), fixes davidrapan#1180.
- Nested battery devices link to their parent with `via_device_id` on HA 2026.8+ (`via_device` is deprecated and
  removed in 2027.8), fixes davidrapan#1149.
- `total_increasing` counters dropping to near zero re-anchor the baseline instead of failing forever
  (ported from thiagofigueiro/ha-solarman), fixes davidrapan#1148.
- `deye_p3`: Grid Power Factor is S16 × 0.001 (−1..1) (ported from jverhoeven/ha-solarman), fixes
  davidrapan#1145.
- Services accept address/register/count `0` (ported from jverhoeven/ha-solarman).

## [v26.10.23_5] - 2026-10-23

### Changed
- Ported from Micka41/ha-solarman: `asyncio.Event` instead of `multiprocessing.Event` in pysolarman,
  non-blocking profile directory listing (davidrapan#1071), `render_readme` in `hacs.json`.

## [v26.10.23_4] - 2026-10-23

### Added
- New profile option `offline_value: <value>`: the sensor stays available and reports that value while the
  device is offline. `deye_micro` uses `offline_value: 0` for Power, PV Power and PV1-4 Power.

## [v26.10.23_3] - 2026-10-23

### Changed
- Ported from Micka41/ha-solarman: non-deprecated device registry API in discovery (HA 2027.8), iterative
  reconnect with backoff instead of recursion.

## [v26.10.23_2] - 2026-10-23

### Changed
- Manifest `codeowners` set to the fork maintainer.

## [v26.10.23_1] - 2026-10-23

### Added
- Brand icon (MDI `solar-power`, Apache-2.0, Pictogrammers).

## [v26.10.23] - 2026-10-23

### Changed
- Restore/persistent sensors keep their last value when a poll yields no value (e.g. a reading rejected by
  validation while a micro-inverter powers down at dusk) instead of switching to `unknown`.
- `deye_micro`: `Device` and `Today Production*` are `persistent`; Device State lookup 2/4 swapped for logger
  firmware MW3_SSL_5408_1.0B (davidrapan#342).

### Fixed
- The real error is no longer masked when a poll fails during setup (before the profile is created).

[Unreleased]: https://github.com/StefanRiese/ha-solarman/compare/v26.10.28...HEAD
[v26.10.28]: https://github.com/StefanRiese/ha-solarman/compare/v26.10.25_2...v26.10.28
[v26.10.25_2]: https://github.com/StefanRiese/ha-solarman/compare/v26.10.25_1...v26.10.25_2
[v26.10.25_1]: https://github.com/StefanRiese/ha-solarman/compare/v26.10.25...v26.10.25_1
[v26.10.25]: https://github.com/StefanRiese/ha-solarman/compare/v26.10.23_7...v26.10.25
[v26.10.23_7]: https://github.com/StefanRiese/ha-solarman/compare/v26.10.23_6...v26.10.23_7
[v26.10.23_6]: https://github.com/StefanRiese/ha-solarman/compare/v26.10.23_5...v26.10.23_6
[v26.10.23_5]: https://github.com/StefanRiese/ha-solarman/compare/v26.10.23_4...v26.10.23_5
[v26.10.23_4]: https://github.com/StefanRiese/ha-solarman/compare/v26.10.23_3...v26.10.23_4
[v26.10.23_3]: https://github.com/StefanRiese/ha-solarman/compare/v26.10.23_2...v26.10.23_3
[v26.10.23_2]: https://github.com/StefanRiese/ha-solarman/compare/v26.10.23_1...v26.10.23_2
[v26.10.23_1]: https://github.com/StefanRiese/ha-solarman/compare/v26.10.23...v26.10.23_1
[v26.10.23]: https://github.com/StefanRiese/ha-solarman/compare/ac1d88b...v26.10.23
