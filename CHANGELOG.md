# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

- No changes yet.

## [1.1.2] - 2026-06-15

### Changed

- Config Flow unique device identification now uses `uuid` with Host/IP fallback
- Duplicate add attempts no longer rely on broader ID field matching

## [1.1.1] - 2026-06-15

### Added

- Integration options now support editing Host/IP in addition to polling interval
- Option labels for Host/IP added in DE/EN translations

### Changed

- Options dialog uses Home Assistant selector fields for reliable input behavior
- Setup now respects Host/IP from integration options after reload

## [1.1.0] - 2026-06-15

### Added

- Options Flow to change polling interval (`scan_interval`) after setup
- New translations for integration options (DE/EN)

### Changed

- Shared base entity class for consistent device metadata across sensors and button
- Concurrent execution for multi-device `liquid_check.start_measure` service calls and refreshes

## [1.0.0] - 2026-06-11

### Added

- Home Assistant custom integration for Liquid-Check (`liquid_check`)
- Config Flow setup with configurable polling interval
- Sensor entities for level, content, age, error, firmware, hardware, tank max level, uptime, pump stats, and Wi-Fi stats
- Service `liquid_check.start_measure`
- Button entity to trigger measurement from the UI
- Automatic delayed refresh (~10 seconds) after triggering a measurement
- German/English translations for entities

### Changed

- Clean initial baseline for this standalone repository
- Stable key-based `unique_id` strategy
- No legacy migration logic in this baseline
