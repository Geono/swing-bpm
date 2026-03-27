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
