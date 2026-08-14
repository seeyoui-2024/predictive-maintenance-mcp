"""
Professional HTML Report Templates for Machinery Diagnostics

This module contains modern, responsive HTML templates for data visualization.
All templates are self-contained with inline CSS and use Plotly.js CDN for interactivity.
"""

import json
from typing import Dict, List, Any, Optional

from .i18n import t
from .i18n.translations import _TRANSLATIONS


def _build_i18n_js(dynamic: Optional[Dict[str, Dict[str, str]]] = None) -> str:
    """Build the window._i18n JavaScript dictionary for client-side language switching.

    Args:
        dynamic: Optional dict of {key: {lang: value}} for dynamic content that
                 needs client-side translation support (e.g. diagnostic statements
                 generated at render time rather than from the static translation table).
    """
    i18n_dict = {}
    for lang_code in ["en", "zh-CN"]:
        for key, value in _TRANSLATIONS.get(lang_code, {}).items():
            if key not in i18n_dict:
                i18n_dict[key] = {}
            i18n_dict[key][lang_code] = value
    if dynamic:
        for key, trans in dynamic.items():
            if key not in i18n_dict:
                i18n_dict[key] = {}
            for lang_code, value in trans.items():
                i18n_dict[key][lang_code] = value
    json_str = json.dumps(i18n_dict, ensure_ascii=False)
    return f"window._i18n = {json_str};"


def get_base_template(
    title: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None,
    include_plotly: bool = True,
    lang: str = "en",
    dynamic_i18n: Optional[Dict[str, Dict[str, str]]] = None,
) -> str:
    """
    Base HTML template with professional styling.

    Args:
        title: Report title
        content: Main HTML content
        metadata: Optional metadata dict (stored as JSON in data attribute)
        include_plotly: Load Plotly from CDN. The per-analysis reports need it
            for their interactive charts. Reports that must open with no
            network access pass ``False`` and draw with inline SVG instead —
            a document that fetches a script is not self-contained.
        lang: Language code ('en' or 'zh-CN') for the report UI.
        dynamic_i18n: Optional dict of {key: {lang: value}} for dynamic
            translations that are not in the static translation table.

    Returns:
        Complete HTML document
    """
    import html as _html
    import json

    # Titles carry signal identifiers, which originate in user input. The
    # <title> element is not a raw-HTML slot the way `content` is.
    safe_title = _html.escape(str(title))

    # Inside a <script> block the JSON is parsed by the HTML tokenizer first,
    # so a literal "</script>" sequence in any value would close the element
    # early. "<\/" is a valid JSON escape for "</" and is inert in HTML.
    metadata_json = json.dumps(metadata or {}, indent=2, default=str).replace(
        "</", "<\\/"
    )
    metadata_section = f'<script type="application/json" id="report-metadata">\n{metadata_json}\n</script>'
    plotly_tag = (
        '<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>'
        if include_plotly
        else "<!-- self-contained: no external scripts -->"
    )

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="generator" content="Predictive Maintenance MCP Server">
    <title>{safe_title}</title>
    {plotly_tag}
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --success-color: #27ae60;
            --warning-color: #f39c12;
            --danger-color: #e74c3c;
            --background: #f8f9fa;
            --card-background: #ffffff;
            --text-primary: #2c3e50;
            --text-secondary: #7f8c8d;
            --border-color: #e0e0e0;
            --shadow: 0 2px 8px rgba(0,0,0,0.1);
            --shadow-hover: 0 4px 16px rgba(0,0,0,0.15);
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: var(--background);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 0;
            margin: 0;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 1rem;
            box-shadow: var(--shadow);
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        .header-content {{
            max-width: 1400px;
            margin: 0 auto;
            position: relative;
        }}

        .lang-toggle {{
            position: fixed;
            top: 1rem;
            right: 1rem;
            display: flex;
            gap: 0.25rem;
            z-index: 1000;
        }}

        .lang-btn {{
            padding: 0.35rem 0.85rem;
            border: 1px solid rgba(255,255,255,0.5);
            border-radius: 6px;
            background: transparent;
            color: white;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.2s;
        }}

        .lang-btn.active {{
            background: white;
            color: var(--primary-color);
        }}

        .lang-btn:hover {{
            background: rgba(255,255,255,0.2);
        }}
        
        .header h1 {{
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }}
        
        .header .subtitle {{
            opacity: 0.95;
            font-size: 1rem;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 1rem;
        }}
        
        .card {{
            background: var(--card-background);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: var(--shadow);
            transition: box-shadow 0.3s ease;
        }}
        
        .card:hover {{
            box-shadow: var(--shadow-hover);
        }}
        
        .card-title {{
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-primary);
            border-bottom: 2px solid var(--secondary-color);
            padding-bottom: 0.5rem;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}
        
        .info-item {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid var(--secondary-color);
        }}
        
        .info-label {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.25rem;
            font-weight: 600;
        }}
        
        .info-value {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
        }}
        
        .chart-container {{
            background: var(--card-background);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: var(--shadow);
        }}
        
        .footer {{
            text-align: center;
            padding: 2rem 1rem;
            color: var(--text-secondary);
            border-top: 1px solid var(--border-color);
            margin-top: 3rem;
        }}
        
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.875rem;
            font-weight: 600;
            text-transform: uppercase;
        }}
        
        .badge-success {{
            background: var(--success-color);
            color: white;
        }}
        
        .badge-warning {{
            background: var(--warning-color);
            color: white;
        }}
        
        .badge-danger {{
            background: var(--danger-color);
            color: white;
        }}
        
        .badge-info {{
            background: var(--secondary-color);
            color: white;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 1.5rem;
            }}
            .info-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        @media print {{
            .header {{
                position: static;
            }}
            .card {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    {metadata_section}
    <div class="lang-toggle">
        <button onclick="switchLang('en')" id="btn-en" class="lang-btn {'active' if lang == 'en' else ''}">EN</button>
        <button onclick="switchLang('zh-CN')" id="btn-zh" class="lang-btn {'active' if lang == 'zh-CN' else ''}">中文</button>
    </div>
    {content}
    <div class="footer">
        <p>Generated by <strong>Predictive Maintenance MCP Server</strong></p>
        <p style="font-size: 0.875rem; margin-top: 0.5rem; color: var(--text-secondary);">
            Professional machinery diagnostics and vibration analysis
        </p>
    </div>
<script>
    {_build_i18n_js(dynamic=dynamic_i18n)}
    function switchLang(lang) {{
        localStorage.setItem('pdm_lang', lang);
        document.documentElement.lang = lang;
        document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
        var btnId = lang === 'zh-CN' ? 'zh' : 'en';
        var btn = document.getElementById('btn-' + btnId);
        if (btn) btn.classList.add('active');
        // Translate all elements with data-i18n
        document.querySelectorAll('[data-i18n]').forEach(function(el) {{
            var key = el.getAttribute('data-i18n');
            if (window._i18n && window._i18n[key] && window._i18n[key][lang]) {{
                el.textContent = window._i18n[key][lang];
            }}
        }});
    }}

    (function() {{
        var saved = localStorage.getItem('pdm_lang');
        if (saved) {{
            document.documentElement.lang = saved;
            document.querySelectorAll('.lang-btn').forEach(btn => btn.classList.remove('active'));
            var btnId = saved === 'zh-CN' ? 'btn-zh' : 'btn-en';
            var btn = document.getElementById(btnId);
            if (btn) btn.classList.add('active');
            // Apply translations for saved language
            document.querySelectorAll('[data-i18n]').forEach(function(el) {{
                var key = el.getAttribute('data-i18n');
                if (window._i18n && window._i18n[key] && window._i18n[key][saved]) {{
                    el.textContent = window._i18n[key][saved];
                }}
            }});
        }}
    }})();
    </script>
</body>
</html>"""


def create_fft_report(
    signal_file: str,
    sampling_rate: float,
    frequencies: List[float],
    magnitudes_db: List[float],
    peaks: List[Dict[str, float]],
    metadata: Dict[str, Any],
    lang: str = "en",
) -> str:
    """
    Create professional FFT spectrum report.

    Args:
        signal_file: Signal filename
        sampling_rate: Sampling rate in Hz
        frequencies: Frequency array
        magnitudes_db: Magnitude array in dB
        peaks: List of detected peaks with 'frequency' and 'magnitude_db'
        metadata: Additional metadata
        lang: Language code ('en' or 'zh-CN')

    Returns:
        Complete HTML report
    """
    # Info cards
    info_cards = f"""
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label" data-i18n="ui.sampling_rate">{t("ui.sampling_rate", lang)}</div>
            <div class="info-value">{sampling_rate:.0f} Hz</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="ui.frequency_range">{t("ui.frequency_range", lang)}</div>
            <div class="info-value">0 - {max(frequencies):.0f} Hz</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="ui.signal_length">{t("ui.signal_length", lang)}</div>
            <div class="info-value">{metadata.get('num_samples', 'N/A'):,}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="ui.duration">{t("ui.duration", lang)}</div>
            <div class="info-value">{metadata.get('duration', 0):.2f} s</div>
        </div>
    </div>
    """

    # Peaks table
    peaks_html = f"<div class='card'><h3 class='card-title' data-i18n='ui.detected_peaks'>🎯 {t('ui.detected_peaks', lang)}</h3><table style='width:100%; border-collapse: collapse;'>"
    peaks_html += f"<tr style='background: #f5f7fa; font-weight: 600;'><th style='padding: 0.75rem; text-align: left;' data-i18n='ui.rank'>{t('ui.rank', lang)}</th><th style='padding: 0.75rem; text-align: left;' data-i18n='ui.frequency_hz'>{t('ui.frequency_hz', lang)}</th><th style='padding: 0.75rem; text-align: left;' data-i18n='ui.magnitude_db'>{t('ui.magnitude_db', lang)}</th><th style='padding: 0.75rem; text-align: left;' data-i18n='ui.note'>{t('ui.note', lang)}</th></tr>"

    for i, peak in enumerate(peaks[:10], 1):
        freq = peak["frequency"]
        mag_db = peak["magnitude_db"]
        note = peak.get("note", "")

        peaks_html += f"<tr style='border-bottom: 1px solid #e0e0e0;'>"
        peaks_html += f"<td style='padding: 0.75rem;'><strong>#{i}</strong></td>"
        peaks_html += (
            f"<td style='padding: 0.75rem; font-family: monospace;'>{freq:.2f}</td>"
        )
        peaks_html += (
            f"<td style='padding: 0.75rem; font-family: monospace;'>{mag_db:.1f}</td>"
        )
        peaks_html += f"<td style='padding: 0.75rem; color: #e74c3c;'>{note}</td>"
        peaks_html += "</tr>"

    peaks_html += "</table></div>"

    # Plotly chart
    chart_div = "<div class='chart-container'><div id='fft-chart'></div></div>"

    # Plotly script
    peak_freqs = [p["frequency"] for p in peaks[:10]]
    peak_mags = [p["magnitude_db"] for p in peaks[:10]]
    peak_labels = [f"{p['frequency']:.1f}" for p in peaks[:10]]

    plotly_script = f"""
    <script>
        var spectrum = {{
            x: {frequencies},
            y: {magnitudes_db},
            type: 'scatter',
            mode: 'lines',
            name: '{t("chart.label.spectrum", lang)}',
            line: {{
                color: '#667eea',
                width: 1.5
            }},
            hovertemplate: '%{{x:.2f}} Hz<br>%{{y:.1f}} dB<extra></extra>'
        }};
        
        var peaks = {{
            x: {peak_freqs},
            y: {peak_mags},
            type: 'scatter',
            mode: 'markers+text',
            name: '{t("chart.label.peaks", lang)}',
            marker: {{
                color: '#e74c3c',
                size: 10,
                symbol: 'diamond',
                line: {{
                    color: 'white',
                    width: 2
                }}
            }},
            text: {peak_labels},
            textposition: 'top center',
            textfont: {{
                size: 10,
                color: '#e74c3c',
                family: 'monospace'
            }},
            hovertemplate: '%{{x:.2f}} Hz<br>%{{y:.1f}} dB<extra></extra>'
        }};
        
        var layout = {{
            title: {{
                text: '{t("chart.title.fft", lang)}',
                font: {{ size: 20, color: '#2c3e50' }}
            }},
            xaxis: {{
                title: '{t("chart.axis.frequency", lang)}',
                gridcolor: '#e0e0e0',
                showgrid: true
            }},
            yaxis: {{
                title: '{t("chart.axis.magnitude_db", lang)}',
                gridcolor: '#e0e0e0',
                showgrid: true
            }},
            hovermode: 'closest',
            plot_bgcolor: '#fafafa',
            paper_bgcolor: 'white',
            showlegend: true,
            legend: {{
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(255,255,255,0.9)',
                bordercolor: '#ccc',
                borderwidth: 1
            }},
            margin: {{ t: 80, r: 30, b: 60, l: 70 }}
        }};
        
        var config = {{
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
        }};
        
        Plotly.newPlot('fft-chart', [spectrum, peaks], layout, config);
    </script>
    """

    content = f"""
    <div class="header">
        <div class="header-content">
            <h1 data-i18n="report.title.fft">📊 {t("report.title.fft", lang)}</h1>
            <p class="subtitle">{signal_file}</p>
        </div>
    </div>
    <div class="container">
        {info_cards}
        {chart_div}
        {peaks_html}
    </div>
    {plotly_script}
    """

    return get_base_template(
        title=f"FFT Analysis - {signal_file}", content=content, metadata=metadata, lang=lang
    )


def create_envelope_report(
    signal_file: str,
    sampling_rate: float,
    filter_band: tuple,
    time_data: List[float],
    filtered_signal: List[float],
    envelope: List[float],
    env_freq: List[float],
    env_mag_db: List[float],
    peaks: List[Dict[str, float]],
    bearing_freqs: Optional[Dict[str, float]],
    metadata: Dict[str, Any],
    lang: str = "en",
) -> str:
    """
    Create professional envelope analysis report.

    Args:
        signal_file: Signal filename
        sampling_rate: Sampling rate
        filter_band: (low, high) Hz
        time_data: Time array for signal plot
        filtered_signal: Filtered signal
        envelope: Envelope signal
        env_freq: Envelope spectrum frequencies
        env_mag_db: Envelope spectrum magnitudes in dB
        peaks: Detected peaks
        bearing_freqs: Optional dict with BPFO, BPFI, BSF, FTF
        metadata: Additional metadata
        lang: Language code ('en' or 'zh-CN')

    Returns:
        Complete HTML report
    """
    # Info cards
    info_cards = f"""
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label" data-i18n="ui.filter_range">{t("ui.filter_range", lang)}</div>
            <div class="info-value">{filter_band[0]:.0f}-{filter_band[1]:.0f} Hz</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="ui.sampling_rate">{t("ui.sampling_rate", lang)}</div>
            <div class="info-value">{sampling_rate:.0f} Hz</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="ui.signal_length">{t("ui.signal_length", lang)}</div>
            <div class="info-value">{metadata.get('num_samples', 'N/A'):,}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="ui.duration">{t("ui.duration", lang)}</div>
            <div class="info-value">{metadata.get('duration', 0):.2f} s</div>
        </div>
    </div>
    """

    # Bearing frequencies reference (if provided)
    bearing_ref = ""
    if bearing_freqs:
        bearing_ref = f"<div class='card'><h3 class='card-title' data-i18n='ui.bearing_char_freq'>📌 {t('ui.bearing_char_freq', lang)}</h3><div class='info-grid'>"
        colors = {
            "BPFO": "#e74c3c",
            "BPFI": "#f39c12",
            "BSF": "#3498db",
            "FTF": "#2ecc71",
        }
        for name, freq in bearing_freqs.items():
            if freq:
                color = colors.get(name, "#95a5a6")
                bearing_ref += f"""
                <div class="info-item" style="border-left-color: {color};">
                    <div class="info-label">{name}</div>
                    <div class="info-value" style="color: {color};">{freq:.2f} Hz</div>
                </div>
                """
        bearing_ref += "</div></div>"

    # Peaks table
    peaks_html = f"<div class='card'><h3 class='card-title' data-i18n='ui.envelope_spectrum_peaks'>🎯 {t('ui.envelope_spectrum_peaks', lang)}</h3><table style='width:100%; border-collapse: collapse;'>"
    peaks_html += f"<tr style='background: #f5f7fa; font-weight: 600;'><th style='padding: 0.75rem; text-align: left;' data-i18n='ui.rank'>{t('ui.rank', lang)}</th><th style='padding: 0.75rem; text-align: left;' data-i18n='ui.frequency_hz'>{t('ui.frequency_hz', lang)}</th><th style='padding: 0.75rem; text-align: left;' data-i18n='ui.magnitude_db'>{t('ui.magnitude_db', lang)}</th><th style='padding: 0.75rem; text-align: left;' data-i18n='ui.match'>{t('ui.match', lang)}</th></tr>"

    for i, peak in enumerate(peaks[:10], 1):
        freq = peak["frequency"]
        mag_db = peak["magnitude_db"]
        match = peak.get("match", "")

        peaks_html += f"<tr style='border-bottom: 1px solid #e0e0e0;'>"
        peaks_html += f"<td style='padding: 0.75rem;'><strong>#{i}</strong></td>"
        peaks_html += (
            f"<td style='padding: 0.75rem; font-family: monospace;'>{freq:.2f}</td>"
        )
        peaks_html += (
            f"<td style='padding: 0.75rem; font-family: monospace;'>{mag_db:.1f}</td>"
        )
        peaks_html += f"<td style='padding: 0.75rem; color: #e74c3c; font-weight: 600;'>{match}</td>"
        peaks_html += "</tr>"

    peaks_html += "</table></div>"

    # Charts
    charts_div = "<div class='chart-container'><div id='envelope-charts'></div></div>"

    # Plotly script with subplots
    peak_freqs = [p["frequency"] for p in peaks[:10]]
    peak_mags = [p["magnitude_db"] for p in peaks[:10]]

    # Bearing frequency markers
    bearing_markers_script = ""
    if bearing_freqs:
        for name, freq in bearing_freqs.items():
            if freq and freq <= max(env_freq):
                colors = {
                    "BPFO": "#e74c3c",
                    "BPFI": "#f39c12",
                    "BSF": "#3498db",
                    "FTF": "#2ecc71",
                }
                color = colors.get(name, "#95a5a6")
                bearing_markers_script += f"""
        data.push({{
            x: [{freq}, {freq}],
            y: [-60, 0],
            type: 'scatter',
            mode: 'lines',
            name: '{name}',
            line: {{ color: '{color}', width: 2, dash: 'dash' }},
            xaxis: 'x2',
            yaxis: 'y2',
            showlegend: true,
            hovertemplate: '{name}: {freq:.2f} Hz<extra></extra>'
        }});
        """

    plotly_script = f"""
    <script>
        var filtered = {{
            x: {time_data},
            y: {filtered_signal},
            type: 'scatter',
            mode: 'lines',
            name: '{t("chart.label.filtered_signal", lang)}',
            line: {{ color: '#95a5a6', width: 0.8 }},
            xaxis: 'x',
            yaxis: 'y',
            hovertemplate: '%{{x:.3f}} s<br>%{{y:.4f}}<extra></extra>'
        }};
        
        var envelope_trace = {{
            x: {time_data},
            y: {envelope},
            type: 'scatter',
            mode: 'lines',
            name: '{t("chart.label.envelope", lang)}',
            line: {{ color: '#e74c3c', width: 2 }},
            xaxis: 'x',
            yaxis: 'y',
            hovertemplate: '%{{x:.3f}} s<br>%{{y:.4f}}<extra></extra>'
        }};
        
        var spectrum = {{
            x: {env_freq},
            y: {env_mag_db},
            type: 'scatter',
            mode: 'lines',
            name: '{t("chart.label.envelope_spectrum", lang)}',
            line: {{ color: '#11998e', width: 1.5 }},
            xaxis: 'x2',
            yaxis: 'y2',
            hovertemplate: '%{{x:.2f}} Hz<br>%{{y:.1f}} dB<extra></extra>'
        }};
        
        var peaks = {{
            x: {peak_freqs},
            y: {peak_mags},
            type: 'scatter',
            mode: 'markers',
            name: '{t("chart.label.peaks", lang)}',
            marker: {{
                color: '#e74c3c',
                size: 10,
                symbol: 'circle',
                line: {{ color: 'white', width: 2 }}
            }},
            xaxis: 'x2',
            yaxis: 'y2',
            hovertemplate: '%{{x:.2f}} Hz<br>%{{y:.1f}} dB<extra></extra>'
        }};
        
        var data = [filtered, envelope_trace, spectrum, peaks];
        
        {bearing_markers_script}
        
        var layout = {{
            title: {{
                text: '{t("chart.title.envelope", lang)}',
                font: {{ size: 20, color: '#2c3e50' }}
            }},
            grid: {{ rows: 2, columns: 1, subplots: [['xy'], ['x2y2']], roworder: 'top to bottom' }},
            xaxis: {{
                title: '{t("chart.axis.time", lang)}',
                domain: [0, 1],
                anchor: 'y'
            }},
            yaxis: {{
                title: '{t("chart.axis.amplitude", lang)}',
                domain: [0.55, 1],
                anchor: 'x'
            }},
            xaxis2: {{
                title: '{t("chart.axis.frequency", lang)}',
                domain: [0, 1],
                anchor: 'y2'
            }},
            yaxis2: {{
                title: '{t("chart.axis.magnitude_db", lang)}',
                domain: [0, 0.45],
                anchor: 'x2',
                range: [-60, 5]
            }},
            hovermode: 'closest',
            showlegend: true,
            legend: {{
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(255,255,255,0.9)',
                bordercolor: '#ccc',
                borderwidth: 1
            }},
            margin: {{ t: 80, r: 30, b: 60, l: 70 }},
            height: 800
        }};
        
        var config = {{
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
        }};
        
        Plotly.newPlot('envelope-charts', data, layout, config);
    </script>
    """

    content = f"""
    <div class="header">
        <div class="header-content">
            <h1 data-i18n="report.title.envelope">📈 {t("report.title.envelope", lang)}</h1>
            <p class="subtitle">{signal_file}</p>
        </div>
    </div>
    <div class="container">
        {info_cards}
        {bearing_ref}
        {charts_div}
        {peaks_html}
    </div>
    {plotly_script}
    """

    return get_base_template(
        title=f"Envelope Analysis - {signal_file}", content=content, metadata=metadata, lang=lang
    )


def create_iso_report(
    signal_file: str, iso_result: Dict[str, Any], metadata: Dict[str, Any],
    lang: str = "en",
) -> str:
    """
    Create professional ISO 20816-3 evaluation report.

    Args:
        signal_file: Signal filename
        iso_result: ISO evaluation result dict
        metadata: Additional metadata
        lang: Language code ('en' or 'zh-CN')

    Returns:
        Complete HTML report
    """
    zone = iso_result["zone"]
    severity = iso_result["severity_level"]
    rms_velocity = iso_result["rms_velocity"]

    # Zone color and icon
    zone_colors = {
        "A": ("#27ae60", "✓"),
        "B": ("#f39c12", "⚠"),
        "C": ("#e67e22", "⚠"),
        "D": ("#c0392b", "🚨"),
    }
    color, icon = zone_colors.get(zone, ("#95a5a6", "?"))

    # Status badge
    status_badge = f"""
    <div style="text-align: center; margin: 2rem 0;">
        <div style="display: inline-block; padding: 1.5rem 3rem; border-radius: 20px; background: {color}; color: white; font-size: 1.5rem; font-weight: 700; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
            {icon} Zone {zone} - {severity}
        </div>
    </div>
    """

    # Info cards
    info_cards = f"""
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label" data-i18n="ui.rms_velocity">{t("ui.rms_velocity", lang)}</div>
            <div class="info-value">{rms_velocity:.2f} mm/s</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="ui.evaluation_zone">{t("ui.evaluation_zone", lang)}</div>
            <div class="info-value" style="color: {color};">Zone {zone}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="ui.machine_group">{t("ui.machine_group", lang)}</div>
            <div class="info-value">{iso_result['machine_group']}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="ui.support_type">{t("ui.support_type", lang)}</div>
            <div class="info-value">{iso_result['support_type'].title()}</div>
        </div>
    </div>
    """

    # Zone boundaries
    boundaries_card = f"""
    <div class="card">
        <h3 class="card-title" data-i18n="ui.zone_boundaries">📏 {t("ui.zone_boundaries", lang)}</h3>
        <div class="info-grid">
            <div class="info-item" style="border-left-color: #27ae60;">
                <div class="info-label" data-i18n="ui.zone_ab">{t("ui.zone_ab", lang)}</div>
                <div class="info-value">{iso_result['boundary_ab']:.1f} mm/s</div>
            </div>
            <div class="info-item" style="border-left-color: #f39c12;">
                <div class="info-label" data-i18n="ui.zone_bc">{t("ui.zone_bc", lang)}</div>
                <div class="info-value">{iso_result['boundary_bc']:.1f} mm/s</div>
            </div>
            <div class="info-item" style="border-left-color: #e67e22;">
                <div class="info-label" data-i18n="ui.zone_cd">{t("ui.zone_cd", lang)}</div>
                <div class="info-value">{iso_result['boundary_cd']:.1f} mm/s</div>
            </div>
        </div>
    </div>
    """

    # Interpretation
    interpretation_card = f"""
    <div class="card">
        <h3 class="card-title" data-i18n="ui.interpretation">💡 {t("ui.interpretation", lang)}</h3>
        <p style="font-size: 1.1rem; line-height: 1.8; color: var(--text-primary);">
            {iso_result['zone_description']}
        </p>
    </div>
    """

    # Chart
    chart_div = "<div class='chart-container'><div id='iso-chart'></div></div>"

    boundaries = [
        0,
        iso_result["boundary_ab"],
        iso_result["boundary_bc"],
        iso_result["boundary_cd"],
        iso_result["boundary_cd"] * 1.3,
    ]

    _aba = f"{iso_result['boundary_ab']:.1f}"
    _bc = f"{iso_result['boundary_bc']:.1f}"
    _cd = f"{iso_result['boundary_cd']:.1f}"
    _val = f"{rms_velocity:.2f}"

    hover_zone_a = t("chart.hover.zone_a", lang).replace("{ab}", _aba)
    hover_zone_b = t("chart.hover.zone_b", lang).replace("{ab}", _aba).replace("{bc}", _bc)
    hover_zone_c = t("chart.hover.zone_c", lang).replace("{bc}", _bc).replace("{cd}", _cd)
    hover_zone_d = t("chart.hover.zone_d", lang).replace("{cd}", _cd)
    hover_measured = t("chart.hover.measured", lang).replace("{value}", _val)

    plotly_script = f"""
    <script>
        var boundaries = {{
            AB: {iso_result['boundary_ab']},
            BC: {iso_result['boundary_bc']},
            CD: {iso_result['boundary_cd']},
            max: {iso_result['boundary_cd'] * 1.3}
        }};
        
        var rmsVelocity = {rms_velocity};
        
        var trace1 = {{
            x: [boundaries.AB],
            y: ['{t("chart.label.vibration_severity", lang)}'],
            name: '{t("chart.label.zone_a", lang)}',
            type: 'bar',
            orientation: 'h',
            marker: {{
                color: '#27ae60',
                line: {{ color: '#229954', width: 2 }}
            }},
            hovertemplate: '{hover_zone_a}'
        }};
        
        var trace2 = {{
            x: [boundaries.BC - boundaries.AB],
            y: ['{t("chart.label.vibration_severity", lang)}'],
            name: '{t("chart.label.zone_b", lang)}',
            type: 'bar',
            orientation: 'h',
            marker: {{
                color: '#f39c12',
                line: {{ color: '#e67e22', width: 2 }}
            }},
            hovertemplate: '{hover_zone_b}'
        }};
        
        var trace3 = {{
            x: [boundaries.CD - boundaries.BC],
            y: ['{t("chart.label.vibration_severity", lang)}'],
            name: '{t("chart.label.zone_c", lang)}',
            type: 'bar',
            orientation: 'h',
            marker: {{
                color: '#e67e22',
                line: {{ color: '#d35400', width: 2 }}
            }},
            hovertemplate: '{hover_zone_c}'
        }};
        
        var trace4 = {{
            x: [boundaries.max - boundaries.CD],
            y: ['{t("chart.label.vibration_severity", lang)}'],
            name: '{t("chart.label.zone_d", lang)}',
            type: 'bar',
            orientation: 'h',
            marker: {{
                color: '#c0392b',
                line: {{ color: '#a93226', width: 2 }}
            }},
            hovertemplate: '{hover_zone_d}'
        }};
        
        var marker = {{
            x: [rmsVelocity],
            y: ['{t("chart.label.vibration_severity", lang)}'],
            mode: 'markers+text',
            type: 'scatter',
            name: '{t("chart.label.measured", lang)}',
            marker: {{
                color: '#2c3e50',
                size: 20,
                symbol: 'circle',
                line: {{ color: '#fff', width: 3 }}
            }},
            text: [rmsVelocity.toFixed(2) + ' mm/s'],
            textposition: 'top center',
            textfont: {{ size: 14, color: '#2c3e50', family: 'Arial Black' }},
            hovertemplate: '{hover_measured}'
        }};
        
        var data = [trace1, trace2, trace3, trace4, marker];
        
        var layout = {{
            title: {{
                text: '{t("chart.title.iso", lang)}',
                font: {{ size: 20, color: '#2c3e50' }}
            }},
            barmode: 'stack',
            xaxis: {{
                title: '{t("chart.axis.rms_velocity", lang)}',
                range: [0, boundaries.max],
                showgrid: true,
                gridcolor: '#ecf0f1',
                zeroline: true
            }},
            yaxis: {{
                showticklabels: false
            }},
            height: 400,
            margin: {{ l: 50, r: 50, t: 80, b: 80 }},
            showlegend: true,
            legend: {{
                orientation: 'h',
                x: 0.5,
                xanchor: 'center',
                y: -0.2
            }},
            hovermode: 'closest',
            plot_bgcolor: '#fafafa',
            paper_bgcolor: 'white'
        }};
        
        var config = {{
            responsive: true,
            displayModeBar: true,
            displaylogo: false,
            modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
        }};
        
        Plotly.newPlot('iso-chart', data, layout, config);
    </script>
    """

    content = f"""
    <div class="header">
        <div class="header-content">
            <h1>📋 {t("ui.iso_evaluation", lang)}</h1>
            <p class="subtitle">{signal_file}</p>
        </div>
    </div>
    <div class="container">
        {status_badge}
        {info_cards}
        {chart_div}
        {boundaries_card}
        {interpretation_card}
    </div>
    {plotly_script}
    """

    return get_base_template(
        title=f"ISO 20816-3 - {signal_file}", content=content, metadata=metadata, lang=lang
    )
