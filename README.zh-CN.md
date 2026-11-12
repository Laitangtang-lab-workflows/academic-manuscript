# academic-manuscript

**AI 辅助手稿管线的总入口：六站流程（写作→标记→翻译→引用→净本→出稿）加实测的 .md 手稿格式规范与对齐 ISO 的数学排版规范，配符号登记表审计脚本。**

> [!NOTE]
> 本仓**全部内容由 AI 维护**，人类定方向、做决策，详见 [AI 维护声明](#ai-维护声明)。英文说明见 [README.md](README.md)。

## 解决什么问题

AI 进入手稿流程后，混乱来得很容易：交付稿里留着标记、各节符号字形不一致、引用键悬空、"终稿"存了三个版本。本 skill 是让整条管线保持诚实的唯一入口：

- **六站一站到底、正本唯一**：工作语言起草 → 标记加工（生成/改写/扩/缩/查证）→ 三遍法翻译 → 引用编号加生成文献列表 → 清标记出净本 → Word 出稿。.md 文件是唯一入库物，下游全部可再生
- **零标记交付闸门**：终稿必须全文扫描无任何标记残留——残留即事故，不是警告
- **对齐 ISO 80000 的数学排版规范**：标量斜体、矢量粗斜体、张量粗正体、无量纲数与微分正体、下标字形随类别，边界情形有既定裁定、示例可查
- **符号登记表加审计脚本**：符号字形先登记再使用；`symbol_audit.py` 报未登记、字形不符与 `\text` 残留（报告不代改），还能从既有手稿再生登记表骨架
- **手稿 .md 本身的格式规范**：文头块、章节结构、出稿时剥离的作者提示标题、图源可再生、每稿自持的 RIS 引用池

本 skill 只登记接口；实现住在配套 skill（标记管线 = academic-markup，docx 版式 = word-standards，文献符号 = lit-symbol-translation，文献库 = note-gen）。

## skill 安装

```
git clone https://github.com/Laitangtang-lab-workflows/academic-manuscript ~/.agents/skills/academic-manuscript
```

兼容一切支持 SKILL.md 约定的 agent 框架；审计脚本需 Python 3。

## 仓库结构

| 路径 | 内容 |
|---|---|
| `SKILL.md` | skill 入口：铁律、六站、格式规范、数学速查 |
| `references/math-typesetting.md` | 数学排版规范全文 |
| `references/manuscript-dir-agents.md` | 手稿区 AGENTS.md 模板 |
| `scripts/symbol_audit.py` | 符号登记审计（只报告）与登记表骨架生成 |

## AI 维护声明

本仓全部内容（代码、文档、本 README）由 AI 会话在人类监督下编写与更新。这条管线之所以存在，正因 AI 会话是这些手稿的主笔，规则是它们给自己写的护栏。提交均由机器生成，人类把关方向与决策，不逐行审码。

## 证书

[CC0-1.0](LICENSE)——公有领域贡献。可任意使用、fork、并入任何项目，无须署名（注明出处是善意但非义务）。

提交 PR 即表示同意你的贡献同样以 CC0 贡献。
