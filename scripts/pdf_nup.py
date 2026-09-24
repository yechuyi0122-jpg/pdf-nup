"""PDF 重排版工具（1-up / 2-up / 4-up）

布局：
  1-up — 一页对一页，保持源页面原始尺寸与方向（含 /Rotate 旋转页），
         不缩放、不合并，仅可选加页码角标（页码按每页自身方向自动落位）。
  2-up — A4 横向 (842×595 pt)，2 列 1 行，左半放第 i 页、右半放第 i+1 页，
         等比缩放居中，奇数尾页只放左半区（不补空白页）。
  4-up — 2×2 网格，每格放一页，等比缩放居中，尾页不足 4 张时剩余位置留空。
         方向可选：
           portrait  — A4 纵向 595×842（每格 297.5×421）
           landscape — A4 横向 842×595（每格 421×297.5）

可选 --page-badge：在每页绘制页码角标「本页页码/总页码」（如 1/3），
默认宋体（simsun.ttc）10 号，可通过 --badge-font / --badge-size 调整。

仅读取源 PDF，不修改源文件。
"""
import argparse
import os

import pymupdf

# 2-up 固定 A4 横向
LAYOUT_2UP = (842, 595)
# 4-up 两种方向
LAYOUT_4UP = {"portrait": (595, 842), "landscape": (842, 595)}
# 页码角标默认：宋体 10 号，距右边缘 30pt、基线距顶部 25pt
DEFAULT_BADGE_FONT = r"C:\Windows\Fonts\simsun.ttc"
DEFAULT_BADGE_SIZE = 10.0
DEFAULT_BADGE_MARGIN = 30.0
DEFAULT_BADGE_BASELINE = 25.0
DEFAULT_BADGE_BOTTOM = 12.0
DEFAULT_BADGE_ROTATE = -90.0


def draw_page_badges(doc, font_path, size, margin, baseline, bottom=None, rotate=None):
    """在每页绘制「本页页码/总页码」角标（右对齐）。

    位置**逐页**按「该页自身」的方向自动判定（以 page.rect 为准，已含 /Rotate
    旋转后的可见尺寸），因此 1-up 时源文件各页方向不一致也能各自正确落位：
      - 横向（宽 > 高，如 2-up A4 横向、1-up 的横版源页）：右下角页脚（长边翻阅习惯）。
      - 纵向（高 >= 宽，如 4-up 纵向、1-up 的竖版源页）：右上角页眉。
    baseline 控制右上角页眉基线距顶；bottom 控制右下角页脚基线距底；
    rotate 仅对横向页脚生效，向右旋转 90° 使页码竖向立于页脚。
    """
    if bottom is None:
        bottom = DEFAULT_BADGE_BOTTOM
    if rotate is None:
        rotate = DEFAULT_BADGE_ROTATE
    font = pymupdf.Font(fontfile=font_path)
    total = doc.page_count
    for i, page in enumerate(doc):
        text = f"{i + 1}/{total}"
        w = font.text_length(text, fontsize=size)
        r = page.rect
        if r.width > r.height:
            # 横向 → 右下角页脚，默认向右旋 90°（rotate=-90，顺时针）。
            # 旋转后：文字自锚点向下延伸 w，字身向右伸展约 ascender*size。
            x = r.width - margin - font.ascender * size
            y = r.height - bottom - w
            rot = rotate
        else:
            # 纵向 → 右上角页眉，不旋转
            x = r.width - margin - w
            y = baseline
            rot = 0
        page.insert_text(
            pymupdf.Point(x, y),
            text,
            fontsize=size,
            fontname="badgefont",
            fontfile=font_path,
            color=(0, 0, 0),
            rotate=rot,
        )


def _place_page(target_page, src_doc, idx, cell_rect):
    """将 src_doc 第 idx 页等比缩放居中放入 cell_rect 区域。"""
    r = src_doc[idx].rect
    if r.width <= 0 or r.height <= 0:
        return
    scale = min(cell_rect.width / r.width, cell_rect.height / r.height)
    w, h = r.width * scale, r.height * scale
    x0 = cell_rect.x0 + (cell_rect.width - w) / 2.0
    y0 = cell_rect.y0 + (cell_rect.height - h) / 2.0
    target_page.show_pdf_page(
        pymupdf.Rect(x0, y0, x0 + w, y0 + h), src_doc, idx
    )


def one_up(src_path, dst_path, badge=None):
    """1-up：一页对一页，单页单面。

    保持源页面原始尺寸与方向（page.rect 已含 /Rotate 旋转效果），不缩放、
    不合并、不补空白页，输出页数 == 源页数。可选加页码角标。
    """
    src = pymupdf.open(src_path)
    dst = pymupdf.open()
    for i in range(src.page_count):
        r = src[i].rect
        if r.width <= 0 or r.height <= 0:
            continue
        page = dst.new_page(width=r.width, height=r.height)
        page.show_pdf_page(page.rect, src, i)
    if badge:
        draw_page_badges(dst, *badge)
    dst.save(dst_path)
    src.close()
    dst.close()


def two_up_landscape(src_path, dst_path, badge=None):
    """A4 横向 2-up：2 列 1 行，左半放第 i 页、右半放第 i+1 页。"""
    page_w, page_h = LAYOUT_2UP
    half_w = page_w / 2.0
    src = pymupdf.open(src_path)
    dst = pymupdf.open()
    for i in range(0, src.page_count, 2):
        page = dst.new_page(width=page_w, height=page_h)
        # 左半区
        _place_page(page, src, i, pymupdf.Rect(0, 0, half_w, page_h))
        # 右半区（若存在下一页）
        if i + 1 < src.page_count:
            _place_page(page, src, i + 1, pymupdf.Rect(half_w, 0, page_w, page_h))
    if badge:
        draw_page_badges(dst, *badge)
    dst.save(dst_path)
    src.close()
    dst.close()


def four_up(src_path, dst_path, orientation="portrait", badge=None):
    """4-up：2×2 网格，每格放一页，等比缩放居中，尾页不足留空。"""
    if orientation not in LAYOUT_4UP:
        raise SystemExit(f"无效方向: {orientation}（可选 portrait / landscape）")
    page_w, page_h = LAYOUT_4UP[orientation]
    cell_w, cell_h = page_w / 2.0, page_h / 2.0
    src = pymupdf.open(src_path)
    dst = pymupdf.open()
    for i in range(0, src.page_count, 4):
        page = dst.new_page(width=page_w, height=page_h)
        for slot in range(4):
            idx = i + slot
            if idx >= src.page_count:
                break
            col = slot % 2
            row = slot // 2
            cell = pymupdf.Rect(
                col * cell_w, row * cell_h,
                col * cell_w + cell_w, row * cell_h + cell_h,
            )
            _place_page(page, src, idx, cell)
    if badge:
        draw_page_badges(dst, *badge)
    dst.save(dst_path)
    src.close()
    dst.close()


def main():
    parser = argparse.ArgumentParser(
        description="PDF 重排版（1-up / 2-up / 4-up）"
    )
    parser.add_argument("--input", required=True, help="源 PDF 路径")
    parser.add_argument("--output", required=True, help="输出 PDF 路径")
    parser.add_argument(
        "--layout", choices=["1up", "2up", "4up"], required=True,
        help="1up: 单页单面，保持源页面原始尺寸与方向；2up: A4 横向 2 列 1 行；4up: 2×2 网格",
    )
    parser.add_argument(
        "--orientation", choices=["portrait", "landscape"], default="portrait",
        help="4-up 方向（仅 4up 生效）：portrait 纵向 / landscape 横向；1up 忽略此项（沿用源页面方向）",
    )
    parser.add_argument(
        "--page-badge", action="store_true",
        help="在每页绘制页码角标「本页页码/总页码」；横向输出在右下角页脚、纵向输出在右上角页眉",
    )
    parser.add_argument("--badge-font", default=DEFAULT_BADGE_FONT, help="角标字体文件路径（默认宋体 simsun.ttc）")
    parser.add_argument("--badge-size", type=float, default=DEFAULT_BADGE_SIZE, help="角标字号（默认 10）")
    parser.add_argument("--badge-margin", type=float, default=DEFAULT_BADGE_MARGIN, help="角标距右边缘 pt（默认 30）")
    parser.add_argument("--badge-baseline", type=float, default=DEFAULT_BADGE_BASELINE, help="纵向页眉角标基线距顶部 pt（默认 25）")
    parser.add_argument("--badge-bottom", type=float, default=DEFAULT_BADGE_BOTTOM, help="横向页脚角标基线距底部 pt（默认 12）")
    parser.add_argument("--badge-rotate", type=float, default=DEFAULT_BADGE_ROTATE, help="横向页脚角标旋转角度，默认 -90（向右旋 90°，顺时针）")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        raise SystemExit(f"输入文件不存在: {args.input}")
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)

    badge = None
    if args.page_badge:
        if not os.path.isfile(args.badge_font):
            raise SystemExit(f"角标字体文件不存在: {args.badge_font}")
        badge = (args.badge_font, args.badge_size, args.badge_margin, args.badge_baseline, args.badge_bottom, args.badge_rotate)

    if args.layout == "1up":
        one_up(args.input, args.output, badge=badge)
        print(f"[OK] 1-up 已生成: {args.output}" + ("（含页码角标）" if badge else ""))
    elif args.layout == "2up":
        two_up_landscape(args.input, args.output, badge=badge)
        print(f"[OK] 2-up 已生成: {args.output}" + ("（含页码角标）" if badge else ""))
    else:
        four_up(args.input, args.output, args.orientation, badge=badge)
        print(f"[OK] 4-up ({args.orientation}) 已生成: {args.output}" + ("（含页码角标）" if badge else ""))


if __name__ == "__main__":
    main()
