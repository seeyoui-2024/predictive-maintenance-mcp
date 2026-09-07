"""
Professional HTML Report Templates for Machinery Diagnostics

This module contains modern, responsive HTML templates for data visualization.
All templates are self-contained with inline CSS and use Plotly.js CDN for interactivity.
"""

from typing import Dict, List, Any, Optional
from .i18n import get_i18n, I18n


def get_base_template(
    title: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None,
    include_plotly: bool = True,
    language: str = "en",
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
<html lang="en">
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
            .language-toggle {{
                display: none;
            }}
        }}
        
        .language-toggle {{
            position: fixed;
            top: 1rem;
            right: 1rem;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 8px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.15);
            padding: 0.5rem;
            display: flex;
            gap: 0.25rem;
        }}
        
        .lang-btn {{
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.875rem;
            transition: all 0.2s ease;
            background: transparent;
            color: var(--text-secondary);
        }}
        
        .lang-btn:hover {{
            background: var(--background);
        }}
        
        .lang-btn.active {{
            background: var(--secondary-color);
            color: white;
        }}
    </style>
</head>
<body>
    {metadata_section}
    <div class="language-toggle">
        <button class="lang-btn {'active' if language == 'en' else ''}" onclick="switchLanguage('en', this, event)">English</button>
        <button class="lang-btn {'active' if language == 'zh' else ''}" onclick="switchLanguage('zh', this, event)">中文</button>
    </div>
    {content}
    <div class="footer">
        <p>{_get_footer_text(language)}</p>
        <p style="font-size: 0.875rem; margin-top: 0.5rem; color: var(--text-secondary);">
            {_get_footer_subtext(language)}
        </p>
    </div>
    <script>
        // Translation dictionary for client-side switching
        var translations = {{
            "en": {{
                "sampling_rate": "Sampling Rate",
                "frequency_range": "Frequency Range",
                "signal_length": "Signal Length",
                "duration": "Duration",
                "filter_range": "Filter Range",
                "detected_peaks": "Detected Peaks",
                "envelope_spectrum_peaks": "Envelope Spectrum Peaks",
                "rank": "Rank",
                "frequency_hz": "Frequency (Hz)",
                "magnitude_db": "Magnitude (dB)",
                "note": "Note",
                "match": "Match",
                "rms_velocity": "RMS Velocity",
                "evaluation_zone": "Evaluation Zone",
                "machine_group": "Machine Group",
                "support_type": "Support Type",
                "zone_boundaries": "Zone Boundaries",
                "interpretation": "Interpretation",
                "bearing_frequencies": "Bearing Characteristic Frequencies",
                "fft_title": "FFT Spectrum Analysis",
                "envelope_title": "Envelope Analysis",
                "iso_title": "ISO 20816-3 Evaluation",
                "generated_by": "Generated by",
                "server_name": "Predictive Maintenance MCP Server",
                "professional_diagnostics": "Professional machinery diagnostics and vibration analysis",
                "hz": "Hz",
                "mm_s": "mm/s",
                "seconds": "s",
                "spectrum": "Spectrum",
                "peaks": "Peaks",
                "filtered_signal": "Filtered Signal",
                "envelope": "Envelope",
                "envelope_spectrum": "Envelope Spectrum",
                "amplitude": "Amplitude",
                "zone_a_b": "Zone A/Zone B",
                "zone_b_c": "Zone B/Zone C",
                "zone_c_d": "Zone C/Zone D",
                "vibration_severity": "Vibration Severity",
                "new_machine_condition": "New machine condition",
                "acceptable_operation": "Acceptable operation",
                "unsatisfactory": "Unsatisfactory",
                "severe_condition": "Severe condition",
                "measured": "Measured",
                "vibration_severity_iso": "Vibration Severity according to ISO 20816-3",
                "zone_a": "Zone A",
                "zone_b": "Zone B",
                "zone_c": "Zone C",
                "zone_d": "Zone D",
                "new": "New",
                "acceptable": "Acceptable",
                "severe": "Severe",
                "zone_description_new": "The machine is in new condition, vibration levels are very low.",
                "zone_description_acceptable": "The measured vibration level is within acceptable limits for this machine class.",
                "zone_description_unsatisfactory": "The vibration level is higher than acceptable. Maintenance should be planned.",
                "zone_description_severe": "The vibration level is dangerously high. Immediate action is required.",
                "rigid": "rigid",
                "flexible": "flexible",
                "plot_signal_title": "Time-Domain Signal",
                "statistics_overlay": "Statistical reference lines: RMS (green dashed), Peak (red dotted), Mean (orange dash-dot)",
                "time_s": "Time (s)",
                "signal": "Signal",
                "rms": "RMS",
                "peak_pos": "Peak (+)",
                "peak_neg": "Peak (−)",
                "mean": "Mean",
                "pca_title": "PCA Visualization",
                "model_name": "Model",
                "total_segments": "Total Segments",
                "total_anomalies": "Anomalies",
                "anomaly_ratio": "Anomaly Ratio",
                "pca_variance": "Variance Explained",
                "total_variance": "Total (2D)",
                "validation_metrics": "Validation Metrics",
                "overall_accuracy": "Overall Accuracy",
                "correct_predictions": "Correct Predictions",
                "feature_comparison_title": "Time-Domain Feature Comparison",
                "num_groups": "Groups",
                "num_features": "Features",
                "segments": "segments",
                "healthy": "Healthy",
                "faulty": "Faulty",
                "diagnostic_report": "Diagnostic Report",
                "evidence": "Evidence",
                "evidence_strength": "Evidence strength",
                "indicators_disagree": "Indicators disagree",
                "bearing_frequency_matching": "Bearing frequency matching",
                "calculated_against_measured": "Calculated against measured",
                "element": "Element",
                "calculated": "Calculated",
                "measured_hz": "Measured",
                "deviation": "Deviation",
                "verdict": "Verdict",
                "match_found": "match",
                "no_match": "no match",
                "envelope_spectrum_chart": "Envelope spectrum",
                "no_envelope_figure": "This report carries no envelope spectrum figure.",
                "anomaly_detection": "Anomaly detection",
                "spectral_energy_distribution": "Spectral energy distribution",
                "comparison_with_baseline": "Comparison with baseline",
                "recommended_actions": "Recommended actions",
                "why": "Why",
                "evidence_label": "Evidence",
                "provenance": "Provenance",
                "signal": "Signal",
                "shaft_speed_rpm": "Shaft speed (RPM)",
                "bearing": "Bearing",
                "iso_machine_group_support": "ISO machine group / support",
                "server_version": "Server version",
                "generated": "Generated",
                "to_resolve": "To resolve",
                "iso_severity": "ISO severity"
            }},
            "zh": {{
                "sampling_rate": "采样率",
                "frequency_range": "频率范围",
                "signal_length": "信号长度",
                "duration": "持续时间",
                "filter_range": "滤波范围",
                "detected_peaks": "检测到的峰值",
                "envelope_spectrum_peaks": "包络谱峰值",
                "rank": "排名",
                "frequency_hz": "频率 (Hz)",
                "magnitude_db": "幅值 (dB)",
                "note": "备注",
                "match": "匹配",
                "rms_velocity": "均方根速度",
                "evaluation_zone": "评估区域",
                "machine_group": "机器组别",
                "support_type": "支撑类型",
                "zone_boundaries": "区域边界",
                "interpretation": "解释说明",
                "bearing_frequencies": "轴承特征频率",
                "fft_title": "FFT频谱分析",
                "envelope_title": "包络分析",
                "iso_title": "ISO 20816-3 评估",
                "generated_by": "生成者",
                "server_name": "预测性维护MCP服务器",
                "professional_diagnostics": "专业机械诊断和振动分析",
                "hz": "Hz",
                "mm_s": "mm/s",
                "seconds": "秒",
                "spectrum": "频谱",
                "peaks": "峰值",
                "filtered_signal": "滤波信号",
                "envelope": "包络",
                "envelope_spectrum": "包络谱",
                "amplitude": "幅值",
                "zone_a_b": "A区/B区",
                "zone_b_c": "B区/C区",
                "zone_c_d": "C区/D区",
                "vibration_severity": "振动严重程度",
                "new_machine_condition": "新机器状态",
                "acceptable_operation": "可接受运行",
                "unsatisfactory": "不满意",
                "severe_condition": "严重状态",
                "measured": "测量值",
                "vibration_severity_iso": "根据ISO 20816-3的振动严重程度",
                "zone_a": "A区",
                "zone_b": "B区",
                "zone_c": "C区",
                "zone_d": "D区",
                "new": "新",
                "acceptable": "可接受",
                "severe": "严重",
                "zone_description_new": "机器处于新状态，振动水平非常低。",
                "zone_description_acceptable": "测量的振动水平在该机器类别的可接受范围内。",
                "zone_description_unsatisfactory": "振动水平高于可接受范围。应计划维护。",
                "zone_description_severe": "振动水平危险地高。需要立即采取行动。",
                "rigid": "刚性",
                "flexible": "柔性",
                "plot_signal_title": "时域信号",
                "statistics_overlay": "统计参考线：均方根 (绿色虚线)、峰值 (红色点线)、均值 (橙色点划线)",
                "time_s": "时间 (s)",
                "signal": "信号",
                "rms": "均方根",
                "peak_pos": "峰值 (+)",
                "peak_neg": "峰值 (−)",
                "mean": "均值",
                "pca_title": "PCA 可视化",
                "model_name": "模型",
                "total_segments": "总片段数",
                "total_anomalies": "异常数",
                "anomaly_ratio": "异常比例",
                "pca_variance": "方差解释",
                "total_variance": "总计 (2D)",
                "validation_metrics": "验证指标",
                "overall_accuracy": "总体准确率",
                "correct_predictions": "正确预测数",
                "feature_comparison_title": "时域特征对比",
                "num_groups": "分组数",
                "num_features": "特征数",
                "segments": "个片段",
                "healthy": "健康",
                "faulty": "故障",
                "diagnostic_report": "诊断报告",
                "evidence": "证据",
                "evidence_strength": "证据强度",
                "indicators_disagree": "指标不一致",
                "bearing_frequency_matching": "轴承频率匹配",
                "calculated_against_measured": "计算值与测量值对比",
                "element": "元件",
                "calculated": "计算值",
                "measured_hz": "测量值",
                "deviation": "偏差",
                "verdict": "判定",
                "match_found": "匹配",
                "no_match": "不匹配",
                "envelope_spectrum_chart": "包络谱",
                "no_envelope_figure": "本报告未包含包络谱图。",
                "anomaly_detection": "异常检测",
                "spectral_energy_distribution": "频谱能量分布",
                "comparison_with_baseline": "与基线对比",
                "recommended_actions": "建议措施",
                "why": "原因",
                "evidence_label": "证据",
                "provenance": "来源信息",
                "signal": "信号",
                "shaft_speed_rpm": "轴转速 (RPM)",
                "bearing": "轴承",
                "iso_machine_group_support": "ISO机器组别 / 支撑类型",
                "server_version": "服务器版本",
                "generated": "生成时间",
                "to_resolve": "解决方法",
                "iso_severity": "ISO 严重程度"
            }}
        }};

        var currentLang = '{language}';
        
        function switchLanguage(lang, btn, event) {{
            currentLang = lang;
            
            // Update button states
            document.querySelectorAll('.lang-btn').forEach(function(b) {{
                b.classList.remove('active');
            }});
            if (btn) btn.classList.add('active');
            else if (event && event.target) event.target.classList.add('active');
            
            // Update text elements with data-i18n attribute
            document.querySelectorAll('[data-i18n]').forEach(function(el) {{
                var key = el.getAttribute('data-i18n');
                if (translations[lang] && translations[lang][key]) {{
                    el.textContent = translations[lang][key];
                }}
            }});
            
            // Update elements with data-i18n-val-en/data-i18n-val-zh attributes
            document.querySelectorAll('[data-i18n-val-en]').forEach(function(el) {{
                var val = el.getAttribute('data-i18n-val-' + lang);
                if (val !== null) {{
                    el.textContent = val;
                    el.setAttribute('data-i18n-val', val);
                }}
            }});
            
            // Update info labels
            document.querySelectorAll('.info-label').forEach(function(el) {{
                var key = el.getAttribute('data-i18n');
                if (key && translations[lang] && translations[lang][key]) {{
                    el.textContent = translations[lang][key];
                }}
            }});
            
            // Update card titles
            document.querySelectorAll('.card-title').forEach(function(el) {{
                var key = el.getAttribute('data-i18n');
                if (key && translations[lang] && translations[lang][key]) {{
                    // Keep the emoji (first character if it's an emoji)
                    var text = el.textContent;
                    var firstChar = text.charAt(0);
                    var code = firstChar.codePointAt(0);
                    var hasEmoji = (code >= 0x1F300 && code <= 0x1F9FF);
                    el.textContent = (hasEmoji ? firstChar + ' ' : '') + translations[lang][key];
                }}
            }});
            
            // Update header titles
            document.querySelectorAll('.header h1').forEach(function(el) {{
                var key = el.getAttribute('data-i18n');
                if (key && translations[lang] && translations[lang][key]) {{
                    var text = el.textContent;
                    var firstChar = text.charAt(0);
                    var code = firstChar.codePointAt(0);
                    var hasEmoji = (code >= 0x1F300 && code <= 0x1F9FF);
                    el.textContent = (hasEmoji ? firstChar + ' ' : '') + translations[lang][key];
                }}
            }});
            
            // Update subtitle
            document.querySelectorAll('.subtitle').forEach(function(el) {{
                var val = el.getAttribute('data-i18n-val-' + lang);
                if (val !== null) {{
                    el.textContent = val;
                    el.setAttribute('data-i18n-val', val);
                }}
            }});
            
            // Update footer
            var footerP = document.querySelector('.footer p:first-child');
            if (footerP) {{
                footerP.innerHTML = translations[lang]['generated_by'] + ' <strong>' + translations[lang]['server_name'] + '</strong>';
            }}
            var footerSub = document.querySelector('.footer p:last-child');
            if (footerSub) {{
                footerSub.textContent = translations[lang]['professional_diagnostics'];
            }}
            
            // Update Plotly charts if they exist
            updatePlotlyCharts(lang);
        }}
        
        function updatePlotlyCharts(lang) {{
            // Update FFT chart
            var fftChart = document.getElementById('fft-chart');
            if (fftChart && fftChart.data) {{
                var t = translations[lang];
                var update = {{
                    'title.text': t['fft_title'] || translations['en']['fft_title'],
                    'xaxis.title': t['frequency_hz'] || translations['en']['frequency_hz'],
                    'yaxis.title': t['magnitude_db'] || translations['en']['magnitude_db']
                }};
                // Update trace names
                if (fftChart.data[0]) {{
                    update['data[0].name'] = t['spectrum'] || translations['en']['spectrum'];
                }}
                if (fftChart.data[1]) {{
                    update['data[1].name'] = t['peaks'] || translations['en']['peaks'];
                }}
                Plotly.relayout(fftChart, update);
                if (fftChart.data[0]) {{
                    Plotly.restyle(fftChart, {{'name': [t['spectrum'] || translations['en']['spectrum']]}}, [0]);
                }}
                if (fftChart.data[1]) {{
                    Plotly.restyle(fftChart, {{'name': [t['peaks'] || translations['en']['peaks']]}}, [1]);
                }}
            }}
            
            // Update Envelope chart
            var envelopeChart = document.getElementById('envelope-charts');
            if (envelopeChart && envelopeChart.data) {{
                var t = translations[lang];
                var update = {{
                    'xaxis.title': t['frequency_hz'] || translations['en']['frequency_hz'],
                    'yaxis.title': t['amplitude'] || translations['en']['amplitude']
                }};
                Plotly.relayout(envelopeChart, update);
            }}
            
            // Update ISO chart
            var isoChart = document.getElementById('iso-chart');
            if (isoChart && isoChart.data) {{
                var t = translations[lang];
                var update = {{
                    'title.text': t['vibration_severity_iso'] || translations['en']['vibration_severity_iso'],
                    'xaxis.title': (t['rms_velocity'] || translations['en']['rms_velocity']) + ' (' + (t['mm_s'] || translations['en']['mm_s']) + ')'
                }};
                Plotly.relayout(isoChart, update);
            }}
            
            // Update ISO status badge
            var statusBadge = document.getElementById('status-badge');
            if (statusBadge) {{
                var t = translations[lang];
                var zone = statusBadge.getAttribute('data-zone');
                var severity = statusBadge.getAttribute('data-severity');
                if (zone && severity) {{
                    var zoneText = t['zone_' + zone.toLowerCase()] || translations['en']['zone_' + zone.toLowerCase()];
                    var severityText = t[severity] || translations['en'][severity];
                    statusBadge.textContent = '⚠ ' + zoneText + ' - ' + severityText;
                }}
            }}
            
            // Update zone description
            var zoneDesc = document.getElementById('zone-description');
            if (zoneDesc) {{
                var t = translations[lang];
                var severity = zoneDesc.getAttribute('data-severity');
                if (severity) {{
                    var descKey = 'zone_description_' + severity;
                    zoneDesc.textContent = t[descKey] || translations['en'][descKey];
                }}
            }}
        }}
    </script>
</body>
</html>"""


def _get_footer_text(language: str = "en") -> str:
    """Get footer text based on language."""
    i18n = get_i18n(language)
    return f"{i18n.t('generated_by')} <strong>{i18n.t('server_name')}</strong>"


def _get_footer_subtext(language: str = "en") -> str:
    """Get footer subtext based on language."""
    i18n = get_i18n(language)
    return i18n.t('professional_diagnostics')


def create_fft_report(
    signal_file: str,
    sampling_rate: float,
    frequencies: List[float],
    magnitudes_db: List[float],
    peaks: List[Dict[str, float]],
    metadata: Dict[str, Any],
    language: str = "en",
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
        language: Language code ('en' or 'zh')

    Returns:
        Complete HTML report
    """
    i18n = get_i18n(language)
    
    # Info cards
    info_cards = f"""
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label" data-i18n="sampling_rate">{i18n.t('sampling_rate')}</div>
            <div class="info-value">{sampling_rate:.0f} {i18n.t('hz')}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="frequency_range">{i18n.t('frequency_range')}</div>
            <div class="info-value">0 - {max(frequencies):.0f} {i18n.t('hz')}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="signal_length">{i18n.t('signal_length')}</div>
            <div class="info-value">{metadata.get('num_samples', 'N/A'):,}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="duration">{i18n.t('duration')}</div>
            <div class="info-value">{metadata.get('duration', 0):.2f} {i18n.t('seconds')}</div>
        </div>
    </div>
    """

    # Peaks table
    peaks_html = f"<div class='card'><h3 class='card-title' data-i18n='detected_peaks'>🎯 {i18n.t('detected_peaks')}</h3><table style='width:100%; border-collapse: collapse;'>"
    peaks_html += f"<tr style='background: #f5f7fa; font-weight: 600;'><th style='padding: 0.75rem; text-align: left;' data-i18n='rank'>{i18n.t('rank')}</th><th style='padding: 0.75rem; text-align: left;' data-i18n='frequency_hz'>{i18n.t('frequency_hz')}</th><th style='padding: 0.75rem; text-align: left;' data-i18n='magnitude_db'>{i18n.t('magnitude_db')}</th><th style='padding: 0.75rem; text-align: left;' data-i18n='note'>{i18n.t('note')}</th></tr>"

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
        // Get current language translations
        var t = translations[currentLang] || translations['en'];
        
        var spectrum = {{
            x: {frequencies},
            y: {magnitudes_db},
            type: 'scatter',
            mode: 'lines',
            name: t['spectrum'],
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
            name: t['peaks'],
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
                text: t['fft_title'],
                font: {{ size: 20, color: '#2c3e50' }}
            }},
            xaxis: {{
                title: t['frequency_hz'],
                gridcolor: '#e0e0e0',
                showgrid: true
            }},
            yaxis: {{
                title: t['magnitude_db'],
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
            <h1 data-i18n="fft_title">📊 {i18n.t('fft_title')}</h1>
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
        title=f"{i18n.t('fft_title')} - {signal_file}", content=content, metadata=metadata, language=language
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
    language: str = "en",
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
        language: Language code ('en' or 'zh')

    Returns:
        Complete HTML report
    """
    i18n = get_i18n(language)
    
    # Info cards
    info_cards = f"""
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label" data-i18n="filter_range">{i18n.t('filter_range')}</div>
            <div class="info-value">{filter_band[0]:.0f}-{filter_band[1]:.0f} {i18n.t('hz')}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="sampling_rate">{i18n.t('sampling_rate')}</div>
            <div class="info-value">{sampling_rate:.0f} {i18n.t('hz')}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="signal_length">{i18n.t('signal_length')}</div>
            <div class="info-value">{metadata.get('num_samples', 'N/A'):,}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="duration">{i18n.t('duration')}</div>
            <div class="info-value">{metadata.get('duration', 0):.2f} {i18n.t('seconds')}</div>
        </div>
    </div>
    """

    # Bearing frequencies reference (if provided)
    bearing_ref = ""
    if bearing_freqs:
        bearing_ref = f"<div class='card'><h3 class='card-title' data-i18n='bearing_frequencies'>📌 {i18n.t('bearing_frequencies')}</h3><div class='info-grid'>"
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
                    <div class="info-value" style="color: {color};">{freq:.2f} {i18n.t('hz')}</div>
                </div>
                """
        bearing_ref += "</div></div>"

    # Peaks table
    peaks_html = f"<div class='card'><h3 class='card-title' data-i18n='envelope_spectrum_peaks'>🎯 {i18n.t('envelope_spectrum_peaks')}</h3><table style='width:100%; border-collapse: collapse;'>"
    peaks_html += f"<tr style='background: #f5f7fa; font-weight: 600;'><th style='padding: 0.75rem; text-align: left;' data-i18n='rank'>{i18n.t('rank')}</th><th style='padding: 0.75rem; text-align: left;' data-i18n='frequency_hz'>{i18n.t('frequency_hz')}</th><th style='padding: 0.75rem; text-align: left;' data-i18n='magnitude_db'>{i18n.t('magnitude_db')}</th><th style='padding: 0.75rem; text-align: left;' data-i18n='match'>{i18n.t('match')}</th></tr>"

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
        // Get current language translations
        var t = translations[currentLang] || translations['en'];
        
        var filtered = {{
            x: {time_data},
            y: {filtered_signal},
            type: 'scatter',
            mode: 'lines',
            name: t['filtered_signal'],
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
            name: t['envelope'],
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
            name: t['envelope_spectrum'],
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
            name: t['peaks'],
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
                text: t['time_frequency_domain'],
                font: {{ size: 20, color: '#2c3e50' }}
            }},
            grid: {{ rows: 2, columns: 1, subplots: [['xy'], ['x2y2']], roworder: 'top to bottom' }},
            xaxis: {{
                title: t['seconds'],
                domain: [0, 1],
                anchor: 'y'
            }},
            yaxis: {{
                title: t['amplitude'],
                domain: [0.55, 1],
                anchor: 'x'
            }},
            xaxis2: {{
                title: t['frequency_hz'],
                domain: [0, 1],
                anchor: 'y2'
            }},
            yaxis2: {{
                title: t['magnitude_db'],
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
            <h1 data-i18n="envelope_title">📈 {i18n.t('envelope_title')}</h1>
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
        title=f"{i18n.t('envelope_title')} - {signal_file}", content=content, metadata=metadata, language=language
    )


def create_iso_report(
    signal_file: str, iso_result: Dict[str, Any], metadata: Dict[str, Any], language: str = "en"
) -> str:
    """
    Create professional ISO 20816-3 evaluation report.

    Args:
        signal_file: Signal filename
        iso_result: ISO evaluation result dict
        metadata: Additional metadata
        language: Language code ('en' or 'zh')

    Returns:
        Complete HTML report
    """
    i18n = get_i18n(language)
    zone = iso_result["zone"]
    severity = iso_result["severity_level"]
    rms_velocity = iso_result.get("rms_velocity", iso_result.get("rms_velocity_mm_s", 0))

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
        <div id="status-badge" data-zone="{zone}" data-severity="{severity.lower()}" style="display: inline-block; padding: 1.5rem 3rem; border-radius: 20px; background: {color}; color: white; font-size: 1.5rem; font-weight: 700; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
            {icon} {i18n.t(f'zone_{zone.lower()}')} - {i18n.t(f'{severity.lower()}_level')}
        </div>
    </div>
    """

    # Info cards
    info_cards = f"""
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label" data-i18n="rms_velocity">{i18n.t('rms_velocity')}</div>
            <div class="info-value">{rms_velocity:.2f} {i18n.t('mm_s')}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="evaluation_zone">{i18n.t('evaluation_zone')}</div>
            <div class="info-value" style="color: {color};" data-i18n="zone_{zone.lower()}">{i18n.t(f'zone_{zone.lower()}')}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="machine_group">{i18n.t('machine_group')}</div>
            <div class="info-value">{iso_result['machine_group']}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="support_type">{i18n.t('support_type')}</div>
            <div class="info-value" data-i18n="{iso_result['support_type']}">{i18n.t(iso_result['support_type'])}</div>
        </div>
    </div>
    """

    # Zone boundaries
    boundaries = iso_result.get("boundaries", {})
    boundary_ab = boundaries.get("ab", boundaries.get("zone_a_b", 0))
    boundary_bc = boundaries.get("bc", boundaries.get("zone_b_c", 0))
    boundary_cd = boundaries.get("cd", boundaries.get("zone_c_d", 0))
    
    boundaries_card = f"""
    <div class="card">
        <h3 class="card-title" data-i18n="zone_boundaries">📏 {i18n.t('zone_boundaries')}</h3>
        <div class="info-grid">
            <div class="info-item" style="border-left-color: #27ae60;">
                <div class="info-label" data-i18n="zone_a_b">{i18n.t('zone_a_b')}</div>
                <div class="info-value">{boundary_ab:.1f} {i18n.t('mm_s')}</div>
            </div>
            <div class="info-item" style="border-left-color: #f39c12;">
                <div class="info-label" data-i18n="zone_b_c">{i18n.t('zone_b_c')}</div>
                <div class="info-value">{boundary_bc:.1f} {i18n.t('mm_s')}</div>
            </div>
            <div class="info-item" style="border-left-color: #e67e22;">
                <div class="info-label" data-i18n="zone_c_d">{i18n.t('zone_c_d')}</div>
                <div class="info-value">{boundary_cd:.1f} {i18n.t('mm_s')}</div>
            </div>
        </div>
    </div>
    """

    # Interpretation
    interpretation_card = f"""
    <div class="card">
        <h3 class="card-title" data-i18n="interpretation">💡 {i18n.t('interpretation')}</h3>
        <p id="zone-description" data-severity="{severity.lower()}" style="font-size: 1.1rem; line-height: 1.8; color: var(--text-primary);">
            {i18n.t(f'zone_description_{severity.lower()}')}
        </p>
    </div>
    """

    # Chart
    chart_div = "<div class='chart-container'><div id='iso-chart'></div></div>"

    boundaries_list = [
        0,
        boundary_ab,
        boundary_bc,
        boundary_cd,
        boundary_cd * 1.3,
    ]

    plotly_script = f"""
    <script>
        var boundaries = {{
            AB: {boundary_ab},
            BC: {boundary_bc},
            CD: {boundary_cd},
            max: {boundary_cd * 1.3}
        }};
        
        var rmsVelocity = {rms_velocity};
        
        // Get current language translations
        var t = translations[currentLang] || translations['en'];
        
        var trace1 = {{
            x: [boundaries.AB],
            y: [t['vibration_severity']],
            name: t['zone_a'],
            type: 'bar',
            orientation: 'h',
            marker: {{
                color: '#27ae60',
                line: {{ color: '#229954', width: 2 }}
            }},
            hovertemplate: t['zone_a'] + ': 0 - ' + boundaries.AB + ' ' + t['mm_s'] + '<br>' + t['new_machine_condition'] + '<extra></extra>'
        }};
        
        var trace2 = {{
            x: [boundaries.BC - boundaries.AB],
            y: [t['vibration_severity']],
            name: t['zone_b'],
            type: 'bar',
            orientation: 'h',
            marker: {{
                color: '#f39c12',
                line: {{ color: '#e67e22', width: 2 }}
            }},
            hovertemplate: t['zone_b'] + ': ' + boundaries.AB + ' - ' + boundaries.BC + ' ' + t['mm_s'] + '<br>' + t['acceptable_operation'] + '<extra></extra>'
        }};
        
        var trace3 = {{
            x: [boundaries.CD - boundaries.BC],
            y: [t['vibration_severity']],
            name: t['zone_c'],
            type: 'bar',
            orientation: 'h',
            marker: {{
                color: '#e67e22',
                line: {{ color: '#d35400', width: 2 }}
            }},
            hovertemplate: t['zone_c'] + ': ' + boundaries.BC + ' - ' + boundaries.CD + ' ' + t['mm_s'] + '<br>' + t['unsatisfactory'] + '<extra></extra>'
        }};
        
        var trace4 = {{
            x: [boundaries.max - boundaries.CD],
            y: [t['vibration_severity']],
            name: t['zone_d'],
            type: 'bar',
            orientation: 'h',
            marker: {{
                color: '#c0392b',
                line: {{ color: '#a93226', width: 2 }}
            }},
            hovertemplate: t['zone_d'] + ': > ' + boundaries.CD + ' ' + t['mm_s'] + '<br>' + t['severe_condition'] + '<extra></extra>'
        }};
        
        var marker = {{
            x: [rmsVelocity],
            y: [t['vibration_severity']],
            mode: 'markers+text',
            type: 'scatter',
            name: t['measured'],
            marker: {{
                color: '#2c3e50',
                size: 20,
                symbol: 'circle',
                line: {{ color: '#fff', width: 3 }}
            }},
            text: [rmsVelocity.toFixed(2) + ' ' + t['mm_s']],
            textposition: 'top center',
            textfont: {{ size: 14, color: '#2c3e50', family: 'Arial Black' }},
            hovertemplate: t['rms_velocity'] + ': ' + rmsVelocity.toFixed(2) + ' ' + t['mm_s'] + '<extra></extra>'
        }};
        
        var data = [trace1, trace2, trace3, trace4, marker];
        
        var layout = {{
            title: {{
                text: t['vibration_severity_iso'],
                font: {{ size: 20, color: '#2c3e50' }}
            }},
            barmode: 'stack',
            xaxis: {{
                title: t['rms_velocity'] + ' (' + t['mm_s'] + ')',
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
            <h1 data-i18n="iso_title">📋 {i18n.t('iso_title')}</h1>
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
        title=f"{i18n.t('iso_title')} - {signal_file}", content=content, metadata=metadata, language=language
    )


def create_plot_signal_report(
    signal_id: str,
    plot_div: str,
    duration: float,
    num_samples: int,
    sampling_rate: float,
    show_statistics: bool,
    metadata: Dict[str, Any],
    language: str = "en",
) -> str:
    """Create time-domain signal plot report with i18n support."""
    i18n = get_i18n(language)

    info_cards = f"""
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label" data-i18n="duration">{i18n.t('duration')}</div>
            <div class="info-value">{duration:.3f} {i18n.t('seconds')}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="signal_length">{i18n.t('signal_length')}</div>
            <div class="info-value">{num_samples:,}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="sampling_rate">{i18n.t('sampling_rate')}</div>
            <div class="info-value">{sampling_rate:.0f} {i18n.t('hz')}</div>
        </div>
    </div>
    """

    stats_note = ""
    if show_statistics:
        stats_note = f'<p style="margin-top:1rem;color:var(--text-secondary);font-size:0.9rem;" data-i18n="statistics_overlay">{i18n.t("statistics_overlay")}</p>'

    content = f"""
    <div class="header">
        <div class="header-content">
            <h1 data-i18n="plot_signal_title">📈 {i18n.t('plot_signal_title')}</h1>
            <p class="subtitle">{signal_id}</p>
        </div>
    </div>
    <div class="container">
        {info_cards}
        {stats_note}
        <div class="chart-container"><div id="signal-chart"></div></div>
    </div>
    """

    plotly_script = f"""
    <script>
        var chartData = {plot_div};
        var t = translations[currentLang] || translations['en'];

        function updateSignalChart(lang) {{
            var tr = translations[lang] || translations['en'];
            var chart = document.getElementById('signal-chart');
            if (chart && chart.data) {{
                var update = {{
                    'xaxis.title': tr['time_s'] || 'Time (s)',
                    'yaxis.title': tr['amplitude'] || 'Amplitude'
                }};
                if (chart.data[0]) update['data[0].name'] = tr['signal'] || 'Signal';
                Plotly.relayout(chart, update);
                for (var i = 0; i < chart.data.length; i++) {{
                    if (update['data[' + i + '].name']) {{
                        Plotly.restyle(chart, {{'name': [update['data[' + i + '].name']]}}, [i]);
                    }}
                }}
            }}
        }}

        var origSwitch = window.switchLanguage;
        window.switchLanguage = function(lang, btn, event) {{
            origSwitch(lang, btn, event);
            updateSignalChart(lang);
        }};

        Plotly.newPlot('signal-chart', chartData.data, chartData.layout, chartData.config);
    </script>
    """

    return get_base_template(
        title=f"{i18n.t('plot_signal_title')} - {signal_id}",
        content=content + plotly_script,
        metadata=metadata,
        language=language,
    )


def create_pca_visualization_report(
    model_name: str,
    plot_div: str,
    metadata: Dict[str, Any],
    summary: Dict[str, Any],
    language: str = "en",
) -> str:
    """Create PCA visualization report with i18n support."""
    i18n = get_i18n(language)

    info_cards = f"""
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label" data-i18n="model_name">{i18n.t('model_name')}</div>
            <div class="info-value">{model_name}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="total_segments">{i18n.t('total_segments')}</div>
            <div class="info-value">{summary.get('total_segments', 0)}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="total_anomalies">{i18n.t('total_anomalies')}</div>
            <div class="info-value" style="color: #e74c3c;">{summary.get('total_anomalies', 0)}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="anomaly_ratio">{i18n.t('anomaly_ratio')}</div>
            <div class="info-value">{summary.get('anomaly_ratio', 0)*100:.1f}%</div>
        </div>
    </div>
    """

    variance_info = ""
    if metadata.get('variance_explained_pc1') is not None:
        variance_info = f"""
    <div class="card">
        <h3 class="card-title" data-i18n="pca_variance">📊 {i18n.t('pca_variance')}</h3>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">PC1</div>
                <div class="info-value">{metadata['variance_explained_pc1']*100:.1f}%</div>
            </div>
            <div class="info-item">
                <div class="info-label">PC2</div>
                <div class="info-value">{metadata['variance_explained_pc2']*100:.1f}%</div>
            </div>
            <div class="info-item">
                <div class="info-label" data-i18n="total_variance">{i18n.t('total_variance')}</div>
                <div class="info-value">{metadata.get('total_variance_2d', 0)*100:.1f}%</div>
            </div>
        </div>
    </div>
    """

    validation_info = ""
    if summary.get('validation_metrics'):
        vm = summary['validation_metrics']
        validation_info = f"""
    <div class="card">
        <h3 class="card-title" data-i18n="validation_metrics">✅ {i18n.t('validation_metrics')}</h3>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label" data-i18n="overall_accuracy">{i18n.t('overall_accuracy')}</div>
                <div class="info-value">{vm.get('overall_accuracy', 0)*100:.2f}%</div>
            </div>
            <div class="info-item">
                <div class="info-label" data-i18n="correct_predictions">{i18n.t('correct_predictions')}</div>
                <div class="info-value">{vm.get('correct_predictions', 0)} / {vm.get('total_labeled_segments', 0)}</div>
            </div>
        </div>
    </div>
    """

    content = f"""
    <div class="header">
        <div class="header-content">
            <h1 data-i18n="pca_title">🔍 {i18n.t('pca_title')}</h1>
            <p class="subtitle">{model_name}</p>
        </div>
    </div>
    <div class="container">
        {info_cards}
        {variance_info}
        {validation_info}
        <div class="chart-container"><div id="pca-chart"></div></div>
    </div>
    """

    plotly_script = f"""
    <script>
        var chartData = {plot_div};

        Plotly.newPlot('pca-chart', chartData.data, chartData.layout, chartData.config);
    </script>
    """

    return get_base_template(
        title=f"{i18n.t('pca_title')} - {model_name}",
        content=content + plotly_script,
        metadata=metadata,
        language=language,
    )


def create_feature_comparison_report(
    group_names: str,
    plot_div: str,
    metadata: Dict[str, Any],
    language: str = "en",
) -> str:
    """Create feature comparison report with i18n support."""
    i18n = get_i18n(language)

    features_plotted = metadata.get('features_plotted', [])
    num_features = len(features_plotted)
    groups = metadata.get('groups', {})

    groups_info = ""
    zh_i18n = get_i18n("zh")
    for gname, count in groups.items():
        en_segments_text = "segments"
        zh_segments_text = zh_i18n.t("segments")
        # Translate group name if it's a known key
        group_key = gname.lower()
        en_name = gname
        zh_name = zh_i18n.t(group_key) if zh_i18n.t(group_key) != group_key else gname
        en_val = f"{count} {en_segments_text}"
        zh_val = f"{count} {zh_segments_text}"
        display_name = zh_name if language == "zh" else en_name
        display_val = zh_val if language == "zh" else en_val
        groups_info += f'<div class="info-item"><div class="info-label" data-i18n="{group_key}">{display_name}</div><div class="info-value" data-i18n-val-en="{en_val}" data-i18n-val-zh="{zh_val}" data-i18n-val="{display_val}">{display_val}</div></div>'

    info_cards = f"""
    <div class="info-grid">
        <div class="info-item">
            <div class="info-label" data-i18n="num_groups">{i18n.t('num_groups')}</div>
            <div class="info-value">{len(groups)}</div>
        </div>
        <div class="info-item">
            <div class="info-label" data-i18n="num_features">{i18n.t('num_features')}</div>
            <div class="info-value">{num_features}</div>
        </div>
        {groups_info}
    </div>
    """

    content = f"""
    <div class="header">
        <div class="header-content">
            <h1 data-i18n="feature_comparison_title">📊 {i18n.t('feature_comparison_title')}</h1>
            <p class="subtitle">{group_names}</p>
        </div>
    </div>
    <div class="container">
        {info_cards}
        <div class="chart-container"><div id="feature-chart"></div></div>
    </div>
    """

    plotly_script = f"""
    <script>
        var chartData = {plot_div};

        Plotly.newPlot('feature-chart', chartData.data, chartData.layout, chartData.config);
    </script>
    """

    return get_base_template(
        title=f"{i18n.t('feature_comparison_title')} - {group_names}",
        content=content + plotly_script,
        metadata=metadata,
        language=language,
    )
