---
name: house-modeler
description: >-
  Digitize a building from hand-drawn or photographed floor plans into BOTH accurate 2D floor plans (SVG) and an interactive
  walkable 3D model (Three.js), generated from a single source of truth — geometry arrays in millimetres. Covers wall/door/window
  layout, area calculation, interior furnishing to professional clearance standards, site/plot, levels (raised floor, ramps,
  stairs, terrace, balcony), a physically-correct sun by latitude, and pitched roofs. Use this skill whenever the user wants to
  turn floor plans, architect sketches, or room dimensions into HTML; build or correct a 2D floor plan; create a 3D house /
  apartment / building model or a first-person walkthrough; lay out furniture or check room clearances; add a yard, fence,
  trees, roof, or daylight study — even if they never say "Three.js" or "3D" and just say things like "digitize this house",
  "model my apartment", "make a plan from these photos", or "show what it would look like". Works for NON-technical users too: if
  the person isn't a programmer, run a friendly question-by-question interview (building type, number of floors, rooms, which side
  faces the street, roof, furniture…) and build the whole thing for them — they only answer and look at pictures; never make them
  touch code.
---

# House Modeler

Build a real, dimensionally-accurate digital twin of a building from rough plans. The whole thing is **data-driven**: you keep
the geometry in plain arrays (in millimetres) and generate **both** the 2D SVG plan and the 3D Three.js model from the *same
numbers*. This keeps the two views consistent and makes edits cheap — change a number, both update.

## Golden rules (read first)

1. **One source of truth, in millimetres.** Walls/openings/rooms live in arrays. Never hand-place pixels; compute from data.
2. **Verify with a render, never by guessing.** After every change, screenshot the result (see `references/verification.md`) and
   actually look at it before telling the user it's done. This catches 90% of mistakes (furniture in walls, blocked doors, gaps).
3. **Iterate in small steps, confirm dimensions.** Plans are ambiguous. When a dimension is unclear (axis vs clear, which side a
   door is on, compass orientation), ask one focused question rather than assuming. Re-read the user's exact numbers.
4. **Match the user's intent over "standard".** They know their building; if they say a side is "north" or a wall is somewhere,
   that overrides convention — make the rest (e.g. the sun, labels) consistent with what they said.
5. **Be fast and incremental — do NOT over-think.** This is a live interview, not a one-shot. Take the *next small step* (ask the
   next question, make the next edit) and answer promptly — do not silently plan the whole project before speaking, and don't
   re-derive the entire model each turn. Use **progressive disclosure**: read only the one reference you need for the current step
   (e.g. `geometry-capture.md` when capturing walls), never all of them at once. For the intake, prefer the **AskUserQuestion**
   tool (quick taps) over long prose. A snappy back-and-forth beats minutes on a "thinking…" spinner — especially for non-technical
   users. If a step is simple (asking 4 measurements), just ask; save deep reasoning for genuinely hard geometry.
6. **Speak the user's language in everything they see.** This skill's files are in English because they instruct *you*, but all
   user-facing output follows the conversation's language: the interview questions, your explanations, AND the visible text inside
   the generated files — room names, menu/HUD labels, hover tooltips, button captions, hints. If they chat in Spanish, the rooms
   and UI are in Spanish; Russian → Russian; English → English. Keep code identifiers/comments as you like, but never ship UI
   labels in a language the user isn't using.

## Two ways to start — pick by who you're talking to
- **They have plans / dimensions** (or photos of drawings) → go straight to the Workflow below.
- **They're not technical, or starting from scratch** ("I want to model my house", "design a 2-storey home") → **run the guided
  interview first**: `references/intake-interview.md`. You ask simple questions (building type, floors, rooms, which side faces the
  street, roof, furniture…), mostly multiple-choice, in plain language; they just answer and look at renders; you write all the
  code and build the whole project for them. Default to this mode whenever the person doesn't speak in dimensions/jargon.

## Workflow

1. **Read the plans.** Get dimensions, room divisions, wall thicknesses, door/window positions, stairs. Ask which numbers are
   *by-axis* vs *clear internal* (see conventions). Establish the outer shape as a polygon.
2. **Build the 2D plan(s)** — one SVG per floor, generated from the wall/door/window/room arrays. Number the walls, add hover
   tooltips (wall id/size, room area). See `references/2d-plans.md`.
3. **Compute areas** as you go and report them. See area rules in `references/conventions.md`.
4. **2D approval gate (required).** Before any 3D, capture the storey/**wall height** if not already known, then explicitly ask
   the user whether the 2D plans are correct or need changes — and **loop until they confirm everything is right**. The 3D is
   generated from the same numbers, so fix geometry on the 2D first; don't start the 3D over an unconfirmed plan.
5. **Convert to 3D** from the same arrays: extruded walls with *real* openings, floor slabs (with voids for double-height),
   contour edges + ambient occlusion so white surfaces read, a first-person walkthrough, and on-demand rendering for performance.
   See `references/3d-threejs.md`.
6. **Furnish** room-by-room to professional clearances; audit for overlaps and blocked doors. See `references/interior-and-area.md`.
7. **Context** as requested: site/plot + fence + trees, raised floor + plinth + ramp + entrance steps, terrace/balcony, pitched
   roof (tile vs metal), and a time-of-day / season **sun** that is physically correct for the building's latitude. All in
   `references/3d-threejs.md`.
8. **Hand off.** Keep a `HANDOFF.md` (conventions, coordinate system, what's where, open questions) so any later session can
   continue, and a `README.md` if it will be deployed as a static site.

## Conventions (essentials — full detail in references/conventions.md)

- **Units: mm everywhere.** Convert to metres only at the Three.js boundary (`/1000`).
- **Coordinate mapping:** plan `(x, y)` → 3D `(x, z=y)`, with **Y up**. So plan-y becomes 3D-z; "height" is Y.
- **Wall thickness:** exterior ~400, partitions ~100 (load-bearing internal sometimes 400). Dimensions are usually **by axis**;
  user-given room sizes are often **clear internal** — confirm which.
- **2D walls:** thick lines with `stroke-linecap="square"` so corners close. Doors/windows drawn *over* walls (erase a slice +
  draw the arc/glazing).
- **3D walls:** `THREE.Shape` with holes → `ExtrudeGeometry` gives real window/door openings. Add `EdgesGeometry` contours and a
  GTAO pass, or flat white walls look like a featureless blob.

## Related skills — use them, don't reinvent

- **interior-design-expert** — anthropometric clearances, lighting (IES), colour, space planning. Pull its
  `references/space-planning.md` for the numbers (bed side ≥600 mm, closet front ≥750, walkway 900–1200, toilet front ≥700).
- **skills-for-architects** (`01-site-planning`, `03-programming`, `06-materials-research`) — site/zoning, occupancy/area
  programming, and FF&E (`/product-research` to pick real furniture from a brief).
- **frontend-design** — for a distinctive in-app menu / HUD overlay (room selector, mode toggles) on the 3D viewer.

## Reference files (load as needed)

- `references/intake-interview.md` — **for non-technical users**: the ordered, plain-language question script to drive the whole
  project by interview (building type, floors, rooms, orientation, levels, roof, furniture), then build and show renders.
- `references/geometry-capture.md` — **fast plan capture**: shape-first (rectangle / L-Г / U-П) → derive & number exterior walls
  from a few defining dims → classify interior walls (load-bearing vs partition) → thickness by category with standards. Use this
  to get a real, correctly-proportioned outline in minutes instead of asking for every wall.
- `references/conventions.md` — units, axes, coordinate system, wall thickness, **how to calculate areas**, levels/datum.
- `references/2d-plans.md` — SVG plan pattern: data arrays, drawing walls/openings, hover tooltips.
- `references/3d-threejs.md` — full Three.js recipe: setup, walls/slabs, edges+GTAO, first-person, performance, per-floor
  furniture (`fb()` base-height), **physically-correct sun by latitude**, **pitched roof (tile vs metal)**, site/levels/terrace.
- `references/interior-and-area.md` — furniture clearances, room-by-room furnishing checklist, audit method.
- `references/verification.md` — the render-check loop (headless Chrome + SwiftShader, ImageMagick, temporary camera hashes).
