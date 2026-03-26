# swing-bpm

Automatic BPM detection optimized for **swing & jazz music**.

Standard BPM detectors often misidentify fast swing tempos (180+ BPM) as half-tempo. `swing-bpm` solves this with a hybrid detection algorithm that combines onset analysis with Predominant Local Pulse (PLP), achieving **100% accuracy** on an 80-song test set spanning 80–304 BPM.

## Install

```bash
pip install swing-bpm
```

## Usage

Tag all music files in a folder:

```bash
swing-bpm ~/Music/swing/
```

This will:
1. Detect BPM for each file
2. Rename files with a `[BPM]` prefix (e.g., `[174] Tea For Two.mp3`)
3. Write BPM to audio metadata (ID3 TBPM for MP3/WAV, Vorbis comment for FLAC)

### Options

```bash
swing-bpm ~/Music/swing/ --dry-run       # Preview without changes
swing-bpm ~/Music/swing/ --no-rename     # Metadata only, don't rename
swing-bpm ~/Music/swing/ --no-metadata   # Rename only, don't write metadata
swing-bpm ~/Music/swing/ --overwrite     # Re-detect already tagged files
swing-bpm track1.mp3 track2.flac         # Process specific files
```

### Supported formats

- MP3
- FLAC
- WAV

## How it works

1. **Base detection** — `librosa.beat.beat_track()` finds initial tempo
2. **Half-tempo check** — Measures onset strength at midpoints between detected beats. A high mid/on-beat ratio (>0.30) suggests the true tempo is double
3. **PLP tiebreaker** — For borderline cases (ratio 0.27–0.33), Predominant Local Pulse analysis decides whether to double

This approach is specifically tuned for swing jazz, where the rhythmic structure often confuses general-purpose BPM detectors.

## As a library

```python
from swing_bpm import detect_bpm

bpm = detect_bpm("Tea For Two.mp3")
print(bpm)  # 174
```

## License

MIT
