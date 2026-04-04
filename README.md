# Roborock Q10 S5+ Custom Component for Home Assistant

Custom integration for the **Roborock Q10 S5+** (B01 series) that adds Q10 sensor entities missing from the core Home Assistant integration.

## Why This Exists

As of HA 2026.4.1, the core Roborock integration supports Q10 vacuum control, buttons, switches, selects, and numbers natively via `python-roborock 5.0.0`. However, **Q10 sensor entities** (battery, cleaning stats, consumables) are not yet implemented in the core `sensor.py`.

This custom component is a copy of the HA 2026.4.1 core integration with one addition: Q10 sensor descriptions and a push-based sensor entity class in `sensor.py`.

**When the core integration adds Q10 sensor support, this custom component can be removed.**

## Supported Sensors

| Sensor | Unit | Description |
|--------|------|-------------|
| Battery | % | Current battery level |
| Cleaning time | minutes | Duration of last/current clean |
| Cleaning area | m² | Area covered in last/current clean |
| Total cleaning area | m² | Lifetime total area cleaned |
| Total cleaning count | count | Lifetime total cleans |
| Total cleaning time | hours | Lifetime total cleaning duration |
| Main brush life | % | Main brush remaining life |
| Side brush life | % | Side brush remaining life |
| Filter life | % | Filter remaining life |
| Sensor life | % | Sensor remaining life |
| Cleaning progress | % | Current cleaning progress |

## Requirements

- Home Assistant **2026.4.x** or later
- `python-roborock >= 5.0.0` (installed automatically)
- Roborock Q10 S5+ already configured in HA (via the built-in Roborock integration)

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to **Integrations** → **Custom repositories**
3. Add this repository URL: `https://github.com/McMoobud/roborock-q10`
4. Select category: **Integration**
5. Click **Download**
6. Restart Home Assistant

### Manual

1. Copy the `custom_components/roborock/` folder to your HA `/config/custom_components/roborock/` directory
2. Restart Home Assistant

> **Note:** This replaces the built-in Roborock integration entirely. All core functionality is preserved since the component is based on the same 2026.4.1 source files.

## Upgrading from v2026.3.2-q10

The previous version used a `q10_patch.py` monkey-patch for `python-roborock 4.17.1`. That approach is **no longer needed** — `python-roborock 5.0.0` has native Q10 support with 20 status fields.

To upgrade:

1. Replace your `custom_components/roborock/` folder with this version
2. Delete `q10_patch.py` if it still exists
3. Restart Home Assistant

The `pyrate-limiter` breaking change (`BucketFullException` removed in v4.x) means the old component **will not load** on HA 2026.4.x.

## How It Works

The Q10 uses MQTT push-based status updates (not polling). The custom component adds:

- `RoborockSensorDescriptionQ10` — dataclass for Q10 sensor descriptions
- `RoborockSensorEntityQ10` — entity class with trait listeners on `coordinator.api.status` for real-time push updates
- `Q10_SENSOR_DESCRIPTIONS` — 11 sensor definitions covering battery, cleaning stats, and consumables

All other integration functionality (vacuum control, buttons, switches, selects, numbers, images, binary sensors, time entities) comes directly from the HA 2026.4.1 core code.

## Architecture

```
sensor.py (patched)
├── Core V1 sensors (unchanged)
├── Core A01 sensors (unchanged)
├── Core B01 Q7 sensors (unchanged)
└── Q10 sensors (ADDED)
    ├── RoborockSensorDescriptionQ10
    ├── Q10_SENSOR_DESCRIPTIONS (11 sensors)
    └── RoborockSensorEntityQ10 (push-based via MQTT trait listeners)
```

## Credits

- **Home Assistant Core Team** — base Roborock integration (2026.4.1)
- **@Lash-L, @allenporter** — `python-roborock` library and core integration maintainers
- Q10 sensor patch by McMoobud with Craft Agent
