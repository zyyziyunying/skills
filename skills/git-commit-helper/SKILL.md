---
name: git-commit-helper
description: Git 提交助手。当用户要求提交代码、创建 commit 或整理提交时使用；默认规划原子提交边界，必要时拆分为多个 commit。
---

# Git 提交助手

## 适用范围

用户要求提交代码、创建或整理 commit 时使用。先规划原子边界；一次请求可以产生多个 commit。

## 工作流程

### 安全边界

- 本技能仅使用 `git status`、`git diff`、`git ls-files`、`git log`、`git add`、`git restore --staged` 和 `git commit`。验证命令必须已获用户任务或项目规则授权，且与当前提交直接相关。
- 不执行 `git push`、`git reset`、`git clean`、`git checkout`、`git switch`、`git rebase`、`git merge` 或 `git stash`；不修改远端、切换分支、重写历史或丢弃工作区内容。需要这些操作时停下说明。

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
目标不是把一次用户请求压成一个 commit，而是创建语义清晰、可回滚、可 review 的原子提交。提交前先判断提交边界；以下原子拆分规则是默认策略，用户明确要求单个 commit 时以其要求为准：

- 每个 commit 只包含一个逻辑目的；功能代码和对应测试通常放在一起。
- 纯格式化、依赖、生成文件和文档与功能/修复分开，除非不可分割；多个 bugfix、功能点、重构或行为变更混在一起时必须拆分。
- 已 staged 的内容也要检查是否混杂；如果 staged 内容不是一个原子变更，先说明当前 staged 状态、拟调整范围和原因。未经用户确认，不要改写用户已有 index。
- 不要为了减少 commit 数合并无关改动。
- 如果用户明确要求单个 commit，遵循该要求；必要时简要说明合并多个主题的代价，不要求用户再次坚持。

根据检查结果形成提交计划：

- 如果只有一个清晰、原子的变更组，创建一个 commit。
- 如果有多个独立变更组且用户未要求单个 commit，列出 commit 顺序，并逐个 stage、commit。
- 如果边界无法可靠判断，先读取必要 diff；仍不清楚时停下询问，不要猜测提交。

只有在需要辨别细节时，才展开完整的 `git diff` 或 `git diff --cached`。

### 3. Stage 当前提交边界
按提交计划逐个准备 index：

- 如果已经有 staged 更改且它正好是当前原子提交，直接使用。
- 如果 staged 内容混杂，先说明当前 staged 状态和拟调整范围；只有用户确认后，才可用 `git restore --staged <path>` 把混杂内容退回工作区，再只 stage 当前提交需要的路径。
- 如果没有 staged 更改，优先只 stage 当前提交相关路径，不要默认全量 `git add .`。
- 如果同一个文件内包含当前提交范围之外的改动，只 stage 相关 hunk；无法可靠隔离范围时停下说明。用户要求单个 commit 且所有改动都在已授权范围内时，无需为拆分主题而拆分 hunk。
- 调整 index 时不得丢弃工作区内容，不得使用会删除或覆盖用户改动的命令。
- 每次提交前检查 staged 内容：
```bash
git diff --cached --stat
git diff --cached
```

### 4. 生成 Commit Message

分析当前 staged 内容，生成符合规范的 commit message：

**格式规范**：`type(scope): description`

**类型（type）**：按 staged 内容选最准确的 `feat`、`fix`、`refactor`、`docs`、`style`、`test`、`chore` 或 `perf`。

**作用域（scope）**：可选，表示影响的模块或组件

**描述（description）**：
- 使用中文
- 简洁明了，说明做了什么
- 第一行不超过 50 字符
- 如果变更包含 breaking change，可使用 `feat!` / `fix!`
- 如果需要正文，简要写出做了什么和为什么
- 默认不添加工具追踪标记；只有用户明确要求，或仓库提交规范已经要求类似标记时，才在正文中添加

### 5. 执行提交

根据提交计划逐个提交。提交前，只运行用户任务或项目规则已经授权、且与 staged 内容直接相关的必要轻量检查，例如静态分析、格式检查或相关测试。不要把触发本技能视为安装依赖、访问网络、构建产物或运行模拟器/设备的授权；需要新授权时停下说明。无法运行或被项目规则禁止的检查，应在最终说明中明确列出。

把 commit message 作为不经 shell 展开的字面文本传给 Git。不要把生成内容放进未加引号或双引号的 `-m` 参数，也不要使用命令替换、反引号、变量展开或 `eval`；消息可能包含来自文件名、代码或用户输入的 `$()`、反引号、`$VAR` 或单引号。

当执行工具只接受 shell 命令字符串时，优先用带**单引号分隔符**的 HEREDOC 写入 `git commit --file=-`。分隔符必须加单引号，并且不得作为消息中的独立一行出现：
```bash
git commit --file=- <<'CODEX_COMMIT_MESSAGE_EOF'
[生成的提交信息主题]

[可选的详细描述]
CODEX_COMMIT_MESSAGE_EOF
```

单引号分隔符会禁止 shell 对消息正文做命令、反引号和变量展开。若运行时提供结构化 argv 或字面 stdin 接口，也可以直接使用；不要自行拼接未经严格 shell escaping 的命令字符串。

如果有多个提交，完成一个 commit 后重新检查剩余 diff，再准备下一个提交边界。

### 6. 验证提交

每次提交后显示状态；全部提交完成后再显示最终状态和最新提交。最终回复中说明实际运行过的检查，以及因项目约束或环境限制未运行的检查：
```bash
git status --short
git log --oneline -1
```

## 注意事项

- 没有可提交内容时，不要强行生成 commit。
- 以项目近期历史对齐语气和粒度；重要变更可在正文交代背景，但不写实现流水账。
