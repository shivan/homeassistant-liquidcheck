# Liquid-Check integration details

Home Assistant custom integration for **Liquid-Check** water level devices.

Device information:
https://liquid-check-info.si-elektronik.de/

## Installation

### HACS

1. Open **HACS**.
2. Click **Explore & Download Repositories**.
3. Search for **Liquid-Check**.
4. Download and restart Home Assistant.

### Manual

Copy the integration folder to:

`<config_dir>/custom_components/liquid_check/`

Then restart Home Assistant.

## Setup

Set up via Home Assistant UI.

Configurable options:

- Host/IP
- `scan_interval` (seconds)

After setup, Host/IP and `scan_interval` can be changed via:

- **Settings → Devices & Services → Liquid-Check → Configure**

## Exposed values

- Firmware version
- Hardware version
- Level (%)
- Water level (m)
- Content (L)
- Last measurement age (duration)
- Error code
- Tank max level
- System uptime
- Pump total runs
- Pump total runtime
- Wi-Fi signal (RSSI)
- Wi-Fi SSID

## Trigger measurement

### Service

`liquid_check.start_measure`

- Without `entry_id`: triggers all configured devices
- With `entry_id`: triggers one specific device
- After triggering, values are refreshed automatically after ~10 seconds

Example:

```yaml
action:
  - service: liquid_check.start_measure
    data:
      entry_id: "01J..."
```

### Button entity

A button entity is created for each configured device to trigger a measurement directly from the UI.
After pressing the button, values are refreshed automatically after ~10 seconds.

## Quick file guide

- `__init__.py`: setup, service registration, delayed refresh for service call
- `button.py`: button entity + delayed refresh after press
- `sensor.py`: sensor entities and payload mapping
- `const.py`: sensor definitions and constants
- `translations/de.json`, `translations/en.json`: entity name translations
- `manifest.json`: integration version and requirements
