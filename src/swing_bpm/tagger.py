"""Write BPM to file metadata and rename files."""

import os
import re

from mutagen.flac import FLAC
from mutagen.id3 import TIT2, TBPM
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


def _title_from_filename(file_path: str) -> str:
    """Extract a title from the filename (without extension and BPM prefix)."""
    name = os.path.splitext(os.path.basename(file_path))[0]
    return BPM_TAG_PATTERN.sub("", name)


def write_bpm_to_title(file_path: str, bpm: int) -> None:
    """Prepend [BPM] to the title metadata tag. Falls back to filename if title is empty."""
    ext = os.path.splitext(file_path)[1].lower()
    fallback = _title_from_filename(file_path)

    if ext == ".mp3":
        audio = MP3(file_path)
        if audio.tags is None:
            audio.add_tags()
        title = str(audio.tags.get("TIT2", ""))
        clean_title = BPM_TAG_PATTERN.sub("", title).strip()
        if not clean_title:
            clean_title = fallback
        audio.tags.add(TIT2(encoding=3, text=[f"[{bpm}] {clean_title}"]))
        audio.save()

    elif ext == ".flac":
        audio = FLAC(file_path)
        title = audio.get("title", [""])[0]
        clean_title = BPM_TAG_PATTERN.sub("", title).strip()
        if not clean_title:
            clean_title = fallback
        audio["title"] = [f"[{bpm}] {clean_title}"]
        audio.save()

    elif ext == ".wav":
        audio = WAVE(file_path)
        if audio.tags is None:
            audio.add_tags()
        title = str(audio.tags.get("TIT2", ""))
        clean_title = BPM_TAG_PATTERN.sub("", title).strip()
        if not clean_title:
            clean_title = fallback
        audio.tags.add(TIT2(encoding=3, text=[f"[{bpm}] {clean_title}"]))
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
