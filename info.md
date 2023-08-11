# homeassistant-liquidcheck

Home Assistant Component for liquid-check. Liquid-Check is a water level meter for cisterns. See https://liquid-check-info.si-elektronik.de/ for more information. 

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

## Installation

### Using HACS

> HACS is a community store for integrations, Frontend extensions, etc. It makes installation and maintenance of this component much easier. You can find instructions on how to install HACS [here](https://hacs.xyz/).

Navigate to HACS in you Home Assistants Interface.

Click "Explore & Download Repositories"

Search for "Liquid-Check"

Click "Download this Repository with HACS".

Select the version you wish do download and finally click "Download".

Restart Home Assistant.

### Manual installation

Copy this folder to `<config_dir>/custom_components/liquid-check/`.

Restart Home Assistant.

## Configuration

The integration is configurated via UI.

Provided values are:

* firmware version
* measure in percent
* measure in meters
* content in liters
* age 
* error