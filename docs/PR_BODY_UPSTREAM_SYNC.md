## Summary

This PR ports fork-specific changes from `7weazel7/homeassistant-liquidcheck` onto current `shivan/homeassistant-liquidcheck` (`upstream/main`) in one clean commit.

## Why these changes exist

This is **not** a pure mirror sync. The fork intentionally differs in several areas:
- Home Assistant UX improvements (options flow, service behavior, button entity)
- Additional diagnostics/entities and translation coverage
- Fork-specific metadata/versioning/docs/CI alignment

## What changed

### Integration behavior
- Added options flow (`host`, `scan_interval`) with connectivity validation
- Added update-listener based reload when options change
- Improved service `liquid_check.start_measure` handling (`entry_id` support, delayed refresh)
- Added button entity to trigger measurements from UI

### Entity model
- Introduced shared base entity class for consistent `device_info`
- Expanded sensor set (hardware, Wi-Fi, uptime, pump stats, tank max level)
- Added translation keys, diagnostic categories, and precision hints

### Metadata and docs
- Updated `manifest.json` ownership/links/version and integration metadata
- Updated `hacs.json` minimum HA version
- Expanded README/info docs and added changelog/history

### CI/repo housekeeping
- Adjusted HACS/Hassfest workflows to fork preferences
- Removed unused workflow and cleaned repo ignore/asset structure

## Compatibility / reviewer notes

- Changes are intentional fork behavior, not only formatting.
- Please review `docs/UPSTREAM_DIFF_AND_RATIONALE.md` for per-file rationale.

## Validation checklist

- [ ] Integration setup works via Config Flow
- [ ] Options update (`host`, `scan_interval`) reloads correctly
- [ ] Service call works for one `entry_id` and all entries
- [ ] Button entity triggers measure and refreshes values
- [ ] Translations (DE/EN) resolve correctly
- [ ] HACS/Hassfest pass
