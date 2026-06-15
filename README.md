# Liquid-Check for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
![Version](https://img.shields.io/github/v/release/shivan/homeassistant-liquidcheck)

Home Assistant integration for **Liquid-Check**, a high-precision water level meter for cisterns and tanks.

<p align="center">
  <img src="https://raw.githubusercontent.com/shivan/homeassistant-liquidcheck/main/brand/logo.png" width="150">
</p>

## Features

- **Real-time Monitoring:** Track water level (m), volume (L), and percentage (%).
- **Connectivity Status:** Monitor device health and signal strength.
- **Easy Setup:** Full support for Home Assistant Config Flow (UI-based configuration).
- **Service Integration:** Trigger manual measurements via Home Assistant services.

## Upgrade

Upgrade for 1.x to 2.x needs re-installation because of major changes. Please uninstall the integration and then re-install.

Unfortunately there is no clean upgrade path without a fresh installation. (at least not without breaking hassfest or hacs checks)

## Installation

Version 2.x Requires Home Assistant 2025.6.0 or newer.

### Option 1: HACS (Recommended)

1. Open **HACS** in Home Assistant.
2. Go to **Integrations**.
3. Click the three dots in the top right and select **Custom repositories**.
4. Add `https://github.com/shivan/homeassistant-liquidcheck` as an **Integration**.
5. Search for "Liquid-Check" and click **Download**.
6. Restart Home Assistant.

### Option 2: Manual

1. Download the latest release.
2. Copy the `custom_components/liquid_check` folder into your Home Assistant `<config>/custom_components/` directory.
3. Restart Home Assistant.

## Configuration

1. In Home Assistant, go to **Settings** > **Devices & Services**.
2. Click **Add Integration** and search for **Liquid-Check**.
3. Enter the IP address or hostname of your Liquid-Check device.

---

*For more information about the hardware, visit [liquid-check-info.si-elektronik.de](https://liquid-check-info.si-elektronik.de/).*
