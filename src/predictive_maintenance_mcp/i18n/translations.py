SUPPORTED_LANGUAGES = ["en", "zh-CN"]

_TRANSLATIONS = {
    "en": {
        "report.title.fft": "FFT Spectrum Analysis",
        "report.title.envelope": "Envelope Analysis",
        "report.title.iso": "ISO 15243:2017 Assessment",
        "report.title.diagnostic": "Bearing Diagnostic Report",
        "report.title.maint_recommendations": "Maintenance Recommendations",
        "report.title.feature_comparison": "Feature Comparison",
        "report.title.pca_visualization": "PCA Visualization",

        "ui.sampling_rate": "Sampling Rate",
        "ui.frequency_range": "Frequency Range",
        "ui.signal_length": "Signal Length",
        "ui.duration": "Duration",
        "ui.filter_range": "Filter Range",
        "ui.rpm": "RPM",
        "ui.poles": "Poles",
        "ui.frequency": "Frequency",
        "ui.magnitude": "Magnitude",
        "ui.peak": "Peak",
        "ui.note": "Note",
        "ui.match": "Match",
        "ui.rank": "Rank",
        "ui.value": "Value",
        "ui.unit": "Unit",
        "ui.action": "Action",
        "ui.urgency": "Urgency",
        "ui.description": "Description",
        "ui.motivation": "Motivation",
        "ui.evidence": "Evidence",
        "ui.detected_peaks": "Detected Peaks",
        "ui.bearing_char_freq": "Bearing Characteristic Frequencies",
        "ui.envelope_spectrum_peaks": "Envelope Spectrum Peaks",
        "ui.rms_velocity": "RMS Velocity",
        "ui.evaluation_zone": "Evaluation Zone",
        "ui.machine_group": "Machine Group",
        "ui.support_type": "Support Type",
        "ui.zone_boundaries": "Zone Boundaries",
        "ui.interpretation": "Interpretation",
        "ui.zone_ab": "Zone A/B",
        "ui.zone_bc": "Zone B/C",
        "ui.zone_cd": "Zone C/D",
        "ui.vibration_severity": "Vibration Severity",
        "ui.iso_evaluation": "ISO 20816-3 Evaluation",
        "ui.harmonic": "Harmonic",
        "ui.frequency_hz": "Frequency (Hz)",
        "ui.magnitude_db": "Magnitude (dB)",

        "chart.title.fft": "FFT Spectrum Analysis",
        "chart.title.envelope": "Envelope Analysis (Time + Frequency Domain)",
        "chart.title.iso": "Vibration Severity according to ISO 20816-3",
        "chart.axis.frequency": "Frequency (Hz)",
        "chart.axis.magnitude_db": "Magnitude (dB re. max)",
        "chart.axis.time": "Time (s)",
        "chart.axis.amplitude": "Amplitude",
        "chart.axis.rms_velocity": "RMS Velocity (mm/s)",
        "chart.label.vibration_severity": "Vibration Severity",
        "chart.label.filtered_signal": "Filtered Signal",
        "chart.label.envelope": "Envelope",
        "chart.label.spectrum": "Spectrum",
        "chart.label.envelope_spectrum": "Envelope Spectrum",
        "chart.label.peaks": "Peaks",
        "chart.label.measured": "Measured",
        "chart.label.zone_a": "Zone A",
        "chart.label.zone_b": "Zone B",
        "chart.label.zone_c": "Zone C",
        "chart.label.zone_d": "Zone D",

        "chart.hover.zone_a": "Zone A: 0 - {ab} mm/s<br>New machine condition<extra></extra>",
        "chart.hover.zone_b": "Zone B: {ab} - {bc} mm/s<br>Acceptable operation<extra></extra>",
        "chart.hover.zone_c": "Zone C: {bc} - {cd} mm/s<br>Unsatisfactory<extra></extra>",
        "chart.hover.zone_d": "Zone D: > {cd} mm/s<br>Severe condition<extra></extra>",
        "chart.hover.measured": "Measured RMS Velocity: {value} mm/s<extra></extra>",

        "iso.zone_a": "Zone A — Normal. No actionable findings. Continue routine monitoring.",
        "iso.zone_b": "Zone B — Attention. Early signs of deterioration detected. Increase monitoring frequency.",
        "iso.zone_c": "Zone C — Alert. Significant defect detected. Plan maintenance action within short timeframe.",
        "iso.zone_d": "Zone D — Danger. Severe defect detected. Immediate action required to prevent catastrophic failure.",

        "severity.good": "Good",
        "severity.acceptable": "Acceptable",
        "severity.unsatisfactory": "Unsatisfactory",
        "severity.dangerous": "Dangerous",

        "fault.outer_race": "Outer Race Fault",
        "fault.inner_race": "Inner Race Fault",
        "fault.ball": "Ball Fault",
        "fault.roller": "Roller Fault",
        "fault.cage": "Cage Fault",

        "diag.healthy": "Healthy",
        "diag.warning": "Warning",
        "diag.danger": "Danger",
        "diag.no_fault_detected": "No fault detected",
        "diag.fault_detected": "Fault detected",

        "rec.increase_monitoring": "Increase monitoring frequency",
        "rec.schedule_maintenance": "Schedule maintenance within 7 days",
        "rec.immediate_shutdown": "Immediate shutdown and inspection required",
        "rec.plan_replacement": "Plan bearing replacement during next scheduled downtime",
        "rec.visual_inspection": "Perform visual inspection and check lubrication",
        "rec.no_action": "No action required",
        "rec.review_lubrication": "Review lubrication regimen and consider re-greasing",
        "rec.check_alignment": "Check shaft alignment and coupling condition",

        "evidence.high": "High",
        "evidence.moderate": "Moderate",
        "evidence.low": "Low",
        "evidence.none": "None",

        "meta.generated_by": "Generated by Predictive Maintenance MCP",
        "meta.professional_diagnostics": "Professional Machinery Diagnostics",
        "meta.language": "Language",

        "baseline.no_baseline": "No baseline available",
        "baseline.stable": "Stable — No significant change from baseline",
        "baseline.improving": "Improving — Positive trend observed",
        "baseline.worsening": "Worsening — Degradation progressing",

        "doc.statistical_summary": "Statistical Summary",
        "doc.parameter": "Parameter",
        "doc.value": "Value",
        "doc.fft_peaks": "FFT Spectrum — Top Peaks",
        "doc.env_peaks": "Envelope Analysis — Top Peaks",
        "doc.bearing_freqs": "Bearing Characteristic Frequencies",
        "doc.value_hz": "Value (Hz)",
        "doc.iso_eval": "ISO 20816-3 Evaluation",
        "doc.diagnostic_summary": "Diagnostic Summary",
        "doc.diagnostic_report": "Diagnostic Report",

        "report.title.bearing_matching": "Bearing frequency matching",
        "report.title.calc_vs_measured": "Calculated against measured",
        "report.title.anomaly_detection": "Anomaly detection",
        "report.title.spectral_energy": "Spectral energy distribution",
        "report.title.recommendations": "Recommended actions",
        "report.title.baseline_comparison": "Comparison with baseline",
        "report.title.iso_severity": "ISO severity",
        "report.title.evidence": "Evidence",
        "report.title.evidence_strength": "Evidence strength",
        "report.title.provenance": "Provenance",
        "report.title.indicators_disagree": "Indicators disagree",

        "ui.to_resolve": "To resolve:",
        "ui.element": "Element",
        "ui.calculated": "Calculated",
        "ui.deviation": "Deviation",
        "ui.verdict": "Verdict",
        "ui.no_match": "no match",
        "ui.signal": "Signal",
        "ui.bearing": "Bearing",
        "ui.machine_group_support": "ISO machine group / support",
        "ui.server_version": "Server version",
        "ui.generated": "Generated",
        "ui.why": "Why:",

        "evidence.strength_explanation": "Evidence strength counts independent corroborating findings — it is not a confidence score and not a probability.",

        "rec.urgency.high": "High urgency",
        "rec.urgency.medium": "Medium urgency",
        "rec.urgency.low": "Low urgency",

        "status.present": "Present",
        "status.absent": "Absent",
        "status.refused": "Refused",
        "status.assessed": "Assessed",
        "status.unknown": "Unknown",

        "iso.zone.A.description": "New machine condition. Vibration is excellent.",
        "iso.zone.A.severity": "Good",
        "iso.zone.B.description": "Acceptable for unrestricted long-term operation.",
        "iso.zone.B.severity": "Acceptable",
        "iso.zone.C.description": "Unsatisfactory for long-term operation. Plan maintenance soon.",
        "iso.zone.C.severity": "Unsatisfactory",
        "iso.zone.D.description": "Vibration severity may cause damage. Immediate action required!",
        "iso.zone.D.severity": "Unacceptable",
        "iso.support.rigid": "rigid",
        "iso.support.flexible": "flexible",

        "diag.iso.refused": "ISO severity was not assessed. {reason}",
        "diag.iso.assessed": (
            "ISO 20816-3: RMS velocity {rms:.2f} mm/s places this machine in "
            "Zone {zone} ({severity}) for machine group "
            "{machine_group} on a {support_type} support. {description}"
        ),

        "diag.bearing.absent": (
            "Bearing characteristic-frequency matching was not attempted: "
            "no bearing designation was supplied for this signal, so BPFO, "
            "BPFI, BSF and FTF could not be computed. Without it, a "
            "spectral peak cannot be attributed to a specific bearing "
            "element."
        ),
        "diag.bearing.absent_remedy": (
            "Re-run the diagnosis with a bearing_id present in the "
            "catalog, or add the bearing designation to the signal's "
            "companion metadata."
        ),
        "diag.bearing.matched_part": (
            "{fault_type} expected at {expected_hz:.2f} Hz, "
            "measured at {measured_hz:.2f} Hz "
            "({deviation_pct:.2f}% deviation)"
        ),
        "diag.bearing.matched_statement": (
            "Bearing {bearing_id} at {shaft_freq:.1f} Hz shaft "
            "speed: {matched_parts}. The remaining characteristic "
            "frequencies did not match."
        ),
        "diag.bearing.no_match": (
            "Bearing {bearing_id}: none of the four characteristic "
            "frequencies (BPFO, BPFI, BSF, FTF) matched a peak in the "
            "envelope spectrum within tolerance."
        ),

        "diag.anomaly.absent": (
            "No anomaly-model verdict is available for this signal: no "
            "trained model was found. The pattern-level check that would "
            "corroborate or contradict the severity reading is therefore "
            "missing from this assessment."
        ),
        "diag.anomaly.absent_remedy": (
            "Train an anomaly model on healthy signals from this machine, "
            "then re-run the diagnosis."
        ),
        "diag.anomaly.assessed": (
            "Anomaly model verdict: {health} — {counted} "
            "({ratio_pct:.1f}%) fall outside the learned healthy pattern."
        ),

        "diag.energy.absent": (
            "No spectral energy distribution is available: the STFT band "
            "breakdown was not computed, so the frequency region carrying "
            "the signal's energy cannot be named."
        ),
        "diag.energy.assessed": (
            "Spectral energy is concentrated in the {dominant} band "
            "({share:.0f}% of total STFT energy). High-frequency dominance "
            "is consistent with impulsive excitation of structural "
            "resonances; low-frequency dominance is consistent with "
            "shaft-order sources such as unbalance or misalignment."
        ),

        "diag.verdict.fault_indicated": (
            "A {label} fault is indicated: the envelope spectrum peak "
            "matches the {fault_type} characteristic frequency of this "
            "bearing within {deviation_pct:.2f}%."
        ),
        "diag.verdict.no_bearing_fault": (
            "No bearing fault is indicated: no characteristic frequency "
            "matched a peak in the envelope spectrum."
        ),
        "diag.verdict.no_bearing_verdict": (
            "No bearing fault verdict was reached, because characteristic-"
            "frequency matching was not attempted."
        ),
        "diag.verdict.non_bearing_source": (
            " Broadband vibration is nonetheless elevated "
            "(Zone {zone}), so a non-bearing source should be considered."
        ),
        "diag.verdict.anomaly_flags": (
            " The anomaly model nonetheless flags this signal as departing "
            "from the learned healthy pattern, so a source outside the "
            "bearing's characteristic frequencies should be considered."
        ),

        "diag.evidence.bearing_match": (
            "{acronym} match: expected {expected_hz:.2f} Hz, measured "
            "{measured_hz:.2f} Hz, deviation {deviation_pct:.2f}%."
        ),
        "diag.evidence.harmonics_add": (
            " {harmonics} harmonic(s) of {acronym} are also present, which "
            "a single noise peak would not produce."
        ),
        "diag.evidence.dominant_freq": (
            "Dominant frequency in the raw spectrum: {peak:.1f} Hz."
        ),

        "diag.disagreement.statement": (
            "Indicators disagree. Zone {zone} describes overall "
            "vibration energy as acceptable, while {dissenting} indicate "
            "a developing fault. These are not contradictory: a localised "
            "defect can be unambiguous in the envelope spectrum while the "
            "broadband level it contributes is still low. The fault-pattern "
            "evidence governs the recommended action; the ISO zone "
            "describes how far the condition has progressed."
        ),
        "diag.disagreement.anomaly_dissent": (
            "the anomaly model ({health}, {ratio_pct:.0f}% of segments)"
        ),
        "diag.disagreement.match_dissent": (
            "the characteristic-frequency match ({names})"
        ),

        "diag.rec.severity_unavailable": (
            "The severity verdict is unavailable until this is resolved."
        ),
        "diag.rec.fault_motivation": (
            "The characteristic frequency of this bearing element "
            "matched a peak in the envelope spectrum within tolerance"
            "{acronym_suffix}"
        ),
        "diag.rec.fault_motivation_acronym": " ({acronym}).",
        "diag.rec.iso_motivation_severity": (
            "ISO Zone {zone} is classified as {severity_lower}."
        ),
        "diag.rec.iso_motivation_plain": "ISO Zone {zone}.",
        "diag.rec.disagreement_action": (
            "Treat this as actionable despite the acceptable ISO zone"
        ),
        "diag.rec.disagreement_description": (
            "Fault-pattern evidence and the severity zone describe "
            "different stages of the same condition."
        ),
        "diag.rec.anomaly_absent_description": (
            "Pattern-level corroboration is unavailable without a "
            "trained model."
        ),

        "diag.baseline.absent": (
            "No healthy baseline was supplied for this machine, so the "
            "readings below are absolute rather than relative. Whether "
            "this condition is new, stable, or worsening cannot be "
            "determined from a single acquisition."
        ),
        "diag.baseline.absent_remedy": (
            "Re-run the diagnosis with a baseline signal id from the "
            "same machine in a known-good state."
        ),
        "diag.baseline.refused": (
            "Baseline comparison was refused: {incompatible} A delta "
            "between measurements taken under different conditions "
            "would look like a change in machine condition."
        ),
        "diag.baseline.refused_remedy": (
            "Supply a baseline acquired from the same measurement point "
            "under the same declared conditions."
        ),
        "diag.baseline.no_indicators": (
            "A baseline was supplied ({signal_id}), but no indicator "
            "could be compared: the two diagnoses share no assessed "
            "block. Whether this condition is new, stable, or worsening "
            "cannot be determined."
        ),
        "diag.baseline.no_indicators_remedy": (
            "Ensure both signals declare their unit so the severity "
            "and anomaly blocks are assessed rather than refused."
        ),
        "diag.baseline.stable": (
            "Compared with baseline {signal_id}: no measurable change "
            "in any compared indicator. The condition described above "
            "is stable, not developing."
        ),
        "diag.baseline.moved": (
            "Compared with baseline {signal_id}: {moved_count} of "
            "{total_count} indicators moved. {headline_statement}"
        ),

        "diag.delta.rms_unchanged": (
            "RMS velocity is unchanged against baseline "
            "({now:.2f} mm/s, was {then:.2f} mm/s)."
        ),
        "diag.delta.rms_changed": (
            "RMS velocity is {delta_abs:.2f} mm/s {direction} than "
            "baseline ({now:.2f} mm/s, was {then:.2f} mm/s)."
        ),
        "diag.delta.anomaly_unchanged": (
            "The share of anomalous segments is unchanged against "
            "baseline ({now:.0f}%, was {then:.0f}%) \u2014 a difference "
            "of under one percentage point."
        ),
        "diag.delta.anomaly_changed": (
            "The share of anomalous segments is {delta_abs:.0f} "
            "percentage points {direction} than baseline "
            "({now:.0f}%, was {then:.0f}%)."
        ),
        "diag.delta.envelope_unchanged": (
            "Envelope amplitude at the {acronym} frequency is unchanged "
            "against baseline."
        ),
        "diag.delta.envelope_changed": (
            "Envelope amplitude at the {acronym} frequency is "
            "{delta_db:.1f} dB {direction} than baseline \u2014 the "
            "defect signature itself, not overall machine noise."
        ),

        "diag.baseline.incompatible_unit": (
            "the signal declares its unit as '{signal_unit}' while the "
            "baseline declares '{baseline_unit}'."
        ),
        "diag.baseline.incompatible_bearing": (
            "the signal was analysed against bearing '{signal_bearing}' "
            "and the baseline against '{baseline_bearing}'."
        ),

        "fault.label.outer_race": "outer race",
        "fault.label.inner_race": "inner race",
        "fault.label.ball": "ball",
        "fault.label.cage": "cage",
        "fault.label.roller": "roller",

        "rec.zone.A.action": "Continue normal monitoring",
        "rec.zone.A.description": (
            "Vibration levels are within acceptable limits. "
            "Maintain regular monitoring schedule."
        ),
        "rec.zone.B.action": "Schedule inspection",
        "rec.zone.B.description": (
            "Vibration levels are elevated. "
            "Schedule a visual and operational inspection."
        ),
        "rec.zone.C.action": "Plan maintenance within 2 weeks",
        "rec.zone.C.description": (
            "Vibration levels are unsatisfactory. "
            "Plan corrective maintenance within two weeks."
        ),
        "rec.zone.D.action": "Immediate shutdown recommended",
        "rec.zone.D.description": (
            "Vibration levels are unacceptable and may cause damage. "
            "Immediate shutdown and inspection recommended."
        ),
        "rec.zone.unknown.action": "Review vibration data manually",
        "rec.zone.unknown.description": (
            "Unknown severity zone '{zone}'. "
            "Manual review of vibration data is recommended."
        ),
        "rec.fault.outer_race": "Replace bearing, check alignment",
        "rec.fault.inner_race": "Replace bearing, inspect shaft condition",
        "rec.fault.ball": "Replace bearing, check lubrication system",
        "rec.fault.cage": "Replace bearing, investigate contamination",
        "rec.fault.misalignment": "Realign coupling, check foundation bolts",
        "rec.fault.unbalance": "Balance rotor, check for deposit buildup",
        "rec.fault.looseness": "Tighten foundation bolts, inspect mounting",
        "rec.fault.description": "Detected fault: {fault}.",
    },

    "zh-CN": {
        "report.title.fft": "FFT 频谱分析",
        "report.title.envelope": "包络分析",
        "report.title.iso": "ISO 15243:2017 评估",
        "report.title.diagnostic": "轴承诊断报告",
        "report.title.maint_recommendations": "维护建议",
        "report.title.feature_comparison": "特征对比",
        "report.title.pca_visualization": "PCA 可视化",

        "ui.sampling_rate": "采样率",
        "ui.frequency_range": "频率范围",
        "ui.signal_length": "信号长度",
        "ui.duration": "持续时间",
        "ui.filter_range": "滤波范围",
        "ui.rpm": "转速",
        "ui.poles": "极数",
        "ui.frequency": "频率",
        "ui.magnitude": "幅值",
        "ui.peak": "峰值",
        "ui.note": "备注",
        "ui.match": "匹配",
        "ui.rank": "排名",
        "ui.value": "数值",
        "ui.unit": "单位",
        "ui.action": "措施",
        "ui.urgency": "紧急程度",
        "ui.description": "描述",
        "ui.motivation": "依据",
        "ui.evidence": "证据",
        "ui.detected_peaks": "检测到的峰值",
        "ui.bearing_char_freq": "轴承特征频率",
        "ui.envelope_spectrum_peaks": "包络谱峰值",
        "ui.rms_velocity": "RMS 速度",
        "ui.evaluation_zone": "评估区域",
        "ui.machine_group": "机组类型",
        "ui.support_type": "支承类型",
        "ui.zone_boundaries": "区域边界",
        "ui.interpretation": "解读",
        "ui.zone_ab": "区域 A/B",
        "ui.zone_bc": "区域 B/C",
        "ui.zone_cd": "区域 C/D",
        "ui.vibration_severity": "振动严重度",
        "ui.iso_evaluation": "ISO 20816-3 评估",
        "ui.harmonic": "谐波",
        "ui.frequency_hz": "频率 (Hz)",
        "ui.magnitude_db": "幅值 (dB)",

        "chart.title.fft": "FFT 频谱分析",
        "chart.title.envelope": "包络分析（时域 + 频域）",
        "chart.title.iso": "根据 ISO 20816-3 的振动严重度",
        "chart.axis.frequency": "频率 (Hz)",
        "chart.axis.magnitude_db": "幅值 (dB re. 最大值)",
        "chart.axis.time": "时间 (s)",
        "chart.axis.amplitude": "幅值",
        "chart.axis.rms_velocity": "RMS 速度 (mm/s)",
        "chart.label.vibration_severity": "振动严重度",
        "chart.label.filtered_signal": "滤波信号",
        "chart.label.envelope": "包络",
        "chart.label.spectrum": "频谱",
        "chart.label.envelope_spectrum": "包络谱",
        "chart.label.peaks": "峰值",
        "chart.label.measured": "实测",
        "chart.label.zone_a": "区域 A",
        "chart.label.zone_b": "区域 B",
        "chart.label.zone_c": "区域 C",
        "chart.label.zone_d": "区域 D",

        "chart.hover.zone_a": "区域 A: 0 - {ab} mm/s<br>新机器状态<extra></extra>",
        "chart.hover.zone_b": "区域 B: {ab} - {bc} mm/s<br>可接受运行<extra></extra>",
        "chart.hover.zone_c": "区域 C: {bc} - {cd} mm/s<br>不满意<extra></extra>",
        "chart.hover.zone_d": "区域 D: > {cd} mm/s<br>严重状态<extra></extra>",
        "chart.hover.measured": "实测 RMS 速度: {value} mm/s<extra></extra>",

        "iso.zone_a": "区域 A — 正常。无异常发现，继续常规监测。",
        "iso.zone_b": "区域 B — 关注。检测到早期劣化迹象，建议增加监测频率。",
        "iso.zone_c": "区域 C — 警告。检测到明显缺陷，需在短期内安排维护。",
        "iso.zone_d": "区域 D — 危险。检测到严重缺陷，需立即采取措施以防止灾难性故障。",

        "severity.good": "良好",
        "severity.acceptable": "可接受",
        "severity.unsatisfactory": "不满意",
        "severity.dangerous": "危险",

        "fault.outer_race": "外圈故障",
        "fault.inner_race": "内圈故障",
        "fault.ball": "钢球故障",
        "fault.roller": "滚子故障",
        "fault.cage": "保持架故障",

        "diag.healthy": "健康",
        "diag.warning": "警告",
        "diag.danger": "危险",
        "diag.no_fault_detected": "未检测到故障",
        "diag.fault_detected": "检测到故障",

        "rec.increase_monitoring": "提高监测频率",
        "rec.schedule_maintenance": "在 7 天内安排维护",
        "rec.immediate_shutdown": "需立即停机检查",
        "rec.plan_replacement": "在下次计划停机时安排轴承更换",
        "rec.visual_inspection": "进行目视检查并检查润滑状态",
        "rec.no_action": "无需采取措施",
        "rec.review_lubrication": "检查润滑方案并考虑重新润滑",
        "rec.check_alignment": "检查轴对中和联轴器状态",

        "evidence.high": "高",
        "evidence.moderate": "中等",
        "evidence.low": "低",
        "evidence.none": "无",

        "meta.generated_by": "由预测性维护 MCP 生成",
        "meta.professional_diagnostics": "专业机械诊断",
        "meta.language": "语言",

        "baseline.no_baseline": "无基准数据",
        "baseline.stable": "稳定 — 与基准相比无显著变化",
        "baseline.improving": "改善 — 观察到积极趋势",
        "baseline.worsening": "恶化 — 劣化正在进展",

        "doc.statistical_summary": "统计摘要",
        "doc.parameter": "参数",
        "doc.value": "数值",
        "doc.fft_peaks": "FFT 频谱 — 主要峰值",
        "doc.env_peaks": "包络分析 — 主要峰值",
        "doc.bearing_freqs": "轴承特征频率",
        "doc.value_hz": "数值 (Hz)",
        "doc.iso_eval": "ISO 20816-3 评估",
        "doc.diagnostic_summary": "诊断摘要",
        "doc.diagnostic_report": "诊断报告",

        "report.title.bearing_matching": "轴承频率匹配",
        "report.title.calc_vs_measured": "计算值与实测值对比",
        "report.title.anomaly_detection": "异常检测",
        "report.title.spectral_energy": "频谱能量分布",
        "report.title.recommendations": "建议措施",
        "report.title.baseline_comparison": "与基准对比",
        "report.title.iso_severity": "ISO 严重度",
        "report.title.evidence": "证据",
        "report.title.evidence_strength": "证据强度",
        "report.title.provenance": "溯源信息",
        "report.title.indicators_disagree": "指标不一致",

        "ui.to_resolve": "解决方法：",
        "ui.element": "元件",
        "ui.calculated": "计算值",
        "ui.deviation": "偏差",
        "ui.verdict": "结论",
        "ui.no_match": "不匹配",
        "ui.signal": "信号",
        "ui.bearing": "轴承",
        "ui.machine_group_support": "ISO 机组类型 / 支承",
        "ui.server_version": "服务器版本",
        "ui.generated": "生成时间",
        "ui.why": "依据：",

        "evidence.strength_explanation": "证据强度统计独立的佐证发现 — 它不是置信分数，也不是概率。",

        "rec.urgency.high": "高紧急度",
        "rec.urgency.medium": "中紧急度",
        "rec.urgency.low": "低紧急度",

        "status.present": "存在",
        "status.absent": "不存在",
        "status.refused": "已拒绝",
        "status.assessed": "已评估",
        "status.unknown": "未知",

        "iso.zone.A.description": "新机器状态，振动极为优良。",
        "iso.zone.A.severity": "良好",
        "iso.zone.B.description": "可接受，适合长期无限制运行。",
        "iso.zone.B.severity": "可接受",
        "iso.zone.C.description": "不适合长期运行，应尽快安排维护。",
        "iso.zone.C.severity": "不满意",
        "iso.zone.D.description": "振动严重度可能导致损坏，需立即采取措施！",
        "iso.zone.D.severity": "不可接受",
        "iso.support.rigid": "刚性",
        "iso.support.flexible": "柔性",

        "diag.iso.refused": "ISO 严重度未进行评估。{reason}",
        "diag.iso.assessed": (
            "ISO 20816-3：RMS 速度 {rms:.2f} mm/s，该机组处于 "
            "{zone} 区域（{severity}），机组类型为 "
            "{machine_group}，支承方式为 {support_type}。{description}"
        ),

        "diag.bearing.absent": (
            "未进行轴承特征频率匹配：该信号未提供轴承型号，因此 "
            "无法计算 BPFO、BPFI、BSF 和 FTF。没有这些信息，频谱峰值 "
            "无法归因于具体的轴承元件。"
        ),
        "diag.bearing.absent_remedy": (
            "重新运行诊断，确保目录中存在 bearing_id，或将轴承型号 "
            "添加到信号的元数据中。"
        ),
        "diag.bearing.matched_part": (
            "{fault_type} 预期频率 {expected_hz:.2f} Hz，"
            "实测频率 {measured_hz:.2f} Hz"
            "（偏差 {deviation_pct:.2f}%）"
        ),
        "diag.bearing.matched_statement": (
            "轴承 {bearing_id}，轴转速 {shaft_freq:.1f} Hz："
            "{matched_parts}。其余特征频率未匹配。"
        ),
        "diag.bearing.no_match": (
            "轴承 {bearing_id}：四个特征频率（BPFO、BPFI、BSF、FTF）"
            "均未与包络谱中的峰值在容差范围内匹配。"
        ),

        "diag.anomaly.absent": (
            "该信号没有异常模型判定：未找到训练好的模型。因此，"
            "用于证实或反驳严重度读数的模式级检查在本次评估中缺失。"
        ),
        "diag.anomaly.absent_remedy": (
            "在该机器的健康信号上训练异常模型，然后重新运行诊断。"
        ),
        "diag.anomaly.assessed": (
            "异常模型判定：{health} — {counted} "
            "（{ratio_pct:.1f}%）超出了学习到的健康模式。"
        ),

        "diag.energy.absent": (
            "没有频谱能量分布数据：未计算 STFT 频段分解，因此无法"
            "确定信号能量集中的频率区域。"
        ),
        "diag.energy.assessed": (
            "频谱能量集中在 {dominant} 频段"
            "（占 STFT 总能量的 {share:.0f}%）。高频主导与结构共振的"
            "脉冲激励一致；低频主导与不平衡或不对中等轴序源一致。"
        ),

        "diag.verdict.fault_indicated": (
            "检测到 {label} 故障：包络谱峰值在 "
            "{deviation_pct:.2f}% 容差内匹配了该轴承的 "
            "{fault_type} 特征频率。"
        ),
        "diag.verdict.no_bearing_fault": (
            "未检测到轴承故障：无特征频率与包络谱峰值匹配。"
        ),
        "diag.verdict.no_bearing_verdict": (
            "未得出轴承故障结论，因为未尝试进行特征频率匹配。"
        ),
        "diag.verdict.non_bearing_source": (
            " 尽管如此，宽带振动仍然升高（{zone} 区域），"
            "应考虑非轴承来源。"
        ),
        "diag.verdict.anomaly_flags": (
            " 异常模型仍将该信号标记为偏离学习到的健康模式，"
            "因此应考虑轴承特征频率以外的来源。"
        ),

        "diag.evidence.bearing_match": (
            "{acronym} 匹配：预期 {expected_hz:.2f} Hz，"
            "实测 {measured_hz:.2f} Hz，"
            "偏差 {deviation_pct:.2f}%。"
        ),
        "diag.evidence.harmonics_add": (
            " {acronym} 的 {harmonics} 次谐波也存在，"
            "单一噪声峰值不会产生这种现象。"
        ),
        "diag.evidence.dominant_freq": (
            "原始频谱中的主导频率：{peak:.1f} Hz。"
        ),

        "diag.disagreement.statement": (
            "指标不一致。{zone} 区域将整体振动能量描述为可接受，"
            "而 {dissenting} 表明正在发展的故障。这些并不矛盾："
            "局部缺陷在包络谱中可以是明确无误的，而其贡献的宽带"
            "水平仍然较低。故障模式证据决定了建议措施；ISO 区域"
            "描述了状态发展到了什么程度。"
        ),
        "diag.disagreement.anomaly_dissent": (
            "异常模型（{health}，{ratio_pct:.0f}% 的频段）"
        ),
        "diag.disagreement.match_dissent": (
            "特征频率匹配（{names}）"
        ),

        "diag.rec.severity_unavailable": (
            "在问题解决之前，严重度判定不可用。"
        ),
        "diag.rec.fault_motivation": (
            "该轴承元件的特征频率在容差范围内与包络谱峰值匹配"
            "{acronym_suffix}"
        ),
        "diag.rec.fault_motivation_acronym": "（{acronym}）。",
        "diag.rec.iso_motivation_severity": (
            "ISO {zone} 区域分类为 {severity_lower}。"
        ),
        "diag.rec.iso_motivation_plain": "ISO {zone} 区域。",
        "diag.rec.disagreement_action": (
            "尽管 ISO 区域可接受，仍应视为需要采取措施"
        ),
        "diag.rec.disagreement_description": (
            "故障模式证据和严重度区域描述了同一状态的不同阶段。"
        ),
        "diag.rec.anomaly_absent_description": (
            "没有训练好的模型，无法进行模式级佐证。"
        ),

        "diag.baseline.absent": (
            "未为该机器提供健康基准，因此以下读数为绝对值而非"
            "相对值。无法通过单次采集确定该状态是新的、稳定的"
            "还是正在恶化的。"
        ),
        "diag.baseline.absent_remedy": (
            "重新运行诊断，使用同一机器在已知良好状态下的"
            "基准信号 ID。"
        ),
        "diag.baseline.refused": (
            "基准比较被拒绝：{incompatible} 在不同条件下测量的"
            "增量看起来会像机器状态的变化。"
        ),
        "diag.baseline.refused_remedy": (
            "提供在相同声明条件下从同一测量点获取的基准。"
        ),
        "diag.baseline.no_indicators": (
            "已提供基准（{signal_id}），但无法比较任何指标："
            "两个诊断没有共同的已评估区块。无法确定该状态是"
            "新的、稳定的还是正在恶化的。"
        ),
        "diag.baseline.no_indicators_remedy": (
            "确保两个信号都声明了其单位，以使严重度和异常区块"
            "被评估而非被拒绝。"
        ),
        "diag.baseline.stable": (
            "与基准 {signal_id} 相比：任何比较指标均无可测量"
            "变化。上述描述的状态是稳定的，而非正在发展。"
        ),
        "diag.baseline.moved": (
            "与基准 {signal_id} 相比：{total_count} 个指标中有 "
            "{moved_count} 个发生了变化。{headline_statement}"
        ),

        "diag.delta.rms_unchanged": (
            "RMS 速度与基准相比无变化"
            "（当前 {now:.2f} mm/s，基准 {then:.2f} mm/s）。"
        ),
        "diag.delta.rms_changed": (
            "RMS 速度比基准 {direction} "
            "{delta_abs:.2f} mm/s"
            "（当前 {now:.2f} mm/s，基准 {then:.2f} mm/s）。"
        ),
        "diag.delta.anomaly_unchanged": (
            "异常频段占比与基准相比无变化"
            "（当前 {now:.0f}%，基准 {then:.0f}%）——"
            "差异不足一个百分点。"
        ),
        "diag.delta.anomaly_changed": (
            "异常频段占比比基准 {direction} "
            "{delta_abs:.0f} 个百分点"
            "（当前 {now:.0f}%，基准 {then:.0f}%）。"
        ),
        "diag.delta.envelope_unchanged": (
            "{acronym} 频率处的包络幅值与基准相比无变化。"
        ),
        "diag.delta.envelope_changed": (
            "{acronym} 频率处的包络幅值比基准 "
            "{delta_db:.1f} dB {direction} —— 缺陷特征本身的变化，"
            "而非整机噪声的变化。"
        ),

        "diag.baseline.incompatible_unit": (
            "信号声明其单位为 '{signal_unit}'，而基准声明为 "
            "'{baseline_unit}'。"
        ),
        "diag.baseline.incompatible_bearing": (
            "信号是针对轴承 '{signal_bearing}' 分析的，"
            "而基准是针对轴承 '{baseline_bearing}' 分析的。"
        ),

        "fault.label.outer_race": "外圈",
        "fault.label.inner_race": "内圈",
        "fault.label.ball": "钢球",
        "fault.label.cage": "保持架",
        "fault.label.roller": "滚子",

        "rec.zone.A.action": "继续常规监测",
        "rec.zone.A.description": (
            "振动水平在可接受范围内。保持定期监测计划。"
        ),
        "rec.zone.B.action": "安排检查",
        "rec.zone.B.description": (
            "振动水平已升高。安排目视和运行检查。"
        ),
        "rec.zone.C.action": "在 2 周内安排维护",
        "rec.zone.C.description": (
            "振动水平不满意。在两周内计划纠正性维护。"
        ),
        "rec.zone.D.action": "建议立即停机",
        "rec.zone.D.description": (
            "振动水平不可接受，可能造成损坏。"
            "建议立即停机检查。"
        ),
        "rec.zone.unknown.action": "人工审查振动数据",
        "rec.zone.unknown.description": (
            "未知严重度区域 '{zone}'。建议人工审查振动数据。"
        ),
        "rec.fault.outer_race": "更换轴承，检查对中",
        "rec.fault.inner_race": "更换轴承，检查轴 condition",
        "rec.fault.ball": "更换轴承，检查润滑系统",
        "rec.fault.cage": "更换轴承，调查污染",
        "rec.fault.misalignment": "重新对中联轴器，检查基础螺栓",
        "rec.fault.unbalance": "平衡转子，检查积垢",
        "rec.fault.looseness": "紧固基础螺栓，检查安装",
        "rec.fault.description": "检测到故障：{fault}。",
    },
}


def t(key: str, lang: str = "en", **kwargs) -> str:
    lang = lang if lang in _TRANSLATIONS else "en"
    translations = _TRANSLATIONS[lang]
    key_lower = key.lower()
    for k, v in translations.items():
        if k.lower() == key_lower:
            if kwargs:
                try:
                    return v.format(**kwargs)
                except (KeyError, ValueError, TypeError):
                    return v
            return v
    return key