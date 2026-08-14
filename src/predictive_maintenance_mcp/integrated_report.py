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
from typing import Any, Dict, List, Optional

from .figures import figure_to_svg
from .html_templates import get_base_template
from .i18n import t

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


def _dyn_put(dyn: Optional[Dict[str, Dict[str, str]]], key: str, en: str, zh: Optional[str]) -> None:
    """Populate one dynamic i18n entry.  No-op when *dyn* is None."""
    if dyn is None:
        return
    dyn[key] = {"en": en, "zh-CN": zh if zh is not None else en}


def _remedy_paragraph(
    remedy: Optional[str],
    remedy_zh: Optional[str] = None,
    lang: str = "en",
    dyn: Optional[Dict[str, Dict[str, str]]] = None,
    key: str = "",
) -> str:
    if not remedy:
        return ""
    if key:
        _dyn_put(dyn, key, remedy, remedy_zh)
    return (
        f'<p style="margin-top:0.75rem;{_MUTED}">'
        f'<strong data-i18n="ui.to_resolve">{t("ui.to_resolve", lang)}</strong> '
        f'<span data-i18n="{key}">{_esc(remedy)}</span></p>'
    )


def _status_badge(
    status: Optional[str],
    lang: str = "en",
    dyn: Optional[Dict[str, Dict[str, str]]] = None,
) -> str:
    css = _STATUS_BADGE.get(status or "", "badge-info")
    status_display = t(f"status.{status or 'unknown'}", lang)
    zh_display = t(f"status.{status or 'unknown'}", "zh-CN")
    dyn_key = f"diag.status.badge.{status or 'unknown'}"
    _dyn_put(dyn, dyn_key, status_display, zh_display)
    return (
        f'<span class="badge {css}" style="margin-left:0.5rem;"'
        f' data-i18n="{dyn_key}">'
        f"{_esc(status_display)}</span>"
    )


def _block_card(
    title: str,
    block: dict[str, Any],
    block_zh: Optional[dict[str, Any]] = None,
    lang: str = "en",
    i18n_key: str = "",
    dyn: Optional[Dict[str, Dict[str, str]]] = None,
    block_key: str = "",
) -> str:
    """Render one indicator block, including its authored absence statement.

    A block whose input was missing still renders. A silently omitted section
    reads as "nothing to report", which is a different claim from "this could
    not be determined, and here is what that costs you".
    """
    title_attr = f' data-i18n="{i18n_key}"' if i18n_key else ""

    statement = block.get("statement") or ""
    statement_zh = None
    if block_zh:
        statement_zh = block_zh.get("statement")
    _dyn_put(dyn, f"diag.{block_key}.statement", statement, statement_zh)

    remedy = block.get("remedy")
    remedy_zh = None
    if block_zh:
        remedy_zh = block_zh.get("remedy")

    return (
        '<div class="card">'
        f'<h2 class="card-title"{title_attr}>{_esc(title)}'
        f'{_status_badge(block.get("status"), lang=lang, dyn=dyn)}</h2>'
        f'<p data-i18n="diag.{block_key}.statement">{_esc(statement)}</p>'
        f'{_remedy_paragraph(remedy, remedy_zh, lang=lang, dyn=dyn, key=f"diag.{block_key}.remedy")}'
        "</div>"
    )


def _bearing_table(
    block: dict[str, Any],
    block_zh: Optional[dict[str, Any]] = None,
    lang: str = "en",
    dyn: Optional[Dict[str, Dict[str, str]]] = None,
) -> str:
    """Calculated against measured, with a verdict per bearing element.

    Putting the two numbers side by side is what lets a reader check the
    match rather than accept it.
    """
    rows = block.get("rows") or []
    rows_zh = []
    if block_zh:
        rows_zh = block_zh.get("rows") or []
    if not rows:
        return ""

    cells = []
    for i, row in enumerate(rows):
        row_zh = rows_zh[i] if i < len(rows_zh) else {}

        measured = (
            f"{row['measured_hz']:.2f} Hz" if row.get("measured_hz") else "&mdash;"
        )
        deviation = (
            f"{row['deviation_pct']:.2f}%"
            if row.get("deviation_pct") is not None
            else "&mdash;"
        )
        verdict_css = "badge-danger" if row["matched"] else "badge-success"
        verdict_text_en = t("ui.match", lang) if row["matched"] else t("ui.no_match", lang)
        verdict_text_zh = t("ui.match", "zh-CN") if row["matched"] else t("ui.no_match", "zh-CN")

        fault_type_en = row["fault_type"]
        fault_type_zh = row_zh.get("fault_type") if row_zh else None

        _dyn_put(dyn, f"diag.bearing.fault_type.{i}", fault_type_en, fault_type_zh)
        _dyn_put(dyn, f"diag.bearing.verdict.{i}", verdict_text_en, verdict_text_zh)

        cells.append(
            "<tr>"
            f'<td data-i18n="diag.bearing.fault_type.{i}">{_esc(fault_type_en)}</td>'
            f"<td>{row['expected_hz']:.2f} Hz</td>"
            f"<td>{measured}</td>"
            f"<td>{deviation}</td>"
            f'<td><span class="badge {verdict_css}"'
            f' data-i18n="diag.bearing.verdict.{i}">{_esc(verdict_text_en)}</span></td>'
            "</tr>"
        )

    return (
        '<div class="card">'
        f'<h2 class="card-title" data-i18n="report.title.calc_vs_measured">{t("report.title.calc_vs_measured", lang)}</h2>'
        '<table style="width:100%;border-collapse:collapse;">'
        '<thead><tr style="text-align:left;border-bottom:2px solid var(--border-color);">'
        f"<th data-i18n=\"ui.element\">{t('ui.element', lang)}</th><th data-i18n=\"ui.calculated\">{t('ui.calculated', lang)}</th><th data-i18n=\"ui.measured\">{t('ui.measured', lang)}</th>"
        f"<th data-i18n=\"ui.deviation\">{t('ui.deviation', lang)}</th><th data-i18n=\"ui.verdict\">{t('ui.verdict', lang)}</th></tr></thead>"
        f'<tbody>{"".join(cells)}</tbody>'
        "</table></div>"
    )


def _figure_card(
    figure: Optional[dict[str, Any]],
    figure_zh: Optional[dict[str, Any]] = None,
    lang: str = "en",
    dyn: Optional[Dict[str, Dict[str, str]]] = None,
) -> str:
    """The figure that closes the matching argument, or a note that it is absent."""
    if not figure:
        no_figure_en = (
            "This report carries no envelope spectrum figure, so the "
            "frequency match cannot be checked visually here \u2014 only "
            "against the values in the table above."
        )
        no_figure_zh = None
        if figure_zh:
            no_figure_zh = figure_zh.get("no_figure_text")
        _dyn_put(dyn, "diag.figure.no_figure", no_figure_en, no_figure_zh)
        return (
            '<div class="card">'
            f'<h2 class="card-title" data-i18n="report.title.envelope_spectrum">{t("report.title.envelope_spectrum", lang)}</h2>'
            f'<p data-i18n="diag.figure.no_figure">{_esc(no_figure_en)}</p>'
            "</div>"
        )

    caption_en = figure.get("caption", "")
    caption_zh = None
    if figure_zh:
        caption_zh = figure_zh.get("caption")
    _dyn_put(dyn, "diag.figure.caption", caption_en, caption_zh)

    return (
        '<div class="chart-container">'
        f'<h2 class="card-title" data-i18n="report.title.envelope_spectrum">{t("report.title.envelope_spectrum", lang)}</h2>'
        f"{figure_to_svg(figure)}"
        f'<p style="margin-top:1rem;{_MUTED}font-size:0.9rem;"'
        f' data-i18n="diag.figure.caption">{_esc(caption_en)}</p>'
        "</div>"
    )


def _recommendations_card(
    recommendations: list[dict[str, Any]],
    recommendations_zh: Optional[list[dict[str, Any]]] = None,
    lang: str = "en",
    dyn: Optional[Dict[str, Dict[str, str]]] = None,
) -> str:
    """Each action with the reasoning and the evidence it rests on."""
    if not recommendations:
        return ""

    items_zh = recommendations_zh or []

    items: list[str] = []
    for i, rec in enumerate(recommendations):
        rec_zh = items_zh[i] if i < len(items_zh) else {}

        urgency = rec.get("urgency", "medium")
        badge = _URGENCY_BADGE.get(urgency, "badge-info")

        action_en = rec["action"]
        action_zh = rec_zh.get("action") if rec_zh else None
        _dyn_put(dyn, f"diag.rec.{i}.action", action_en, action_zh)

        description_en = rec.get("description") or ""
        description_zh = rec_zh.get("description") if rec_zh else None
        _dyn_put(dyn, f"diag.rec.{i}.description", description_en, description_zh)

        motivation_en = rec.get("motivation") or ""
        motivation_zh = rec_zh.get("motivation") if rec_zh else None
        _dyn_put(dyn, f"diag.rec.{i}.motivation", motivation_en, motivation_zh)

        urgency_display_en = rec.get("urgency_display", urgency)
        urgency_display_zh = rec_zh.get("urgency_display") if rec_zh else None
        _dyn_put(dyn, f"diag.rec.{i}.urgency", urgency_display_en, urgency_display_zh)

        evidence_items = rec.get("evidence", [])
        evidence_items_zh = rec_zh.get("evidence", []) if rec_zh else []
        evidence_parts: list[str] = []
        for j, item in enumerate(evidence_items):
            item_zh = evidence_items_zh[j] if j < len(evidence_items_zh) else None
            _dyn_put(dyn, f"diag.rec.{i}.evidence.{j}", item, item_zh)
            evidence_parts.append(
                f'<p style="margin-top:0.25rem;{_MUTED}font-size:0.9rem;"'
                f' data-i18n="diag.rec.{i}.evidence.{j}">'
                f"{t('ui.evidence', lang)}: {_esc(item)}</p>"
            )
        evidence_html = "".join(evidence_parts)

        items.append(
            '<div style="padding:1rem 0;border-bottom:1px solid var(--border-color);">'
            '<p style="font-weight:600;font-size:1.05rem;">'
            f'<span class="badge {badge}" style="margin-right:0.5rem;"'
            f' data-i18n="diag.rec.{i}.urgency">{_esc(urgency_display_en)}</span>'
            f'<span data-i18n="diag.rec.{i}.action">{_esc(action_en)}</span></p>'
            f'<p style="margin-top:0.4rem;"'
            f' data-i18n="diag.rec.{i}.description">{_esc(description_en)}</p>'
            f'<p style="margin-top:0.4rem;{_MUTED}">'
            f"<strong data-i18n=\"ui.why\">{t('ui.why', lang)}</strong> "
            f'<span data-i18n="diag.rec.{i}.motivation">{_esc(motivation_en)}</span></p>'
            f"{evidence_html}</div>"
        )

    return (
        '<div class="card">'
        f'<h2 class="card-title" data-i18n="report.title.recommendations">{t("report.title.recommendations", lang)}</h2>'
        f'{"".join(items)}</div>'
    )


def _baseline_card(
    baseline: dict[str, Any],
    baseline_zh: Optional[dict[str, Any]] = None,
    lang: str = "en",
    dyn: Optional[Dict[str, Dict[str, str]]] = None,
) -> str:
    statement_en = baseline.get("statement") or ""
    statement_zh = baseline_zh.get("statement") if baseline_zh else None
    _dyn_put(dyn, "diag.baseline.statement", statement_en, statement_zh)

    deltas_list = baseline.get("deltas", [])
    deltas_zh_list = baseline_zh.get("deltas", []) if baseline_zh else []
    deltas_parts: list[str] = []
    for i, delta in enumerate(deltas_list):
        delta_en = delta["statement"]
        delta_zh = deltas_zh_list[i]["statement"] if i < len(deltas_zh_list) else None
        _dyn_put(dyn, f"diag.baseline.delta.{i}", delta_en, delta_zh)
        deltas_parts.append(
            f'<li style="margin-bottom:0.4rem;"'
            f' data-i18n="diag.baseline.delta.{i}">{_esc(delta_en)}</li>'
        )
    delta_list = (
        f'<ul style="margin-top:0.75rem;padding-left:1.25rem;">{"".join(deltas_parts)}</ul>'
        if deltas_parts
        else ""
    )

    remedy = baseline.get("remedy")
    remedy_zh = baseline_zh.get("remedy") if baseline_zh else None

    return (
        '<div class="card">'
        f'<h2 class="card-title" data-i18n="report.title.baseline_comparison">{t("report.title.baseline_comparison", lang)}'
        f'{_status_badge(baseline.get("status"), lang=lang, dyn=dyn)}</h2>'
        f'<p data-i18n="diag.baseline.statement">{_esc(statement_en)}</p>'
        f"{delta_list}"
        f'{_remedy_paragraph(remedy, remedy_zh, lang=lang, dyn=dyn, key="diag.baseline.remedy")}'
        "</div>"
    )


def _iso_card(
    iso: dict[str, Any],
    iso_zh: Optional[dict[str, Any]] = None,
    lang: str = "en",
    dyn: Optional[Dict[str, Dict[str, str]]] = None,
) -> str:
    statement_en = iso.get("statement") or ""
    statement_zh = iso_zh.get("statement") if iso_zh else None
    _dyn_put(dyn, "diag.iso.statement", statement_en, statement_zh)

    note_en = iso.get("standard_note") or ""
    note_zh = iso_zh.get("standard_note") if iso_zh else None
    _dyn_put(dyn, "diag.iso.note", note_en, note_zh)

    note_html = (
        f'<p style="margin-top:0.75rem;font-size:0.875rem;{_MUTED}"'
        f' data-i18n="diag.iso.note">{_esc(note_en)}</p>'
        if note_en
        else ""
    )

    remedy = iso.get("remedy")
    remedy_zh = iso_zh.get("remedy") if iso_zh else None

    return (
        '<div class="card">'
        f'<h2 class="card-title" data-i18n="report.title.iso_severity">{t("report.title.iso_severity", lang)}'
        f'{_status_badge(iso.get("status"), lang=lang, dyn=dyn)}</h2>'
        f'<p data-i18n="diag.iso.statement">{_esc(statement_en)}</p>'
        f"{note_html}"
        f'{_remedy_paragraph(remedy, remedy_zh, lang=lang, dyn=dyn, key="diag.iso.remedy")}'
        "</div>"
    )


def _evidence_card(
    evidence: dict[str, Any],
    evidence_zh: Optional[dict[str, Any]] = None,
    lang: str = "en",
    dyn: Optional[Dict[str, Dict[str, str]]] = None,
) -> str:
    strength_en = evidence["strength"]
    strength_zh = evidence_zh["strength"] if evidence_zh else None
    _dyn_put(dyn, "diag.evidence.strength", strength_en, strength_zh)

    explanation_en = evidence["strength_explanation"]
    explanation_zh = evidence_zh["strength_explanation"] if evidence_zh else None
    _dyn_put(dyn, "diag.evidence.strength_explanation", explanation_en, explanation_zh)

    items_list = evidence["statements"]
    items_zh_list = evidence_zh["statements"] if evidence_zh else []
    items_html_parts: list[str] = []
    for i, item in enumerate(items_list):
        item_zh = items_zh_list[i] if i < len(items_zh_list) else None
        _dyn_put(dyn, f"diag.evidence.item.{i}", item, item_zh)
        items_html_parts.append(
            f'<li style="margin-bottom:0.5rem;"'
            f' data-i18n="diag.evidence.item.{i}">{_esc(item)}</li>'
        )
    items_html = "".join(items_html_parts)

    return (
        '<div class="card">'
        f'<h2 class="card-title" data-i18n="report.title.evidence">{t("report.title.evidence", lang)}</h2>'
        f'<p><strong><span data-i18n="report.title.evidence_strength">{t("report.title.evidence_strength", lang)}</span>: '
        f'<span data-i18n="diag.evidence.strength">{_esc(strength_en)}</span></strong></p>'
        f'<p style="{_MUTED}font-size:0.9rem;margin-top:0.25rem;"'
        f' data-i18n="diag.evidence.strength_explanation">{_esc(explanation_en)}</p>'
        f'<ul style="margin-top:0.9rem;padding-left:1.25rem;">{items_html}</ul>'
        "</div>"
    )


def _provenance_card(
    provenance: dict[str, Any],
    provenance_zh: Optional[dict[str, Any]] = None,
    generated_at: str = "",
    generated_at_zh: str = "",
    lang: str = "en",
    dyn: Optional[Dict[str, Dict[str, str]]] = None,
) -> str:
    label_defs = [
        ("ui.signal", provenance.get("signal_id")),
        ("ui.rpm", provenance.get("rpm")),
        ("ui.bearing", provenance.get("bearing_id")),
        ("ui.machine_group_support", f"{provenance.get('machine_group')} / {provenance.get('support_type')}"),
        ("ui.server_version", provenance.get("server_version")),
        ("ui.generated", generated_at),
    ]
    zh_label_defs = []
    if provenance_zh:
        zh_label_defs = [
            ("ui.signal", provenance_zh.get("signal_id")),
            ("ui.rpm", provenance_zh.get("rpm")),
            ("ui.bearing", provenance_zh.get("bearing_id")),
            ("ui.machine_group_support", f"{provenance_zh.get('machine_group')} / {provenance_zh.get('support_type')}"),
            ("ui.server_version", provenance_zh.get("server_version")),
            ("ui.generated", generated_at_zh or generated_at),
        ]

    cells_parts: list[str] = []
    for i, (key, value) in enumerate(label_defs):
        zh_value = zh_label_defs[i][1] if i < len(zh_label_defs) else None
        _dyn_put(dyn, f"diag.provenance.label.{i}", t(key, lang), t(key, "zh-CN"))
        _dyn_put(dyn, f"diag.provenance.value.{i}", str(value), str(zh_value) if zh_value is not None else None)
        cells_parts.append(
            '<div class="info-item">'
            f'<div class="info-label" data-i18n="diag.provenance.label.{i}">{_esc(t(key, lang))}</div>'
            f'<div class="info-value" style="font-size:1rem;" data-i18n="diag.provenance.value.{i}">{_esc(str(value))}</div>'
            "</div>"
        )

    return (
        '<div class="card">'
        f'<h2 class="card-title" data-i18n="report.title.provenance">{t("report.title.provenance", lang)}</h2>'
        f'<div class="info-grid">{"".join(cells_parts)}</div>'
        "</div>"
    )


def create_integrated_diagnostic_report(
    advisory: dict[str, Any],
    figure: Optional[dict[str, Any]] = None,
    advisory_zh: Optional[dict[str, Any]] = None,
    figure_zh: Optional[dict[str, Any]] = None,
    generated_at: str = "",
    generated_at_zh: str = "",
    lang: str = "en",
) -> str:
    """Render the server-authored advisory as one integrated document.

    Args:
        advisory: Payload from
            :func:`.decision_support.advisory.build_advisory`. Every
            evaluative string rendered here comes from it.
        figure: Optional description from
            :func:`.figures.build_annotated_envelope_figure`.
        advisory_zh: Chinese version of *advisory*.  When *None*, the
            English text is used for both language keys (backward-compatible
            fallback).
        figure_zh: Chinese version of *figure*.  When *None*, the English
            text is used for both language keys.
        generated_at: Generation timestamp, passed in rather than read from
            the clock. Reproducibility is a claim about content, and a
            template that reads the clock cannot make it.
        generated_at_zh: Chinese timestamp or equivalent display string.
        lang: Default language for the initial render.

    Returns:
        A complete, self-contained HTML document with no external references.
    """
    dyn: Dict[str, Dict[str, str]] = {}

    verdict = advisory["verdict"]
    verdict_zh = advisory_zh["verdict"] if advisory_zh else None

    verdict_statement_en = verdict["statement"]
    verdict_statement_zh = verdict_zh["statement"] if verdict_zh else None
    _dyn_put(dyn, "diag.verdict.statement", verdict_statement_en, verdict_statement_zh)

    disagreements = advisory.get("disagreements", [])
    disagreements_zh = advisory_zh.get("disagreements", []) if advisory_zh else []
    disagreement_html_parts: list[str] = []
    for i, entry in enumerate(disagreements):
        entry_zh = disagreements_zh[i] if i < len(disagreements_zh) else {}
        stmt_en = entry["statement"]
        stmt_zh = entry_zh.get("statement") if entry_zh else None
        _dyn_put(dyn, f"diag.disagreement.{i}.statement", stmt_en, stmt_zh)
        disagreement_html_parts.append(
            '<div class="card" style="border-left:4px solid var(--warning-color);">'
            f'<h2 class="card-title" data-i18n="report.title.indicators_disagree">{t("report.title.indicators_disagree", lang)}</h2>'
            f'<p data-i18n="diag.disagreement.{i}.statement">{_esc(stmt_en)}</p></div>'
        )
    disagreements_html = "".join(disagreement_html_parts)

    evidence_zh = advisory_zh.get("evidence") if advisory_zh else None
    iso_zh = advisory_zh.get("iso") if advisory_zh else None
    bearing_match_zh = advisory_zh.get("bearing_match") if advisory_zh else None
    anomaly_zh = advisory_zh.get("anomaly") if advisory_zh else None
    spectral_energy_zh = advisory_zh.get("spectral_energy") if advisory_zh else None
    baseline_zh = advisory_zh.get("baseline_comparison") if advisory_zh else None
    recommendations_zh = advisory_zh.get("recommendations") if advisory_zh else None
    provenance_zh = advisory_zh.get("provenance") if advisory_zh else None

    content = (
        '<div class="header"><div class="header-content">'
        f'<h1 data-i18n="report.title.diagnostic">{t("report.title.diagnostic", lang)} &mdash; {_esc(advisory["signal_id"])}</h1>'
        f'<p class="subtitle" data-i18n="diag.verdict.statement">{_esc(verdict_statement_en)}</p>'
        "</div></div>"
        '<div class="container">'
        f'{_evidence_card(advisory["evidence"], evidence_zh, lang=lang, dyn=dyn)}'
        f'{_iso_card(advisory["iso"], iso_zh, lang=lang, dyn=dyn)}'
        f"{disagreements_html}"
        f'{_block_card(t("report.title.bearing_matching", lang), advisory["bearing_match"], bearing_match_zh, lang=lang, i18n_key="report.title.bearing_matching", dyn=dyn, block_key="bearing_matching")}'
        f'{_bearing_table(advisory["bearing_match"], bearing_match_zh, lang=lang, dyn=dyn)}'
        f'{_figure_card(figure, figure_zh, lang=lang, dyn=dyn)}'
        f'{_block_card(t("report.title.anomaly_detection", lang), advisory["anomaly"], anomaly_zh, lang=lang, i18n_key="report.title.anomaly_detection", dyn=dyn, block_key="anomaly_detection")}'
        f'{_block_card(t("report.title.spectral_energy", lang), advisory["spectral_energy"], spectral_energy_zh, lang=lang, i18n_key="report.title.spectral_energy", dyn=dyn, block_key="spectral_energy")}'
        f'{_baseline_card(advisory["baseline_comparison"], baseline_zh, lang=lang, dyn=dyn)}'
        f'{_recommendations_card(advisory["recommendations"], recommendations_zh, lang=lang, dyn=dyn)}'
        f'{_provenance_card(advisory["provenance"], provenance_zh, generated_at, generated_at_zh, lang=lang, dyn=dyn)}'
        "</div>"
    )

    return get_base_template(
        title=f"{t('report.title.diagnostic', lang)} - {advisory['signal_id']}",
        content=content,
        metadata={
            "report_type": "integrated_diagnostic",
            "provenance": advisory["provenance"],
            "verdict": verdict,
            "evidence_strength": advisory["evidence"]["strength"],
        },
        include_plotly=False,
        lang=lang,
        dynamic_i18n=dyn,
    )