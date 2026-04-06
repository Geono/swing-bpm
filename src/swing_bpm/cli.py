"""Command-line interface for swing-bpm."""

import argparse
import os
import sys

from swing_bpm import __version__
from swing_bpm.detector import detect_bpm
from swing_bpm.tagger import (
    has_bpm_tag,
    is_supported,
    rename_with_bpm,
    write_bpm_metadata,
    write_bpm_to_title,
)


def main():
    parser = argparse.ArgumentParser(
        prog="swing-bpm",
        description="Detect BPM of swing/jazz music files and tag them.",
    )
    parser.add_argument(
        "path",
        nargs="+",
        help="Audio files or directories to process.",
    )
    parser.add_argument(
        "--no-rename",
        action="store_true",
        help="Skip renaming files (only write metadata).",
    )
    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Skip writing metadata (only rename files).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-detect and overwrite existing BPM tags.",
    )
    parser.add_argument(
        "--tag-title",
        action="store_true",
        help="Prepend [BPM] to the title metadata tag.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes.",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args()

    print("swing-bpm — by Kuno Kim (https://instagram.com/kuno.headswing)\n")

    files = _collect_files(args.path)
    if not files:
        print("No supported audio files found.", file=sys.stderr)
        sys.exit(1)

    total = len(files)
    print(f"Found {total} audio file(s)\n")

    for i, file_path in enumerate(files, 1):
        filename = os.path.basename(file_path)

        if has_bpm_tag(filename) and not args.overwrite:
            print(f"[{i}/{total}] Skip (already tagged): {filename}")
            continue

        print(f"[{i}/{total}] Analyzing: {filename}", end="", flush=True)

        try:
            bpm = detect_bpm(file_path)
        except Exception as e:
            print(f" -> Error: {e}")
            continue

        print(f" -> {bpm} BPM")

        if args.dry_run:
            if not args.no_rename:
                from swing_bpm.tagger import BPM_TAG_PATTERN
                clean = BPM_TAG_PATTERN.sub("", filename)
                print(f"         Would rename to: [{bpm}] {clean}")
            if not args.no_metadata:
                print(f"         Would write BPM metadata: {bpm}")
            if args.tag_title:
                print(f"         Would tag title with: [{bpm}]")
            continue

        if not args.no_metadata:
            try:
                write_bpm_metadata(file_path, bpm)
            except Exception as e:
                print(f"         Metadata write failed: {e}")

        if args.tag_title:
            try:
                write_bpm_to_title(file_path, bpm)
            except Exception as e:
                print(f"         Title tag failed: {e}")

        if not args.no_rename:
            try:
                new_path = rename_with_bpm(file_path, bpm)
                if new_path != file_path:
                    file_path = new_path
            except Exception as e:
                print(f"         Rename failed: {e}")

    print("\nDone!")


def _collect_files(paths: list[str]) -> list[str]:
    """Collect all supported audio files from given paths (recursive)."""
    files = []
    for path in paths:
        path = os.path.expanduser(path)
        if os.path.isfile(path) and is_supported(path):
            files.append(os.path.abspath(path))
        elif os.path.isdir(path):
            for dirpath, _, filenames in os.walk(path):
                for entry in sorted(filenames):
                    full = os.path.join(dirpath, entry)
                    if is_supported(full):
                        files.append(os.path.abspath(full))
    return files
