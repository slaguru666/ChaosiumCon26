#!/usr/bin/env python3
"""
DALL-E 3 image generator for the Stormbringer MJ bridge queue.

Reads queued prompts from the mj_bridge queue.jsonl, generates images via
DALL-E 3, downloads them into the asset library, and marks jobs as done.

Usage:
    python3 scripts/dalle_generate.py --api-key sk-...
    python3 scripts/dalle_generate.py --api-key sk-... --limit 5
    python3 scripts/dalle_generate.py --api-key sk-... --quality hd
    python3 scripts/dalle_generate.py --api-key sk-... --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE = REPO_ROOT / "output" / "assets" / "midjourney" / "queue.jsonl"
DEFAULT_LIBRARY = REPO_ROOT / "output" / "assets" / "midjourney"
DEFAULT_PROJECT = "Stormbringer"


# ── Aspect ratio → DALL-E 3 size mapping ─────────────────────────────────────

AR_TO_SIZE: dict[str, str] = {
    "1:1":   "1024x1024",
    "2:3":   "1024x1792",
    "3:4":   "1024x1792",
    "9:16":  "1024x1792",
    "16:9":  "1792x1024",
    "3:2":   "1792x1024",
    "2:1":   "1792x1024",
}
DEFAULT_SIZE = "1792x1024"


def extract_ar(params: str) -> str:
    """Pull --ar value from a Midjourney param string and return DALL-E size."""
    match = re.search(r"--ar\s+(\d+:\d+)", params or "")
    if match:
        return AR_TO_SIZE.get(match.group(1), DEFAULT_SIZE)
    return DEFAULT_SIZE


def clean_prompt(prompt: str) -> str:
    """Strip Midjourney-specific flags that DALL-E doesn't understand."""
    cleaned = re.sub(r"--(?:ar|v|style|no|chaos|weird|tile|q|s|seed)\s*\S*", "", prompt)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip().rstrip(",")
    return cleaned


# ── Queue I/O ─────────────────────────────────────────────────────────────────

def read_queue(path: Path) -> list[dict]:
    if not path.exists():
        return []
    jobs = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                jobs.append(json.loads(line))
    return jobs


def write_queue(path: Path, jobs: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for job in jobs:
            fh.write(json.dumps(job, ensure_ascii=True, sort_keys=True) + "\n")


def append_index(library: Path, metadata: dict) -> None:
    index = library / "index.jsonl"
    index.parent.mkdir(parents=True, exist_ok=True)
    with index.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(metadata, ensure_ascii=True, sort_keys=True) + "\n")


# ── DALL-E 3 API call ─────────────────────────────────────────────────────────

# Size mapping for gpt-image-2
GI2_SIZE_MAP: dict[str, str] = {
    "1024x1024": "1024x1024",
    "1024x1792": "1024x1536",   # portrait
    "1792x1024": "1536x1024",   # landscape
}


def generate_image(
    api_key: str,
    prompt: str,
    size: str = "1792x1024",
    quality: str = "standard",
) -> bytes:
    """Call gpt-image-2 and return raw PNG bytes."""
    # Map legacy DALL-E sizes to gpt-image-2 sizes
    gi2_size = GI2_SIZE_MAP.get(size, "1536x1024")
    # Map quality: standard→medium, hd→high
    gi2_quality = "high" if quality == "hd" else "medium"

    payload = json.dumps({
        "model": "gpt-image-2",
        "prompt": prompt,
        "n": 1,
        "size": gi2_size,
        "quality": gi2_quality,
        "output_format": "png",
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error {exc.code}: {error_body}") from exc

    import base64
    b64 = body["data"][0]["b64_json"]
    return base64.b64decode(b64)


def download_image(image_bytes: bytes, dest: Path) -> None:
    """Write image bytes to dest."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(image_bytes)


# ── Slug / filename helpers ───────────────────────────────────────────────────

def slugify(value: str, max_len: int = 60) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug[:max_len] or "image"


def utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def compact_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


# ── Main generation loop ──────────────────────────────────────────────────────

def run(args: argparse.Namespace) -> int:
    jobs = read_queue(args.queue)
    queued = [j for j in jobs if j.get("status") == "queued"
              and j.get("project", DEFAULT_PROJECT) == args.project]

    if not queued:
        print("No queued prompts found for project:", args.project)
        return 0

    limit = args.limit if args.limit else len(queued)
    to_process = queued[:limit]

    project_dir = args.library / slugify(args.project)
    project_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {len(to_process)} image(s) via DALL-E 3 "
          f"[quality={args.quality}]")
    print(f"Output → {project_dir}\n")

    job_index = {j["id"]: j for j in jobs}
    generated = 0
    failed = 0

    for job in to_process:
        notes = job.get("notes", "")
        raw_prompt = job.get("prompt", "")
        params = job.get("midjourney_params", "")
        size = extract_ar(params)
        prompt = clean_prompt(raw_prompt)

        label = notes or job["id"]
        print(f"[{generated + 1}/{len(to_process)}] {label}")
        print(f"  size={size}  prompt={prompt[:80]}…")

        if args.dry_run:
            print("  [dry-run — skipped]\n")
            continue

        try:
            image_bytes = generate_image(args.api_key, prompt, size=size, quality=args.quality)

            filename = f"{compact_stamp()}_{slugify(notes or job['id'], 50)}.png"
            dest = project_dir / filename
            download_image(image_bytes, dest)

            sidecar = {
                "id": f"asset_{dest.stem}",
                "generated_at": utc_stamp(),
                "prompt_id": job["id"],
                "prompt": prompt,
                "raw_mj_prompt": raw_prompt,
                "asset_path": str(dest),
                "project": args.project,
                "notes": notes,
                "model": "gpt-image-2",
                "size": size,
                "quality": args.quality,

            }
            sidecar_path = dest.with_suffix(".json")
            sidecar_path.write_text(
                json.dumps(sidecar, indent=2, ensure_ascii=True, sort_keys=True),
                encoding="utf-8",
            )
            append_index(args.library, sidecar)

            job_index[job["id"]]["status"] = "done"
            job_index[job["id"]]["asset_path"] = str(dest)
            job_index[job["id"]]["generated_at"] = utc_stamp()

            print(f"  ✓ saved → {dest.name}\n")
            generated += 1

        except Exception as exc:
            print(f"  ✗ FAILED: {exc}\n", file=sys.stderr)
            job_index[job["id"]]["status"] = "error"
            job_index[job["id"]]["error"] = str(exc)
            failed += 1

        # Brief pause to stay inside OpenAI rate limits
        if generated < len(to_process):
            time.sleep(args.delay)

    write_queue(args.queue, list(job_index.values()))

    print(f"Done — {generated} generated, {failed} failed.")
    if failed:
        print("Failed jobs have status='error' in the queue. Re-run to retry.")
    return 0 if failed == 0 else 1


# ── CLI ───────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Generate queued Stormbringer prompts via DALL-E 3."
    )
    p.add_argument(
        "--api-key",
        default=os.environ.get("OPENAI_API_KEY", ""),
        help="OpenAI API key (or set OPENAI_API_KEY env var).",
    )
    p.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    p.add_argument("--library", type=Path, default=DEFAULT_LIBRARY)
    p.add_argument("--project", default=DEFAULT_PROJECT)
    p.add_argument("--quality", choices=["standard", "hd"], default="hd",
                   help="DALL-E 3 quality tier (default: hd).")
    p.add_argument("--limit", type=int, default=0,
                   help="Max images to generate (0 = all queued).")
    p.add_argument("--delay", type=float, default=3.0,
                   help="Seconds between API calls (default: 3).")
    p.add_argument("--dry-run", action="store_true",
                   help="Print what would be generated without calling the API.")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not args.api_key and not args.dry_run:
        print("Error: provide --api-key or set OPENAI_API_KEY.", file=sys.stderr)
        return 2
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
