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

## Test results

Tested on 80 swing/jazz tracks with human-verified BPM labels (80–304 BPM). All detected values fall within ±10 BPM of the true tempo.

<details>
<summary><strong>Full test results (80 songs, 100% accuracy)</strong></summary>

| True BPM | Detected | Diff | Artist | Title |
|----------|----------|------|--------|-------|
| 80 | 81 | +1 | Eyal Vilner | Don't You Feel My Leg |
| 82 | 83 | +1 | Eyal Vilner | Tell Me Pretty Baby |
| 100 | 96 | -4 | Eyal Vilner | After The Lights Go Down Low |
| 107 | 108 | +1 | Helen Humes | Sneaking Around With You |
| 114 | 117 | +3 | Eyal Vilner | Will You Be My Quarantine? |
| 116 | 123 | +7 | Lou Rawls | Just Squeeze Me (But Don't Tease Me) |
| 118 | 117 | -1 | Brooks Prumo Orchestra | Blue Lester |
| 120 | 117 | -3 | Eyal Vilner | Call Me Tomorrow, I Come Next Week |
| 125 | 123 | -2 | Eyal Vilner | Just A Lucky So And So |
| 126 | 129 | +3 | Mint Julep Jazz Band | Exactly Like You |
| 127 | 123 | -4 | Frank Sinatra | You Make Me Feel So Young |
| 128 | 129 | +1 | Eyal Vilner | I Don't Want to be Kissed |
| 128 | 129 | +1 | The Griffin Brothers | Riffin' With Griffin' |
| 128 | 129 | +1 | Shirt Tail Stompers | Oh Me, Oh My, Oh Gosh |
| 130 | 136 | +6 | Lou Rawls | I'd Rather Drink Muddy Water |
| 133 | 123 | -10 | Louis Jordan | No Sale |
| 134 | 136 | +2 | The Treniers | Drink Wine, Spo-Dee-O-Dee |
| 134 | 136 | +2 | Fred Mollin, Blue Sea Band | Shoo Fly Pie And Apple Pan Dowdy |
| 134 | 136 | +2 | Naomi & Her Handsome Devils | Take It Easy Greasy |
| 135 | 136 | +1 | Indigo Swing | The Best You Can |
| 138 | 136 | -2 | Benny Goodman | What Can I Say After I Say I'm Sorry |
| 139 | 136 | -3 | Louis Jordan | Cole Slaw (Sorghum Switch) |
| 140 | 136 | -4 | Count Basie | Things Ain't What They Used To Be |
| 143 | 136 | -7 | George Williams | Celery Stalks At Midnight |
| 153 | 152 | -1 | Roy Eldridge | Jump Through the Window |
| 155 | 161 | +6 | Brooks Prumo Orchestra | Broadway |
| 155 | 161 | +6 | Illinois Jacquet | What's This |
| 156 | 161 | +5 | The Griffin Brothers | Shuffle Bug |
| 160 | 152 | -8 | Count Basie | Swingin' The Blues |
| 161 | 161 | +0 | Mercer Ellington | Steppin' Into Swing Society |
| 162 | 161 | -1 | Eyal Vilner | Blue Skies |
| 166 | 167 | +1 | Ella Fitzgerald | Mack The Knife (Live) |
| 167 | 161 | -6 | Count Basie | Fair And Warmer |
| 170 | 172 | +2 | Count Basie & His Orchestra | Sweets |
| 170 | 178 | +8 | Duke Ellington, Johnny Hodges | Villes Ville Is the Place, Man |
| 171 | 172 | +1 | Johnny Hodges | Something to Pat Your Foot To |
| 173 | 178 | +5 | Duke Ellington | Let's Get Together |
| 174 | 172 | -2 | Eyal Vilner | Bumpy Tour Bus |
| 174 | 172 | -2 | Eyal Vilner | Tea For Two |
| 176 | 178 | +2 | Eyal Vilner | T'aint What You Do |
| 180 | 185 | +5 | Eyal Vilner | I Want Coffee |
| 181 | 191 | +10 | Bud Freeman's Summa Cum Laude Orchestra | You Took Advantage Of Me |
| 182 | 178 | -4 | Eyal Vilner | I Love The Rhythm in a Riff |
| 182 | 178 | -4 | The Glenn Crytzer Orchestra | Jive at Five |
| 182 | 185 | +3 | Harry James And His Orchestra | Trumpet Blues and Cantabile |
| 182 | 191 | +9 | Bud Freeman's Summa Cum Laude Orchestra | You Took Advantage Of Me |
| 190 | 191 | +1 | Illinois Jacquet | Bottom's Up |
| 190 | 199 | +9 | Eyal Vilner | Chabichou |
| 190 | 191 | +1 | Tommy Dorsey | Well Git It |
| 192 | 199 | +7 | The Griffin Brothers | Blues With A Beat |
| 192 | 191 | -1 | Freddie Jackson | Duck Fever |
| 195 | 191 | -4 | Earl "Fatha" Hines | Hollywood Hop |
| 195 | 199 | +4 | The Griffin Brothers | Blues With A Beat |
| 195 | 199 | +4 | Count Basie | It's Sand, Man |
| 195 | 199 | +4 | Chick Webb | Lindyhopper's Delight |
| 196 | 191 | -5 | Naomi & Her Handsome Devils | I Know How To Do It |
| 203 | 199 | -4 | Ella Fitzgerald, Chick Webb | I Want To Be Happy |
| 205 | 199 | -6 | Jack McVea & His Orchestra | Ube Dubie |
| 205 | 199 | -6 | Jonathan Stout & His Campus Five | Wholly Cats |
| 207 | 215 | +8 | Brooks Prumo Orchestra | Dinah |
| 210 | 207 | -3 | — | Diga Diga Doo |
| 210 | 215 | +5 | Artie Shaw | Oh! Lady, Be Good |
| 210 | 207 | -3 | Harry James | Trumpet Blues And Cantabile |
| 212 | 207 | -5 | Count Basie & His Orchestra | Fantail |
| 215 | 215 | +0 | — | Riff Time |
| 216 | 215 | -1 | Benny Goodman | Jam Session 1936 |
| 220 | 225 | +5 | — | Jammin' the Blues |
| 222 | 225 | +3 | — | Clap Hands, Here Comes Charlie |
| 225 | 225 | +0 | — | Harlem Jump |
| 227 | 225 | -2 | — | Sing You Sinners |
| 228 | 235 | +7 | Earl Hines | The Earl |
| 230 | 225 | -5 | Eyal Vilner | Lobby Call Blues |
| 230 | 235 | +5 | Brooks Prumo Orchestra | Six Cats And A Prince |
| 240 | 235 | -5 | Eyal Vilner | Swing Brother Swing |
| 245 | 246 | +1 | Eyal Vilner | Jumpin' At The Woodside |
| 246 | 246 | +0 | Count Basie | Jumping At The Woodside |
| 250 | 258 | +8 | Brooks Prumo Orchestra | Peek-A-Boo |
| 250 | 258 | +8 | Eyal Vilner | Swingin' Uptown |
| 255 | 258 | +3 | King Of Swing Orchestra | Bugle Call Rag |
| 304 | 304 | +0 | Eyal Vilner | Hellzapoppin' |

</details>

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

## 테스트 결과

사람이 직접 확인한 BPM 라벨이 있는 스윙/재즈 80곡(80~304 BPM)으로 테스트했습니다. 모든 측정값이 실제 템포 대비 ±10 BPM 이내입니다.

<details>
<summary><strong>전체 테스트 결과 (80곡, 정확도 100%)</strong></summary>

| 실제 BPM | 측정 | 차이 | 아티스트 | 곡명 |
|----------|------|------|----------|------|
| 80 | 81 | +1 | Eyal Vilner | Don't You Feel My Leg |
| 82 | 83 | +1 | Eyal Vilner | Tell Me Pretty Baby |
| 100 | 96 | -4 | Eyal Vilner | After The Lights Go Down Low |
| 107 | 108 | +1 | Helen Humes | Sneaking Around With You |
| 114 | 117 | +3 | Eyal Vilner | Will You Be My Quarantine? |
| 116 | 123 | +7 | Lou Rawls | Just Squeeze Me (But Don't Tease Me) |
| 118 | 117 | -1 | Brooks Prumo Orchestra | Blue Lester |
| 120 | 117 | -3 | Eyal Vilner | Call Me Tomorrow, I Come Next Week |
| 125 | 123 | -2 | Eyal Vilner | Just A Lucky So And So |
| 126 | 129 | +3 | Mint Julep Jazz Band | Exactly Like You |
| 127 | 123 | -4 | Frank Sinatra | You Make Me Feel So Young |
| 128 | 129 | +1 | Eyal Vilner | I Don't Want to be Kissed |
| 128 | 129 | +1 | The Griffin Brothers | Riffin' With Griffin' |
| 128 | 129 | +1 | Shirt Tail Stompers | Oh Me, Oh My, Oh Gosh |
| 130 | 136 | +6 | Lou Rawls | I'd Rather Drink Muddy Water |
| 133 | 123 | -10 | Louis Jordan | No Sale |
| 134 | 136 | +2 | The Treniers | Drink Wine, Spo-Dee-O-Dee |
| 134 | 136 | +2 | Fred Mollin, Blue Sea Band | Shoo Fly Pie And Apple Pan Dowdy |
| 134 | 136 | +2 | Naomi & Her Handsome Devils | Take It Easy Greasy |
| 135 | 136 | +1 | Indigo Swing | The Best You Can |
| 138 | 136 | -2 | Benny Goodman | What Can I Say After I Say I'm Sorry |
| 139 | 136 | -3 | Louis Jordan | Cole Slaw (Sorghum Switch) |
| 140 | 136 | -4 | Count Basie | Things Ain't What They Used To Be |
| 143 | 136 | -7 | George Williams | Celery Stalks At Midnight |
| 153 | 152 | -1 | Roy Eldridge | Jump Through the Window |
| 155 | 161 | +6 | Brooks Prumo Orchestra | Broadway |
| 155 | 161 | +6 | Illinois Jacquet | What's This |
| 156 | 161 | +5 | The Griffin Brothers | Shuffle Bug |
| 160 | 152 | -8 | Count Basie | Swingin' The Blues |
| 161 | 161 | +0 | Mercer Ellington | Steppin' Into Swing Society |
| 162 | 161 | -1 | Eyal Vilner | Blue Skies |
| 166 | 167 | +1 | Ella Fitzgerald | Mack The Knife (Live) |
| 167 | 161 | -6 | Count Basie | Fair And Warmer |
| 170 | 172 | +2 | Count Basie & His Orchestra | Sweets |
| 170 | 178 | +8 | Duke Ellington, Johnny Hodges | Villes Ville Is the Place, Man |
| 171 | 172 | +1 | Johnny Hodges | Something to Pat Your Foot To |
| 173 | 178 | +5 | Duke Ellington | Let's Get Together |
| 174 | 172 | -2 | Eyal Vilner | Bumpy Tour Bus |
| 174 | 172 | -2 | Eyal Vilner | Tea For Two |
| 176 | 178 | +2 | Eyal Vilner | T'aint What You Do |
| 180 | 185 | +5 | Eyal Vilner | I Want Coffee |
| 181 | 191 | +10 | Bud Freeman's Summa Cum Laude Orchestra | You Took Advantage Of Me |
| 182 | 178 | -4 | Eyal Vilner | I Love The Rhythm in a Riff |
| 182 | 178 | -4 | The Glenn Crytzer Orchestra | Jive at Five |
| 182 | 185 | +3 | Harry James And His Orchestra | Trumpet Blues and Cantabile |
| 182 | 191 | +9 | Bud Freeman's Summa Cum Laude Orchestra | You Took Advantage Of Me |
| 190 | 191 | +1 | Illinois Jacquet | Bottom's Up |
| 190 | 199 | +9 | Eyal Vilner | Chabichou |
| 190 | 191 | +1 | Tommy Dorsey | Well Git It |
| 192 | 199 | +7 | The Griffin Brothers | Blues With A Beat |
| 192 | 191 | -1 | Freddie Jackson | Duck Fever |
| 195 | 191 | -4 | Earl "Fatha" Hines | Hollywood Hop |
| 195 | 199 | +4 | The Griffin Brothers | Blues With A Beat |
| 195 | 199 | +4 | Count Basie | It's Sand, Man |
| 195 | 199 | +4 | Chick Webb | Lindyhopper's Delight |
| 196 | 191 | -5 | Naomi & Her Handsome Devils | I Know How To Do It |
| 203 | 199 | -4 | Ella Fitzgerald, Chick Webb | I Want To Be Happy |
| 205 | 199 | -6 | Jack McVea & His Orchestra | Ube Dubie |
| 205 | 199 | -6 | Jonathan Stout & His Campus Five | Wholly Cats |
| 207 | 215 | +8 | Brooks Prumo Orchestra | Dinah |
| 210 | 207 | -3 | — | Diga Diga Doo |
| 210 | 215 | +5 | Artie Shaw | Oh! Lady, Be Good |
| 210 | 207 | -3 | Harry James | Trumpet Blues And Cantabile |
| 212 | 207 | -5 | Count Basie & His Orchestra | Fantail |
| 215 | 215 | +0 | — | Riff Time |
| 216 | 215 | -1 | Benny Goodman | Jam Session 1936 |
| 220 | 225 | +5 | — | Jammin' the Blues |
| 222 | 225 | +3 | — | Clap Hands, Here Comes Charlie |
| 225 | 225 | +0 | — | Harlem Jump |
| 227 | 225 | -2 | — | Sing You Sinners |
| 228 | 235 | +7 | Earl Hines | The Earl |
| 230 | 225 | -5 | Eyal Vilner | Lobby Call Blues |
| 230 | 235 | +5 | Brooks Prumo Orchestra | Six Cats And A Prince |
| 240 | 235 | -5 | Eyal Vilner | Swing Brother Swing |
| 245 | 246 | +1 | Eyal Vilner | Jumpin' At The Woodside |
| 246 | 246 | +0 | Count Basie | Jumping At The Woodside |
| 250 | 258 | +8 | Brooks Prumo Orchestra | Peek-A-Boo |
| 250 | 258 | +8 | Eyal Vilner | Swingin' Uptown |
| 255 | 258 | +3 | King Of Swing Orchestra | Bugle Call Rag |
| 304 | 304 | +0 | Eyal Vilner | Hellzapoppin' |

</details>

## 라이브러리로 사용

```python
from swing_bpm import detect_bpm

bpm = detect_bpm("Tea For Two.mp3")
print(bpm)  # 174
```
