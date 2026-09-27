#!/usr/bin/env python3
"""Optional maintainer command: render the chart from Chapter 10's visible table.

Requires Matplotlib and a local Chinese font. No model or network is used.
The normal course tests use only the standard library and do not import this file.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from lesson_data import MODULE, numeric_table, table_fingerprint


def render(font_path: Path | None = None) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager

    rows = numeric_table("quarterly-evidence")
    if rows[0] != ["指标", "第一季度", "第二季度", "单位"]:
        raise ValueError("The renderer expects the declared quarterly table columns")
    records = {r[0]: r[1:] for r in rows[1:]}
    sales = [float(records["销售额"][0]), float(records["销售额"][1])]
    visits = float(records["访问量"][1])
    if font_path is not None:
        if not font_path.is_file():
            raise ValueError(f"Font file does not exist: {font_path}")
        font = font_manager.FontProperties(fname=str(font_path))
    else:
        candidates = ["Noto Sans CJK SC", "Noto Sans CJK JP", "Microsoft YaHei",
                      "PingFang SC", "SimHei", "WenQuanYi Zen Hei"]
        installed = {f.name for f in font_manager.fontManager.ttflist}
        selected = next((n for n in candidates if n in installed), None)
        if selected is None:
            raise RuntimeError("No Chinese font found; pass --font /path/to/local/font")
        font = font_manager.FontProperties(family=selected)
    target = MODULE / "assets" / "quarterly-evidence.svg"
    target.parent.mkdir(parents=True, exist_ok=True)
    # A single, data-driven plot using Matplotlib's default colors.
    with matplotlib.rc_context({"svg.hashsalt": "llm-quarterly-evidence-v1"}):
        fig, ax = plt.subplots(figsize=(7, 3.8))
        ax.plot([1, 2], sales, marker="o", linewidth=2)
        ax.set(xlim=(0.7, 2.3), ylim=(0, max(sales) * 1.5))
        ax.set_xticks([1, 2], rows[0][1:3], fontproperties=font)
        ax.set_ylabel(f"销售额（{records['销售额'][2]}）", fontproperties=font)
        ax.set_title("教学图表：销售额变化", fontproperties=font, pad=12)
        for x, value in zip([1, 2], sales):
            ax.annotate(f"{value:g}", (x, value), xytext=(0, 10),
                        textcoords="offset points", ha="center")
        ax.text(0.98, 0.94,
                f"旁注：第二季度访问量 {visits:g} {records['访问量'][2]}\n不是本题要比较的销售额",
                transform=ax.transAxes, ha="right", va="top", fontproperties=font)
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        try:
            fig.savefig(target, format="svg", metadata={
                "Date": None,
                "Description": "quarterly-evidence source-sha256=" + table_fingerprint(rows)
            })
        finally:
            plt.close(fig)
    # Canonical line endings keep generated SVG clean in Git diffs.
    target.write_text("\n".join(line.rstrip() for line in target.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    return target


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", type=Path, help="An existing local Chinese font file")
    args = parser.parse_args()
    print(render(args.font))


if __name__ == "__main__":
    main()
