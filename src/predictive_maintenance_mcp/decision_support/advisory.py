"""ISO 13374 Block 6 — server-authored advisory.

Every evaluative sentence a report shows a human is written *here*, by the
server that computed the numbers. Renderers place these strings; they never
compose their own.

This exists because the previous arrangement let the caller author report
content (see ``generate_diagnostic_report_docx``'s ``sections`` argument).
When the caller is a language model, the numbers survive the trip and the
labels do not: a superseded standard name, a machine-class vocabulary this
codebase does not use, and a "confidence" grade that
:mod:`..decision_support.recommendations` deliberately refuses to produce.

Three rules hold throughout:

1. Standard names, zone descriptions, and threshold provenance are read from
   :mod:`..diagnostics.iso20816` — the single source of that vocabulary — and
   never re-typed here.
2. No field, value, or sentence is a confidence or a probability. Evidential
   weight is conveyed by naming the facts that support a finding, and the
   categorical ``evidence_strength`` always travels with a sentence saying
   what it counts.
3. A missing input produces an authored statement about the absence and the
   conclusion it makes unavailable. It never produces a missing section — a
   silently absent block reads as "nothing to report".
"""

from __future__ import annotations

import math
from typing import Any, Optional

from ..diagnostics.bearing_analyzer import FAULT_TYPE_CANONICAL
from .recommendations import generate_recommendations
from ..i18n import t

#: Block status vocabulary. ``ASSESSED`` means the block reached a verdict;
#: ``REFUSED`` means the engine declined to answer and said why; ``ABSENT``
#: means an input the block needs was never supplied.
ASSESSED = "assessed"
REFUSED = "refused"
ABSENT = "absent"

#: Always rendered next to ``evidence_strength``. The categorical value on its
#: own invites a reader — or a model — to hear a probability; this sentence is
#: what stops that reading.
EVIDENCE_STRENGTH_EXPLANATION = (
    "Evidence strength counts independent corroborating findings — it is "
    "not a confidence score and not a probability."
)

#: Keys a ``diagnose_vibration`` result must carry. Guessing at a partial
#: result would produce authored sentences about numbers that were never
#: computed, which is the failure mode this module exists to prevent.
_REQUIRED_KEYS = ("signal_id", "iso_severity", "fft_summary", "stft_summary")

_ACCEPTABLE_ZONES = ("A", "B")

#: Which baseline delta leads the comparison sentence, most specific first.
#: Chosen by what the movement MEANS, not by magnitude: the three deltas are
#: measured in dB, mm/s and percentage points, so "the biggest number" would
#: rank them by unit scale rather than by diagnostic weight — the anomaly
#: ratio, living on a 0-100 scale, would win almost every time.
_HEADLINE_ORDER = ("envelope_magnitude", "rms_velocity", "anomaly_ratio")


def _fault_label(canonical: Optional[str], lang: str = "en") -> str:
    """Render a canonical fault type as prose ('outer_race' -> 'outer race')."""
    if not canonical:
        return ""
    return t(f"fault.label.{canonical}", lang)


def _acronym_for(canonical: Optional[str]) -> str:
    """Reverse-map a canonical fault type to its bearing acronym."""
    for acronym, value in FAULT_TYPE_CANONICAL.items():
        if value == canonical:
            return acronym
    return ""


# ---------------------------------------------------------------------------
# ISO severity
# ---------------------------------------------------------------------------


def _build_iso_block(iso: dict, lang: str = "en") -> dict:
    """Author the ISO severity block, or carry the engine's refusal forward."""
    if iso.get("status") == "refused":
        return {
            "status": REFUSED,
            "statement": t("diag.iso.refused", lang, reason=iso['reason']),
            "reason": iso["reason"],
            "remedy": iso["remedy"],
            "standard_note": None,
        }

    zone = iso["zone"]
    rms = iso["rms_velocity_mm_s"]
    severity = iso.get("severity_level", "")
    description = iso.get("zone_description", "")
    boundaries = iso.get("boundaries", {})

    statement = t("diag.iso.assessed", lang,
        rms=rms, zone=zone, severity=severity,
        machine_group=iso.get('machine_group', ''),
        support_type=iso.get('support_type', ''),
        description=description
    ).strip()

    return {
        "status": ASSESSED,
        "statement": statement,
        "zone": zone,
        "severity_level": severity,
        "rms_velocity_mm_s": rms,
        "boundaries": boundaries,
        "evaluation_band": iso.get("frequency_range"),
        "standard_note": iso.get("threshold_provenance"),
    }


# ---------------------------------------------------------------------------
# Bearing characteristic-frequency matching
# ---------------------------------------------------------------------------


def _build_bearing_block(bearing_faults: Optional[dict], lang: str = "en") -> dict:
    """Author the frequency-matching block, or state why it was not attempted."""
    if not bearing_faults:
        return {
            "status": ABSENT,
            "statement": t("diag.bearing.absent", lang),
            "remedy": t("diag.bearing.absent_remedy", lang),
            "rows": [],
        }

    rows = []
    for check in bearing_faults.get("fault_checks", []):
        rows.append(
            {
                "fault_type": check["fault_type"],
                "fault_canonical": check.get("fault_type_canonical"),
                "expected_hz": check["expected_frequency_hz"],
                "measured_hz": check.get("detected_frequency_hz"),
                "deviation_pct": check.get("deviation_pct"),
                "magnitude": check.get("magnitude"),
                "harmonics": len(check.get("harmonics_detected") or []),
                "matched": bool(check.get("detected")),
                "evidence_strength": check.get("evidence_strength", "none"),
            }
        )

    matched = [r for r in rows if r["matched"]]
    if matched:
        parts = [
            t("diag.bearing.matched_part", lang,
                fault_type=r['fault_type'],
                expected_hz=r['expected_hz'],
                measured_hz=r['measured_hz'],
                deviation_pct=r['deviation_pct']
            )
            for r in matched
        ]
        statement = t("diag.bearing.matched_statement", lang,
            bearing_id=bearing_faults.get('bearing_id', ''),
            shaft_freq=bearing_faults.get('shaft_frequency_hz', 0.0),
            matched_parts='; '.join(parts)
        )
    else:
        statement = t("diag.bearing.no_match", lang,
            bearing_id=bearing_faults.get('bearing_id', '')
        )

    return {
        "status": ASSESSED,
        "statement": statement,
        "bearing_id": bearing_faults.get("bearing_id"),
        "shaft_frequency_hz": bearing_faults.get("shaft_frequency_hz"),
        "bearing_frequencies": bearing_faults.get("bearing_frequencies", {}),
        "rows": rows,
    }


# ---------------------------------------------------------------------------
# Anomaly detection
# ---------------------------------------------------------------------------


def _build_anomaly_block(anomaly: Optional[dict], lang: str = "en") -> dict:
    """Author the anomaly block, or state that no model verdict exists."""
    if not anomaly:
        return {
            "status": ABSENT,
            "statement": t("diag.anomaly.absent", lang),
            "remedy": t("diag.anomaly.absent_remedy", lang),
        }

    health = anomaly["overall_health"]
    ratio = anomaly["anomaly_ratio"]
    segments = anomaly.get("num_segments")
    counted = (
        f"{round(ratio * segments)} of {segments} segments"
        if segments
        else f"{ratio * 100:.1f}% of segments"
    )
    return {
        "status": ASSESSED,
        "statement": t("diag.anomaly.assessed", lang,
            health=health, counted=counted, ratio_pct=ratio * 100
        ),
        "overall_health": health,
        "anomaly_ratio": ratio,
        "num_segments": segments,
    }


# ---------------------------------------------------------------------------
# Spectral energy distribution
# ---------------------------------------------------------------------------


def _build_energy_block(stft_summary: dict, lang: str = "en") -> dict:
    """Author the spectral-energy block from the STFT band breakdown."""
    entries = stft_summary.get("energy_per_band") or []
    bands = {entry["band"]: entry["energy"] for entry in entries}
    if not bands:
        return {
            "status": ABSENT,
            "statement": t("diag.energy.absent", lang),
            "bands": {},
        }

    total = sum(bands.values())
    dominant = max(bands, key=lambda k: bands[k])
    share = (bands[dominant] / total * 100) if total else 0.0
    return {
        "status": ASSESSED,
        "statement": t("diag.energy.assessed", lang,
            dominant=dominant, share=share
        ),
        "bands": dict(bands),
        "dominant_band": dominant,
        "dominant_share_pct": round(share, 1),
    }


# ---------------------------------------------------------------------------
# Verdict and evidence
# ---------------------------------------------------------------------------


def _build_verdict(bearing_block: dict, iso_block: dict, anomaly_block: dict, lang: str = "en") -> dict:
    """Author the headline verdict from the blocks that reached one."""
    matched = [r for r in bearing_block.get("rows", []) if r["matched"]]
    if matched:
        primary = max(
            matched,
            key=lambda r: {"high": 3, "moderate": 2, "low": 1}.get(
                r["evidence_strength"], 0
            ),
        )
        canonical = primary["fault_canonical"]
        label = _fault_label(canonical, lang)
        return {
            "statement": t("diag.verdict.fault_indicated", lang,
                label=label,
                fault_type=primary['fault_type'],
                deviation_pct=primary['deviation_pct']
            ),
            "fault_canonical": canonical,
            "fault_acronym": primary["fault_type"],
        }

    if bearing_block["status"] == ASSESSED:
        headline = t("diag.verdict.no_bearing_fault", lang)
    else:
        headline = t("diag.verdict.no_bearing_verdict", lang)

    if iso_block["status"] == ASSESSED and iso_block["zone"] not in _ACCEPTABLE_ZONES:
        headline += t("diag.verdict.non_bearing_source", lang, zone=iso_block['zone'])
    elif anomaly_block.get("overall_health") in ("Faulty", "Suspicious"):
        headline += t("diag.verdict.anomaly_flags", lang)

    return {"statement": headline, "fault_canonical": None, "fault_acronym": ""}


def _build_evidence(
    diagnosis: dict,
    bearing_block: dict,
    iso_block: dict,
    anomaly_block: dict,
    energy_block: dict,
    lang: str = "en",
) -> dict:
    """Collect the facts that support the verdict, as authored sentences."""
    statements: list[str] = []

    for row in bearing_block.get("rows", []):
        if not row["matched"]:
            continue
        acronym = row["fault_type"]
        sentence = t("diag.evidence.bearing_match", lang,
            acronym=acronym,
            expected_hz=row['expected_hz'],
            measured_hz=row['measured_hz'],
            deviation_pct=row['deviation_pct']
        )
        if row["harmonics"]:
            sentence += t("diag.evidence.harmonics_add", lang,
                harmonics=row["harmonics"], acronym=acronym
            )
        statements.append(sentence)

    if iso_block["status"] == ASSESSED:
        statements.append(iso_block["statement"])
    if anomaly_block["status"] == ASSESSED:
        statements.append(anomaly_block["statement"])
    if energy_block["status"] == ASSESSED:
        statements.append(energy_block["statement"])

    peak = diagnosis.get("fft_summary", {}).get("peak_frequency_hz")
    if peak is not None:
        statements.append(t("diag.evidence.dominant_freq", lang, peak=peak))

    return {
        "strength": diagnosis.get("evidence_strength", "none"),
        "strength_explanation": t("evidence.strength_explanation", lang),
        "statements": statements,
    }


# ---------------------------------------------------------------------------
# Indicator disagreement (R6)
# ---------------------------------------------------------------------------


def _build_disagreements(
    iso_block: dict, bearing_block: dict, anomaly_block: dict, lang: str = "en",
) -> list[dict]:
    """Name the indicators that disagree, and which one governs the action.

    A refused ISO block is not an indicator and cannot disagree with one — an
    absent verdict is silence, not a contradicting opinion.
    """
    if iso_block["status"] != ASSESSED:
        return []
    if iso_block["zone"] not in _ACCEPTABLE_ZONES:
        return []

    dissenting: list[str] = []
    if anomaly_block.get("overall_health") in ("Faulty", "Suspicious"):
        dissenting.append(
            t("diag.disagreement.anomaly_dissent", lang,
                health=anomaly_block['overall_health'],
                ratio_pct=anomaly_block['anomaly_ratio'] * 100
            )
        )
    strong_matches = [
        r
        for r in bearing_block.get("rows", [])
        if r["matched"] and r["evidence_strength"] in ("high", "moderate")
    ]
    if strong_matches:
        names = ", ".join(r["fault_type"] for r in strong_matches)
        dissenting.append(t("diag.disagreement.match_dissent", lang, names=names))

    if not dissenting:
        return []

    return [
        {
            "statement": t("diag.disagreement.statement", lang,
                zone=iso_block['zone'],
                dissenting=' and '.join(dissenting)
            ),
            "governing_indicator": "fault-pattern evidence",
            "deferring_indicator": f"ISO zone {iso_block['zone']}",
        }
    ]


# ---------------------------------------------------------------------------
# Recommendations (R7)
# ---------------------------------------------------------------------------


def _build_recommendations(
    iso_block: dict,
    bearing_block: dict,
    anomaly_block: dict,
    disagreements: list[dict],
    lang: str = "en",
) -> list[dict]:
    """Attach a motivation and its supporting evidence to each action."""
    recommendations: list[dict] = []

    if iso_block["status"] == REFUSED:
        recommendations.append(
            {
                "action": iso_block["remedy"],
                "urgency": "medium",
                "description": t("diag.rec.severity_unavailable", lang),
                "motivation": iso_block["reason"],
                "evidence": [iso_block["statement"]],
            }
        )
        zone = None
    else:
        zone = iso_block["zone"]

    fault_types = [
        r["fault_canonical"]
        for r in bearing_block.get("rows", [])
        if r["matched"] and r["fault_canonical"]
    ]

    if zone is not None:
        zone_only = generate_recommendations(severity_zone=zone, lang=lang)
        base = generate_recommendations(severity_zone=zone, fault_types=fault_types, lang=lang)
        for index, entry in enumerate(base):
            fault_index = index - len(zone_only)
            if fault_index >= 0:
                acronym = _acronym_for(fault_types[fault_index])
                motivation = t("diag.rec.fault_motivation", lang,
                    acronym_suffix=t("diag.rec.fault_motivation_acronym", lang, acronym=acronym) if acronym else "."
                )
                evidence = [bearing_block["statement"]]
            else:
                severity = iso_block.get("severity_level")
                if severity:
                    motivation = t("diag.rec.iso_motivation_severity", lang,
                        zone=zone, severity_lower=severity.lower()
                    )
                else:
                    motivation = t("diag.rec.iso_motivation_plain", lang, zone=zone)
                evidence = [iso_block["statement"]]
            recommendations.append(
                {**entry, "motivation": motivation, "evidence": evidence}
            )

    if disagreements:
        recommendations.insert(
            0,
            {
                "action": t("diag.rec.disagreement_action", lang),
                "urgency": "medium",
                "description": t("diag.rec.disagreement_description", lang),
                "motivation": disagreements[0]["statement"],
                "evidence": [disagreements[0]["statement"]],
            },
        )

    if anomaly_block["status"] == ABSENT:
        recommendations.append(
            {
                "action": anomaly_block["remedy"],
                "urgency": "low",
                "description": t("diag.rec.anomaly_absent_description", lang),
                "motivation": anomaly_block["statement"],
                "evidence": [anomaly_block["statement"]],
            }
        )

    for rec in recommendations:
        urgency = rec.get("urgency", "medium")
        rec["urgency_display"] = t(f"rec.urgency.{urgency}", lang)

    return recommendations


# ---------------------------------------------------------------------------
# Baseline comparison (R8)
# ---------------------------------------------------------------------------


def build_baseline_comparison(
    diagnosis: dict, baseline: Optional[dict], lang: str = "en",
) -> dict[str, Any]:
    """Author the comparison against a healthy reference signal.

    An absolute figure tells a technician where the machine is; a delta tells
    them where it is going. When no baseline is supplied the block still
    renders — it states the absence and the conclusion that absence costs.
    """
    if not baseline:
        return {
            "status": ABSENT,
            "statement": t("diag.baseline.absent", lang),
            "remedy": t("diag.baseline.absent_remedy", lang),
            "deltas": [],
        }

    incompatible = _baseline_incompatibility(diagnosis, baseline, lang)
    if incompatible:
        return {
            "status": REFUSED,
            "statement": t("diag.baseline.refused", lang, incompatible=incompatible),
            "remedy": t("diag.baseline.refused_remedy", lang),
            "deltas": [],
        }

    deltas = [
        delta
        for delta in (
            _rms_delta(diagnosis, baseline, lang=lang),
            _anomaly_delta(diagnosis, baseline, lang=lang),
            _envelope_delta(diagnosis, baseline, lang=lang),
        )
        if delta is not None
    ]

    if not deltas:
        return {
            "status": ABSENT,
            "statement": t("diag.baseline.no_indicators", lang,
                signal_id=baseline.get('signal_id', '')
            ),
            "remedy": t("diag.baseline.no_indicators_remedy", lang),
            "deltas": [],
        }

    moved = [d for d in deltas if d["direction"] != "unchanged"]
    if not moved:
        statement = t("diag.baseline.stable", lang,
            signal_id=baseline.get('signal_id', '')
        )
    else:
        headline = min(moved, key=lambda d: _HEADLINE_ORDER.index(d["indicator"]))
        statement = t("diag.baseline.moved", lang,
            signal_id=baseline.get('signal_id', ''),
            moved_count=len(moved),
            total_count=len(deltas),
            headline_statement=headline['statement']
        )

    return {
        "status": ASSESSED,
        "statement": statement,
        "baseline_signal_id": baseline.get("signal_id"),
        "remedy": "",
        "deltas": deltas,
    }


def _baseline_incompatibility(diagnosis: dict, baseline: dict, lang: str = "en") -> str:
    """Return a reason the two signals cannot be compared, or an empty string."""
    signal_iso = diagnosis.get("iso_severity", {})
    baseline_iso = baseline.get("iso_severity", {})
    if (
        signal_iso.get("status") == "assessed"
        and baseline_iso.get("status") == "assessed"
    ):
        signal_unit = signal_iso.get("original_unit")
        baseline_unit = baseline_iso.get("original_unit")
        if signal_unit != baseline_unit:
            return t("diag.baseline.incompatible_unit", lang,
                signal_unit=signal_unit, baseline_unit=baseline_unit
            )

    signal_bearing = diagnosis.get("bearing_id")
    baseline_bearing = baseline.get("bearing_id")
    if signal_bearing and baseline_bearing and signal_bearing != baseline_bearing:
        return t("diag.baseline.incompatible_bearing", lang,
            signal_bearing=signal_bearing, baseline_bearing=baseline_bearing
        )

    return ""


def _direction(delta: float, tolerance: float) -> str:
    if abs(delta) < tolerance:
        return "unchanged"
    return "higher" if delta > 0 else "lower"


def _direction_display(direction: str, lang: str = "en") -> str:
    mapping = {
        "unchanged": t("baseline.stable", lang),
        "higher": t("baseline.worsening", lang),
        "lower": t("baseline.improving", lang),
    }
    return mapping.get(direction, direction)


def _rms_delta(diagnosis: dict, baseline: dict, lang: str = "en") -> Optional[dict]:
    signal_iso = diagnosis.get("iso_severity", {})
    baseline_iso = baseline.get("iso_severity", {})
    if (
        signal_iso.get("status") != "assessed"
        or baseline_iso.get("status") != "assessed"
    ):
        return None

    now = signal_iso["rms_velocity_mm_s"]
    then = baseline_iso["rms_velocity_mm_s"]
    delta = now - then
    direction = _direction(delta, 0.005)
    if direction == "unchanged":
        statement = t("diag.delta.rms_unchanged", lang, now=now, then=then)
    else:
        statement = t("diag.delta.rms_changed", lang,
            delta_abs=abs(delta), direction=direction, now=now, then=then
        )
    return {
        "indicator": "rms_velocity",
        "unit": "mm/s",
        "value": now,
        "baseline_value": then,
        "delta": round(delta, 4),
        "direction": direction,
        "statement": statement,
    }


def _anomaly_delta(diagnosis: dict, baseline: dict, lang: str = "en") -> Optional[dict]:
    signal_anomaly = diagnosis.get("anomaly_detection")
    baseline_anomaly = baseline.get("anomaly_detection")
    if not signal_anomaly or not baseline_anomaly:
        return None

    now = signal_anomaly["anomaly_ratio"] * 100
    then = baseline_anomaly["anomaly_ratio"] * 100
    delta = now - then
    direction = _direction(delta, 0.05)
    if direction == "unchanged":
        statement = t("diag.delta.anomaly_unchanged", lang, now=now, then=then)
    else:
        statement = t("diag.delta.anomaly_changed", lang,
            delta_abs=abs(delta), direction=direction, now=now, then=then
        )
    return {
        "indicator": "anomaly_ratio",
        "unit": "percentage points",
        "value": round(now, 2),
        "baseline_value": round(then, 2),
        "delta": round(delta, 2),
        "direction": direction,
        "statement": statement,
    }


def _envelope_delta(diagnosis: dict, baseline: dict, lang: str = "en") -> Optional[dict]:
    """Compare envelope amplitude at the fault frequency that actually matched.

    This is the delta that separates "the machine is noisier" from "this
    specific defect grew": it looks only at the frequency the verdict rests on.
    """
    signal_faults = diagnosis.get("bearing_faults")
    baseline_faults = baseline.get("bearing_faults")
    if not signal_faults or not baseline_faults:
        return None

    matched = next(
        (
            c
            for c in signal_faults.get("fault_checks", [])
            if c.get("detected") and c.get("magnitude")
        ),
        None,
    )
    if matched is None:
        return None

    reference = next(
        (
            c
            for c in baseline_faults.get("fault_checks", [])
            if c["fault_type"] == matched["fault_type"] and c.get("magnitude")
        ),
        None,
    )
    if reference is None:
        return None

    now = matched["magnitude"]
    then = reference["magnitude"]
    delta_db = 20 * math.log10(now / then)
    direction = _direction(delta_db, 0.05)
    acronym = matched["fault_type"]
    if direction == "unchanged":
        statement = t("diag.delta.envelope_unchanged", lang, acronym=acronym)
    else:
        statement = t("diag.delta.envelope_changed", lang,
            acronym=acronym, delta_db=abs(delta_db), direction=direction
        )
    return {
        "indicator": "envelope_magnitude",
        "unit": "dB",
        "value": now,
        "baseline_value": then,
        "delta": round(delta_db, 2),
        "direction": direction,
        "statement": statement,
    }


# ---------------------------------------------------------------------------
# Provenance
# ---------------------------------------------------------------------------


def _build_provenance(diagnosis: dict, lang: str = "en") -> dict:
    """Record what was analysed and by which server version."""
    # Imported inside the function: the package __init__ pulls in the MCP
    # server, and this module is imported from within that import chain.
    from .. import __version__

    return {
        "signal_id": diagnosis.get("signal_id"),
        "rpm": diagnosis.get("rpm"),
        "bearing_id": diagnosis.get("bearing_id"),
        "machine_group": diagnosis.get("machine_group"),
        "support_type": diagnosis.get("support_type"),
        "server_version": __version__,
    }


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_advisory(
    diagnosis: dict,
    baseline_diagnosis: Optional[dict] = None,
    lang: str = "en",
) -> dict[str, Any]:
    """Turn a ``diagnose_vibration`` result into server-authored statements.

    Every string in the returned payload is written here or by a module this
    one reads from. Renderers place these strings; a renderer that composes
    its own evaluative sentence has broken the contract this function exists
    to hold.

    Args:
        diagnosis: A result from
            :func:`..decision_support.diagnosis_pipeline.diagnose_vibration`.
        baseline_diagnosis: Optional result for a healthy reference signal on
            the same machine. When omitted, the comparison block states the
            absence and the conclusion it makes unavailable.

    Returns:
        The advisory payload: verdict, evidence, per-indicator blocks,
        indicator disagreements, baseline comparison, recommendations, and
        provenance.

    Raises:
        ValueError: If ``diagnosis`` is not a recognisable diagnosis result.
            Authoring sentences about numbers that were never computed is the
            failure this module exists to prevent, so a partial input is
            refused rather than filled in.
    """
    missing = [k for k in _REQUIRED_KEYS if k not in diagnosis]
    if missing:
        raise ValueError(
            f"Not a diagnose_vibration result — missing {missing}. Pass the "
            f"dict returned by diagnose_vibration(); the advisory layer does "
            f"not re-run analysis and cannot author statements about values "
            f"it was not given."
        )

    iso_block = _build_iso_block(diagnosis["iso_severity"], lang=lang)
    bearing_block = _build_bearing_block(diagnosis.get("bearing_faults"), lang=lang)
    anomaly_block = _build_anomaly_block(diagnosis.get("anomaly_detection"), lang=lang)
    energy_block = _build_energy_block(diagnosis["stft_summary"], lang=lang)

    verdict = _build_verdict(bearing_block, iso_block, anomaly_block, lang=lang)
    evidence = _build_evidence(
        diagnosis, bearing_block, iso_block, anomaly_block, energy_block, lang=lang
    )
    disagreements = _build_disagreements(iso_block, bearing_block, anomaly_block, lang=lang)
    baseline_block = build_baseline_comparison(diagnosis, baseline_diagnosis, lang=lang)
    recommendations = _build_recommendations(
        iso_block, bearing_block, anomaly_block, disagreements, lang=lang
    )

    return {
        "signal_id": diagnosis["signal_id"],
        "verdict": verdict,
        "evidence": evidence,
        "iso": iso_block,
        "bearing_match": bearing_block,
        "anomaly": anomaly_block,
        "spectral_energy": energy_block,
        "disagreements": disagreements,
        "baseline_comparison": baseline_block,
        "recommendations": recommendations,
        "provenance": _build_provenance(diagnosis, lang=lang),
    }


def collect_statements(advisory: dict, lang: str = "en") -> list[str]:
    """Return every authored statement in the payload, in document order.

    This is the surface the cross-rendering parity test asserts on: a
    statement present here and absent from a rendering means that rendering
    dropped something the server said.
    """
    statements: list[str] = []

    def add(value: Optional[str]) -> None:
        if value and value not in statements:
            statements.append(value)

    add(advisory["verdict"]["statement"])
    for block_key in ("iso", "bearing_match", "anomaly", "spectral_energy"):
        add(advisory[block_key].get("statement"))
        add(advisory[block_key].get("remedy"))
    for entry in advisory["disagreements"]:
        add(entry["statement"])
    add(advisory["baseline_comparison"].get("statement"))
    for sentence in advisory["baseline_comparison"].get("deltas", []):
        add(sentence.get("statement"))
    for sentence in advisory["evidence"]["statements"]:
        add(sentence)
    add(advisory["evidence"]["strength_explanation"])
    for rec in advisory["recommendations"]:
        add(rec["action"])
        add(rec["description"])
        add(rec["motivation"])

    return statements
