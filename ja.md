---
title: 日本語
layout: default
nav_order: 3
description: "スウィング＆ジャズ音楽に最適化された自動BPM検出ツール"
permalink: /ja
---

# swing-bpm (日本語)
{: .fs-9 }

スウィング＆ジャズ音楽に最適化された**自動BPM検出ツール**です。
{: .fs-6 .fw-300 }

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-サポート-yellow?style=flat&logo=buy-me-a-coffee&logoColor=white)](https://buymeacoffee.com/kunokim)
[![PyPI](https://img.shields.io/pypi/v/swing-bpm?color=blue)](https://pypi.org/project/swing-bpm/)

[はじめる](#インストール){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHub](https://github.com/Geono/swing-bpm){: .btn .fs-5 .mb-4 .mb-md-0 }
[English](/swing-bpm/){: .btn .fs-5 .mb-4 .mb-md-0 }
[한국어](/swing-bpm/ko){: .btn .fs-5 .mb-4 .mb-md-0 }
[中文](/swing-bpm/zh){: .btn .fs-5 .mb-4 .mb-md-0 }

---

一般的なBPM検出ツールは、速いスウィングテンポ（180+ BPM）を半分の速さで誤認識することがよくあります。`swing-bpm`はオンセット解析とPLP（Predominant Local Pulse）を組み合わせたハイブリッドアルゴリズムでこの問題を解決し、80〜304 BPMの80曲テストで**100%の精度**を達成しました。

![Before and After](before-after.png)

## インストール

```bash
pip install swing-bpm
```

アップデート:

```bash
pip install --upgrade swing-bpm
```

<details>
<summary><strong>ソースからインストール（別の方法）</strong></summary>

### macOS

1. Python 3.9以上をインストール（既にあればスキップ）:
   ```bash
   brew install python
   ```

2. swing-bpmをダウンロードしてインストール:
   ```bash
   git clone https://github.com/Geono/swing-bpm.git
   cd swing-bpm
   pip3 install .
   ```

### Windows

1. [python.org](https://www.python.org/downloads/)からPython 3.9以上をインストールします。インストール時に**「Add Python to PATH」に必ずチェック**を入れてください。

2. Gitがなければ[Git for Windows](https://git-scm.com/downloads/win)をインストールします。

3. **コマンドプロンプト**または**PowerShell**を開き、以下を入力します:
   ```
   git clone https://github.com/Geono/swing-bpm.git
   cd swing-bpm
   pip install .
   ```

   Gitがなければ[ZIPファイルをダウンロード](https://github.com/Geono/swing-bpm/archive/refs/heads/main.zip)して解凍し、そのフォルダ内で`pip install .`を実行してください。

### ソースからのアップデート

```bash
cd swing-bpm
git pull
pip3 install .
```

`pipx`でインストールした場合:

```bash
cd swing-bpm
git pull
pipx install --force .
```

</details>

## 使い方

フォルダ内の全音楽ファイルにBPMタグを付ける:

```bash
# macOS
swing-bpm --rename ~/Music/swing/

# Windows
swing-bpm --rename "C:\Users\ユーザー名\Music\swing"
```

サブフォルダも自動的にスキャンし、各ファイルに対して:
1. BPMを自動検出
2. ファイル名の先頭に`[BPM]`を追加（例: `[174] Tea For Two.mp3`）
3. オーディオメタデータにBPMを書き込み（MP3/WAV: ID3 TBPM、FLAC: Vorbisコメント）

### オプション

```bash
swing-bpm ./music/ --dry-run       # 変更なしでプレビューのみ
swing-bpm ./music/                 # メタデータのみ書き込み（リネームなし）
swing-bpm ./music/ --no-metadata   # メタデータ書き込みをスキップ（--renameと併用）
swing-bpm ./music/ --tag-title     # タイトルメタデータの先頭に[BPM]を追加
swing-bpm ./music/ --overwrite     # タグ済みファイルも再検出
swing-bpm ./music/ --range         # テンポが変化する曲のBPM範囲（min~max）を検出
swing-bpm track1.mp3 track2.flac   # 特定のファイルのみ処理
```

`--rename`オプションはファイル名の先頭に`[BPM]`プレフィックスを追加します（例: `[174] Tea For Two.mp3`）。デフォルトではメタデータのみ書き込みます。

`--tag-title`オプションはタイトルメタデータ（ID3 TIT2など）の先頭に`[BPM]`を追加します。MixxxなどのDJソフトウェアでBPMメタデータを正しく読み取れない場合に便利です。タイトルカラムから直接BPMを確認できます。タイトルメタデータが空のファイルはファイル名を代わりに使用します。

`--range`オプションはテンポが変化する曲のBPM範囲を検出します（例: ゆっくり始まって速くなる曲）。オーディオを30秒のオーバーラップする区間に分割し、各区間で4段階検出アルゴリズムを実行してmin〜max範囲を出力します。ファイルは`[120~180]`形式でタグ付けされ、TBPMメタデータには中央値が、コメントフィールドに全範囲が保存されます。

### 対応フォーマット

- MP3
- FLAC
- WAV

## 仕組み

### 問題点

ほとんどのBPM検出ツールは、オーディオ内の繰り返しリズムパターンからテンポを計算します。スウィングジャズでは、各小節の1拍目と3拍目にリズムセクションの強いアクセントが入り、2拍目と4拍目は比較的軽くなります。速いテンポ（180+ BPM）では、検出ツールが1拍・3拍の強いアクセントだけを捉えて実際のテンポの半分を検出してしまいます。200 BPMの曲が100 BPMとして検出される、という具合です。

### 解決策: 4段階ハイブリッド方式

**第1段階: 基本検出**

`librosa.beat.beat_track()`で初期テンポを推定します。遅い〜中程度のテンポではうまく動きますが、速い曲では半分のテンポを返すことが頻繁にあります。

**第2段階: オンセット比率解析**

**オンセット** = ドラムのヒット、ホーンのアクセント、ピアノコードのアタックなど、オーディオ内でエネルギーが急激に発生する瞬間です。検出された各ビート位置のオンセット強度と、ビート間の*中間点*のオンセット強度を比較します。

実際のテンポが検出値の2倍なら、その中間点は本物のビートなので強いオンセットがあるはずです。この比率を計算します: `中間点のオンセット強度 / ビート上のオンセット強度`。

- **比率 < 0.27** → 中間点が静か、検出テンポは正しい
- **比率 > 0.33** → 中間点にも強いヒット、実際のテンポは2倍
- **比率 0.27〜0.33** → 判断が曖昧、追加判定が必要

**第3段階: PLPによる判定**

境界ケースでは**PLP（Predominant Local Pulse、優勢局所パルス）**アルゴリズムを使用します。ビートトラッキングが単一のグローバルテンポに固定されるのに対し、PLPは各瞬間の体感的な「脈拍」をフレーム単位で独立推定し、中央値を取ります。

**第4段階: PLP安定性ガード** *（v0.2.0で追加）*

基本テンポが遅い場合（< 105 BPM）、ウォーキングベース、ピアノコンピング、ボーカルフレージングがビート間を埋めるため、オンセット比率が実際より高く出ることがあります。PLP安定性（標準偏差）を確認して2倍処理の可否を判定します。

## ライブラリとして使用

```python
from swing_bpm import detect_bpm, detect_bpm_range

bpm = detect_bpm("Tea For Two.mp3")
print(bpm)  # 174

# テンポが変化する曲
min_bpm, max_bpm, median_bpm = detect_bpm_range("Darktown Strutters Ball.mp3")
print(f"{min_bpm}~{max_bpm} (median {median_bpm})")  # 89~157 (median 152)
```

## テスト結果

人間が確認したBPMラベル付きのスウィング/ジャズ80曲（80〜304 BPM）でテストしました。すべての検出値が実際のテンポに対して±10 BPM以内です。

さらに417曲（80〜304 BPM）で検証した結果、99.3%が±10 BPM以内、平均絶対誤差は3.2 BPMでした。

---

## サポート

このツールが役に立ったら、コーヒーをおごってください!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-サポート-yellow?style=flat&logo=buy-me-a-coffee&logoColor=white)](https://buymeacoffee.com/kunokim)

## 謝辞

テストおよび開発に使用したサンプル音源を提供してくださった[sabok](https://www.instagram.com/sabok_swing/)さんに感謝します。
