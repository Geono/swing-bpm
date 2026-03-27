"""Write BPM to file metadata and rename files."""

import os
import re

from mutagen.flac import FLAC
from mutagen.id3 import TBPM
from mutagen.mp3 import MP3
from mutagen.wave import WAVE


SUPPORTED_EXTENSIONS = {".mp3", ".flac", ".wav"}
BPM_TAG_PATTERN = re.compile(r"^\[\d+(?:~\d+)?\]\s*")


def write_bpm_metadata(file_path: str, bpm: int) -> None:
    """Write BPM to audio file metadata.

    - MP3/WAV: ID3 TBPM tag
    - FLAC: Vorbis comment 'bpm' field
    """
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".mp3":
        audio = MP3(file_path)
        if audio.tags is None:
            audio.add_tags()
        audio.tags.add(TBPM(encoding=3, text=[str(bpm)]))
        audio.save()

    elif ext == ".flac":
        audio = FLAC(file_path)
        audio["bpm"] = [str(bpm)]
        audio.save()

    elif ext == ".wav":
        audio = WAVE(file_path)
        if audio.tags is None:
            audio.add_tags()
        audio.tags.add(TBPM(encoding=3, text=[str(bpm)]))
        audio.save()


def rename_with_bpm(file_path: str, bpm: int) -> str:
    """Rename file to include ``[bpm]`` prefix. Returns new path."""
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)

    clean_name = BPM_TAG_PATTERN.sub("", filename)
    new_name = f"[{bpm}] {clean_name}"
    new_path = os.path.join(directory, new_name)

    if new_path != file_path:
        os.rename(file_path, new_path)

    return new_path


def has_bpm_tag(filename: str) -> bool:
    """Check if filename already has a [BPM] prefix."""
    return bool(BPM_TAG_PATTERN.match(os.path.basename(filename)))


def is_supported(file_path: str) -> bool:
    """Check if file extension is supported."""
    return os.path.splitext(file_path)[1].lower() in SUPPORTED_EXTENSIONS
