# Roborock Q10 S5+ — Home Assistant Custom Component

Adds full support for the **Roborock Q10 S5+** (B01 series, model `roborock.vacuum.ss07`) to Home Assistant.

The official Roborock integration detects Q10 devices but doesn't support them. This custom component patches the core integration to add:

- **Vacuum entity** with start/stop/pause/dock/locate/fan speed controls
- **Battery sensor** (0-100%)
- **Cleaning sensors** — current clean time, area, progress
- **Lifetime stats** — total clean area, count, and time
- **Consumable sensors** — main brush, side brush, filter, sensor, and mop pad life (%)
- **Fault sensor** — error code reporting

## How It Works

This custom component copies the official Roborock integration and adds:
1. **Q10 coordinator** (`RoborockB01Q10UpdateCoordinator`) — MQTT-based status updates via `Q10PropertiesApi`
2. **Q10 vacuum entity** (`RoborockQ10Vacuum`) — maps `YXDeviceState` to HA vacuum activities
3. **Q10 sensors** — battery, cleaning stats, consumables, fault codes
4. **Runtime library patch** — extends `Q10Status` with additional DPS fields for consumables and stats

The Q10 uses a different protocol (YX/B01) from older Roborock models (V1/RPC). The `python-roborock` library already supports Q10 via `Q10PropertiesApi`, but the core HA integration hadn't wired it up.

## Installation

### Method 1: HACS (Recommended)
1. Add this repo as a [custom HACS repository](https://hacs.xyz/docs/faq/custom_repositories)
2. Search for "Roborock Q10" and install
3. Restart Home Assistant

### Method 2: Manual
1. Copy the `custom_components/roborock/` folder to your HA `config/custom_components/` directory
2. Restart Home Assistant
3. The custom component will override the core Roborock integration

### After Installation
- If you previously dismissed the Roborock DHCP discovery, delete the ignored config entry first
- Add the Roborock integration normally — your Q10 should now be detected and set up

## Requirements

- Home Assistant 2026.3+
- `python-roborock >= 4.17.1`
- Roborock cloud account (for initial auth)

## Entities Created

| Entity | Type | Description |
|--------|------|-------------|
| `vacuum.roborock_q10_s5` | Vacuum | Main vacuum entity with full controls |
| `sensor.*_battery` | Sensor | Battery level (%) |
| `sensor.*_cleaning_time` | Sensor | Current clean session time |
| `sensor.*_cleaning_area` | Sensor | Current clean session area (m²) |
| `sensor.*_cleaning_progress` | Sensor | Current clean progress (%) |
| `sensor.*_total_clean_area` | Sensor | Lifetime total area cleaned |
| `sensor.*_total_clean_count` | Sensor | Lifetime total clean count |
| `sensor.*_total_clean_time` | Sensor | Lifetime total cleaning time |
| `sensor.*_main_brush_life` | Sensor | Main brush remaining life (%) |
| `sensor.*_side_brush_life` | Sensor | Side brush remaining life (%) |
| `sensor.*_filter_life` | Sensor | Filter remaining life (%) |
| `sensor.*_sensor_life` | Sensor | Sensor remaining life (%) |
| `sensor.*_mop_life` | Sensor | Mop pad remaining life (%) |
| `sensor.*_fault` | Sensor | Fault/error code (when active) |

## Notes

- When HA core adds native Q10 support, **remove this custom component** to avoid conflicts
- The custom component overrides the entire core Roborock integration
- Room-specific cleaning is not yet supported (Q10's `START_CLEAN` with `cmd: 2` needs room ID mapping)
- Consumable values are percentages (not hours like V1 models)

## Credits

- [python-roborock](https://github.com/Python-roborock/python-roborock) — the Q10 API support already existed in the library
- [Home Assistant Roborock integration](https://github.com/home-assistant/core/tree/dev/homeassistant/components/roborock) — base integration
- [Feature request discussion](https://github.com/home-assistant/core/issues/144138) — community demand for Q10 support
