#!/usr/bin/env python3
"""Batch-transcribe WhatsApp .opus voice messages via the OpenAI Whisper API.

Whisper does not accept .opus uploads, so each file is first converted to .ogg
with ffmpeg. Requires ffmpeg on PATH and OPENAI_API_KEY in the environment.

Usage:
    python transcribe_audio.py <folder> [<folder> ...] [--language pt] [--output transcriptions.json]
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from openai import OpenAI


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folders", nargs="+", help="Extracted chat folders containing .opus files")
    parser.add_argument("--language", default=None, help="ISO 639-1 language code, e.g. en, pt, es")
    parser.add_argument("--output", default="transcriptions.json", help="Output JSON path")
    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set", file=sys.stderr)
        return 1
    if shutil.which("ffmpeg") is None:
        print("ffmpeg not found on PATH", file=sys.stderr)
        return 1

    audio_files: list[Path] = []
    for folder in args.folders:
        audio_files.extend(sorted(Path(folder).glob("*.opus")))
    if not audio_files:
        print("No .opus files found in the given folders", file=sys.stderr)
        return 1

    client = OpenAI()
    results: dict[str, str] = {}
    for i, audio_path in enumerate(audio_files):
        key = f"{audio_path.parent.name}/{audio_path.name}"
        print(f"[{i + 1}/{len(audio_files)}] Transcribing {key}...")
        tmp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
                tmp_path = tmp.name
            subprocess.run(
                ["ffmpeg", "-y", "-i", str(audio_path), "-c:a", "libopus", tmp_path],
                capture_output=True,
                check=True,
            )
            with open(tmp_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=args.language,
                )
            results[key] = transcript.text
        except Exception as e:
            results[key] = f"ERROR: {e}"
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(results)} transcripts to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
