"""Runtime monkey-patch for Q10Status.

Extends the python-roborock library's Q10Status dataclass with additional
DPS fields for consumables, fault codes, and lifetime statistics.

This patch is applied at import time by __init__.py so that the
DpsDataConverter picks up the new fields before the coordinator starts.
"""

import dataclasses
import logging

_LOGGER = logging.getLogger(__name__)

_Q10_EXTRA_FIELDS = [
    ("main_brush_life", "MAIN_BRUSH_LIFE"),
    ("side_brush_life", "SIDE_BRUSH_LIFE"),
    ("filter_life", "FILTER_LIFE"),
    ("sensor_life", "SENSOR_LIFE"),
    ("rag_life", "RAG_LIFE"),
    ("fault", "FAULT"),
    ("total_clean_area", "TOTAL_CLEAN_AREA"),
    ("total_clean_count", "TOTAL_CLEAN_COUNT"),
    ("total_clean_time", "TOTAL_CLEAN_TIME"),
    ("mop_state", "MOP_STATE"),
]


def apply() -> None:
    """Patch Q10Status with additional DPS fields and rebuild the converter."""
    try:
        from roborock.data.b01_q10.b01_q10_containers import Q10Status
        from roborock.data.b01_q10.b01_q10_code_mappings import B01_Q10_DP
        from roborock.devices.traits.b01.q10 import status as q10_status_mod
        from roborock.devices.traits.b01.q10.common import DpsDataConverter
    except ImportError:
        _LOGGER.warning("Could not import Q10 modules for patching - skipping")
        return

    existing_fields = list(Q10Status.__dataclass_fields__.values())
    if not existing_fields:
        _LOGGER.warning("Q10Status has no fields - skipping patch")
        return
    field_type_sentinel = existing_fields[0]._field_type

    patched = 0
    for name, dps_name in _Q10_EXTRA_FIELDS:
        if name in Q10Status.__dataclass_fields__:
            continue
        dps_id = getattr(B01_Q10_DP, dps_name, None)
        if dps_id is None:
            _LOGGER.debug("B01_Q10_DP.%s not found - skipping field %s", dps_name, name)
            continue
        f = dataclasses.field(default=None, metadata={"dps": dps_id})
        f.name = name
        f._field_type = field_type_sentinel
        Q10Status.__dataclass_fields__[name] = f
        setattr(Q10Status, name, None)
        patched += 1

    if patched > 0:
        q10_status_mod._CONVERTER = DpsDataConverter.from_dataclass(Q10Status)
        _LOGGER.debug("Patched Q10Status with %d additional DPS fields", patched)
