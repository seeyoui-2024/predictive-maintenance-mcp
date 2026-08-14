"""
ISO 13374 Block 6 — Decision Support: Maintenance Recommendations.

Rule-based recommendation engine for vibration-based maintenance decisions.
"""

from __future__ import annotations

from ..diagnostics.bearing_analyzer import FAULT_TYPE_CANONICAL
from ..i18n import t

# Mapping from fault type keyword to translation key for maintenance advice.
# Bearing keys are the canonical fault vocabulary (bearing_analyzer
# FAULT_TYPE_CANONICAL values); the rest are machine-level faults.
_FAULT_RECOMMENDATIONS: dict[str, str] = {
    "outer_race": "rec.fault.outer_race",
    "inner_race": "rec.fault.inner_race",
    "ball": "rec.fault.ball",
    "cage": "rec.fault.cage",
    "misalignment": "rec.fault.misalignment",
    "unbalance": "rec.fault.unbalance",
    "looseness": "rec.fault.looseness",
}

# The bearing part of the vocabulary MUST mirror the canonical fault types
# produced by check_bearing_faults / diagnose_vibration.
assert set(FAULT_TYPE_CANONICAL.values()) <= set(
    _FAULT_RECOMMENDATIONS
), "recommendation vocabulary out of sync with FAULT_TYPE_CANONICAL"

#: Closed fault-type vocabulary accepted by generate_recommendations.
VALID_FAULT_TYPES: tuple[str, ...] = tuple(sorted(_FAULT_RECOMMENDATIONS))


def generate_recommendations(
    severity_zone: str,
    fault_types: list[str] | None = None,
    lang: str = "en",
) -> list[dict]:
    """Generate maintenance recommendations based on severity and faults.

    Deliberately takes no "confidence" input: a caller-supplied
    confidence number would be repeated verbatim in advisory output
    without any evidential basis.

    Args:
        severity_zone: ISO 20816-3 zone letter — ``"A"``, ``"B"``,
            ``"C"``, or ``"D"``.
        fault_types: Optional list of detected fault keywords from the
            closed vocabulary ``VALID_FAULT_TYPES`` (e.g.
            ``["outer_race", "misalignment"]``).
        lang: Language code for translations.

    Returns:
        List of recommendation dicts, each containing ``action``,
        ``urgency``, and ``description``.

    Raises:
        ValueError: If any fault type is outside ``VALID_FAULT_TYPES`` —
            unknown values used to be dropped silently, which hid typos
            (e.g. 'BPFO' instead of 'outer_race').
    """
    if fault_types:
        unknown = [f for f in fault_types if f.lower() not in _FAULT_RECOMMENDATIONS]
        if unknown:
            raise ValueError(
                f"Unknown fault type(s) {unknown} — allowed values: "
                f"{list(VALID_FAULT_TYPES)}. Bearing acronyms map to the "
                f"canonical vocabulary as BPFO=outer_race, BPFI=inner_race, "
                f"BSF=ball, FTF=cage."
            )

    zone = severity_zone.upper()

    zone_map: dict[str, tuple[str, str, str]] = {
        "A": ("rec.zone.A.action", "low", "rec.zone.A.description"),
        "B": ("rec.zone.B.action", "medium", "rec.zone.B.description"),
        "C": ("rec.zone.C.action", "high", "rec.zone.C.description"),
        "D": ("rec.zone.D.action", "critical", "rec.zone.D.description"),
    }

    if zone not in zone_map:
        action_key, urgency, desc_key = (
            "rec.zone.unknown.action",
            "medium",
            "rec.zone.unknown.description",
        )
        action = t(action_key, lang)
        description = t(desc_key, lang, zone=severity_zone)
    else:
        action_key, urgency, desc_key = zone_map[zone]
        action = t(action_key, lang)
        description = t(desc_key, lang)

    recommendations: list[dict] = [
        {"action": action, "urgency": urgency, "description": description}
    ]

    if fault_types:
        for fault in fault_types:
            key = fault.lower()
            if key in _FAULT_RECOMMENDATIONS:
                recommendations.append(
                    {
                        "action": t(_FAULT_RECOMMENDATIONS[key], lang),
                        "urgency": urgency,
                        "description": t("rec.fault.description", lang, fault=fault),
                    }
                )

    return recommendations