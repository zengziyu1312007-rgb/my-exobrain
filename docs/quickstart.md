# 安装与第一次使用

需要一个支持 Skill 且能读写文件的 AI 助手。运行附带脚本时需要 Python 3.10+，不需要 pip 包、额外 API key 或后台服务。

## 下载

可用 GitHub 的 Code → Download ZIP，也可：

```bash
git clone https://github.com/zengziyu1312007-rgb/my-exobrain.git
cd my-exobrain
```

解压 ZIP 后，在解压目录打开终端或交给文件助手读取 README。下载项目与建立个人外脑是两个步骤。

## 安装

```bash
python3 scripts/install.py --target codex --dry-run
python3 scripts/install.py --target codex
```

Claude Code 将 `codex` 改成 `claude`。安装器只复制本项目完整技能并校验内容；同内容再次安装会返回 already-installed，不同内容则停止保留旧版。

自定义工具路径：`python3 scripts/install.py --dest /实际路径/skills/my-exobrain`。目标是完整技能目录，不是个人记录目录。不要只复制 SKILL.md，scripts、references、assets 也需要保留。

不运行安装器也可手工复制 `skills/my-exobrain` 整个文件夹到工具的技能目录。更新时先检查旧版是否有自定义内容，备份后再有意识地替换，安装器不会强制覆盖。

安装路径依据：[Codex](https://learn.chatgpt.com/docs/build-skills)、[Claude Code](https://code.claude.com/docs/en/skills)，核查于 2026-10-12。安装脚本已测试，两个产品里的自动触发和版本差异仍需使用者实测。

## 空白初始化与个性化

```bash
python3 skills/my-exobrain/scripts/init_brain.py ~/my-exobrain --mode both --dry-run
python3 skills/my-exobrain/scripts/init_brain.py ~/my-exobrain --mode both
```

然后在 `~/my-exobrain` 打开文件助手，按 README 的启动话术开始访谈。脚本不向你提问，也不写个人背景；个性化由助手在获准后完成。

已有外脑就直接让助手读原规则和索引，保留已有结构。不要重跑脚本覆盖，也不需要迁移整个历史目录。要从工作扩展到生活时补必要目录和索引即可。

## Windows

使用 `py -3` 替代 `python3`，路径可按实际目录填写：

```powershell
py -3 scripts/install.py --target codex
py -3 skills/my-exobrain/scripts/init_brain.py "$env:USERPROFILE/my-exobrain" --mode work
```

脚本采用跨平台路径处理；本次未在 Windows 真机验收。Unix 系统的符号链接路径需使用实际路径。

## 找不到技能或记忆

- 技能未出现：检查 SKILL.md 的位置，确认完整文件夹已复制，新开会话或重启工具。
- 新会话不知道你：确认打开的是个人外脑目录，并明确要求读取 AGENTS.md、索引和当前重点；不保证所有工具自动加载。
- 提示目标非空：这是保护已有内容；直接在原目录继续使用，或选一个新空目录。
- 提示 Git 工作区：选源码仓库之外的本地目录。初始化器不提供强制绕过选项。
- 想用手机：可查看或手动编辑 Markdown；本项目尚无手机专用应用或自动同步服务。
