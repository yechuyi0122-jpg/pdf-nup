---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 550c777a310fec68d053917dc686d83d_34429184b34311f1b20d52540024e231
    ReservedCode1: b9dHHIVu7DPap9GqM92q4Rb/hK5ETz7Dmr3Z85wqgbZeis1r+eXTcWILN1P3KABLVrKsIQPc4uzWX1Pzr7JuhXIsFdEObbdzRUaleLw8r1glOBTA6H+0mlr0i+5d/DASmRm1U1iQo8q+nF1AppNqO1coKrYXDpDXtvpPZ7gV8PVVwrJC192ZjH9GzmY=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 550c777a310fec68d053917dc686d83d_34429184b34311f1b20d52540024e231
    ReservedCode2: b9dHHIVu7DPap9GqM92q4Rb/hK5ETz7Dmr3Z85wqgbZeis1r+eXTcWILN1P3KABLVrKsIQPc4uzWX1Pzr7JuhXIsFdEObbdzRUaleLw8r1glOBTA6H+0mlr0i+5d/DASmRm1U1iQo8q+nF1AppNqO1coKrYXDpDXtvpPZ7gV8PVVwrJC192ZjH9GzmY=
name: pdf-nup
description: 把 PDF 重排版为 1-up（单页单面）/ 2-up（A4 横向并排）/ 4-up（2×2 网格），可选加「本页页码/总页码」角标。凡涉及 PDF 并版、缩排、省纸打印、补/标页码、底稿与报告打印排版的请求，均使用本技能。
---



# PDF 并版技能（pdf-nup）

把一份 PDF 重排版为 **1-up（单页单面，不缩小）**、**2-up（A4 横向并排）** 或 **4-up（2×2 网格）**，可选在每页加「本页页码/总页码」角标。专用于审计报告/底稿批量打印省纸场景。

三种布局的取舍：
- **1-up**：一页对一页、单面输出，**保持源页面原始尺寸与方向**（含 `/Rotate` 旋转页），只做「补页码」不做缩减——适合需要页码、但不并版的原件输出。
- **2-up / 4-up**：把多页缩排到一张 A4 上省纸打印。

**核心约束：仅读取源 PDF，绝不修改、覆盖、移动源文件。**

---

## 一、环境与依赖

- 依赖：`pymupdf`（`import pymupdf`，非 `fitz`）
- 缺失时自行安装，不要要求用户手动装：

```bash
python -m pip install pymupdf
```

- 角标默认字体为系统宋体 `C:\Windows\Fonts\simsun.ttc`。非 Windows 或无宋体时，用 `--badge-font` 指定任意 `.ttf/.ttc` 路径；不指定字体也能跑，只是用默认字体。

---

## 二、脚本位置与用法

脚本已随本技能提供：

```
<skill_dir>/scripts/pdf_nup.py
```

调用方式（把 `<skill_dir>` 换成实际绝对路径）：

```bash
# 1-up（单页单面，保持源页面尺寸与方向）+ 页码角标 → 页码按每页自身方向自动落位
python "<skill_dir>/scripts/pdf_nup.py" --input 源.pdf --output 出.pdf --layout 1up --page-badge

# 2-up（A4 横向并排）+ 页码角标 → 横版页码落在右下角页脚并向右旋 90°
python "<skill_dir>/scripts/pdf_nup.py" --input 源.pdf --output 出.pdf --layout 2up --page-badge

# 4-up 纵向 + 页码角标 → 页码落右上角页眉（不旋转）
python "<skill_dir>/scripts/pdf_nup.py" --input 源.pdf --output 出.pdf --layout 4up --orientation portrait --page-badge

# 4-up 横向 + 页码角标 → 横版页码落右下角页脚并向右旋 90°
python "<skill_dir>/scripts/pdf_nup.py" --input 源.pdf --output 出.pdf --layout 4up --orientation landscape --page-badge
```

### 参数说明

| 参数 | 必填 | 说明 |
|---|---|---|
| `--input` | 是 | 源 PDF 路径 |
| `--output` | 是 | 输出 PDF 路径 |
| `--layout` | 是 | `1up`（单页单面，保持源页面原始尺寸与方向）或 `2up`（A4 横向 2 列 1 行）或 `4up`（2×2 网格） |
| `--orientation` | 否 | 仅 `4up` 生效：`portrait`（默认，595×842）/ `landscape`（842×595）；`1up` 忽略此项（始终沿用源页面方向） |
| `--page-badge` | 否 | 加页码角标；横向输出落右下角页脚、纵向输出落右上角页眉 |
| `--badge-font` | 否 | 角标字体路径，默认宋体 simsun.ttc |
| `--badge-size` | 否 | 角标字号，默认 10 |
| `--badge-margin` | 否 | 角标距右边缘 pt，默认 30 |
| `--badge-baseline` | 否 | 纵向页眉角标基线距顶部 pt，默认 25 |
| `--badge-bottom` | 否 | 横向页脚角标基线距底部 pt，默认 12 |
| `--badge-rotate` | 否 | 横向页脚角标旋转角度，默认 -90 |

### 批量处理

把某目录下所有 PDF 各生成一份「原名+已调整.pdf」的 4-up 纵向带页码版本：

```python
import os, subprocess
SCRIPT = r"<skill_dir>/scripts/pdf_nup.py"
SRC = r"你的目录"
for f in sorted(os.listdir(SRC)):
    if not f.lower().endswith('.pdf') or f.endswith('已调整.pdf'):
        continue
    out = os.path.join(SRC, f[:-4] + '已调整.pdf')
    subprocess.run(["python", SCRIPT, "--input", os.path.join(SRC, f),
                    "--output", out, "--layout", "4up",
                    "--orientation", "portrait", "--page-badge"], check=True)
```

---

## 三、页码角标规则（重要，别改错）

- **总页码 = 输出 PDF 的页数**：`1up` 等于源页数；`2up` = `ceil(源页数/2)`；`4up` = `ceil(源页数/4)`。
- **位置逐页按「该页自身」的方向自动判定**（判定依据是 `page.rect`，已含 `/Rotate` 旋转后的可见尺寸；遵循长边翻阅习惯）：
  - 横向页（宽 > 高，如 2-up / 4-up landscape，以及 1-up 里的横版源页）→ **右下角页脚**，默认**向右旋 90°**（`rotate=-90`，顺时针；字头朝右、读序向下）。
  - 纵向页（高 ≥ 宽，如 4-up portrait，以及 1-up 里的竖版源页）→ **右上角页眉**，不旋转。
- **1-up 混排自适应**：源文件里竖版页、横版页混排（或含 `/Rotate` 旋转页）时，页码在每页各自按当页方向落位，无需人工指定，也不要"统一按第一页方向"处理。
- 默认宋体 10 号，右边距 30pt。
- ⚠️ **旋转锚点坑**：PyMuPDF `insert_text` 的 `rotate` 正角 = **逆时针**，"向右旋"必须用 **-90**。旋转后文字自锚点**向下**延伸 `text_length`、字身向锚点**右侧**伸展约 `ascender*size`，所以横向锚点要写成 `x = page_w - margin - ascender*size`、`y = page_h - bottom - text_length`，否则页码会旋出页面外。

---

## 四、执行流程

1. 确认 `--input` 是用户指定的源 PDF，且存在；确认输出路径（默认放结果产物目录，命名如 `原文件名+并版.pdf`）。
2. 若是**批量**场景，先确认目标目录与命名规则，遵循"少量试点 → 确认结果 → 全量执行"。
3. 选布局：用户没指定时，默认 `4up portrait`（最省纸）；用户说"横向并排/两页一版"用 `2up`；用户说"单页单面 / 不要并版 / 只加页码 / 1-up"用 `1up`（不缩放、不改页面尺寸，只补页码）。
4. 检查 python 环境是否有 `pymupdf`，缺失则 `python -m pip install pymupdf` 后重试。
5. 执行，再按下节清单验证。
6. 最终回复声明产出的 PDF 绝对路径。

---

## 五、输出验证清单（务必执行，不得跳过）

1. **尺寸**：`1up` = 逐页等于源页 `page.rect`（各页可能不同，属正常）；`2up` = 842×595；`4up portrait` = 595×842；`4up landscape` = 842×595。
2. **总页数**：`1up` = 源页数；`2up` = `ceil(源页数/2)`；`4up` = `ceil(源页数/4)`。
3. **页码角标**：逐页对 `get_text("dict")` 的 line 取 `dir`——**按该页自身方向**判定：该页横向时角标应为 `(0,1)`（竖排），纵向时应为 `(1,0)`（横排）；bbox 应在页内（`0≤x≤页宽`、`0≤y≤页高`），且横向页角标落在右下象限、纵向页角标落在右上象限。
4. **1-up 内容无损**：逐页比对「源页 `get_text()` 是否包含于输出页 `get_text()`」（含 `/Rotate` 旋转页），必要时再做像素级比对，确认除新增角标外渲染一致。
5. **源 PDF 大小/修改时间未被改动**（只能读，不能写）。
6. **不得出现「内容由AI生成」「仅供参考」等水印文本**：逐页检索文本层，命中即说明链路被污染，需排查并剔除。
7. **尾页留空**：源页数为奇数（2-up）或不是 4 的倍数（4-up）时，末页应有留空区域，**不补空白页**；1-up 不涉及。

---

## 六、避坑

- 不要用 `fitz` 导入名，本 skill 统一用 `import pymupdf`（新版已不再推荐 `fitz` 别名）。
- 输出目录不存在时脚本会自动创建，但**不要**把输出写到桌面或系统目录；统一写结果产物目录。
- 若源 PDF 本身是加密文档或无文本层（纯扫描件），角标仍可绘制（角标是后画矢量文字），但源内容提取类校验会失败，属预期，不要据此判定失败。
- `1up` **不做尺寸归一化**：输出逐页沿用源页尺寸，源文件混排 A4/A3 或横竖版时输出同样混排，这是设计预期。若用户要求"统一成 A4"，需明确说明 1-up 当前不缩放/不归一，不要偷偷改用 2-up 或私自加缩放。
- `1up` 会把 `/Rotate` 旋转页**展平**（输出页 `rotation=0`、可见尺寸与源一致），避免打印时二次旋转；校验时不要因输出页 `rotation` 为 0 而误判为"方向丢失"。
*（内容由AI生成，仅供参考）*
