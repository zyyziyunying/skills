#!/usr/bin/env python3
"""Create ./goals/<date>-<semantic-slug>/goal.html under the current directory."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
from pathlib import Path
import re
import secrets
import shutil
import sys

DEFAULT_STATUS = "draft"
SHARED_CSS_HREF = "../_shared/goal.css"
SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSET_CSS = SKILL_ROOT / "assets" / "goal.css"


def validate_goal(value: str) -> str:
    goal = " ".join(value.split())
    if not goal:
        raise ValueError("goal must not be empty")
    return goal


def validate_slug(value: str) -> str:
    slug = value.strip()
    if not slug:
        raise ValueError("slug must not be empty")
    if slug != slug.lower():
        raise ValueError("slug must use lowercase letters, digits, and hyphens only")
    if len(slug) > 80:
        raise ValueError("slug must be 80 characters or fewer")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("slug must use lowercase kebab-case")
    return slug


def derive_title(goal: str) -> str:
    return re.sub(r"[。！？.!?]+$", "", goal).strip()


def unique_folder(root: Path, created: str, slug: str) -> Path:
    base = root / "goals" / f"{created}-{slug}"
    if not base.exists():
        return base
    for index in range(2, 100):
        candidate = root / "goals" / f"{created}-{slug}-{index}"
        if not candidate.exists():
            return candidate
    return root / "goals" / f"{created}-{slug}-{secrets.token_hex(3)}"


def ensure_shared_css(root: Path) -> tuple[Path, bool]:
    target = root / "goals" / "_shared" / "goal.css"
    if target.exists():
        if target.is_file():
            return target, False
        raise FileExistsError(f"shared CSS path exists but is not a file: {target}")
    if not ASSET_CSS.is_file():
        raise FileNotFoundError(f"bundled goal CSS asset is missing: {ASSET_CSS}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ASSET_CSS, target)
    return target, True


def build_html(title: str, goal: str, status: str, created: str) -> str:
    safe_title = html.escape(title)
    safe_goal = html.escape(goal)
    safe_status = html.escape(status)
    safe_created = html.escape(created)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{safe_title}</title>
  <link rel="stylesheet" href="{SHARED_CSS_HREF}">
</head>
<body>
  <main>
    <h1>{safe_title}</h1>
    <p class="goal-line"><strong>一句话目标：</strong>{safe_goal}</p>

    <div class="meta" aria-label="Goal metadata">
      <div><span class="label">状态</span>{safe_status}</div>
      <div><span class="label">创建日期</span>{safe_created}</div>
    </div>

    <section>
      <h2>当前状态</h2>
      <p>草稿：待补充当前结论、重要阻塞和下一步。按目标需要自由调整本页结构。</p>
    </section>

    <section>
      <h2>事实源与关联文档</h2>
      <ul>
        <li><code>goal.html</code>：目标、整体状态和文档路由。</li>
        <li>按需添加细分文档，并说明每份文档唯一负责的事实范围。</li>
      </ul>
    </section>

    <section>
      <h2>完成条件</h2>
      <p>待补充足以关闭此目标的可观察结果与验证证据；详细检查可由独立文档负责。</p>
    </section>

    <section>
      <h2>变更记录</h2>
      <ul>
        <li>{safe_created}: 创建 goal 文档。</li>
      </ul>
    </section>
  </main>
</body>
</html>
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create ./goals/<today>-<semantic-slug>/goal.html under the current "
            "directory. Usage: create_goal.py --slug SEMANTIC-SLUG GOAL."
        )
    )
    parser.add_argument(
        "--slug",
        required=True,
        help=(
            "Descriptive lowercase kebab-case folder slug, "
            "for example subscription-global-analytics."
        ),
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help=(
            "Print machine-readable creation metadata instead of only the "
            "goal.html path."
        ),
    )
    parser.add_argument("goal", help="Concise goal outcome.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        root = Path.cwd().resolve()
        created = dt.date.today().isoformat()
        status = DEFAULT_STATUS
        goal = validate_goal(args.goal)
        slug = validate_slug(args.slug)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    title = derive_title(goal)
    if not title:
        title = f"Goal {created}"

    folder = unique_folder(root, created, slug)
    target = folder / "goal.html"

    try:
        shared_css_path, shared_css_created = ensure_shared_css(root)
        folder.mkdir(parents=True, exist_ok=True)
        target.write_text(
            build_html(title, goal, status, created),
            encoding="utf-8",
        )
    except OSError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    if args.as_json:
        print(
            json.dumps(
                {
                    "goal_html_path": str(target),
                    "shared_css_path": str(shared_css_path),
                    "shared_css_created": shared_css_created,
                    "status": status,
                },
                ensure_ascii=False,
            )
        )
    else:
        print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
