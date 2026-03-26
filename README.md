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

---

# swing-bpm (한국어)

스윙 & 재즈 음악에 최적화된 **자동 BPM 측정 도구**입니다.

일반적인 BPM 측정기는 빠른 스윙 템포(180+ BPM)를 절반 속도로 잘못 인식하는 경우가 많습니다. `swing-bpm`은 onset 분석과 PLP(Predominant Local Pulse)를 결합한 하이브리드 알고리즘으로 이 문제를 해결하며, 80~304 BPM 범위의 80곡 테스트에서 **100% 정확도**를 달성했습니다.

## 설치

```bash
pip install swing-bpm
```

## 사용법

폴더 내 모든 음악 파일에 BPM 태그 달기:

```bash
swing-bpm ~/Music/swing/
```

실행하면 각 파일에 대해:
1. BPM을 자동 측정합니다
2. 파일명 앞에 `[BPM]`을 붙입니다 (예: `[174] Tea For Two.mp3`)
3. 오디오 메타데이터에 BPM을 기록합니다 (MP3/WAV: ID3 TBPM, FLAC: Vorbis comment)

### 옵션

```bash
swing-bpm ~/Music/swing/ --dry-run       # 변경 없이 미리보기만
swing-bpm ~/Music/swing/ --no-rename     # 메타데이터만 기록 (파일명 변경 안 함)
swing-bpm ~/Music/swing/ --no-metadata   # 파일명만 변경 (메타데이터 기록 안 함)
swing-bpm ~/Music/swing/ --overwrite     # 이미 태그된 파일도 다시 측정
swing-bpm track1.mp3 track2.flac         # 특정 파일만 처리
```

### 지원 포맷

- MP3
- FLAC
- WAV

## 작동 원리

1. **기본 측정** — `librosa.beat.beat_track()`으로 초기 템포 감지
2. **반박자 보정** — 감지된 비트 사이 중간 지점의 onset 강도를 측정합니다. 중간/비트 비율이 높으면(>0.30) 실제 템포가 2배라는 의미입니다
3. **PLP 판정** — 경계 구간(비율 0.27~0.33)에서는 PLP 분석으로 최종 판정합니다

이 방식은 일반 BPM 측정기가 혼동하기 쉬운 스윙 재즈의 리듬 구조에 맞게 특별히 조정되었습니다.

## 라이브러리로 사용

```python
from swing_bpm import detect_bpm

bpm = detect_bpm("Tea For Two.mp3")
print(bpm)  # 174
```
