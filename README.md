# linkedin-banner-generator

Tiny Python script that generates a 1584×396 LinkedIn cover banner in three minimalist variants:

- **v1 — Pure white** (blank canvas)
- **v2 — Corner mark** (right-aligned name in light gray)
- **v3 — Tagline line** (name top-right + tracked tagline anchored to the bottom)

Built around DM Sans variable font with manual letter-tracking for the tagline.

## Usage

```bash
# Get DM Sans (the script reads from /tmp/dmsans/DMSans-VF.ttf)
mkdir -p /tmp/dmsans && \
  curl -L -o /tmp/dmsans/DMSans-VF.ttf \
  https://github.com/googlefonts/dm-fonts/raw/main/Sans/Variable/DMSans%5Bopsz%2Cwght%5D.ttf

pip install pillow
python3 generate_banners.py
```

Output goes to `outputs/`. Sample renders are committed under that directory.

## Customizing

Edit the `draw_*` calls in `generate_banners.py`. The right-anchored layout uses:
- `right_x` = right padding from canvas edge (default `W - 36`)
- `top_y` = vertical anchor from top (variant 2/3) or computed from the bottom (variant 3 tagline)
- `tracking_em` = letter-spacing in em units (0.18 in the tagline = ~18% extra)
