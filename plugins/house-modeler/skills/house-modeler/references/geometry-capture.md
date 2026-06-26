# Fast geometry capture — get a real plan with the fewest questions

Getting to an accurate plan is the slow, painful part. Don't ask for 20 wall lengths. Capture the **shape** first, derive the
exterior walls from a handful of defining numbers, number them automatically, then handle interior walls by **class** and
thicknesses by **category**. The user should reach a confirmed outline in a couple of minutes.

**Number EVERY wall and talk in wall numbers.** Once the layout exists, give every wall a number — exterior *and* interior — and
show a plan with the numbers drawn on it. From then on, refer to walls by number in every question ("Is wall 7 load-bearing?",
"Where's the door in wall 11?", "Thickness of wall 5?"). Numbers are the shared language: they remove ambiguity and let the user
answer precisely and quickly instead of describing "the wall between the kitchen and the hall".

## Step 1 — Footprint shape (one multiple-choice question)
"Looking from above, what's the overall outline?" Offer:
- **Rectangle / square** — 4 corners, 4 exterior walls.
- **L-shape (Г-образный)** — 6 corners, 6 exterior walls (a rectangle with one corner cut out).
- **U-shape (П-образный)** — 8 corners, 8 exterior walls (a rectangle with a central notch).
- **T-shape** — 8 walls.
- **Other / I'll describe the corners** — fall back to listing corner points.

The shape immediately fixes **how many exterior walls there are**. (If "other", walk corners one at a time, clockwise.)

## Step 2 — Defining dimensions (only the few numbers the shape needs)
Ask just what defines that shape; everything else is computed. Give a one-line sketch so the number is unambiguous. Rough is fine.
- **Rectangle:** outer **width** and **depth**. (2 numbers.)
- **L / Г:** outer **width W**, outer **depth D**, then the **cut-out**: which corner, its **width** and **depth**. (L = big
  rectangle − a corner rectangle.)
- **U / П:** outer **W** and **D**, then the **notch**: its **width** and **depth**, and which side it opens to. (4–5 numbers.)
- **T:** the stem and the bar widths/depths.

```
 Rectangle              L / Г                       U / П
   ── 1 ──            ── 1 ──                    1a   1b
  4│     │2          │       │2          ┌────┐  ┌────┐
   ── 3 ──           │   ┌───┘ notch     │    │  │    │   notch
                     │   │ (cut corner)  │    └──┘    │
                     └───┘               └───────────┘
```

## Step 3 — Build the outline, number the walls, confirm
From shape + numbers, compute the corner polygon and **number the exterior walls clockwise, starting from the front-left (street)
corner**. Then **state every wall's computed length back** for confirmation:
> "Wall 1 (front) = 10.0 m · Wall 2 (right) = 13.0 m · Wall 3 = … — look right? Change any one number and I'll redo it."
Render the bare outline and show it. This is the moment to fix the shape cheaply, before any rooms.

## Step 4 — Anchor orientation to the numbering
Ask which wall faces the **street / entrance** (or which way is north). That fixes the compass and the numbering origin together,
so later the sun and labels are consistent. (See conventions.md.)

## Step 5 — Interior walls: number them all, then classify (talk in numbers)
Get the room layout (rooms + rough positions). Each room edge that isn't an exterior wall is an interior wall — you can place most
from the room sizes, so you rarely need to ask a length directly. Then:
1. **Number every interior wall**, continuing the sequence after the exterior ones (exterior 1..N, interior N+1, N+2, …).
2. **Show a fully-numbered plan** (render it with the numbers drawn on each wall) so the user can see which number is which.
3. **Ask everything by number.** Classify each: *"Wall 7 (kitchen ↔ hall) — load-bearing or a light partition?"* Heuristics to
   offer: walls that line up across floors or carry the floor/roof above are usually **load-bearing** (thicker); thin room
   separators are **partitions**. If the user doesn't know, assume partitions except a clearly major dividing wall → load-bearing,
   and **say what you assumed** (by number). Later, doors/windows are placed the same way: *"Which wall has the entrance — and is
   the door at the left or right end of wall 11?"*

## Step 6 — Thicknesses by CATEGORY (3 answers, not per wall)
Ask once per category and apply to all walls of that type. Offer standards up front so "I don't know" is one tap:
| Category | Default (mm) | Notes |
|---|---|---|
| Exterior | **400** (detached) / 250–300 (apartment) | inner face = axis − t/2 |
| Internal load-bearing | **200–400** | use 400 if it reads structural |
| Partition | **100** | |
> "Do you know your wall thicknesses, or shall I use standards (40 cm outside, 10 cm inner)?" → unknown = use the defaults.
If one wall differs from its category, the user can point to it **by number** ("walls 8 and 12 are thicker, 40 cm") — easy because
every wall is already numbered on the shown plan.

## Step 7 — Openings later
Do doors/windows AFTER the walls are confirmed (during the room walk-through). Keeping wall-capture to *shape → walls → thickness*
is what makes it fast — the user sees a real, correctly-proportioned outline quickly, then you fill in detail.

## Why this is fast
- Shape ⇒ wall count is known (no "how many walls?").
- A few defining dimensions ⇒ **all** exterior wall lengths are computed, not asked one by one.
- Thickness asked **per type** ⇒ 3 answers cover every wall.
- Auto-numbering + a confirm step ⇒ the user corrects one number instead of dictating a table.
