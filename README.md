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
4. **Runtime library patch** — extends `Q10Status` with additional DPS fields for consumables and stats (no manual library modification needed)

The Q10 uses a different protocol (YX/B01) from older Roborock models (V1/RPC). The `python-roborock` library already supports Q10 via `Q10PropertiesApi`, but the core HA integration hadn't wired it up.

## Installation

### Prerequisites

- Home Assistant 2026.3+ with the core Roborock integration files present
- A Roborock cloud account (needed for initial authentication)
- Your Q10 S5+ set up and working in the Roborock app

### Method 1: Install Script (Recommended)

1. **SSH into your Home Assistant instance** (or use the Terminal add-on)

2. **Clone this repo:**
   ```bash
   cd /tmp
   git clone https://github.com/McMoobud/roborock-q10.git
   cd roborock-q10
   ```

3. **Run the install script:**
   ```bash
   chmod +x install.sh
   ./install.sh /config
   ```
   This copies the core Roborock integration into `custom_components/roborock/` and overlays the Q10 patches on top.

4. **Restart Home Assistant:**
   - Go to **Settings > System > Restart**
   - Or run: `ha core restart`

5. **Add the Roborock integration:**
   - Go to **Settings > Devices & Services > Add Integration**
   - Search for **Roborock** and follow the setup flow
   - Sign in with your Roborock cloud account
   - Your Q10 S5+ should be detected and set up automatically

### Method 2: HACS

1. In HACS, go to **Integrations > 3-dot menu > Custom Repositories**
2. Add `McMoobud/roborock-q10` as an **Integration**
3. Search for "Roborock Q10" and install it
4. **Important:** After HACS downloads the files, you still need the unmodified core files. SSH in and run:
   ```bash
   cp -rn /usr/lib/python3.*/site-packages/homeassistant/components/roborock/* /config/custom_components/roborock/
   ```
   (The `-n` flag means "no clobber" — it won't overwrite the Q10-patched files)
5. Restart Home Assistant
6. Add the Roborock integration via **Settings > Devices & Services**

### Method 3: Manual

1. **Copy the core integration** to custom_components:
   ```bash
   mkdir -p /config/custom_components/roborock
   cp -r /usr/lib/python3.*/site-packages/homeassistant/components/roborock/* /config/custom_components/roborock/
   ```

2. **Download and overlay the Q10 files** from this repo's `custom_components/roborock/` folder:
   - `__init__.py` — Q10 device detection + runtime patch loading
   - `q10_patch.py` — Runtime library patch (extends Q10Status with extra DPS fields)
   - `coordinator.py` — Q10 MQTT coordinator
   - `entity.py` — Q10 base entity class
   - `vacuum.py` — Q10 vacuum entity
   - `sensor.py` — Q10 sensor entities
   - `manifest.json` — Updated version

3. Restart Home Assistant and add the Roborock integration

### Troubleshooting

**"Integration not found" or Q10 not detected:**
- Make sure you copied ALL the core integration files first, then overlaid the Q10 patches
- Check that `custom_components/roborock/` has ~20+ files (not just the 7 from this repo)

**"Ignored" config entry from previous DHCP discovery:**
- Go to **Settings > Devices & Services > Roborock**
- Delete any entries with source "ignore"
- Re-add the integration

**Sensors showing "unavailable":**
- The Q10 uses MQTT subscriptions — sensors populate after the first status update (usually within 30 seconds)
- Check the HA logs for `roborock` entries if sensors don't appear

## Requirements

- Home Assistant 2026.3+
- `python-roborock >= 4.17.1` (included with HA 2026.3+)
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
- Room-specific cleaning is not yet supported (Q10's `START_CLEAN` with `cmd: 2` needs room ID mapping)
- Consumable values are percentages (not hours like V1 models)
- The runtime patch (`q10_patch.py`) automatically extends the `python-roborock` library — no manual library modification needed

## Credits

- [python-roborock](https://github.com/Python-roborock/python-roborock) — the Q10 API support already existed in the library
- [Home Assistant Roborock integration](https://github.com/home-assistant/core/tree/dev/homeassistant/components/roborock) — base integration
- [Feature request discussion](https://github.com/home-assistant/core/issues/144138) — community demand for Q10 support
