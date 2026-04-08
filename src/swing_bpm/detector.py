"""Core BPM detection logic using hybrid onset-ratio + PLP approach."""

import librosa
import numpy as np

HOP_LENGTH = 512


def detect_bpm(file_path: str) -> int:
    """Detect BPM of an audio file.

    Uses a hybrid approach optimized for swing/jazz music:
    1. librosa beat_track for base tempo detection
    2. Inter-beat onset ratio to detect half-tempo misdetection
    3. PLP (Predominant Local Pulse) as tiebreaker for borderline cases
    4. PLP stability (std) to reject false doubling on slow ballads

    Args:
        file_path: Path to an audio file (MP3, FLAC, WAV, etc.)

    Returns:
        Detected BPM as an integer.
    """
    y, sr = librosa.load(file_path)
    return _detect_bpm_from_signal(y, sr)


def _detect_bpm_from_signal(y: np.ndarray, sr: int) -> int:
    """Run the 4-stage hybrid algorithm on an audio signal array.

    Same logic as detect_bpm but accepts a pre-loaded signal instead of a file path.
    """
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    base_bpm = float(tempo[0]) if hasattr(tempo, "__len__") else float(tempo)

    if len(beats) < 4:
        return round(base_bpm)

    ratio = _inter_beat_onset_ratio(onset_env, beats)

    plp_cache = {}

    def get_plp_data():
        if "data" not in plp_cache:
            pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr)
            peaks = np.where(librosa.util.localmax(pulse))[0]
            if len(peaks) < 2:
                plp_cache["data"] = (0.0, 0.0)
            else:
                intervals = np.diff(peaks)
                local_bpms = 60.0 * sr / (intervals.astype(float) * HOP_LENGTH)
                plp_cache["data"] = (float(np.median(local_bpms)), float(np.std(local_bpms)))
        return plp_cache["data"]

    if 0.27 <= ratio <= 0.33:
        plp_bpm, _ = get_plp_data()
        if plp_bpm > 0 and abs(plp_bpm / base_bpm - 2.0) < 0.3:
            return round(base_bpm * 2)
        elif plp_bpm > 0 and abs(plp_bpm / base_bpm - 1.0) < 0.3:
            return round(base_bpm)
        else:
            return round(base_bpm * 2) if ratio > 0.30 else round(base_bpm)

    if ratio > 0.30:
        if base_bpm < 105:
            plp_bpm, plp_std = get_plp_data()
            if plp_bpm > 0 and abs(plp_bpm / (base_bpm * 2) - 1.0) < 0.3 and plp_std <= 55:
                return round(base_bpm * 2)
            if plp_std > 40:
                return round(base_bpm)
            return round(base_bpm)
        return round(base_bpm * 2)

    return round(base_bpm)


def detect_bpm_range(
    file_path: str, window_sec: int = 30, overlap: float = 0.5,
) -> tuple[int, int, int]:
    """Detect BPM range for songs with varying tempo.

    Splits the audio into overlapping windows and runs the 4-stage hybrid
    algorithm on each window, then returns the minimum, maximum, and median BPM.

    Args:
        file_path: Path to an audio file (MP3, FLAC, WAV, etc.)
        window_sec: Length of each analysis window in seconds (default 30).
        overlap: Fraction of overlap between consecutive windows (default 0.5).

    Returns:
        Tuple of (min_bpm, max_bpm, median_bpm).
    """
    y, sr = librosa.load(file_path)
    total_samples = len(y)
    window_samples = window_sec * sr
    step_samples = int(window_samples * (1 - overlap))

    if total_samples <= window_samples:
        bpm = _detect_bpm_from_signal(y, sr)
        return (bpm, bpm, bpm)

    bpms = []
    start = 0
    while start + window_samples <= total_samples:
        segment = y[start : start + window_samples]
        bpms.append(_detect_bpm_from_signal(segment, sr))
        start += step_samples

    # Include the tail if there's a remaining segment long enough (>= 10 sec)
    if start < total_samples and (total_samples - start) >= sr * 10:
        segment = y[start:]
        bpms.append(_detect_bpm_from_signal(segment, sr))

    if not bpms:
        bpm = _detect_bpm_from_signal(y, sr)
        return (bpm, bpm, bpm)

    min_bpm = min(bpms)
    max_bpm = max(bpms)
    median_bpm = round(float(np.median(bpms)))

    return (min_bpm, max_bpm, median_bpm)


def _inter_beat_onset_ratio(onset_env: np.ndarray, beats: np.ndarray) -> float:
    """Calculate ratio of onset strength at midpoints between beats vs on beats."""
    mid_strengths = []
    on_beat_strengths = []
    for i in range(len(beats) - 1):
        b1, b2 = beats[i], beats[i + 1]
        mid = (b1 + b2) // 2
        if mid < len(onset_env) and b1 < len(onset_env):
            mid_strengths.append(onset_env[mid])
            on_beat_strengths.append(onset_env[b1])
    if not on_beat_strengths:
        return 0.0
    return float(np.mean(mid_strengths) / np.mean(on_beat_strengths))
