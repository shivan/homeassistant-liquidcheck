# Comparison to `shivan/homeassistant-liquidcheck` (upstream/main)

Purpose: This note documents **what** was changed compared to upstream and **why** the implementation intentionally differs.

Reference:
- Upstream base: `upstream/main` (`98ccbf2`)
- Fork base: `origin/main` (`98414c2`)
- Clean sync commit: `684b4b7`

## 1) Metadata and releases

### Changed
- `custom_components/liquid_check/manifest.json`
- `hacs.json`
- `CHANGELOG.md`
- `README.md`, `info.md`

### Why
- Fork-specific ownership, repository links, and versioning must be accurate.
- Minimum Home Assistant version was raised to `2026.6.0` to match the fork's feature/API level.
- Release history and documentation were expanded for clearer installation, options, and entity behavior.

---

## 2) Configuration and options flow

### Changed
- `custom_components/liquid_check/config_flow.py`

### Why
- Host/IP and polling interval need to be editable after initial setup (Options Flow).
- Validating options against the device (`/infos.json`) reduces misconfiguration risk.
- `unique_id` generation prioritizes `uuid` (host fallback) for more stable device matching.
- No implicit host update during duplicate-add attempts; host changes are handled explicitly through options.

---

## 3) Setup, reload behavior, and service handling

### Changed
- `custom_components/liquid_check/__init__.py`
- `custom_components/liquid_check/services.yaml`

### Why
- Option changes should reliably take effect via integration reload (`update_listener`).
- Service `liquid_check.start_measure` supports targeted triggering via `entry_id` or all configured devices.
- Trigger + refresh uses a defined delay (~10s) so fresh measurements are available when entities update.
- Service schema adds stronger input validation.

---

## 4) Entity model (sensor + button)

### Changed
- Added: `custom_components/liquid_check/entity.py`
- Added: `custom_components/liquid_check/button.py`
- Updated: `custom_components/liquid_check/sensor.py`
- Updated: `custom_components/liquid_check/const.py`

### Why
- A shared base entity removes duplicated logic and keeps `device_info` consistent.
- A dedicated button entity allows manual measurement start directly in the UI.
- Sensors were extended with diagnostics (hardware, Wi-Fi, pump stats, uptime, tank max level).
- Precision/state class/entity category were adjusted for better Home Assistant compliance.
- Integer rounding for selected runtime/counter values improves UI consistency.

---

## 5) Translations and UX

### Changed
- `custom_components/liquid_check/strings.json`
- `custom_components/liquid_check/translations/en.json`
- `custom_components/liquid_check/translations/de.json`

### Why
- Complete naming coverage for new entities/buttons/services in EN/DE.
- Clearer wording in configuration and options dialogs.

---

## 6) CI and repository layout

### Changed
- `.github/workflows/hacs.yaml`
- `.github/workflows/hassfest.yaml`
- `.github/workflows/codeql-analysis.yml` (removed)
- `.gitignore`
- Asset/path updates (`brand`/`img`/`docs`)

### Why
- CI was aligned with the fork's intentionally lean maintenance scope.
- Ignore rules reduce accidental local artifact commits.
- Docs/assets were aligned with current README structure and presentation.

---

## Notes for the PR description

The PR should state explicitly:
1. This is **not a 1:1 upstream mirror sync**, but an intentional fork-specific alignment.
2. Focus on **Home Assistant usability** (options flow, service UX, button entity).
3. Focus on **maintainability** (shared base entity, clearer docs/translations).
4. Potential breaking points are documented transparently (versions, IDs, CI setup).
