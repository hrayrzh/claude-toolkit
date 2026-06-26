# 2D floor plans (SVG, data-driven)

One self-contained HTML file per floor. All geometry comes from arrays; JS draws the SVG and wires hover tooltips.

## Data arrays (mm)
```js
const walls = [ {id:1, x1:0,y1:0, x2:10000,y2:0, t:400, name:'наружная сев.'}, ... ];   // each wall a segment + thickness
const doors  = [ {a:[x1,y1,x2,y2], t:100}, ... ];   // a = the opening span on the wall line
const windows= [ {a:[x1,y1,x2,y2], t:400}, ... ];
const rooms  = [ {n:'Kitchen', x:3300,y:2700, w:9600,h:5400, group:'k'}, ... ]; // label pos + clear size; group merges L-shapes
```

## Drawing
- A `view(mm)` → px scale + padding; draw inside an `<svg>`.
- **Walls:** one thick `<line>` per wall, `stroke-width = t`, `stroke-linecap="square"`. The square cap is essential — butt caps
  leave triangular gaps at corners.
- **Openings (doors/windows):** draw *over* the wall — first a wall-coloured (or background) rectangle to "erase" the slice, then
  the symbol: a quarter-circle swing arc for a door, thin parallel lines / glazing for a window. A garage gate = a wide opening.
- **Dimension labels:** place them *away* from walls; a white label box sitting on a wall reads as a hole in the wall. (Common bug.)

## Hover tooltips
- Give each wall/room SVG element a data-id. On `mouseover`, show a floating `<div>` tooltip:
  - wall → `№id · name · t mm · length mm`
  - room → `area m² · W×H` (and, for L-shaped/grouped rooms, the group total).
- Compute length/area from the data, not from pixels.

## Gotchas
- Keep the 2D and 3D geometry in sync. If you move a wall or the stairs in 3D, mirror it in the 2D file (or note the divergence
  loudly in `HANDOFF.md`). Drift between the two views is a frequent source of confusion.
- Internal load-bearing walls can be 400 mm even though they look "internal" — don't assume 100.
