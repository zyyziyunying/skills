---
name: git-commit-helper
description: Git 提交助手。当用户要求提交代码、创建 commit 或整理提交时使用；默认规划原子提交边界，必要时拆分为多个 commit。
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git ls-files:*), Bash(git log:*), Bash(git add:*), Bash(git restore:*), Bash(git commit:*)
---

# Git 提交助手技能

## 触发时机
- 用户说"提交代码"、"创建 commit"、"commit 一下"
- 用户说"帮我提交"、"提交这些改动"、"提交一下我的代码"
- 用户说"整理提交"、"拆分提交"、"按颗粒度提交"

## 工作流程

### 安全边界
- 只允许使用 frontmatter 中列出的 git 子命令。
- 不要执行 `git push`、`git reset`、`git clean`、`git checkout`、`git switch`、`git rebase`、`git merge`、`git stash` 等会发布、丢弃、移动或重写用户状态的命令。
- 不要自动修改远端、分支、历史或未提交的工作区内容；如果需要超出本技能权限的操作，停下并说明原因。

### 1. 检查工作区
先判断当前仓库是否适合提交，区分 staged、unstaged、untracked、冲突状态和正在进行的 rebase/merge：
```bash
git status --short --branch
git diff --cached --stat
git diff --stat
git ls-files --others --exclude-standard
git log --oneline -5
```

如果发现冲突、rebase 或 merge 进行中，先停下并说明原因，不要自行提交。

### 2. 制定提交计划
目标不是把一次用户请求压成一个 commit，而是创建语义清晰、可回滚、可 review 的原子提交。提交前必须先判断提交边界：

- 每个 commit 只包含一个逻辑目的。
- 功能代码和对应测试通常可以放在同一个 commit。
- 纯格式化、依赖更新、生成文件、文档更新应与功能/修复分开，除非它们是同一变更不可分割的一部分。
- 多个 bugfix、多个功能点、重构与行为变更混在一起时，必须拆分。
- 已 staged 的内容也要检查是否混杂；如果 staged 内容不是一个原子变更，先说明当前 staged 状态、拟调整范围和原因。未经用户确认，不要改写用户已有 index。
- 不要为了减少 commit 数合并无关改动。
- 如果用户明确要求单个 commit，但改动明显跨多个主题，先说明建议拆分；除非用户坚持，否则按原子提交执行。

根据检查结果形成提交计划：

- 如果只有一个清晰、原子的变更组，创建一个 commit。
- 如果有多个独立变更组，列出 commit 顺序，并逐个 stage、commit。
- 如果边界无法可靠判断，先读取必要 diff；仍不清楚时停下询问，不要猜测提交。

只有在需要辨别细节时，才展开完整的 `git diff` 或 `git diff --cached`。

### 3. Stage 当前提交边界
按提交计划逐个准备 index：

- 如果已经有 staged 更改且它正好是当前原子提交，直接使用。
- 如果 staged 内容混杂，先说明当前 staged 状态和拟调整范围；只有用户确认后，才可用 `git restore --staged <path>` 把混杂内容退回工作区，再只 stage 当前提交需要的路径。
- 如果没有 staged 更改，优先只 stage 当前提交相关路径，不要默认全量 `git add .`。
- 如果同一个文件内包含多个无关改动，优先只 stage 相关 hunk；无法可靠拆分时停下说明。
- 调整 index 时不得丢弃工作区内容，不得使用会删除或覆盖用户改动的命令。
- 每次提交前检查 staged 内容：
```bash
git diff --cached --stat
git diff --cached
```

### 4. 生成 Commit Message

分析当前 staged 内容，生成符合规范的 commit message：

**格式规范**：`type(scope): description`

**类型（type）**：
- `feat`: 新功能
- `fix`: 修复 bug
- `refactor`: 重构代码（不改变功能）
- `docs`: 文档更新
- `style`: 代码格式调整
- `test`: 测试相关
- `chore`: 构建/工具/依赖相关
- `perf`: 性能优化

**作用域（scope）**：可选，表示影响的模块或组件

**描述（description）**：
- 使用中文
- 简洁明了，说明做了什么
- 第一行不超过 50 字符
- 如果变更包含 breaking change，可使用 `feat!` / `fix!`
- 如果需要正文，简要写出做了什么和为什么
- 默认不添加工具追踪标记；只有用户明确要求，或仓库提交规范已经要求类似标记时，才在正文中添加

### 5. 执行提交

根据提交计划逐个提交。提交前在不违反项目规则的前提下运行必要的轻量检查，例如静态分析、格式检查或相关测试；如果项目规则禁止构建、运行、模拟器或设备验证，则不要执行这些命令，并在最终说明中明确未运行。

每个 commit 都使用 HEREDOC 格式执行：
```bash
git commit -m "$(cat <<'EOF'
[生成的提交信息主题]

[可选的详细描述]
EOF
)"
```

如果有多个提交，完成一个 commit 后重新检查剩余 diff，再准备下一个提交边界。

### 6. 验证提交

每次提交后显示状态；全部提交完成后再显示最终状态和最新提交。最终回复中说明实际运行过的检查，以及因项目约束或环境限制未运行的检查：
```bash
git status --short
git log --oneline -1
```

## Commit Message 示例

### 示例 1：重构
```
refactor(ai-pet): 提取调试信息到独立扩展

- 创建 controller_test_info.dart 处理调试信息
- 优化 scheduleNextActivity 同步机制
- 删除废弃的注释代码
```

### 示例 2：修复 bug
```
fix(scheduling): 解决活动切换时信息不同步问题

使用 pendingActivity 机制确保活动信息与实际播放状态同步
```

### 示例 3：新功能
```
feat(pet-controller): 添加活动关系可视化展示

在调试信息中显示当前活动的所有可能过渡关系
```

## 注意事项

- 没有可提交内容时，不要强行生成 commit
- 优先遵循项目已有的 commit message 风格；最近几条历史提交仅用于对齐语气和粒度
- 保持提交原子化，一次只做一件事
- 一次用户请求可以产生多个 commit；commit 数量由变更边界决定，不由用户请求次数决定
- 重要更改可在正文说明背景，但不要把实现细节写成流水账
