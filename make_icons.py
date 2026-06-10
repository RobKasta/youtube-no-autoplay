from PIL import Image, ImageDraw
import math, os

def draw_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size / 128  # scale factor

    # ── Background: YouTube-red rounded rectangle ──────────────────────────
    r = int(18 * s)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=r,
                        fill=(200, 0, 0, 255))

    # ── Polar bear (white) ─────────────────────────────────────────────────
    # Body
    bx, by, bw, bh = 28*s, 58*s, 72*s, 52*s
    d.ellipse([bx, by, bx+bw, by+bh], fill=(255, 255, 255, 255))

    # Head
    hx, hy, hr = 64*s, 52*s, 22*s
    d.ellipse([hx-hr, hy-hr, hx+hr, hy+hr], fill=(255, 255, 255, 255))

    # Left ear
    d.ellipse([hx-hr-8*s, hy-hr-2*s, hx-hr+6*s, hy-hr+10*s],
              fill=(255, 255, 255, 255))
    # Right ear
    d.ellipse([hx+hr-6*s, hy-hr-2*s, hx+hr+8*s, hy-hr+10*s],
              fill=(255, 255, 255, 255))

    # Inner ears (slightly red)
    d.ellipse([hx-hr-5*s, hy-hr, hx-hr+3*s, hy-hr+7*s],
              fill=(220, 60, 60, 255))
    d.ellipse([hx+hr-3*s, hy-hr, hx+hr+5*s, hy-hr+7*s],
              fill=(220, 60, 60, 255))

    # Eyes (dark)
    ew = max(2, int(4*s))
    d.ellipse([hx-10*s-ew, hy-6*s-ew, hx-10*s+ew, hy-6*s+ew],
              fill=(40, 20, 10, 255))
    d.ellipse([hx+10*s-ew, hy-6*s-ew, hx+10*s+ew, hy-6*s+ew],
              fill=(40, 20, 10, 255))

    # Nose (dark oval)
    nw, nh = int(8*s), int(5*s)
    d.ellipse([hx-nw, hy+6*s-nh, hx+nw, hy+6*s+nh],
              fill=(40, 20, 10, 255))

    # Smile
    sw = int(10*s)
    d.arc([hx-sw, hy+6*s, hx+sw, hy+16*s], start=10, end=170,
          fill=(40, 20, 10, 255), width=max(1, int(2*s)))

    # Arms (two small ellipses)
    aw, ah = int(14*s), int(8*s)
    # left arm
    d.ellipse([bx-aw+4*s, by+14*s, bx+aw-4*s, by+14*s+ah*2],
              fill=(255, 255, 255, 255))
    # right arm
    d.ellipse([bx+bw-aw-2*s, by+14*s, bx+bw+aw-10*s, by+14*s+ah*2],
              fill=(255, 255, 255, 255))

    # ── Pause symbol (white "||") in bottom-right ──────────────────────────
    # Small dark red badge circle
    cx, cy, cr = 92*s, 96*s, 22*s
    d.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill=(140, 0, 0, 230))

    # Two white pause bars
    pw, ph = int(6*s), int(18*s)
    gap = int(5*s)
    lx = int(cx - gap - pw)
    rx = int(cx + gap)
    ty = int(cy - ph//2)
    by2 = int(cy + ph//2)
    bar_r = max(1, int(2*s))
    d.rounded_rectangle([lx, ty, lx+pw, by2], radius=bar_r,
                        fill=(255, 255, 255, 255))
    d.rounded_rectangle([rx, ty, rx+pw, by2], radius=bar_r,
                        fill=(255, 255, 255, 255))

    return img


base = os.path.dirname(os.path.abspath(__file__))
for size in [16, 48, 128]:
    icon = draw_icon(size)
    path = os.path.join(base, "icons", f"icon{size}.png")
    icon.save(path, "PNG")
    print(f"Saved {path}")
