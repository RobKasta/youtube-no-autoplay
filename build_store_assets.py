"""
Génère les assets pour le Chrome Web Store :
  - store/promo_440x280.png   (petite tuile promotionnelle, obligatoire)
  - store/screenshot_1280x800.png  (screenshot mockup)
  - store/youtube-no-autoplay.zip  (paquet à uploader)
"""
from PIL import Image, ImageDraw, ImageFont
import zipfile, os, shutil

BASE   = os.path.dirname(os.path.abspath(__file__))
EXT    = os.path.join(BASE, "extension")
STORE  = os.path.join(BASE, "store")
os.makedirs(STORE, exist_ok=True)

# ── Couleurs ────────────────────────────────────────────────────────────────
RED    = (200, 0, 0)
DKRED  = (140, 0, 0)
WHITE  = (255, 255, 255)
BG     = (18, 18, 18)
GRAY   = (80, 80, 80)


def draw_bear(d, cx, cy, s):
    """Dessine l'ours polaire (même logique que make_icons.py, taille variable)."""
    # Body
    bw, bh = 72*s, 52*s
    bx, by = cx - bw/2, cy - bh*0.1
    d.ellipse([bx, by, bx+bw, by+bh], fill=WHITE)
    # Head
    hr = 22*s
    hx, hy = cx, cy - bh*0.1 - hr*0.9
    d.ellipse([hx-hr, hy-hr, hx+hr, hy+hr], fill=WHITE)
    # Ears
    for sign in (-1, 1):
        ex = hx + sign*(hr + 2*s)
        d.ellipse([ex-7*s, hy-hr-2*s, ex+7*s, hy-hr+9*s], fill=WHITE)
        d.ellipse([ex-4*s, hy-hr+1*s, ex+4*s, hy-hr+7*s], fill=(220,60,60))
    # Eyes
    ew = max(2, int(3*s))
    for sign in (-1, 1):
        ex = hx + sign*10*s
        d.ellipse([ex-ew, hy-6*s-ew, ex+ew, hy-6*s+ew], fill=(40,20,10))
    # Nose
    nw, nh = 7*s, 4*s
    d.ellipse([hx-nw, hy+6*s-nh, hx+nw, hy+6*s+nh], fill=(40,20,10))
    # Smile
    sw = int(9*s)
    d.arc([hx-sw, hy+6*s, hx+sw, hy+15*s], 10, 170,
          fill=(40,20,10), width=max(1,int(2*s)))
    # Arms
    aw, ah = 13*s, 7*s
    d.ellipse([bx-aw+6*s, by+12*s, bx+aw-2*s, by+12*s+ah*2], fill=WHITE)
    d.ellipse([bx+bw-aw-4*s, by+12*s, bx+bw+aw-8*s, by+12*s+ah*2], fill=WHITE)
    # Pause badge
    cr = 14*s
    px, py = cx + 28*s, cy + 30*s
    d.ellipse([px-cr, py-cr, px+cr, py+cr], fill=(*DKRED, 230))
    pw, ph = 5*s, 14*s
    gap = 4*s
    br = max(1, int(2*s))
    for lx in (px - gap - pw, px + gap):
        x0, y0, x1, y1 = int(lx), int(py-ph/2), int(lx+pw), int(py+ph/2)
        if x1 > x0 and y1 > y0:
            d.rounded_rectangle([x0, y0, x1, y1], radius=br, fill=WHITE)


# ── 1. Petite tuile promotionnelle 440×280 ──────────────────────────────────
W, H = 440, 280
img = Image.new("RGBA", (W, H), (*BG, 255))
d   = ImageDraw.Draw(img)

# Fond dégradé simulé (bandes)
for i in range(H):
    t = i / H
    r = int(18 + 12*t)
    d.line([(0, i), (W, i)], fill=(r, r, r))

# Cercle rouge décoratif
d.ellipse([-60, -60, 200, 200], fill=(*RED, 40))

# Ours
draw_bear(d, 120, 148, 1.55)

# Texte titre
try:
    font_big  = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 28)
    font_sub  = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 15)
    font_tag  = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 13)
except Exception:
    font_big = font_sub = font_tag = ImageFont.load_default()

d.text((235, 70),  "YouTube",         font=font_big, fill=RED)
d.text((235, 104), "No Autoplay",     font=font_big, fill=WHITE)
d.line([(235, 142), (400, 142)], fill=GRAY, width=1)
d.text((235, 152), "Videos play only when",  font=font_sub, fill=(180,180,180))
d.text((235, 172), "YOU click play.",         font=font_sub, fill=(180,180,180))
d.text((235, 210), "Tab restore  •  Cross-device sync",
       font=font_tag, fill=(120,120,120))

out = os.path.join(STORE, "promo_440x280.png")
img.save(out)
print(f"✓  {out}")


# ── 2. Screenshot mockup 1280×800 ──────────────────────────────────────────
W2, H2 = 1280, 800
img2 = Image.new("RGBA", (W2, H2), (15, 15, 15, 255))
d2   = ImageDraw.Draw(img2)

# Fond
for i in range(H2):
    t = i / H2
    r = int(15 + 8*t)
    d2.line([(0, i), (W2, i)], fill=(r, r, r))

# Titre centré
try:
    f_title  = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 52)
    f_sub2   = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
    f_body   = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    f_small  = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
except Exception:
    f_title = f_sub2 = f_body = f_small = ImageFont.load_default()

def centered(draw, text, y, font, color):
    bb = draw.textbbox((0, 0), text, font=font)
    w  = bb[2] - bb[0]
    draw.text(((W2 - w) / 2, y), text, font=font, fill=color)

centered(d2, "YouTube No Autoplay", 80, f_title, WHITE)
centered(d2, "Videos only play when you click. Not on tab restore or device sync.", 155, f_sub2, (160,160,160))

# Ours central
draw_bear(d2, W2//2, 420, 3.2)

# Trois features en bas
features = [
    ("Tab restore", "Ouvre Chrome → vidéos en pause"),
    ("Device sync", "Synchro inter-appareils sans lecture auto"),
    ("On/Off toggle", "Désactivez en un clic depuis la barre"),
]
fx_start = 160
fy = 640
for i, (title, desc) in enumerate(features):
    fx = fx_start + i * 330
    d2.rounded_rectangle([fx, fy, fx+290, fy+100], radius=12, fill=(30,30,30))
    d2.text((fx+20, fy+18), title, font=f_body,  fill=WHITE)
    # wrap desc
    d2.text((fx+20, fy+50), desc,  font=f_small, fill=(140,140,140))

out2 = os.path.join(STORE, "screenshot_1280x800.png")
img2.save(out2)
print(f"✓  {out2}")


# ── 3. ZIP de l'extension ──────────────────────────────────────────────────
zip_path = os.path.join(STORE, "youtube-no-autoplay.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(EXT):
        # exclure fichiers inutiles
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".DS_Store")]
        for file in files:
            if file.startswith(".") or file == ".DS_Store":
                continue
            abs_path = os.path.join(root, file)
            arc_name = os.path.relpath(abs_path, EXT)
            zf.write(abs_path, arc_name)
print(f"✓  {zip_path}")
print("\nContenu du ZIP :")
with zipfile.ZipFile(zip_path) as zf:
    for name in sorted(zf.namelist()):
        print(f"   {name}")
