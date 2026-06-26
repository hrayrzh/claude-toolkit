# Verification — look at a render, don't guess

The single highest-leverage habit. After any geometry change, render the relevant view, open the image, and actually inspect it
before reporting done. Catches furniture-in-walls, blocked doors, roof gaps, wrong sun side, floating objects.

## 2D (SVG) screenshot
```bash
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CH" --headless=new --disable-gpu --force-device-scale-factor=2 --window-size=1100,1300 \
  --screenshot=out.png "file:///abs/path/floor-plans.html"
```

## 3D (WebGL needs SwiftShader + load time)
```bash
"$CH" --headless=new --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader \
  --virtual-time-budget=17000 --window-size=1180,820 --screenshot=out.png \
  "file:///abs/path/house-3d.html#cut"
```
- `--virtual-time-budget` (~16–18 s) lets the CDN modules load and the scene build before the snapshot.
- Crop/resize with ImageMagick to see detail: `magick out.png -crop 600x500+360+230 +repage -resize 1200x zoom.png`.
- Full-size 3D PNGs are large; resize to ~1200 px wide for reading.

## Stable view hashes (keep these)
- `#open` — roof hidden (see into the storeys from above).
- `#cut` — ground floor only (upper floor + its furniture hidden).
- `#fpN` — enter room N (first-person) from the rooms array.

## Temporary verification cameras (add, use, then DELETE)
To inspect a specific spot, add a throwaway hash handler that positions the camera (and maybe hides the roof / picks a sun time),
render, then **remove it** so it doesn't ship. Examples that recur:
- a top-down of one floor (camera high, look straight down; hide roof; for ground floor also hide the upper floor group);
- a façade view from one compass side (to check a gable, steps, ramp, terrace);
- a morning vs evening sun (`setSun(7)` vs `setSun(17)`) to confirm the sun rises on the correct side.

Always clean up temporary hashes/cameras before finishing — they are scaffolding, not deliverables.

## Self-check questions while looking
- Does any furniture intersect a wall or sit in a doorway?
- Is every bed reachable; is there ≥700 in front of toilets; ≥900 through passages?
- Are there gaps/holes in the roof or open gable triangles? Are intended openings (balcony) the only open parts?
- Does the sun rise on the side the user calls east? Is noon sun in the south?
- Does anything float (wrong base height) or sit below grade (level/datum mistake)?
