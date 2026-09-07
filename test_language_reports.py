"""
Test script for Chinese/English language report generation.
Generates FFT, Envelope, and ISO reports in both languages.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
from pathlib import Path

# Import the modules we need to test
from src.report_generator import save_fft_report, save_envelope_report, save_iso_report
from src.i18n import get_i18n


def load_signal(file_path: str) -> tuple:
    """Load signal from CSV file."""
    data = np.loadtxt(file_path, delimiter=',')
    return data


def test_fft_report(signal_data: np.ndarray, sampling_rate: float, signal_name: str, language: str):
    """Generate FFT report."""
    print(f"\n{'='*60}")
    print(f"Testing FFT Report - Language: {language}")
    print(f"{'='*60}")
    
    i18n = get_i18n(language)
    
    # Perform FFT
    N = len(signal_data)
    window = np.hamming(N)
    signal_windowed = signal_data * window
    
    from scipy.fft import fft, fftfreq
    fft_values = fft(signal_windowed)
    frequencies = fftfreq(N, 1 / sampling_rate)
    
    # Positive frequencies only
    positive_idx = frequencies > 0
    frequencies = frequencies[positive_idx]
    magnitudes = 2.0 * np.abs(fft_values[positive_idx]) / N
    
    # Convert to dB
    max_mag = np.max(magnitudes)
    magnitudes_db = 20 * np.log10((magnitudes + 1e-12) / max_mag)
    
    # Find peaks
    from scipy.signal import find_peaks
    freq_resolution = frequencies[1] - frequencies[0]
    min_peak_distance = max(1, int(10 / freq_resolution))
    
    peak_indices, properties = find_peaks(
        magnitudes_db, height=-40, distance=min_peak_distance
    )
    
    # Sort and take top peaks
    peak_mags_db = properties["peak_heights"]
    top_peak_idx = np.argsort(peak_mags_db)[::-1][:15]
    peak_indices = peak_indices[top_peak_idx]
    
    # Build peaks list
    peaks = []
    for idx in peak_indices:
        freq = float(frequencies[idx])
        mag_db = float(magnitudes_db[idx])
        peaks.append({"frequency": freq, "magnitude_db": mag_db, "note": ""})
    
    # Generate report
    result = save_fft_report(
        signal_file=signal_name,
        sampling_rate=sampling_rate,
        frequencies=frequencies,
        magnitudes=magnitudes,
        signal_data=signal_data,
        max_freq=5000.0,
        num_peaks=15,
        language=language,
    )
    
    print(f"{i18n.t('fft_report_saved')}: {result['file_name']}")
    print(f"File: {result['file_path']}")
    return result


def test_envelope_report(signal_data: np.ndarray, sampling_rate: float, signal_name: str, 
                         bearing_freqs: dict, language: str):
    """Generate Envelope report."""
    print(f"\n{'='*60}")
    print(f"Testing Envelope Report - Language: {language}")
    print(f"{'='*60}")
    
    i18n = get_i18n(language)
    
    from scipy.signal import butter, sosfiltfilt, hilbert
    from scipy.fft import fft, fftfreq
    
    # Bandpass filter
    filter_low = 500.0
    filter_high = min(5000.0, sampling_rate / 2 - 1.0)
    nyquist = sampling_rate / 2
    high_norm = min(filter_high, nyquist - 1.0) / nyquist
    
    sos = butter(4, [filter_low / nyquist, high_norm], btype="band", output="sos")
    filtered_signal = sosfiltfilt(sos, signal_data)
    
    # Envelope via Hilbert
    analytic_signal = hilbert(filtered_signal)
    envelope = np.abs(analytic_signal)
    
    # Envelope spectrum
    N = len(envelope)
    env_fft = fft(envelope)
    env_frequencies = fftfreq(N, 1 / sampling_rate)
    
    positive_idx = env_frequencies > 0
    env_frequencies = env_frequencies[positive_idx]
    env_magnitudes = 2.0 * np.abs(env_fft[positive_idx]) / N
    
    # Convert to dB
    max_mag = np.max(env_magnitudes)
    env_mag_db = 20 * np.log10((env_magnitudes + 1e-12) / max_mag)
    
    # Find peaks
    from scipy.signal import find_peaks
    freq_resolution = env_frequencies[1] - env_frequencies[0]
    min_peak_distance = max(1, int(5 / freq_resolution))
    
    peak_indices, properties = find_peaks(
        env_mag_db, height=-40, distance=min_peak_distance
    )
    
    # Sort and take top peaks
    peak_mags_db = properties["peak_heights"]
    top_idx = np.argsort(peak_mags_db)[::-1][:15]
    peak_indices = peak_indices[top_idx]
    
    # Build peaks list with bearing frequency matching
    peaks = []
    for idx in peak_indices:
        freq = float(env_frequencies[idx])
        mag_db = float(env_mag_db[idx])
        
        # Check match with bearing frequencies
        match = ""
        if bearing_freqs:
            for name, bf in bearing_freqs.items():
                if bf and abs(freq - bf) < bf * 0.05:
                    match = f"≈ {name}"
                    break
        
        peaks.append({"frequency": freq, "magnitude_db": mag_db, "match": match})
    
    # Downsample for time data
    downsample_factor = max(1, len(filtered_signal) // 1000)
    time_data = np.linspace(0, len(filtered_signal) / sampling_rate, len(filtered_signal))
    time_display = time_data[::downsample_factor].tolist()
    filtered_display = filtered_signal[::downsample_factor].tolist()
    envelope_display = envelope[::downsample_factor].tolist()
    
    # Generate report
    result = save_envelope_report(
        signal_file=signal_name,
        sampling_rate=sampling_rate,
        filter_band=(filter_low, filter_high),
        filtered_signal=filtered_signal,
        envelope=envelope,
        env_frequencies=env_frequencies,
        env_magnitudes=env_magnitudes,
        bearing_freqs=bearing_freqs,
        max_freq=500.0,
        num_peaks=15,
        language=language,
    )
    
    print(f"{i18n.t('envelope_report_saved')}: {result['file_name']}")
    print(f"File: {result['file_path']}")
    return result


def test_iso_report(signal_data: np.ndarray, sampling_rate: float, signal_name: str, language: str):
    """Generate ISO report."""
    print(f"\n{'='*60}")
    print(f"Testing ISO Report - Language: {language}")
    print(f"{'='*60}")
    
    i18n = get_i18n(language)
    
    # Calculate RMS velocity (approximate - for demo purposes)
    # In real scenario, you would convert acceleration to velocity
    rms_accel = np.sqrt(np.mean(signal_data**2))
    
    # Simulate ISO evaluation result (for demonstration)
    # In real usage, this comes from assess_severity function
    iso_result = {
        "rms_velocity": rms_accel * 100,  # Approximate conversion for demo
        "zone": "B",
        "severity_level": "Acceptable",
        "zone_description": "The measured vibration level is within acceptable limits for this machine class.",
        "machine_group": 2,
        "support_type": "rigid",
        "boundary_ab": 2.3,
        "boundary_bc": 4.5,
        "boundary_cd": 7.1,
        "frequency_range": "10-1000 Hz",
        "operating_speed_rpm": 1500,
        "threshold_provenance": "ISO 20816-3:2022"
    }
    
    # Generate report
    result = save_iso_report(
        signal_file=signal_name,
        iso_result=iso_result,
        language=language,
    )
    
    print(f"{i18n.t('iso_report_saved')}: {result['file_name']}")
    print(f"File: {result['file_path']}")
    return result


def main():
    """Main test function."""
    print("="*60)
    print("Predictive Maintenance MCP - Language Report Test")
    print("="*60)
    
    # Load signal
    signal_file = "data/signals/real_train/baseline_1.csv"
    metadata_file = "data/signals/real_train/baseline_1_metadata.json"
    
    print(f"\nLoading signal from: {signal_file}")
    signal_data = load_signal(signal_file)
    print(f"Signal loaded: {len(signal_data)} samples")
    
    # Load metadata
    import json
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    sampling_rate = metadata['sampling_rate']
    print(f"Sampling rate: {sampling_rate} Hz")
    print(f"Signal unit: {metadata.get('signal_unit', 'unknown')}")
    
    # Bearing frequencies
    bearing_freqs = {
        "BPFO": metadata.get('BPFO'),
        "BPFI": metadata.get('BPFI'),
        "BSF": metadata.get('BSF'),
        "FTF": metadata.get('FTF'),
    }
    print(f"Bearing frequencies: {bearing_freqs}")
    
    signal_name = "baseline_1"
    
    # Test both languages
    results = {}
    
    for lang in ['en', 'zh']:
        print(f"\n\n{'#'*70}")
        print(f"# Testing Language: {'English' if lang == 'en' else 'Chinese'}")
        print(f"{'#'*70}")
        
        results[lang] = {}
        
        # Test FFT report
        results[lang]['fft'] = test_fft_report(signal_data, sampling_rate, signal_name, lang)
        
        # Test Envelope report
        results[lang]['envelope'] = test_envelope_report(signal_data, sampling_rate, signal_name, bearing_freqs, lang)
        
        # Test ISO report
        results[lang]['iso'] = test_iso_report(signal_data, sampling_rate, signal_name, lang)
    
    # Summary
    print("\n\n" + "="*70)
    print("TEST SUMMARY - Generated Reports")
    print("="*70)
    
    for lang, lang_results in results.items():
        lang_name = 'English' if lang == 'en' else 'Chinese'
        print(f"\n{lang_name} Reports:")
        for report_type, result in lang_results.items():
            print(f"  {report_type.upper()}: {result['file_name']}")
    
    print("\n" + "="*70)
    print("Test completed! Check the reports/ directory for generated files.")
    print("="*70)


if __name__ == "__main__":
    main()
