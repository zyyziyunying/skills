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
    goal = value.strip()
    if not goal:
        raise ValueError("goal must not be empty")
    if "\n" in goal or "\r" in goal:
        raise ValueError("goal must be a single sentence without line breaks")
    if len(goal) > 140:
        raise ValueError("goal must be concise, ideally no more than 140 characters")
    goal_without_inner_dots = re.sub(r"(?<=\w)\.(?=\w)", "", goal)
    sentence_endings = re.findall(r"[。！？.!?]", goal_without_inner_dots)
    if len(sentence_endings) > 1:
        raise ValueError("goal must be one sentence; found multiple sentence endings")
    return goal


def validate_slug(value: str) -> str:
    slug = value.strip()
    if not slug:
        raise ValueError("slug must not be empty")
    if slug != slug.lower():
        raise ValueError("slug must use lowercase letters, digits, and hyphens only")
    if len(slug) > 64:
        raise ValueError("slug must be 64 characters or fewer")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)+", slug):
        raise ValueError(
            "slug must be kebab-case with at least three semantic words, "
            "for example subscription-global-analytics"
        )
    words = slug.split("-")
    if not 3 <= len(words) <= 8:
        raise ValueError("slug must contain 3 to 8 semantic words")
    if any(len(word) < 2 for word in words):
        raise ValueError("slug words must be at least 2 characters long")
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
      <p>草稿：待补充当前状态、关键结论、下一步和阻塞问题。</p>
    </section>

    <section>
      <h2>Research 摘要</h2>
      <ul>
        <li>待补充：事实、现状、约束、未知点和证据来源。</li>
      </ul>
    </section>

    <section>
      <h2>Design 决策</h2>
      <ul>
        <li>待补充：选定方案、边界、取舍和被放弃的方案。</li>
      </ul>
    </section>

    <section>
      <h2>Check 验收标准</h2>
      <ul>
        <li><strong>可观察行为：</strong>待补充外部可观察的完成标准、反例、边界和不变量。</li>
        <li><strong>正确性来源：</strong>待补充定义预期行为的事实源、契约、规则或用户确认；不得以当前实现作为唯一依据。</li>
        <li><strong>验证等级：</strong>待补充 L1 / L2 / L3 及理由。</li>
        <li><strong>开发性验证：</strong>待补充开发 Agent 应执行的单元测试、静态检查或局部验证。</li>
        <li><strong>独立验证：</strong>待补充独立测试、Review、E2E、设备或人工证据；若不需要，说明理由。</li>
        <li><strong>完成门槛（待验证）：</strong>待补充哪些结果足以标记 done；验证完成后再记录实际证据。bug 修复还需记录预期的修复前失败信号。</li>
      </ul>
    </section>

    <section>
      <h2>Plan 执行计划</h2>
      <ul>
        <li>待补充：按验收标准拆出的执行步骤。</li>
      </ul>
    </section>

    <section>
      <h2>Problem 记录</h2>
      <ul>
        <li>暂无。问题可以来自任意阶段，记录当前状态和最终结论。</li>
      </ul>
    </section>

    <section>
      <h2>关联文档</h2>
      <ul>
        <li>暂无。若添加 evidence/、assets/ 或 archive/ 材料，在这里链接并用一句话说明内容；当前结论仍保留在 goal.html。</li>
      </ul>
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
            "Lowercase semantic kebab-case folder slug, 3 to 8 words, "
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
    parser.add_argument("goal", help="One-sentence goal.")
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
