# Progressive Prototype Skill

[中文](#中文) · [English](#english)

## 中文

`design-progressive-prototypes` 是一个公开 Codex Skill，用来解决 AI 产品原型常见的两个极端：细节太多，难以理解和修改；或者内容太少，关键流程和状态只能靠人脑补。

它采用一个简单原则：**结构完整，局部精细，按决策逐层展开。** 同一个 `PROTOTYPE.md` 可以继续生成原生可编辑 Figma 或 Pencil `.pen` 文件。

### 能做什么

- 从一句产品想法、PRD、需求说明或已有原型反馈开始。
- 先确认目标、范围、流程、页面和状态组成的最小完整骨架。
- 每轮最多提出三个高影响问题，只细化确认过的 2–3 个页面。
- 输出 Git diff 友好的 `PROTOTYPE.md`、原生 Figma 或 Pencil `.pen`。
- Figma 使用独立 Frame、Auto Layout、Text、组件实例、Variant、变量和原生交互，不交付整屏截图或单一 Vector。
- Pencil 使用独立节点、reusable nodes/refs 和变量，并通过 `--in` 基于旧文件局部迭代。
- 修改时按 `F-##`、`S-##` 追踪影响，不重写无关页面，也不覆盖无冲突的人工视觉调整。

### 输出策略

| 输出 | 默认行为 |
|---|---|
| Document | 完整结构、Mermaid 流程、状态矩阵和文本线框 |
| Figma | 所有页面保留独立骨架，确认页面达到中保真，核心流程和关键异常可点击 |
| Pencil | 与 Figma 相同的渐进式覆盖，保存 `.pen` 和 PNG 预览 |

视觉文件默认优先复用已有设计系统；目标文件没有合适组件时，才创建最小本地组件和变量。

### 安装

让 Codex 使用内置技能安装器：

```text
Use $skill-installer to install the skill from
https://github.com/wentaoz/progressive-prototype-skill/tree/main/skills/design-progressive-prototypes
```

也可以手动克隆后复制技能目录：

```bash
git clone https://github.com/wentaoz/progressive-prototype-skill.git
cp -R progressive-prototype-skill/skills/design-progressive-prototypes ~/.codex/skills/
```

重新启动 Codex 后即可调用：

```text
Use $design-progressive-prototypes to turn this idea into an editable Figma prototype:
我想做一个帮助自由职业者追踪发票和催款的产品。
```

生成 Pencil：

```text
Use $design-progressive-prototypes to turn PROTOTYPE.md into an editable Pencil prototype.
```

局部修改现有 Figma：

```text
Use $design-progressive-prototypes to remove mandatory sign-in from PROTOTYPE.md and this Figma file. Show the affected flows first and preserve unrelated manual visual changes.
```

完整语义示例见 [`examples/appointment-booking/PROTOTYPE.md`](examples/appointment-booking/PROTOTYPE.md)。

### 工具要求

- Figma 输出需要已连接且具有编辑权限的 Figma MCP。
- Pencil 输出需要已安装并登录的 Pencil CLI；连接 Pencil Desktop/MCP 后可进行原生结构校验。
- 工具不可用时，Skill 会说明原因并提供其他输出选项，不会静默换格式。

## English

`design-progressive-prototypes` is a public Codex Skill for avoiding two common AI-prototyping extremes: output that is too detailed to edit or too sparse to evaluate.

Its rule is simple: **complete in structure, detailed only where a decision needs it.** A shared `PROTOTYPE.md` can produce native editable Figma or Pencil `.pen` designs.

### What it does

- Starts from an idea, PRD, requirements note, or existing prototype feedback.
- Confirms a minimum complete skeleton of goals, scope, flows, screens, and states.
- Asks no more than three high-impact questions and details only two or three confirmed screens initially.
- Produces `PROTOTYPE.md`, native Figma, or Pencil `.pen` output.
- Keeps Figma screens as separate Frames using Auto Layout, Text, Instances, Variants, Variables, and native reactions—never a whole-screen bitmap or vector.
- Keeps Pencil screens as separate nodes with reusable nodes/refs and variables, then revises through `--in`.
- Traces revisions through stable `F-##` and `S-##` IDs while preserving unrelated manual visual changes.

### Install

Ask Codex to use its built-in installer:

```text
Use $skill-installer to install the skill from
https://github.com/wentaoz/progressive-prototype-skill/tree/main/skills/design-progressive-prototypes
```

Or clone and copy it manually:

```bash
git clone https://github.com/wentaoz/progressive-prototype-skill.git
cp -R progressive-prototype-skill/skills/design-progressive-prototypes ~/.codex/skills/
```

Restart Codex, then invoke it explicitly:

```text
Use $design-progressive-prototypes to turn this product idea into an editable Figma prototype.
```

For Pencil:

```text
Use $design-progressive-prototypes to turn PROTOTYPE.md into an editable Pencil prototype.
```

See the complete semantic example at [`examples/appointment-booking/PROTOTYPE.md`](examples/appointment-booking/PROTOTYPE.md).

### Requirements

- Figma output requires a connected Figma MCP with edit access.
- Pencil output requires an installed and authenticated Pencil CLI; Pencil Desktop/MCP enables native structural validation.
- If a target is unavailable, the Skill explains the missing prerequisite and offers another target instead of silently substituting one.

## Validation

```bash
python3 -m unittest discover -s tests -v
python3 skills/design-progressive-prototypes/scripts/validate_prototype.py --initial examples/appointment-booking/PROTOTYPE.md
```

## License

[MIT](LICENSE)
