#!/usr/bin/env python3
"""Create ./goals/<date>-<semantic-slug>/goal.html under the current directory."""

from __future__ import annotations

import argparse
import datetime as dt
import html
from pathlib import Path
import re
import secrets
import sys

DEFAULT_STATUS = "draft"


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
    title = re.sub(r"[。！？.!?]+$", "", goal).strip()
    if len(title) <= 28:
        return title
    return f"{title[:28]}..."


def unique_folder(root: Path, created: str, slug: str) -> Path:
    base = root / "goals" / f"{created}-{slug}"
    if not base.exists():
        return base
    for index in range(2, 100):
        candidate = root / "goals" / f"{created}-{slug}-{index}"
        if not candidate.exists():
            return candidate
    return root / "goals" / f"{created}-{slug}-{secrets.token_hex(3)}"


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
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f8fb;
      --panel: #ffffff;
      --text: #172033;
      --muted: #5f6b7a;
      --line: #d9e1ec;
      --accent: #255f85;
      --accent-soft: #e8f3f8;
    }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.62;
    }}
    main {{
      max-width: 980px;
      margin: 0 auto;
      padding: 48px 24px 72px;
    }}
    h1 {{
      margin: 0 0 12px;
      font-size: 34px;
      line-height: 1.18;
      letter-spacing: 0;
    }}
    h2 {{
      margin: 34px 0 12px;
      font-size: 22px;
      letter-spacing: 0;
    }}
    p, li {{
      font-size: 16px;
    }}
    ul {{
      padding-left: 22px;
    }}
    .goal-line {{
      margin: 0 0 18px;
      padding: 16px 18px;
      background: var(--accent-soft);
      border-left: 4px solid var(--accent);
      font-size: 18px;
    }}
    .meta {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
      margin: 20px 0 30px;
    }}
    .meta div, section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
    }}
    .label {{
      display: block;
      color: var(--muted);
      font-size: 13px;
      margin-bottom: 4px;
    }}
    a {{
      color: var(--accent);
    }}
  </style>
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
        <li>待补充：可观察的完成标准和验证方式。</li>
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

    folder.mkdir(parents=True, exist_ok=True)
    target.write_text(
        build_html(title, goal, status, created),
        encoding="utf-8",
    )
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
