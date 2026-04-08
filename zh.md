---
title: 中文
layout: default
nav_order: 4
description: "针对摇摆舞和爵士乐优化的自动BPM检测工具"
permalink: /zh
---

# swing-bpm (中文)
{: .fs-9 }

针对摇摆舞和爵士乐优化的**自动BPM检测工具**。
{: .fs-6 .fw-300 }

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-支持-yellow?style=flat&logo=buy-me-a-coffee&logoColor=white)](https://buymeacoffee.com/kunokim)
[![PyPI](https://img.shields.io/pypi/v/swing-bpm?color=blue)](https://pypi.org/project/swing-bpm/)

[开始使用](#安装){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[GitHub](https://github.com/Geono/swing-bpm){: .btn .fs-5 .mb-4 .mb-md-0 }
[English](/swing-bpm/){: .btn .fs-5 .mb-4 .mb-md-0 }
[한국어](/swing-bpm/ko){: .btn .fs-5 .mb-4 .mb-md-0 }
[日本語](/swing-bpm/ja){: .btn .fs-5 .mb-4 .mb-md-0 }

---

常见的BPM检测工具经常把快速摇摆节奏（180+ BPM）误识别为一半的速度。`swing-bpm`通过结合onset分析和PLP（Predominant Local Pulse）的混合算法解决了这个问题，在80~304 BPM范围的80首测试曲目中达到了**100%的准确率**。

![Before and After](before-after.png)

## 安装

```bash
pip install swing-bpm
```

更新:

```bash
pip install --upgrade swing-bpm
```

<details>
<summary><strong>从源码安装（备选方法）</strong></summary>

### macOS

1. 安装Python 3.9以上版本（已安装则跳过）:
   ```bash
   brew install python
   ```

2. 下载并安装swing-bpm:
   ```bash
   git clone https://github.com/Geono/swing-bpm.git
   cd swing-bpm
   pip3 install .
   ```

### Windows

1. 从[python.org](https://www.python.org/downloads/)安装Python 3.9以上版本。安装时**务必勾选"Add Python to PATH"**。

2. 如果没有Git，请安装[Git for Windows](https://git-scm.com/downloads/win)。

3. 打开**命令提示符**或**PowerShell**，输入以下命令:
   ```
   git clone https://github.com/Geono/swing-bpm.git
   cd swing-bpm
   pip install .
   ```

   如果没有Git，可以[下载ZIP文件](https://github.com/Geono/swing-bpm/archive/refs/heads/main.zip)，解压后在文件夹内运行`pip install .`。

### 从源码更新

```bash
cd swing-bpm
git pull
pip3 install .
```

如果使用`pipx`安装:

```bash
cd swing-bpm
git pull
pipx install --force .
```

</details>

## 使用方法

为文件夹内的所有音乐文件添加BPM标签:

```bash
# macOS
swing-bpm --rename ~/Music/swing/

# Windows
swing-bpm --rename "C:\Users\用户名\Music\swing"
```

程序会自动扫描所有子文件夹，对每个文件:
1. 自动检测BPM
2. 在文件名前添加`[BPM]`前缀（如: `[174] Tea For Two.mp3`）
3. 将BPM写入音频元数据（MP3/WAV: ID3 TBPM，FLAC: Vorbis comment）

### 选项

```bash
swing-bpm ./music/ --dry-run       # 仅预览，不做任何更改
swing-bpm ./music/                 # 只写入元数据（不重命名）
swing-bpm ./music/ --no-metadata   # 跳过写入元数据（与--rename配合使用）
swing-bpm ./music/ --tag-title     # 在标题元数据前添加[BPM]
swing-bpm ./music/ --overwrite     # 重新检测已标记的文件
swing-bpm ./music/ --range         # 检测变速曲目的BPM范围（min~max）
swing-bpm track1.mp3 track2.flac   # 只处理指定文件
```

`--rename`选项在文件名前添加`[BPM]`前缀（如: `[174] Tea For Two.mp3`）。默认只写入元数据。

`--tag-title`选项在标题元数据（ID3 TIT2等）前添加`[BPM]`。在Mixxx等DJ软件无法正确读取BPM元数据时很有用——你可以直接在标题栏看到BPM。如果文件没有标题元数据，则用文件名代替。

`--range`选项检测变速曲目的BPM范围（如: 先慢后快的曲子）。将音频分成30秒的重叠区间，对每个区间运行完整的4阶段检测算法，输出min~max范围。文件以`[120~180]`格式标记，TBPM元数据存储中位数，评论字段保存完整范围。

### 支持的格式

- MP3
- FLAC
- WAV

## 工作原理

### 问题

大多数BPM检测工具通过寻找音频中的重复节奏模式来计算速度。在摇摆爵士乐中，每小节的第1拍和第3拍有节奏组的重音，第2拍和第4拍相对较轻。在快速节奏（180+ BPM）下，检测工具只捕捉到第1、3拍的重音，检测出实际速度的一半。一首200 BPM的曲子会被识别为100 BPM。

### 解决方案: 4阶段混合检测

**第1阶段: 基础检测**

使用`librosa.beat.beat_track()`进行初始速度估计。在慢到中等速度下效果不错，但快速曲目经常返回一半的速度。

**第2阶段: Onset比率分析**

**Onset** = 音频中能量突然爆发的瞬间，比如鼓击、号角重音、钢琴和弦的起奏。测量每个检测到的节拍位置的onset强度，并与节拍*中间点*的onset强度进行比较。

如果实际速度是检测值的2倍，那些中间点其实是真正的节拍，所以会有强烈的onset。计算比率: `中间点onset强度 / 节拍上的onset强度`。

- **比率 < 0.27** → 中间点安静，检测速度正确
- **比率 > 0.33** → 中间点有强烈打击，实际速度是2倍
- **比率 0.27~0.33** → 判断模糊，需要进一步确认

**第3阶段: PLP判定**

在边界情况下使用**PLP（Predominant Local Pulse，主导局部脉冲）**算法。与节拍追踪固定在单一全局速度不同，PLP逐帧独立估计每个时刻的感知"脉搏"，然后取中位数。

**第4阶段: PLP稳定性验证** *（v0.2.0新增）*

当基础速度较慢（< 105 BPM）时，walking bass、钢琴伴奏、人声乐句会填充节拍之间的空间，导致onset比率虚高。通过检查PLP稳定性（标准差）来决定是否进行2倍处理。

## 作为库使用

```python
from swing_bpm import detect_bpm, detect_bpm_range

bpm = detect_bpm("Tea For Two.mp3")
print(bpm)  # 174

# 变速曲目
min_bpm, max_bpm, median_bpm = detect_bpm_range("Darktown Strutters Ball.mp3")
print(f"{min_bpm}~{max_bpm} (median {median_bpm})")  # 89~157 (median 152)
```

## 测试结果

在80首经人工确认BPM标签的摇摆/爵士曲目（80~304 BPM）上测试，所有检测值与实际速度的偏差在±10 BPM以内。

另外在417首曲目（80~304 BPM）上验证，99.3%在±10 BPM以内，平均绝对误差为3.2 BPM。

---

## 支持

如果这个工具帮到了你，请我喝杯咖啡吧!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-支持-yellow?style=flat&logo=buy-me-a-coffee&logoColor=white)](https://buymeacoffee.com/kunokim)

## 致谢

感谢[sabok](https://www.instagram.com/sabok_swing/)提供测试和开发中使用的示例音乐。
