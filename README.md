---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 550c777a310fec68d053917dc686d83d_13e81dd2b7eb11f183c452540024e231
    ReservedCode1: onMrkaAPsvsRfepYaVcFeGpdasn0ZpdU8Nk+ykKg/DYDDiCrro7Qepb4zT8WgjUBdn5wOA8a50/HceJd3uNni8OQJEOAiCxg56NdnvJ7F24JT6PDF6FaRchzTsjIKfmRXhxcwwGBei3y32FmXdQ+9CUDxbFUbA7uuqMhohE1FhgRl9Cb2NShina8eGE=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 550c777a310fec68d053917dc686d83d_13e81dd2b7eb11f183c452540024e231
    ReservedCode2: onMrkaAPsvsRfepYaVcFeGpdasn0ZpdU8Nk+ykKg/DYDDiCrro7Qepb4zT8WgjUBdn5wOA8a50/HceJd3uNni8OQJEOAiCxg56NdnvJ7F24JT6PDF6FaRchzTsjIKfmRXhxcwwGBei3y32FmXdQ+9CUDxbFUbA7uuqMhohE1FhgRl9Cb2NShina8eGE=
---



# pdf-nup

> 把 PDF 重排版为 **1-up / 2-up / 4-up**，并可加「本页/总页」页码角标 —— 为审计底稿、报告、合同的**省纸打印**而生。

一行命令把几百页底稿压成 4-up 双面打印；横版页、竖版页、`/Rotate` 旋转页混排时，页码逐页自动对准。**只读源文件，绝不修改原件。**

- 可作为 **Agent Skill** 使用（遵循 `SKILL.md` 规范，如 Marvis 自定义技能）
- 也可当**普通命令行脚本**跑，无需任何 Agent

```
            ┌─────────────┐                ┌───────┬───────┐
 4 页 A4 →  │  2-up 横向  │   = 1 张 A4    │ 4-up  │ 2×2   │ = 1 张 A4
            └─────────────┘                └───────┴───────┘
```

---

## 为什么需要它

直接打印 300 页底稿既费纸又费时；市面上的「N 页合一」工具常见三个问题：

| 常见痛点 | pdf-nup 的做法 |
|---|---|
| 并版后没有页码，打印出来对不上 | 可选页码角标「本页/总页码」，总页数按**输出**页数计算 |
| 横竖混排时页码跑到页面外或被裁掉 | 逐页按**该页自身方向**落位：横版页 → 右下角页脚并右旋 90°；竖版页 → 右上角页眉 |
| 输出会污染甚至覆盖源文件 | 全程只读源 PDF，输出另存新文件 |
| 尾页被补空白页，浪费纸 | 尾页留空，**不补空白页** |

---

## 特性

- **三种版式**：`1up`（单页单面，保持源页面原始尺寸与方向）/ `2up`（A4 横向并排）/ `4up`（2×2 网格，纵向/横向可选）
- **页码自动落位**：`--page-badge` 一键加「本页/总页码」，横竖混排自适应，无需人工指定
- **源文件只读**：不修改、不覆盖、不移动源 PDF
- **纯矢量绘制**：基于 PyMuPDF，输出不含任何水印文本
- **批量友好**：配合几行循环即可整目录处理（见下方示例）
- **可调角标**：字体、字号、边距、旋转角度均可通过参数覆盖

---

## 快速开始

### 方式 A：作为 Agent Skill（推荐，给 Agent 用）

把仓库塞进 Agent 的**自定义技能目录**：

```
%APPDATA%\Tencent\Marvis\User\<你的用户ID>\skills\custom\pdf-nup\
├── SKILL.md
├── meta.json
└── scripts\
    └── pdf_nup.py
```

> ⚠️ 目录名必须是 `pdf-nup`（GitHub 下载的 ZIP 解压后叫 `pdf-nup-main`，**需重命名**），装完**重启** Agent 才会被扫描到。

然后直接用自然语言：

> 把这份审计报告做成 4-up 省纸打印，记得加页码
> 这份 PDF 太长，帮我两页一版并排排版
> 把底稿目录里的 PDF 全部做成纵向 4-up 并版并加页码

详见 [INSTALL.md](INSTALL.md)。

### 方式 B：命令行使用

```bash
git clone https://github.com/yechuyi0122-jpg/pdf-nup.git
cd pdf-nup
python -m pip install -r requirements.txt

# 造一份合成示例 PDF（6 页，含横竖混排）
python examples/make_sample.py

# 4-up 纵向 + 页码
python scripts/pdf_nup.py --input examples/sample-input.pdf \
                          --output examples/out/sample-4up.pdf \
                          --layout 4up --orientation portrait --page-badge
```

---

## 三种版式怎么选

| 版式 | 输出尺寸 | 每张纸放几页 | 页码位置 | 适用 |
|---|---|---|---|---|
| `1up` | **沿用源页面尺寸**（逐页可不同） | 1 页 / 面 | 按每页自身方向：横版→右下页脚（右旋），竖版→右上页眉 | 不并版，但要**补页码/单页单面**输出 |
| `2up` | A4 横向 `842×595` | 2 页 / 面 | 右下角页脚，右旋 90° | 通用的省纸并版 |
| `4up` `portrait` | A4 纵向 `595×842` | 4 页 / 面 | 右上角页眉 | 最省纸，默认选项 |
| `4up` `landscape` | A4 横向 `842×595` | 4 页 / 面 | 右下角页脚，右旋 90° | 小字号底稿横向阅读 |

---

## 命令行参数

| 参数 | 必填 | 默认 | 说明 |
|---|---|---|---|
| `--input` | ✅ | — | 源 PDF 路径 |
| `--output` | ✅ | — | 输出 PDF 路径（目录不存在会自动创建） |
| `--layout` | ✅ | — | `1up` / `2up` / `4up` |
| `--orientation` | | `portrait` | 仅 `4up` 生效：`portrait` / `landscape`；`1up` 忽略此项 |
| `--page-badge` | | 关闭 | 加页码角标「本页/总页码」 |
| `--badge-font` | | `C:\Windows\Fonts\simsun.ttc` | 角标字体文件（`.ttf` / `.ttc`） |
| `--badge-size` | | `10` | 角标字号（pt） |
| `--badge-margin` | | `30` | 角标距右边缘（pt） |
| `--badge-baseline` | | `25` | 纵向页眉角标基线距顶部（pt） |
| `--badge-bottom` | | `12` | 横向页脚角标基线距底部（pt） |
| `--badge-rotate` | | `-90` | 横向页脚角标旋转角度（`-90` = 向右旋 90°） |

### 常用命令

```bash
# 1-up 单页单面 + 页码（横竖混排自动对准）
python scripts/pdf_nup.py --input 源.pdf --output 出.pdf --layout 1up --page-badge

# 2-up 横向并排 + 页码
python scripts/pdf_nup.py --input 源.pdf --output 出.pdf --layout 2up --page-badge

# 4-up 纵向 + 页码（最省纸）
python scripts/pdf_nup.py --input 源.pdf --output 出.pdf --layout 4up --orientation portrait --page-badge

# 4-up 横向 + 页码
python scripts/pdf_nup.py --input 源.pdf --output 出.pdf --layout 4up --orientation landscape --page-badge

# 非 Windows 或无宋体：换字体
python scripts/pdf_nup.py --input 源.pdf --output 出.pdf --layout 4up --page-badge --badge-font /usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc
```

### 批量处理整个目录

```python
import os, subprocess

SCRIPT = r"path/to/pdf-nup/scripts/pdf_nup.py"
SRC = r"D:\底稿"

for f in sorted(os.listdir(SRC)):
    if not f.lower().endswith(".pdf") or f.endswith("已调整.pdf"):
        continue
    out = os.path.join(SRC, f[:-4] + "已调整.pdf")
    subprocess.run(["python", SCRIPT, "--input", os.path.join(SRC, f),
                    "--output", out, "--layout", "4up",
                    "--orientation", "portrait", "--page-badge"], check=True)
```

> 批量操作建议先拿 1~2 个文件试点，确认效果后再全量跑。

---

## 页码角标规则

- **总页码 = 输出 PDF 的页数**：`1up` 等于源页数；`2up` = `ceil(源页数/2)`；`4up` = `ceil(源页数/4)`。
- **位置逐页按该页自身方向判定**（依据 `page.rect`，已包含 `/Rotate` 旋转后的可见尺寸）：
  - **横向页**（宽 > 高）→ **右下角页脚**，默认**向右旋转 90°**（`rotate=-90`，字头朝右、读序向下）。
  - **纵向页**（高 ≥ 宽）→ **右上角页眉**，不旋转。
- **1-up 混排自适应**：源文件里竖版页、横版页混排时，页码在每页各自落位，无需人工干预。

> ⚠️ **实现坑（PyMuPDF）**：`insert_text` 的 `rotate` 正角是**逆时针**，"向右旋"必须传 **-90**。旋转后文字自锚点**向下**延伸 `text_length`、字身向锚点**右侧**伸展约 `ascender × size`，所以锚点应写成
> `x = page_w - margin - ascender * size`、`y = page_h - bottom - text_length`，否则页码会旋出页面之外。

---

## 输出自检清单

生成后建议逐项核对（`SKILL.md` 中要求 Agent 强制自检）：

1. **尺寸**：`1up` 逐页等于源页 `rect`；`2up` = 842×595；`4up portrait` = 595×842；`4up landscape` = 842×595。
2. **页数**：`1up` = 源页数；`2up` = `ceil(源页数/2)`；`4up` = `ceil(源页数/4)`。
3. **角标朝向**：横向页角标 `dir` 应为 `(0,1)`（竖排），纵向页应为 `(1,0)`（横排）；bbox 必须落在页内。
4. **1-up 内容无损**：源页 `get_text()` 应包含于输出页 `get_text()`。
5. **源文件未被改动**（大小 / 修改时间不变）。
6. **无 AI 水印文本**：逐页检索文本层，不得出现「内容由AI生成」等字样。
7. **尾页留空**：不补空白页。

---

## 目录结构

```
pdf-nup/
├── README.md            # 本文档
├── INSTALL.md           # 安装说明（Agent Skill / 命令行两种方式）
├── LICENSE              # MIT
├── requirements.txt     # pymupdf
├── SKILL.md             # Agent Skill 主文件（含 name / description 触发词）
├── meta.json            # 技能元数据（显示名、版本、适用场景）
├── examples/
│   └── make_sample.py   # 生成合成示例 PDF（不含真实资料）
└── scripts/
    └── pdf_nup.py       # 核心脚本
```

---

## 常见问题

**Q：从 GitHub 下载的 ZIP 解压后目录名叫 `pdf-nup-main`，能直接用吗？**
不能。技能目录名必须与 `name` 一致，请重命名为 `pdf-nup`。

**Q：报错 `ModuleNotFoundError: No module named 'pymupdf'`**
`python -m pip install pymupdf`。注意本工具用 `import pymupdf`，**不是** `import fitz`。

**Q：非 Windows 环境，或系统没有宋体？**
用 `--badge-font` 指定本机已装字体，例如 Noto Sans CJK；不指定字体也能跑，只是角标用默认字体。

**Q：`1up` 输出怎么页数、尺寸和源文件一样？**
这是设计预期——`1up` 不缩放、不合并、不归一化，只做「补页码」，源文件混排 A4/A3 或横竖版时输出同样混排。

**Q：`1up` 输出页的 `rotation` 变成 0 了，是方向丢了吗？**
不是。`1up` 会把 `/Rotate` 旋转页**展平**（可见尺寸与源一致），避免打印时被二次旋转。

**Q：扫描件（无文本层）能加页码吗？**
能。角标是后绘制的矢量文字，与源文件是否有文本层无关；只是第 4 项文本类自检会失效，属预期。

**Q：加密 PDF 能处理吗？**
需先用密码解锁另存后再处理，本工具不做解密。

---

## 限制

- 不含 OCR，不改动源内容，不做页面旋转纠正、去空白页、裁剪等操作。
- `1up` 不做尺寸归一化（如需统一 A4，请用 `2up` / `4up`）。
- 页码格式固定为「本页/总页」，不支持自定义前后缀。

---

## License

[MIT](LICENSE) © 2026 yechuyi0122-jpg

如果这个工具帮你省下了几包打印纸，欢迎点个 Star。
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
