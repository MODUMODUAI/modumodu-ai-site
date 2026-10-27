# -*- coding: utf-8 -*-
"""상품담기 샘플용 상품 이미지. 실상품 사진이 아니라 안내 화면용입니다."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parent / "sample-products"
W = 480


def new_canvas():
    image = Image.new("RGB", (W, W), "#f3f4f6")
    return image, ImageDraw.Draw(image)


def shadow(image, box):
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse(box, fill=(0, 0, 0, 48))
    layer = layer.filter(ImageFilter.GaussianBlur(14))
    return Image.alpha_composite(image.convert("RGBA"), layer).convert("RGB")


def save(image, name):
    OUT.mkdir(exist_ok=True)
    image.save(OUT / name, "PNG")


def chair_caps():
    image, draw = new_canvas()
    image = shadow(image, (90, 340, 390, 400))
    draw = ImageDraw.Draw(image)
    for i, (x, y) in enumerate(((150, 150), (230, 140), (190, 220), (270, 230), (210, 300))):
        draw.rounded_rectangle((x, y, x + 70, y + 48), 16, fill="#d9e4ee", outline="#8aa4bb", width=4)
        draw.ellipse((x + 16, y + 10, x + 54, y + 34), fill="#f7fbff")
    save(image, "01.png")


def clothespins():
    image, draw = new_canvas()
    image = shadow(image, (110, 350, 370, 410))
    draw = ImageDraw.Draw(image)
    colors = ["#e24b4b", "#f0b429", "#3aa0e6", "#46a86a", "#ef7d32"]
    for i, color in enumerate(colors):
        x = 120 + i * 48
        draw.rounded_rectangle((x, 120, x + 34, 340), 8, fill=color)
        draw.rectangle((x + 12, 150, x + 22, 250), fill="#f7f7f7")
        draw.ellipse((x + 8, 250, x + 26, 268), outline="#222", width=3)
    save(image, "02.png")


def heat_packs():
    image, draw = new_canvas()
    image = shadow(image, (80, 340, 400, 410))
    draw = ImageDraw.Draw(image)
    for i, y in enumerate((120, 175, 230)):
        draw.rounded_rectangle((110, y, 370, y + 70), 12, fill="#e7d3b4", outline="#b08968", width=3)
        draw.line((140, y + 35, 340, y + 35), fill="#c4a484", width=2)
    save(image, "03.png")


def pouches():
    image, draw = new_canvas()
    image = shadow(image, (90, 350, 400, 420))
    draw = ImageDraw.Draw(image)
    colors = ["#243044", "#5c6b7a", "#c2b8a3", "#1f4e79", "#8d6e63"]
    for i, color in enumerate(colors):
        x = 70 + i * 62
        draw.rounded_rectangle((x, 130, x + 110, 360), 18, fill=color)
        draw.rectangle((x + 12, 155, x + 98, 175), fill="#d9dde3")
    save(image, "04.png")


def one_sock(draw, x, y, color, cuff):
    draw.rounded_rectangle((x + 8, y + 50, x + 68, y + 80), 14, fill=color)
    draw.ellipse((x + 48, y + 48, x + 78, y + 82), fill=color)
    draw.rounded_rectangle((x + 12, y, x + 40, y + 66), 12, fill=color)
    draw.rectangle((x + 15, y + 3, x + 37, y + 14), fill=cuff)


def socks(name, pairs):
    image, draw = new_canvas()
    image = shadow(image, (80, 360, 410, 430))
    draw = ImageDraw.Draw(image)
    for i, (color, cuff) in enumerate(pairs):
        one_sock(draw, 24 + (i % 5) * 90, 150, color, cuff)
    save(image, name)


def scrubbers():
    image, draw = new_canvas()
    image = shadow(image, (100, 350, 390, 420))
    draw = ImageDraw.Draw(image)
    colors = ["#f2c14e", "#7dba4a", "#f2c14e", "#7dba4a", "#e6b325"]
    for i, color in enumerate(colors):
        x = 80 + (i % 5) * 68
        y = 150 + (i // 5) * 40
        draw.ellipse((x, y, x + 90, y + 70), fill=color, outline="#8a6a12", width=3)
        draw.arc((x + 15, y + 12, x + 75, y + 55), 200, 20, fill="#fff4c2", width=3)
    save(image, "06.png")


def rack():
    image, draw = new_canvas()
    image = shadow(image, (80, 370, 400, 430))
    draw = ImageDraw.Draw(image)
    draw.line((120, 360, 160, 140), fill="#d7dde6", width=10)
    draw.line((360, 360, 320, 140), fill="#d7dde6", width=10)
    for y in (170, 220, 270, 320):
        draw.line((150, y, 330, y), fill="#eef2f6", width=8)
    save(image, "08.png")


def lantern():
    image, draw = new_canvas()
    image = shadow(image, (160, 370, 330, 430))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((185, 120, 295, 360), 28, fill="#2b2f36")
    draw.rounded_rectangle((205, 160, 275, 300), 16, fill="#f4e7b0")
    draw.rectangle((210, 110, 270, 140), fill="#1c1f24")
    draw.ellipse((228, 330, 252, 354), fill="#c9ced6")
    save(image, "09.png")


def shelf():
    image, draw = new_canvas()
    image = shadow(image, (90, 360, 390, 420))
    draw = ImageDraw.Draw(image)
    draw.polygon([(120, 140), (360, 140), (330, 340), (150, 340)], fill="#f7f8fa", outline="#c5ced8")
    draw.line((150, 200, 340, 200), fill="#d5dde6", width=8)
    draw.line((155, 260, 335, 260), fill="#d5dde6", width=8)
    draw.ellipse((150, 120, 190, 160), outline="#9aa8b5", width=6)
    save(image, "10.png")


def cloths():
    image, draw = new_canvas()
    image = shadow(image, (90, 350, 400, 420))
    draw = ImageDraw.Draw(image)
    colors = ["#f7f7f7", "#d7e6f5", "#d9efe0", "#f7f7f7", "#d7e6f5", "#d9efe0"]
    for i, color in enumerate(colors):
        x = 90 + (i % 3) * 100
        y = 110 + (i // 3) * 110
        draw.rounded_rectangle((x, y, x + 120, y + 80), 8, fill=color, outline="#b7c3cf", width=3)
        draw.line((x + 12, y + 20, x + 108, y + 20), fill="#e3e9ef", width=2)
    save(image, "12.png")


def main():
    chair_caps()
    clothespins()
    heat_packs()
    pouches()
    socks("05.png", [("#2c3038", "#d1d5db"), ("#4b5563", "#e5e7eb"), ("#111827", "#9ca3af"), ("#374151", "#f3f4f6"), ("#1f2937", "#e5e7eb")])
    scrubbers()
    socks("07.png", [("#f8fafc", "#cbd5e1"), ("#1e3a5f", "#e2e8f0"), ("#d1d5db", "#f8fafc"), ("#e5e7eb", "#94a3b8"), ("#334155", "#f1f5f9")])
    rack()
    lantern()
    shelf()
    socks("11.png", [("#f9a8d4", "#fce7f3"), ("#93c5fd", "#dbeafe"), ("#fde68a", "#fef3c7"), ("#86efac", "#dcfce7"), ("#fda4af", "#ffe4e6")])
    cloths()
    print(OUT)


if __name__ == "__main__":
    main()
