# Guided intake interview (for non-technical users)

When the user is **not** a programmer — they just want a model of their home and will answer questions — YOU drive the project
with a friendly, ordered interview. They only answer and look at pictures; you write all the code. This file is the script.

## Rules of the interview
- **Be fast — answer in seconds, not minutes.** Each question is simple; just ask it. Don't plan the whole house before speaking,
  don't re-think the model every turn, and don't load all the references — pull only the one you need for this step. The user is
  watching a "thinking…" spinner; long pauses on a trivial question (e.g. "what's the total width?") feel broken. Save real
  reasoning for genuinely tricky geometry, and even then keep it brief.
- **Plain language only.** Never say "Three.js", "array", "millimetres", "mesh", "extrude", or show code. Say *rooms*, *the street
  side*, *the front door*, *floor*, *roughly how wide*. Translate everything for them.
- **Ask one topic at a time**, in small batches. Use **multiple-choice** (AskUserQuestion) for genuine choices — building type,
  number of floors, orientation, roof, furnish yes/no. Use **plain free-text** for the open answers — **dimensions and room
  lists** (don't force these into buttons). For every free-text question, **be concrete: give the exact format you want with a
  short example**, so the user just copies the shape of the answer (see the size and rooms questions below).
- **Offer sensible defaults** and let them accept: "Most houses have ~40 cm exterior walls and 10 cm inner walls — I'll use that
  unless you know otherwise." Don't make them supply numbers they don't have.
- **Show a picture early and often.** After the first floor outline, render it and show them, so they see progress and can correct
  before you go further. Confirm each stage before moving on.
- **Never ask them to edit anything.** They answer; you build, render, and refine.
- If they DON'T have exact dimensions, accept rough ones ("about 4 by 5 metres") or even "make it a normal size" and proceed with
  reasonable values, stating what you assumed.

## Required parameters — capture EVERY one (none are optional)
Before building, you must have all of these. Don't silently skip any (the floor/wall **height** is the one most often forgotten —
always ask it). If the user doesn't know a value, **offer a standard, confirm it, and record it** — but never leave it blank:
- [ ] Building type · number of **floors**
- [ ] **Floor / wall height** per storey (e.g. 3.0 m houses, 2.7 m apartments) — ASK THIS, don't assume silently
- [ ] Footprint **shape** + defining dimensions (→ all exterior wall lengths)
- [ ] **Wall thicknesses** by category (exterior / load-bearing / partition)
- [ ] **Orientation** (which side faces the street / north) + entrance location
- [ ] Plot/yard (for a house): size, front/back, fence · Garage: yes/where
- [ ] **Rooms** per floor (+ stairs, hall) · interior walls classified (load-bearing vs partition)
- [ ] Levels (raised floor? ramp/steps), terrace, balcony · **Roof** (flat / tile / metal / later)
- [ ] Furniture (full / main rooms / none) · style
Tick them off as you go; if any is still missing when you're about to build, ask for it first.

## Question flow (in order)

**1 — What are we building?** (multiple-choice)
- Apartment (one level inside a building) · Detached house · Townhouse/duplex · Other.

**2 — Floors & height.** How many floors? (1 / 2 / 3 / more.) Basement or attic? And — **always ask** — **how tall is each floor**
(wall/storey height)? Offer a default (3.0 m houses, 2.7 m apartments) but get an answer; don't assume it silently.

**3 — Footprint shape & exterior walls (the fast part — use `geometry-capture.md`).** Don't ask for many wall lengths. First ask
the **overall outline shape** (Rectangle/square · L-shape Г · U-shape П · T · other) — that fixes how many walls there are. Then
ask only the **few defining dimensions** as **plain free text with a concrete example**, e.g.: *"Just type the overall size as
width × length in metres — e.g. `7 × 10`. (For an L/U shape, also the cut-out, e.g. `cut-out 3 × 2`.) Approximate is fine — or say
'guess it' and I'll use a typical size."* Then **auto-number the exterior walls clockwise**, state each computed length back for a
one-number confirm, and render the bare outline. Ask **wall thickness by category** (exterior / load-bearing / partition) with
standards offered if they don't know. Full protocol: `geometry-capture.md`.

**4 — Orientation & entrance** (multiple-choice, only for houses with land). "Which side faces the street / where's the main
entrance?" (North / South / East / West / Not sure.) Confirm which way is north — this fixes the sun later. If unsure, pick a
sensible default and tell them they can change it.

**5 — The plot / yard** (if a house). Roughly how big is the land? Where's the front yard vs the back garden? Any fence?

**6 — Garage & parking.** Garage? attached or separate? which side? car enters from the street side.

**7 — Rooms, floor by floor (free text, concrete prompt).** Ask per floor with an explicit format and an example, and let them
locate rooms by the **compass sides** or the **wall numbers** from the plan they just saw:
> *"List the rooms on this floor, one per line, with roughly where each sits — for example:*
> *  kitchen — top-left (by walls 1 & 6)*
> *  living room — top-right*
> *  bedroom — bottom-right corner*
> *  bathroom — middle, next to the bedroom*
> *Add a rough size if you know it (e.g. `4 × 5 m`); if not, I'll use sensible sizes and we'll check it on the plan."*
Keep this as free text — don't force it into buttons. Then ask specifically where the **stairs** and the **entrance/hall** go (on
multi-floor homes), again by side or wall number. Confirm the layout on a rendered plan before moving on.

**8 — Levels & outdoor features** (multiple-choice where possible).
- Is the ground floor raised above the yard (steps/ramp up to the door)? roughly how much?
- A terrace/patio? a balcony? where?
- Roof: flat · pitched with **tile** · pitched with **metal** · decide later.

**9 — Finish & furniture** (multiple-choice).
- Furnish the rooms? (yes, fully · just the main rooms · empty for now.)
- Style: minimal/white · warm/wood · other.

## Then build — show pictures, and GATE on the 2D before any 3D
Report in plain language and confirm at each stage:
1. Draw **floor 1** (outline + walls + rooms) → render, show.
2. Other floors the same way → render, show each.
3. **2D approval gate (REQUIRED).** When the 2D plans are done, explicitly ask: *"Is everything correct on the plans, or is there
   anything to change?"* Make any changes and re-show. **Loop here until the user says it's all good.** Do **not** start the 3D
   until the 2D is approved — the 3D is generated from the same numbers, so fixing geometry on the 2D first avoids redoing the 3D.
4. **Only after the 2D is confirmed** → build the 3D model → show an overview render.
5. Furnish to standard clearances → show top-downs / a walk-through.
6. Add yard, roof, sun, levels as chosen → show.
At the end, offer the walkthrough ("open this file, click a room to step inside") and, if they want it online, the deploy README.

## Tone
Be warm, concrete, and reassuring. They're trusting you with their home; a quick picture beats a paragraph. When something is
ambiguous, ask **one** simple question rather than guessing — but keep momentum; don't interrogate. The goal: a non-programmer
ends up with a real 2D plan + walkable 3D model just by chatting and looking at renders.
