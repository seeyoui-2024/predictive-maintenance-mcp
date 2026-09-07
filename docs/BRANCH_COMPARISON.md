# Branch Comparison: main vs feat/bilingual-reports

## Overview

This document compares the two branches with bilingual (EN/ZH) support implementations.

---

## Directory Structure

| Component | main | feat/bilingual-reports |
|-----------|------|------------------------|
| Source code | `src/` | `src/predictive_maintenance_mcp/` |
| i18n module | `src/i18n.py` (single file) | `src/predictive_maintenance_mcp/i18n/` (package) |
| Translation keys | `diagnostic_report` | `report.title.diagnostic` |
| Language code | `zh` | `zh-CN` |

---

## Translation Coverage

| Feature | main | feat/bilingual-reports |
|---------|------|------------------------|
| Total translation keys | ~120 | ~400+ |
| Dynamic diagnostic statements | Partial (string replacement) | Complete (templated) |
| Chart translations | No | Yes (Plotly charts) |
| ISO zone descriptions | Simple | Detailed (with severity) |
| Recommendations | Simple | Detailed (with fault types) |

---

## Client-Side Switching Mechanism

| Aspect | main | feat/bilingual-reports |
|--------|------|------------------------|
| Switching method | `data-i18n-val-en/zh` attributes | `window._i18n` JS dictionary |
| Function signature | `switchLanguage(lang, btn, event)` | `switchLanguage(lang)` |
| Chart switching | No | Yes (Plotly restyle) |

---

## Feature Completeness

| Feature | main | feat/bilingual-reports |
|---------|------|------------------------|
| 8 report types | All supported | Partial support |
| DOCX translation | Supported | Not found |
| Test files | Present | Missing |
| Documentation | Complete | Missing |
| Data files | Complete | Missing |

---

## Translation Key Examples

### main branch (`src/i18n.py`)

```python
TRANSLATIONS = {
    "en": {
        "diagnostic_report": "Diagnostic Report",
        "evidence": "Evidence",
        "rms_velocity": "RMS velocity",
        "zone_c": "Zone C",
        ...
    },
    "zh": {
        "diagnostic_report": "诊断报告",
        "evidence": "证据",
        "rms_velocity": "均方根速度",
        "zone_c": "C区",
        ...
    }
}
```

### feat/bilingual-reports branch (`src/predictive_maintenance_mcp/i18n/translations.py`)

```python
_TRANSLATIONS = {
    "en": {
        "report.title.diagnostic": "Bearing Diagnostic Report",
        "ui.rms_velocity": "RMS Velocity",
        "iso.zone_c": "Zone C — Alert. Significant defect detected.",
        "diag.bearing.matched_statement": "Bearing {bearing_id} at {shaft_freq:.1f} Hz shaft speed: {matched_parts}.",
        ...
    },
    "zh-CN": {
        "report.title.diagnostic": "轴承诊断报告",
        "ui.rms_velocity": "均方根速度",
        "iso.zone_c": "C区 — 警报。检测到显著缺陷。",
        "diag.bearing.matched_statement": "轴承 {bearing_id} 在 {shaft_freq:.1f} Hz 轴速下：{matched_parts}。",
        ...
    }
}
```

---

## Client-Side JavaScript

### main branch

```javascript
function switchLanguage(lang, btn, event) {
    document.querySelectorAll('[data-i18n-val-' + lang + ']').forEach(el => {
        el.textContent = el.getAttribute('data-i18n-val-' + lang);
    });
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[key] && translations[key][lang]) {
            el.textContent = translations[key][lang];
        }
    });
}
```

### feat/bilingual-reports branch

```javascript
function switchLanguage(lang) {
    window._currentLang = lang;
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (window._i18n[key] && window._i18n[key][lang]) {
            el.textContent = window._i18n[key][lang];
        }
    });
    // Update Plotly charts
    if (window._plotlyCharts) {
        window._plotlyCharts.forEach(chartId => {
            updatePlotlyLanguage(chartId, lang);
        });
    }
}
```

---

## Recommendations

1. **Keep main branch** as the primary branch (complete project structure)
2. **Consider merging** translation keys from feat/bilingual-reports for better coverage
3. **Delete feat/bilingual-reports** after merging to avoid confusion

---

## How to Merge Translation Keys

If you want to use the more complete translations from feat/bilingual-reports:

```bash
# Extract translations from feat/bilingual-reports
git show origin/feat/bilingual-reports:src/predictive_maintenance_mcp/i18n/translations.py > /tmp/feat_translations.py

# Compare with main translations
diff src/i18n.py /tmp/feat_translations.py

# Manually merge the additional keys into src/i18n.py
```

---

*Document generated: 2026-09-07*
