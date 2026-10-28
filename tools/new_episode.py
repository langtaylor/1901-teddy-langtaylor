#!/usr/bin/env python3
"""Create a Taylor Lang episode from templates/episode-base.

Examples:
  python tools/new_episode.py 2
  python tools/new_episode.py next
"""

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "episode-base"
EPISODES = ROOT / "episodes"
MAX_EPISODE = 1000
TEXT_EXTENSIONS = {".md", ".yaml", ".yml", ".json", ".txt"}


def episode_path(number: int) -> Path:
    hundred_start = ((number - 1) // 100) * 100 + 1
    ten_start = ((number - 1) // 10) * 10 + 1
    return (
        EPISODES
        / f"{hundred_start:04d}-{hundred_start + 99:04d}"
        / f"{ten_start:04d}-{ten_start + 9:04d}"
        / f"EP{number:04d}"
    )


def existing_episode_ids() -> set[int]:
    """Include old flat folders so they cannot accidentally be duplicated."""
    ids: set[int] = set()
    if not EPISODES.exists():
        return ids
    for path in EPISODES.rglob("EP[0-9][0-9][0-9][0-9]"):
        if path.is_dir():
            ids.add(int(path.name[2:]))
    return ids


def prepare_metadata(target: Path, number: int) -> None:
    episode_id = f"EP{number:04d}"
    replacements = {
        "{{EPISODE_ID}}": episode_id,
        "{{EPISODE_NUMBER}}": str(number),
        "EP0000": episode_id,
    }
    for file in target.rglob("*"):
        if not file.is_file() or file.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            original = file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = original
        for source, replacement in replacements.items():
            updated = updated.replace(source, replacement)
        if updated != original:
            file.write_text(updated, encoding="utf-8")

    yaml_file = target / "episode.yaml"
    if yaml_file.exists():
        content = yaml_file.read_text(encoding="utf-8")
        id_line = re.compile(r"^id\s*:\s*.*$", flags=re.MULTILINE)
        if id_line.search(content):
            content = id_line.sub(f"id: {episode_id}", content, count=1)
        else:
            content = f"id: {episode_id}\n" + content
        yaml_file.write_text(content, encoding="utf-8")
    else:
        yaml_file.write_text(f"id: {episode_id}\nstatus: draft\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Taylor Lang episode directory")
    parser.add_argument("episode", help="Episode number 1–1000, or 'next'")
    args = parser.parse_args()

    if not TEMPLATE.is_dir():
        parser.error(f"템플릿 폴더가 없습니다: {TEMPLATE}")

    existing = existing_episode_ids()
    if args.episode.lower() == "next":
        number = next((n for n in range(1, MAX_EPISODE + 1) if n not in existing), None)
        if number is None:
            parser.error("EP0001~EP1000이 모두 존재합니다.")
    else:
        try:
            number = int(args.episode)
        except ValueError:
            parser.error("에피소드 번호는 1~1000의 정수 또는 next여야 합니다.")
        if not 1 <= number <= MAX_EPISODE:
            parser.error("에피소드 번호는 1~1000이어야 합니다.")

    destination = episode_path(number)
    if number in existing or destination.exists():
        parser.error(f"EP{number:04d}가 이미 존재합니다. 기존 파일은 덮어쓰지 않습니다.")

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(TEMPLATE, destination)
    prepare_metadata(destination, number)
    print(f"생성 완료: {destination.relative_to(ROOT)}")
    print(f"에피소드 ID: EP{number:04d}")


if __name__ == "__main__":
    main()
