"""Render static portfolio exports from the aggregate Power BI dataset."""

from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "chart_data.csv"
EXPORT_DIR = ROOT / "powerbi" / "exports"

WIDTH, HEIGHT = 1600, 1080
BG = "#FFFFFF"
TEXT = "#222222"
MUTED = "#666666"
GRID = "#E7E7E7"
NAVY = "#17365D"
GOLD = "#B8860B"
GRAY = "#7A7A7A"
LIGHT_NAVY = "#5B7FA3"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    candidates = [Path("C:/Windows/Fonts") / name]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default(size=size)


def load_rows() -> list[dict[str, str]]:
    with DATA_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def x_scale(value: float, left: int, right: int) -> int:
    return round(left + (right - left) * value / 100)


def draw_axis(draw: ImageDraw.ImageDraw, left: int, right: int, top: int, bottom: int) -> None:
    for tick in (0, 25, 50, 75, 100):
        x = x_scale(tick, left, right)
        draw.line((x, top, x, bottom), fill=GRID, width=2)
        label = str(tick)
        box = draw.textbbox((0, 0), label, font=font(23))
        draw.text((x - (box[2] - box[0]) / 2, bottom + 10), label, fill=MUTED, font=font(23))


def draw_interval(
    draw: ImageDraw.ImageDraw,
    row: dict[str, str],
    y: int,
    left: int,
    right: int,
    color: str,
) -> None:
    estimate = float(row["estimate"])
    low = float(row["ci_low"])
    high = float(row["ci_high"])
    x_low = x_scale(low, left, right)
    x_high = x_scale(high, left, right)
    x_est = x_scale(estimate, left, right)
    draw.line((x_low, y, x_high, y), fill=color, width=8)
    draw.line((x_low, y - 10, x_low, y + 10), fill=color, width=4)
    draw.line((x_high, y - 10, x_high, y + 10), fill=color, width=4)
    draw.ellipse((x_est - 11, y - 11, x_est + 11, y + 11), fill=color)
    draw.text((x_high + 14, y - 17), f"{estimate:.1f}%", fill=TEXT, font=font(25, bold=True))


def render() -> tuple[Path, Path]:
    rows = load_rows()
    by_metric = {
        metric: [row for row in rows if row["metric_id"] == metric]
        for metric in {row["metric_id"] for row in rows}
    }
    order = ["Christian", "Other faith", "No religious affiliation"]
    for metric_rows in by_metric.values():
        metric_rows.sort(key=lambda row: order.index(row["belief_group"]))

    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    draw.text((90, 55), "Faith and self-reported health", fill=TEXT, font=font(52, bold=True))
    draw.text(
        (90, 125),
        "U.S. adults, General Social Survey 2022 · survey-weighted estimates with 95% confidence intervals",
        fill=MUTED,
        font=font(27),
    )

    left, right = 480, 1450
    draw.text((90, 205), "Excellent or good general health", fill=TEXT, font=font(31, bold=True))
    draw_axis(draw, left, right, 250, 505)
    for idx, row in enumerate(by_metric["good_or_better_pct"]):
        y = 295 + idx * 82
        draw.text((90, y - 18), row["belief_group"], fill=TEXT, font=font(27))
        draw_interval(draw, row, y, left, right, NAVY)

    draw.line((90, 560, 1510, 560), fill=GRID, width=3)
    draw.text((90, 600), "Eight or more unhealthy days in the past month", fill=TEXT, font=font(31, bold=True))
    draw.text((90, 642), "Lower values indicate fewer respondents reporting frequent unhealthy days.", fill=MUTED, font=font(24))
    draw_axis(draw, left, right, 700, 940)

    physical = {row["belief_group"]: row for row in by_metric["physical_8plus_pct"]}
    mental = {row["belief_group"]: row for row in by_metric["mental_8plus_pct"]}
    for idx, group in enumerate(order):
        center = 750 + idx * 82
        draw.text((90, center - 18), group, fill=TEXT, font=font(27))
        draw_interval(draw, physical[group], center - 14, left, right, GOLD)
        draw_interval(draw, mental[group], center + 18, left, right, LIGHT_NAVY)

    draw.rectangle((930, 615, 952, 637), fill=GOLD)
    draw.text((965, 610), "Physical", fill=TEXT, font=font(24))
    draw.rectangle((1100, 615, 1122, 637), fill=LIGHT_NAVY)
    draw.text((1135, 610), "Mental", fill=TEXT, font=font(24))

    draw.text(
        (90, 1010),
        "Descriptive associations, not causal effects. No religious affiliation does not necessarily mean atheist.",
        fill=TEXT,
        font=font(23, bold=True),
    )
    draw.text(
        (90, 1045),
        "Source: NORC General Social Survey 2022. Weight: WTSSNRPS; design: VSTRAT + VPSU.",
        fill=MUTED,
        font=font(22),
    )

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    png_path = EXPORT_DIR / "christian_wellbeing_report.png"
    pdf_path = EXPORT_DIR / "christian_wellbeing_report.pdf"
    image.save(png_path, optimize=True)
    image.save(pdf_path, "PDF", resolution=300.0)
    return png_path, pdf_path


if __name__ == "__main__":
    for path in render():
        print(path.relative_to(ROOT))
