# Conventions: units, coordinates, dimensions, areas, levels

## Units
- **Millimetres everywhere** in the data. Only divide by 1000 when handing a value to Three.js (which works in metres).
- Keep one global "floor height" (e.g. 3000) and reuse it.

## Coordinate system
- Plan is `x` = right (east on the drawing), `y` = down (south on the drawing).
- 3D mapping: `worldX = x/1000`, `worldZ = y/1000`, **Y is up**. So **plan-y becomes 3D-z**, and Y is height.
- Decide a **datum (level 0)** early. If the building sits above grade, level 0 = finished floor and the ground sits *below* it
  (e.g. ground at −0.5 m). Put a plinth/foundation between them. Ramps and entrance steps bridge ground→floor.

## Axis vs clear dimensions (ask!)
- Overall/structural dimensions on architect drawings are usually **by axis** (centre-line of walls).
- A room size a client quotes ("the garage is 5.5 m") is often the **clear internal** dimension.
- These differ by a wall thickness. Always confirm which you're given before laying out, or rooms drift by 100–400 mm.

## Wall thickness (typical)
| Wall | Thickness (mm) |
|---|---|
| Exterior | 400 |
| Internal partition | 100 |
| Internal load-bearing | 400 |
Inner face offset from the axis = thickness/2 (so a 400 axis wall has its face 200 mm in).

## Compass / orientation
- The user fixes which physical side faces the street / north. **That overrides any default.** Once fixed, derive east/west and
  make the sun consistent (see the sun section in `3d-threejs.md`). Don't argue handedness — match what they stated.
- If entrance + garage face the street, that's usually the "front"; living rooms with big glazing usually face the private/back
  and the sunny side. Confirm with one question if it conflicts with the model.

## Calculating areas
- **Room (net/usable) area** = clear internal width × clear internal height (inside the wall faces). For L-shaped rooms, split
  into rectangles and sum; report the group total.
- **Subtract notches** the user carves out (e.g. "give 800×1200 of the corner to the hall").
- **Gross / footprint** = by the outer axes, minus any cut-outs (a porch notch, a courtyard).
- Report areas per room and a floor total as you build, and keep them in `HANDOFF.md`. They double as a sanity check: if a
  computed area is wildly off, a dimension is wrong.

## Example (mm)
- Outer shape polygon: `[[0,0],[10000,0],[10000,11000],[4800,11000],[4800,13000],[0,13000]]` — a 10×11 block plus a 4.8×2
  wing, with a 5.2×2 porch notch cut from one corner.
- A garage quoted as 4.4 × 5.5 m **clear** → area 24.2 m²; a 1.2 m-deep utility room over it → its `y` span is 1200 clear.
