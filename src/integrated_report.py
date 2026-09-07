"""Integrated diagnostic report template.

This module places strings; it never composes them. Every evaluative sentence
it renders arrives already written from
:mod:`.decision_support.advisory`, and the template's only job is layout.

The analogy that shaped it is the radiology report: an annotated image, the
findings, the impression, the recommendation — and nobody expects the imaging
software to write the impression. What this template contributes is the
annotation and the arrangement, not the judgement.

It lives outside :mod:`.html_templates` for two reasons: that module is
already long and is excluded from the coverage gate, and this one is the
report whose contract most needs test coverage.
"""

from __future__ import annotations

import html
from typing import Any, Optional

from .figures import figure_to_svg
from .html_templates import get_base_template
from .i18n import get_i18n

_URGENCY_BADGE = {
    "low": "badge-success",
    "medium": "badge-warning",
    "high": "badge-warning",
    "critical": "badge-danger",
}

_STATUS_BADGE = {
    "assessed": "badge-info",
    "refused": "badge-warning",
    "absent": "badge-warning",
}

_MUTED = "color:var(--text-secondary);"


def _esc(value: Any) -> str:
    """Escape a value for HTML. Signal ids reach this template from user input."""
    return html.escape(str(value if value is not None else ""))


def _val_attrs(en_val: str, zh_val: str, lang: str) -> str:
    """Return data-i18n-val-en and data-i18n-val-zh attributes for client-side switching."""
    return f' data-i18n-val-en="{_esc(en_val)}" data-i18n-val-zh="{_esc(zh_val)}" data-i18n-val="{_esc(zh_val if lang == "zh" else en_val)}"'


def _remedy_paragraph(remedy: Optional[str], to_resolve: str = "To resolve", to_resolve_key: str = "to_resolve", lang: str = "en", en_remedy: str = "", zh_remedy: str = "") -> str:
    if not remedy:
        return ""
    display_remedy = remedy
    return (
        f'<p style="margin-top:0.75rem;{_MUTED}">'
        f'<strong><span data-i18n="{to_resolve_key}">{_esc(to_resolve)}</span>:</strong> '
        f'<span{_val_attrs(en_remedy, zh_remedy, lang)}>{_esc(display_remedy)}</span></p>'
    )


def _status_badge(status: Optional[str], lang: str = "en") -> str:
    css = _STATUS_BADGE.get(status or "", "badge-info")
    en_status = status or ""
    status_map = {"assessed": "已评估", "refused": "已拒绝", "absent": "缺失"}
    zh_status = status_map.get(en_status, en_status)
    display_status = zh_status if lang == "zh" else en_status
    return (
        f'<span class="badge {css}" style="margin-left:0.5rem;"'
        f'{_val_attrs(en_status, zh_status, lang)}>'
        f"{_esc(display_status)}</span>"
    )


def _block_card(title: str, block: dict[str, Any], i18n: Any = None, title_key: str = "", lang: str = "en") -> str:
    """Render one indicator block, including its authored absence statement.

    A block whose input was missing still renders. A silently omitted section
    reads as "nothing to report", which is a different claim from "this could
    not be determined, and here is what that costs you".
    """
    from .i18n import get_i18n
    zh_i18n = get_i18n("zh")
    
    to_resolve = i18n.t("to_resolve") if i18n else "To resolve"
    title_attr = f' data-i18n="{title_key}"' if title_key else ""
    
    # Get both EN and ZH statements
    en_statement = block.get("statement", "")
    zh_statement = en_statement
    zh_statement = en_statement.replace("BPFO frequency", zh_i18n.t("bpfo_frequency"))
    zh_statement = zh_statement.replace("Anomaly ratio", zh_i18n.t("anomaly_ratio"))
    zh_statement = zh_statement.replace("Energy concentrated", zh_i18n.t("energy_concentrated"))
    
    # Get both EN and ZH remedies
    en_remedy = block.get("remedy", "")
    zh_remedy = en_remedy
    if en_remedy:
        zh_remedy = en_remedy.replace("Plan maintenance", zh_i18n.t("plan_maintenance"))
        zh_remedy = zh_remedy.replace("Monitor condition", zh_i18n.t("monitor_condition"))
        zh_remedy = zh_remedy.replace("inspection", zh_i18n.t("inspection"))
    display_remedy = zh_remedy if lang == "zh" else en_remedy
    
    return (
        '<div class="card">'
        f'<h2 class="card-title"{title_attr}>{_esc(title)}'
        f'{_status_badge(block.get("status"), lang)}</h2>'
        f'<p{_val_attrs(en_statement, zh_statement, lang)}>{_esc(zh_statement if lang == "zh" else en_statement)}</p>'
        f'{_remedy_paragraph(display_remedy, to_resolve, lang=lang, en_remedy=en_remedy, zh_remedy=zh_remedy)}'
        "</div>"
    )


def _bearing_table(block: dict[str, Any], i18n: Any = None, lang: str = "en") -> str:
    """Calculated against measured, with a verdict per bearing element.

    Putting the two numbers side by side is what lets a reader check the
    match rather than accept it.
    """
    rows = block.get("rows") or []
    if not rows:
        return ""

    from .i18n import get_i18n
    zh_i18n = get_i18n("zh")
    
    element_label = i18n.t("element") if i18n else "Element"
    calculated_label = i18n.t("calculated") if i18n else "Calculated"
    measured_label = i18n.t("measured_hz") if i18n else "Measured"
    deviation_label = i18n.t("deviation") if i18n else "Deviation"
    verdict_label = i18n.t("verdict") if i18n else "Verdict"
    en_match_text = "match"
    zh_match_text = zh_i18n.t("match_found")
    en_no_match_text = "no match"
    zh_no_match_text = zh_i18n.t("no_match")
    calc_vs_meas = i18n.t("calculated_against_measured") if i18n else "Calculated against measured"

    cells = []
    for row in rows:
        measured = (
            f"{row['measured_hz']:.2f} Hz" if row.get("measured_hz") else "&mdash;"
        )
        deviation = (
            f"{row['deviation_pct']:.2f}%"
            if row.get("deviation_pct") is not None
            else "&mdash;"
        )
        verdict_css = "badge-danger" if row["matched"] else "badge-success"
        if row["matched"]:
            display_verdict = zh_match_text if lang == "zh" else en_match_text
            verdict_attrs = _val_attrs(en_match_text, zh_match_text, lang)
        else:
            display_verdict = zh_no_match_text if lang == "zh" else en_no_match_text
            verdict_attrs = _val_attrs(en_no_match_text, zh_no_match_text, lang)
        cells.append(
            "<tr>"
            f"<td>{_esc(row['fault_type'])}</td>"
            f"<td>{row['expected_hz']:.2f} Hz</td>"
            f"<td>{measured}</td>"
            f"<td>{deviation}</td>"
            f'<td><span class="badge {verdict_css}"{verdict_attrs}>{display_verdict}</span></td>'
            "</tr>"
        )

    return (
        '<div class="card">'
        f'<h2 class="card-title" data-i18n="calculated_against_measured">{_esc(calc_vs_meas)}</h2>'
        '<table style="width:100%;border-collapse:collapse;">'
        '<thead><tr style="text-align:left;border-bottom:2px solid var(--border-color);">'
        f'<th data-i18n="element">{_esc(element_label)}</th><th data-i18n="calculated">{_esc(calculated_label)}</th><th data-i18n="measured_hz">{_esc(measured_label)}</th>'
        f'<th data-i18n="deviation">{_esc(deviation_label)}</th><th data-i18n="verdict">{_esc(verdict_label)}</th></tr></thead>'
        f'<tbody>{"".join(cells)}</tbody>'
        "</table></div>"
    )


def _figure_card(figure: Optional[dict[str, Any]], i18n: Any = None, lang: str = "en") -> str:
    """The figure that closes the matching argument, or a note that it is absent."""
    from .i18n import get_i18n
    zh_i18n = get_i18n("zh")
    
    envelope_chart = i18n.t("envelope_spectrum_chart") if i18n else "Envelope spectrum"
    en_no_envelope = "This report carries no envelope spectrum figure, so the frequency match cannot be checked visually here — only against the values in the table above."
    zh_no_envelope = zh_i18n.t("no_envelope_figure")
    display_no_envelope = zh_no_envelope if lang == "zh" else en_no_envelope

    if not figure:
        return (
            '<div class="card">'
            f'<h2 class="card-title" data-i18n="envelope_spectrum_chart">{_esc(envelope_chart)}</h2>'
            f'<p{_val_attrs(en_no_envelope, zh_no_envelope, lang)}>{_esc(display_no_envelope)}</p>'
            "</div>"
        )

    return (
        '<div class="chart-container">'
        f'<h2 class="card-title" data-i18n="envelope_spectrum_chart">{_esc(envelope_chart)}</h2>'
        f"{figure_to_svg(figure)}"
        f'<p style="margin-top:1rem;{_MUTED}font-size:0.9rem;">'
        f'{_esc(figure["caption"])}</p>'
        "</div>"
    )


def _recommendations_card(recommendations: list[dict[str, Any]], i18n: Any = None, lang: str = "en") -> str:
    """Each action with the reasoning and the evidence it rests on."""
    if not recommendations:
        return ""

    from .i18n import get_i18n
    zh_i18n = get_i18n("zh")
    
    why_label = i18n.t("why") if i18n else "Why"
    evidence_label = i18n.t("evidence_label") if i18n else "Evidence"
    rec_actions = i18n.t("recommended_actions") if i18n else "Recommended actions"

    items = []
    for rec in recommendations:
        en_urgency = rec.get("urgency", "medium")
        urgency_map = {"low": "低", "medium": "中", "high": "高", "critical": "紧急"}
        zh_urgency = urgency_map.get(en_urgency, en_urgency)
        display_urgency = zh_urgency if lang == "zh" else en_urgency
        badge = _URGENCY_BADGE.get(en_urgency, "badge-info")
        
        en_action = rec.get("action", "")
        zh_action = en_action
        if en_action:
            zh_action = en_action.replace("Schedule bearing inspection", zh_i18n.t("schedule_bearing_inspection"))
            zh_action = zh_action.replace("Monitor condition", zh_i18n.t("monitor_condition"))
            zh_action = zh_action.replace("Plan maintenance", zh_i18n.t("plan_maintenance"))
        
        en_desc = rec.get("description", "")
        zh_desc = en_desc
        if en_desc:
            zh_desc = en_desc.replace("Visual inspection", zh_i18n.t("visual_inspection"))
            zh_desc = zh_desc.replace("inspection", zh_i18n.t("inspection"))
        
        en_motivation = rec.get("motivation", "")
        zh_motivation = en_motivation
        if en_motivation:
            zh_motivation = en_motivation.replace("ISO zone C indicates attention needed", zh_i18n.t("iso_zone_c_indicates"))
            zh_motivation = zh_motivation.replace("ISO zone", zh_i18n.t("iso_zone"))
        
        evidence = "".join(
            f'<p style="margin-top:0.25rem;{_MUTED}font-size:0.9rem;">'
            f'<span data-i18n="evidence_label">{_esc(evidence_label)}</span>: {_esc(item)}</p>'
            for item in rec.get("evidence", [])
        )
        items.append(
            '<div style="padding:1rem 0;border-bottom:1px solid var(--border-color);">'
            '<p style="font-weight:600;font-size:1.05rem;">'
            f'<span class="badge {badge}" style="margin-right:0.5rem;"'
            f'{_val_attrs(en_urgency, zh_urgency, lang)}>'
            f"{_esc(display_urgency)}</span>"
            f'<span{_val_attrs(en_action, zh_action, lang)}>{_esc(en_action if lang == "en" else zh_action)}</span></p>'
            f'<p{_val_attrs(en_desc, zh_desc, lang)} style="margin-top:0.4rem;">{_esc(en_desc if lang == "en" else zh_desc)}</p>'
            f'<p style="margin-top:0.4rem;{_MUTED}">'
            f'<strong><span data-i18n="why">{_esc(why_label)}</span>:</strong> '
            f'<span{_val_attrs(en_motivation, zh_motivation, lang)}>{_esc(en_motivation if lang == "en" else zh_motivation)}</span></p>'
            f"{evidence}</div>"
        )

    return (
        '<div class="card">'
        f'<h2 class="card-title" data-i18n="recommended_actions">{_esc(rec_actions)}</h2>'
        f'{"".join(items)}</div>'
    )


def _baseline_card(baseline: dict[str, Any], i18n: Any = None, lang: str = "en") -> str:
    from .i18n import get_i18n
    zh_i18n = get_i18n("zh")
    
    to_resolve = i18n.t("to_resolve") if i18n else "To resolve"
    comparison_title = i18n.t("comparison_with_baseline") if i18n else "Comparison with baseline"

    en_statement = baseline.get("statement", "")
    zh_statement = en_statement
    if en_statement:
        zh_statement = en_statement.replace("No baseline available for comparison", zh_i18n.t("no_baseline_available"))
    
    deltas = "".join(
        f'<li style="margin-bottom:0.4rem;"{_val_attrs(delta["statement"], delta["statement"], lang)}>{_esc(delta["statement"])}</li>'
        for delta in baseline.get("deltas", [])
    )
    delta_list = (
        f'<ul style="margin-top:0.75rem;padding-left:1.25rem;">{deltas}</ul>'
        if deltas
        else ""
    )
    
    # Get both EN and ZH remedies
    en_remedy = baseline.get("remedy", "")
    zh_remedy = en_remedy
    if en_remedy:
        zh_remedy = en_remedy.replace("Plan maintenance", zh_i18n.t("plan_maintenance"))
        zh_remedy = zh_remedy.replace("Monitor condition", zh_i18n.t("monitor_condition"))
        zh_remedy = zh_remedy.replace("inspection", zh_i18n.t("inspection"))
    display_remedy = zh_remedy if lang == "zh" else en_remedy
    
    return (
        '<div class="card">'
        f'<h2 class="card-title" data-i18n="comparison_with_baseline">{_esc(comparison_title)}'
        f'{_status_badge(baseline.get("status"), lang)}</h2>'
        f'<p{_val_attrs(en_statement, zh_statement, lang)}>{_esc(zh_statement if lang == "zh" else en_statement)}</p>'
        f"{delta_list}"
        f'{_remedy_paragraph(display_remedy, to_resolve, lang=lang, en_remedy=en_remedy, zh_remedy=zh_remedy)}'
        "</div>"
    )


def _iso_card(iso: dict[str, Any], i18n: Any = None, lang: str = "en") -> str:
    from .i18n import get_i18n
    zh_i18n = get_i18n("zh")
    
    to_resolve = i18n.t("to_resolve") if i18n else "To resolve"
    iso_title = i18n.t("iso_severity") if i18n else "ISO severity"
    
    # Get EN and ZH statements
    en_statement = iso.get("statement", "")
    zh_statement = en_statement
    for zone in ["A", "B", "C", "D"]:
        if en_statement == f"Zone {zone}":
            zh_statement = zh_i18n.t(f"zone_{zone.lower()}")
        elif en_statement == zone:
            zh_statement = zh_i18n.t(f"zone_{zone.lower()}")

    # Get EN and ZH standard notes
    en_note = iso.get("standard_note", "")
    zh_note = en_note  # Standard note is typically not translated

    # Get EN and ZH remedies
    en_remedy = iso.get("remedy", "")
    zh_remedy = en_remedy
    zh_remedy = en_remedy.replace("Plan maintenance", zh_i18n.t("plan_maintenance"))
    zh_remedy = zh_remedy.replace("Monitor condition", zh_i18n.t("monitor_condition"))
    zh_remedy = zh_remedy.replace("inspection", zh_i18n.t("inspection"))
    
    return (
        '<div class="card">'
        f'<h2 class="card-title" data-i18n="iso_severity">{_esc(iso_title)}'
        f'{_status_badge(iso.get("status"), lang)}</h2>'
        f'<p{_val_attrs(en_statement, zh_statement, lang)}>{_esc(zh_statement if lang == "zh" else en_statement)}</p>'
        f'<p{_val_attrs(en_note, zh_note, lang)} style="margin-top:0.75rem;font-size:0.875rem;{_MUTED}">'
        f'{_esc(zh_note if lang == "zh" else en_note)}</p>'
        f'{_remedy_paragraph(zh_remedy if lang == "zh" else en_remedy, to_resolve, lang=lang, en_remedy=en_remedy, zh_remedy=zh_remedy)}'
        "</div>"
    )


def _evidence_card(evidence: dict[str, Any], i18n: Any = None, lang: str = "en") -> str:
    from .i18n import get_i18n
    zh_i18n = get_i18n("zh")
    
    evidence_title = i18n.t("evidence") if i18n else "Evidence"
    strength_label = i18n.t("evidence_strength") if i18n else "Evidence strength"
    
    # Get EN and ZH strength values
    en_strength = evidence["strength"]
    zh_strength = zh_i18n.t(en_strength.lower())
    if zh_strength == en_strength.lower():
        zh_strength = en_strength
    
    # Get EN and ZH strength explanations
    en_explanation = evidence["strength_explanation"]
    zh_explanation = en_explanation
    zh_explanation = en_explanation.replace("ISO evaluation indicates", zh_i18n.t("iso_evaluation_indicates"))
    zh_explanation = zh_explanation.replace("Zone", zh_i18n.t("zone"))
    zh_explanation = zh_explanation.replace("with severity level", zh_i18n.t("with_severity_level"))
    for severity in ["New", "Acceptable", "Unsatisfactory", "Severe"]:
        zh_explanation = zh_explanation.replace(severity, zh_i18n.t(severity.lower()))

    # Get EN and ZH evidence items
    en_items = []
    zh_items = []
    for item in evidence["statements"]:
        en_items.append(item)
        zh_item = item
        zh_item = zh_item.replace("RMS velocity", zh_i18n.t("rms_velocity"))
        zh_item = zh_item.replace("ISO zone", zh_i18n.t("iso_zone"))
        zh_item = zh_item.replace("Severity", zh_i18n.t("severity"))
        for zone in ["A", "B", "C", "D"]:
            zh_item = zh_item.replace(f"Zone {zone}", zh_i18n.t(f"zone_{zone.lower()}"))
        for severity in ["New", "Acceptable", "Unsatisfactory", "Severe"]:
            zh_item = zh_item.replace(severity, zh_i18n.t(severity.lower()))
        zh_items.append(zh_item)
    
    # Build items HTML with both EN and ZH values
    items_html = ""
    for en_item, zh_item in zip(en_items, zh_items):
        display_item = zh_item if lang == "zh" else en_item
        items_html += f'<li style="margin-bottom:0.5rem;"{_val_attrs(en_item, zh_item, lang)}>{_esc(display_item)}</li>'
    
    return (
        '<div class="card">'
        f'<h2 class="card-title" data-i18n="evidence">{_esc(evidence_title)}</h2>'
        f'<p><strong><span data-i18n="evidence_strength">{_esc(strength_label)}</span>: '
        f'<span{_val_attrs(en_strength, zh_strength, lang)}>{_esc(zh_strength if lang == "zh" else en_strength)}</span></strong></p>'
        f'<p{_val_attrs(en_explanation, zh_explanation, lang)} style="{_MUTED}font-size:0.9rem;margin-top:0.25rem;">'
        f'{_esc(zh_explanation if lang == "zh" else en_explanation)}</p>'
        f'<ul style="margin-top:0.9rem;padding-left:1.25rem;">{items_html}</ul>'
        "</div>"
    )


def _provenance_card(provenance: dict[str, Any], generated_at: str, i18n: Any = None, lang: str = "en") -> str:
    from .i18n import get_i18n
    zh_i18n = get_i18n("zh")
    
    en_signal_label = "Signal"
    zh_signal_label = zh_i18n.t("signal")
    en_rpm_label = "Shaft speed (RPM)"
    zh_rpm_label = zh_i18n.t("shaft_speed_rpm")
    en_bearing_label = "Bearing"
    zh_bearing_label = zh_i18n.t("bearing")
    en_iso_label = "ISO machine group / support"
    zh_iso_label = zh_i18n.t("iso_machine_group_support")
    en_version_label = "Server version"
    zh_version_label = zh_i18n.t("server_version")
    en_generated_label = "Generated"
    zh_generated_label = zh_i18n.t("generated")
    en_provenance_title = "Provenance"
    zh_provenance_title = zh_i18n.t("provenance")

    fields = [
        (en_signal_label, zh_signal_label, provenance.get("signal_id")),
        (en_rpm_label, zh_rpm_label, provenance.get("rpm")),
        (en_bearing_label, zh_bearing_label, provenance.get("bearing_id")),
        (
            en_iso_label, zh_iso_label,
            f"{provenance.get('machine_group')} / {zh_i18n.t(provenance.get('support_type', ''))}",
        ),
        (en_version_label, zh_version_label, provenance.get("server_version")),
        (en_generated_label, zh_generated_label, generated_at),
    ]
    cells = "".join(
        '<div class="info-item">'
        f'<div class="info-label"{_val_attrs(en_label, zh_label, lang)}>{_esc(en_label if lang == "en" else zh_label)}</div>'
        f'<div class="info-value" style="font-size:1rem;">{_esc(value)}</div>'
        "</div>"
        for en_label, zh_label, value in fields
    )
    return (
        '<div class="card">'
        f'<h2 class="card-title" data-i18n="provenance">{_esc(en_provenance_title if lang == "en" else zh_provenance_title)}</h2>'
        f'<div class="info-grid">{cells}</div>'
        "</div>"
    )


def create_integrated_diagnostic_report(
    advisory: dict[str, Any],
    figure: Optional[dict[str, Any]] = None,
    generated_at: str = "",
    language: str = "en",
) -> str:
    """Render the server-authored advisory as one integrated document.

    Args:
        advisory: Payload from
            :func:`.decision_support.advisory.build_advisory`. Every
            evaluative string rendered here comes from it.
        figure: Optional description from
            :func:`.figures.build_annotated_envelope_figure`.
        generated_at: Generation timestamp, passed in rather than read from
            the clock. Reproducibility is a claim about content, and a
            template that reads the clock cannot make it.
        language: Language code ('en' or 'zh', default: 'en')

    Returns:
        A complete, self-contained HTML document with no external references.
    """
    i18n = get_i18n(language)
    verdict = advisory["verdict"]
    
    # Get EN and ZH verdict statements
    en_verdict = verdict["statement"]
    zh_verdict = en_verdict
    if i18n:
        zh_verdict = en_verdict.replace("Machine condition", i18n.t("machine_condition"))
        zh_verdict = zh_verdict.replace("Zone", i18n.t("zone"))
        for zone in ["A", "B", "C", "D"]:
            zh_verdict = zh_verdict.replace(f"Zone {zone}", i18n.t(f"zone_{zone.lower()}"))
        for severity in ["New", "Acceptable", "Unsatisfactory", "Severe"]:
            zh_verdict = zh_verdict.replace(severity, i18n.t(severity.lower()))

    disagreements = "".join(
        '<div class="card" style="border-left:4px solid var(--warning-color);">'
        f'<h2 class="card-title" data-i18n="indicators_disagree">{_esc(i18n.t("indicators_disagree"))}</h2>'
        f'<p>{_esc(entry["statement"])}</p></div>'
        for entry in advisory["disagreements"]
    )

    content = (
        '<div class="header"><div class="header-content">'
        f'<h1 data-i18n="diagnostic_report">{_esc(i18n.t("diagnostic_report"))} &mdash; {_esc(advisory["signal_id"])}</h1>'
        f'<p class="subtitle"{_val_attrs(en_verdict, zh_verdict, language)}>{_esc(zh_verdict if language == "zh" else en_verdict)}</p>'
        "</div></div>"
        '<div class="container">'
        f"{_evidence_card(advisory['evidence'], i18n, language)}"
        f"{_iso_card(advisory['iso'], i18n, language)}"
        f"{disagreements}"
        f"{_block_card(i18n.t('bearing_frequency_matching'), advisory['bearing_match'], i18n, title_key='bearing_frequency_matching', lang=language)}"
        f"{_bearing_table(advisory['bearing_match'], i18n, language)}"
        f"{_figure_card(figure, i18n, language)}"
        f"{_block_card(i18n.t('anomaly_detection'), advisory['anomaly'], i18n, title_key='anomaly_detection', lang=language)}"
        f"{_block_card(i18n.t('spectral_energy_distribution'), advisory['spectral_energy'], i18n, title_key='spectral_energy_distribution', lang=language)}"
        f"{_baseline_card(advisory['baseline_comparison'], i18n, language)}"
        f"{_recommendations_card(advisory['recommendations'], i18n, language)}"
        f"{_provenance_card(advisory['provenance'], generated_at, i18n, language)}"
        "</div>"
    )

    return get_base_template(
        title=f"{i18n.t('diagnostic_report')} - {advisory['signal_id']}",
        content=content,
        metadata={
            "report_type": "integrated_diagnostic",
            "provenance": advisory["provenance"],
            "verdict": verdict,
            "evidence_strength": advisory["evidence"]["strength"],
        },
        include_plotly=False,
        language=language,
    )
