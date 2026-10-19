# 我的外脑 · My Exobrain

**把经历留下来，让 AI 下次接着帮你做事。**

一个中文优先、以本地 Markdown 文件为基础的开源 Skill。用几句对话认识你的当下需求，完成第一件真实任务，再逐步积累背景、知识、经验与方法。

由 **Peter 玩 AI** 发起 · MIT License · v0.1.0

## 直接复制完整提示词

不安装 Skill 也可以开始：[个人 AI 外脑｜初始化提示词完整版](skills/my-exobrain/references/initialization-prompt.md)。复制其中“提示词开始”到“提示词结束”之间的全部内容给 AI，不需要先填写个人资料。

有文件读写能力时，在自己准备的独立外脑目录里使用；只有聊天能力时，先让 AI 生成待保存文本，再自行保存，下次提供相关文件。已有外脑沿用原结构，不重新初始化。

完整版提示词与 Skill 共用协作原则，文件布局可以不同。[两套布局如何对应](docs/quickstart.md#提示词与-skill-的文件对应)。2026-10-19 的提示词与协作规则更新已进入 main；旧的 v0.1.0 Release 附件仍是原发布版，需要本次更新请下载 [main 最新 ZIP](https://github.com/zengziyu1312007-rgb/my-exobrain/archive/refs/heads/main.zip)。[本次更新说明](docs/update-2026-10-19.md)。

## 从生活或工作开始

| 方向 | 它帮你留下什么 | 你可以这样说 |
|---|---|---|
| 生活成长 | 学习的实际应用、选择依据、小行动和成长反馈 | “我想学点东西，但总学完就忘，先帮我用起来。” |
| 工作成长与效率 | 项目信息、个人贡献、能力证据、可复用流程 | “帮我整理这周的工作，再留下能用于月度回顾的成长记录。” |
| 两者都有／暂不区分 | 围绕眼前的事组合需要的模块 | “我先说最近最头疼的一件事，你帮我一起理清楚。” |

工作用户也可以聊生活，生活用户也可以做周报。方向随需求调整，不需要重新建一个外脑。

## 三步开始

### 1. 下载并安装 Skill

下载 [项目 ZIP](https://github.com/zengziyu1312007-rgb/my-exobrain/archive/refs/heads/main.zip)，解压后将文件夹交给你的 AI 文件助手，说：

> 请阅读这个项目的 README.md，把 skills/my-exobrain 完整安装到我的技能目录，包含 scripts、references 和 assets。保留已有同名技能，不覆盖。先安装技能，实际外脑记录放在另一个本地文件夹。

Codex 用户也可以直接发送：

> 用 $skill-installer 安装 https://github.com/zengziyu1312007-rgb/my-exobrain 中 skills/my-exobrain 这个技能。

需要手动安装时，在解压后的项目目录运行，要求 Python 3.10+：

```bash
# Codex：默认装到 ~/.agents/skills/my-exobrain
python3 scripts/install.py --target codex

# Claude Code：默认装到 ~/.claude/skills/my-exobrain
python3 scripts/install.py --target claude
```

两条选择适合自己的即可。技能未出现时新开会话或重启工具。[详细说明与 Windows 用法](docs/quickstart.md)。

### 2. 一句话初始化自己的外脑

在支持 Skill 且能读写本地文件的 AI 助手里发送：

```text
请用 my-exobrain 帮我初始化自己的外脑，放到 ~/my-exobrain。
工作、学习、生活和创作可以一起使用，不需要我先选类型。
从我现在最想做成的一件事开始，一次问一个必要问题。
先约定哪些内容可以保存，再完成第一件真实任务。
```

Codex 可显式用 `$my-exobrain`，Claude Code 可用 `/my-exobrain`。不必先填完整履历，不需要交代不愿记录的隐私。

也可先生成空白文件夹：

```bash
python3 skills/my-exobrain/scripts/init_brain.py ~/my-exobrain --mode life
```

`--mode` 支持 `life`、`work`、`both`、`auto`。加 `--dry-run` 可只预览。脚本只生成空白底稿，已有目录非空就停止，不覆盖旧记录。

### 3. 下次打开自己的外脑，继续做事

在 `~/my-exobrain` 打开文件助手，发送：

> 读取 AGENTS.md、00_入口/资料索引.md 和 00_入口/当前重点.md，再继续帮我做今天的任务。只读本次需要且获准的资料。

背景有误可以直接纠正；想记录就说“这条记下来”；只想聊就说“这次不记”。约定过的保存类别持续有效，不用每条重新批准。

## 外脑长什么样

```text
my-exobrain/                 ← 你自己的本地记录，与公开源码分开
├── AGENTS.md                协作与读取规则
├── CLAUDE.md                指向同一套规则的入口
├── 00_入口/
│   ├── 协作约定.md           怎样帮你，哪些可以记
│   ├── 我的背景.md           你确认且允许保存的背景
│   ├── 当前重点.md           眼下在做什么、下一步是什么
│   ├── 经验与原则.md         实际积累的经验
│   ├── 资料索引.md           资料在哪里、何时使用
│   └── 确认与变化.md         纠错、决定与变化
├── 10_生活/                 选生活或两者兼用时启用
└── 20_工作/                 选工作或两者兼用时启用
```

`auto` 先不生成方向目录；项目、日记、流程等按实际需要再增加。已有外脑会优先复用原结构。

## 日常可以这样用

- **做事**：“根据我的时间限制，把这个目标拆成明天能做的一步。”
- **积累**：“这次工作里的个人贡献和新学到的方法，帮我记下来。”
- **找回**：“上次为什么决定这样做？请告诉我依据在哪。”
- **复盘**：“按已有记录回顾这周，哪些有效，下一步调整什么？”
- **纠错**：“这个安排从下周开始改了，更新当前重点和相关记录。”
- **控制记忆**：“这段只用于本次对话。”／“删除我指定的这条记录。”

看两个[虚构使用示例](examples/scenarios.md)。

## 数据留在哪里

开源仓库只包含技能、空白模板、脚本和虚构示例，不收集使用者的记录。附带脚本不联网、不调用模型、不上传、不创建 Git 仓库；实际内容默认保存在独立本地目录。

初始化会拒绝 Git 工作区，并生成默认忽略实际记录的 `.gitignore`。这些措施帮助减少误提交，**不提供加密、访问控制或模型服务端保密保证**。你使用的 AI、云盘和同步工具仍可能处理文件；公司资料要先确认权属与允许用途。[数据与使用边界](docs/privacy.md)。

## 适用环境与当前范围

Skill 可安装到 Codex、Claude Code 等支持 `SKILL.md` 的文件助手。普通聊天窗口可照流程交流，但没有文件工具时无法替你持久化或跨会话读取。Python 脚本仅用标准库；AI 工具自己的账户与使用费用另计。

v0.1.0 已验证初始化、安装、旧数据保护及独立打包；main 的提示词更新见更新说明。真实用户的长期使用效果、不同工具中的自动触发仍需实践。它目前是个人文件工作流，未提供后台自动运行、企业多人权限或专用手机 App。[验证范围](docs/validation.md)。

## 参与与设计

- [设计说明](docs/design.md)：统一入口、两条成长线与初始化节奏。
- [贡献指南](CONTRIBUTING.md)：提交改进与复现问题，使用虚构或脱敏数据。
- [行为验收场景](evals/scenarios.md)：检查是否尊重已有背景、未知与保存范围。
- [MIT License](LICENSE)：允许使用、修改与再分发，保留许可声明。

本项目的目录与安装路径参考 [OpenAI Skills 官方文档](https://learn.chatgpt.com/docs/build-skills) 和 [Claude Code Skills 官方文档](https://code.claude.com/docs/en/skills)，核查日期 2026-10-12；工具版本与设置可能影响加载方式。
