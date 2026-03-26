"""Core BPM detection logic using hybrid onset-ratio + PLP approach."""

import librosa
import numpy as np


def detect_bpm(file_path: str) -> int:
    """Detect BPM of an audio file.

    Uses a hybrid approach optimized for swing/jazz music:
    1. librosa beat_track for base tempo detection
    2. Inter-beat onset ratio to detect half-tempo misdetection
    3. PLP (Predominant Local Pulse) as tiebreaker for borderline cases

    Args:
        file_path: Path to an audio file (MP3, FLAC, WAV, etc.)

    Returns:
        Detected BPM as an integer.
    """
    y, sr = librosa.load(file_path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)

    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    base_bpm = float(tempo[0]) if hasattr(tempo, "__len__") else float(tempo)

    if len(beats) < 4:
        return round(base_bpm)

    ratio = _inter_beat_onset_ratio(onset_env, beats)

    if 0.27 <= ratio <= 0.33:
        plp_bpm = _plp_bpm(onset_env, sr)
        if plp_bpm > 0 and abs(plp_bpm / base_bpm - 2.0) < 0.3:
            return round(base_bpm * 2)
        elif plp_bpm > 0 and abs(plp_bpm / base_bpm - 1.0) < 0.3:
            return round(base_bpm)
        else:
            return round(base_bpm * 2) if ratio > 0.30 else round(base_bpm)

    if ratio > 0.30:
        return round(base_bpm * 2)

    return round(base_bpm)


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


def _plp_bpm(onset_env: np.ndarray, sr: int) -> float:
    """Calculate BPM using Predominant Local Pulse."""
    pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr)
    peaks = np.where(librosa.util.localmax(pulse))[0]
    if len(peaks) < 2:
        return 0.0
    intervals = np.diff(peaks)
    hop = 512
    return 60.0 * sr / (float(np.median(intervals)) * hop)
