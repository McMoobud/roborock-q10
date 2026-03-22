# Roborock Q10 S5+ — Home Assistant Custom Component

Adds full support for the **Roborock Q10 S5+** (B01 series, model `roborock.vacuum.ss07`) to Home Assistant.

The official Roborock integration detects Q10 devices but doesn't support them. This custom component patches the core integration to add:

- **Vacuum entity** with start/stop/pause/dock/locate/fan speed controls
- **Battery sensor** (0-100%)
- **Cleaning sensors** — current clean time, area, progress
- **Lifetime stats** — total clean area, count, and time
- **Consumable sensors** — main brush, side brush, filter, sensor, and mop pad life (%)
- **Fault sensor** — error code reporting

## Installation

### HACS (Recommended)

1. In HACS, go to **Integrations > ⋮ menu > Custom Repositories**
2. Add `McMoobud/roborock-q10` as an **Integration**
3. Search for "Roborock Q10" and install
4. Restart Home Assistant
5. Add the Roborock integration via **Settings > Devices & Services > Add Integration**

### Manual

1. Copy the `custom_components/roborock/` folder from this repo into your HA `config/custom_components/` directory
2. Restart Home Assistant
3. Add the Roborock integration via **Settings > Devices & Services > Add Integration**

### After Installation

- If you previously dismissed the Roborock DHCP discovery, delete the ignored config entry first (Settings > Devices & Services > Roborock > delete ignored entry)
- Sign in with your Roborock cloud account — your Q10 should be detected and set up automatically

## How It Works

This custom component overrides the official Roborock integration and adds:

1. **Q10 coordinator** (`RoborockB01Q10UpdateCoordinator`) — MQTT-based status updates via `Q10PropertiesApi`
2. **Q10 vacuum entity** (`RoborockQ10Vacuum`) — maps `YXDeviceState` to HA vacuum activities
3. **Q10 sensors** — battery, cleaning stats, consumables, fault codes
4. **Runtime library patch** (`q10_patch.py`) — extends `Q10Status` with additional DPS fields at runtime, no manual library modification needed

The Q10 uses a different protocol (YX/B01) from older Roborock models (V1/RPC). The `python-roborock` library already has Q10 support via `Q10PropertiesApi`, but the core HA integration hadn't wired it up.

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

## Vacuum Controls

| Action | Description |
|--------|-------------|
| Start | Begin a full clean |
| Pause | Pause current clean |
| Stop | Stop current clean |
| Return to dock | Send vacuum back to charging dock |
| Locate | Make the vacuum beep to find it |
| Set fan speed | `close`, `quiet`, `normal`, `strong`, `max`, `super` |

## Notes

- When HA core adds native Q10 support, **remove this custom component** to avoid conflicts
- The custom component overrides the entire core Roborock integration — other Roborock models will continue to work normally
- Room-specific cleaning is not yet supported
- Consumable values are percentages (not hours like V1 models)

## Credits

See [CREDITS.md](CREDITS.md) for full attribution to the original contributors.
