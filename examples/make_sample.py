"""生成一份用于试跑 pdf-nup 的示例 PDF（纯合成数据，不含任何真实资料）。

生成 6 页：
  - 第 1/3/4/6 页：A4 纵向（595×842）
  - 第 2/5 页：A4 横向（842×595）
用于验证 1-up 的横竖混排页码自适应，以及 2-up / 4-up 的并版效果。

用法：
    python examples/make_sample.py [输出路径]
    # 不传输出路径时，默认写到 examples/sample-input.pdf
"""
import os
import sys

import pymupdf

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "sample-input.pdf")

PORTRAIT = (595, 842)
LANDSCAPE = (842, 595)
# 横向的页号（1-based）
LANDSCAPE_PAGES = {2, 5}
TOTAL = 6


def main():
    doc = pymupdf.open()
    for i in range(1, TOTAL + 1):
        w, h = LANDSCAPE if i in LANDSCAPE_PAGES else PORTRAIT
        page = doc.new_page(width=w, height=h)
        page.insert_text((60, 80), f"SAMPLE PAGE {i} / {TOTAL}", fontsize=20)
        page.insert_text(
            (60, 120),
            "synthetic demo data - safe to share",
            fontsize=11,
        )
        # 画个框，方便肉眼确认缩放与留白
        page.draw_rect(
            pymupdf.Rect(60, 150, w - 60, h - 80), color=(0.6, 0.6, 0.6), width=1
        )
        for k in range(1, 12):
            page.insert_text(
                (70, 170 + k * 30),
                f"{'line' :>5} {k:02d}  " + "-" * 40,
                fontsize=9,
            )
    doc.save(OUT)
    doc.close()
    print(f"[OK] 示例 PDF 已生成: {OUT}")


if __name__ == "__main__":
    main()
