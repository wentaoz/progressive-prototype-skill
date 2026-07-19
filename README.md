# Progressive Prototype Skill

[中文](#中文) · [English](#english)

## 中文

`design-progressive-prototypes` 是一个公开 Codex Skill，用来解决 AI 产品原型常见的两个极端：细节太多，难以理解和修改；或者内容太少，关键流程和状态只能靠人脑补。

它采用一个简单原则：**结构完整，局部精细，按决策逐层展开。**

### 能做什么

- 从一句产品想法、PRD、需求说明或已有原型反馈开始。
- 先展示目标、范围、流程、页面和状态组成的最小完整骨架。
- 每轮最多提出三个高影响问题。
- 推荐 2–3 个最值得细化的页面，确认后才生成文本线框。
- 把结果保存为一个 Git diff 友好的 `PROTOTYPE.md`。
- 修改时追踪受影响的流程和页面，不重写无关部分。

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
Use $design-progressive-prototypes to turn this product idea into a progressively detailed prototype:
我想做一个帮助自由职业者追踪发票和催款的产品。
```

已有材料也可以直接使用：

```text
Use $design-progressive-prototypes to restructure this PRD into a complete prototype without over-designing it.
```

修改现有原型：

```text
Use $design-progressive-prototypes to remove mandatory sign-in from PROTOTYPE.md and show the affected flows before editing.
```

完整示例见 [`examples/appointment-booking/PROTOTYPE.md`](examples/appointment-booking/PROTOTYPE.md)。

### 边界

v0.1.0 不直接生成 Figma、React、HTML 或高保真视觉稿。它先把产品意图、流程、页面、状态和关键交互变成稳定的共享模型，再为后续设计或实现提供清晰输入。

## English

`design-progressive-prototypes` is a public Codex Skill for avoiding two common AI-prototyping extremes: output that is too detailed to understand and edit, or too sparse to evaluate without filling in the gaps yourself.

Its rule is simple: **complete in structure, detailed only where a decision needs it.**

### What it does

- Starts from a product idea, PRD, requirements note, or existing prototype feedback.
- Presents a minimum complete skeleton of goals, scope, flows, screens, and states.
- Asks no more than three high-impact questions per checkpoint.
- Recommends two or three screens for detail and waits for confirmation.
- Produces one Git-diff-friendly `PROTOTYPE.md` with Mermaid flows and editable text wireframes.
- Traces revision impact and keeps unrelated sections stable.

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
Use $design-progressive-prototypes to turn this idea into a complete, progressively detailed prototype.
```

See the complete example at [`examples/appointment-booking/PROTOTYPE.md`](examples/appointment-booking/PROTOTYPE.md).

### Current boundary

v0.1.0 does not directly generate Figma files, React, HTML, or high-fidelity visual design. It creates a stable product model that those downstream artifacts can use.

## Validation

```bash
python3 -m unittest discover -s tests -v
python3 skills/design-progressive-prototypes/scripts/validate_prototype.py --initial examples/appointment-booking/PROTOTYPE.md
```

## License

[MIT](LICENSE)
