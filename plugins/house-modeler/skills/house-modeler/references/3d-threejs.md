# 3D model (Three.js) — full recipe

Single self-contained HTML. Same data arrays as the 2D plan (converted mm→m at use). Table of contents:
1. Setup · 2. Walls with real openings · 3. Slabs & voids · 4. Edges + ambient occlusion · 5. First-person walkthrough ·
6. Performance (on-demand + frozen shadows) · 7. Per-floor furniture (`fb()` base-height) · 8. Sun by latitude ·
9. Pitched roof (tile vs metal) · 10. Site, levels, ramp, steps, terrace, balcony · 11. Quick test hashes.

## 1. Setup
- Load Three.js via importmap from a CDN (jsdelivr), e.g. `three@0.171` + `examples/jsm` (OrbitControls, EffectComposer,
  RenderPass, **GTAOPass**, OutputPass). No build step.
- Renderer: `antialias`, `setPixelRatio(min(devicePixelRatio,1.5))`, `PCFSoftShadowMap`, ACES tone mapping.
- Lights: a `HemisphereLight`, a low `AmbientLight`, and one `DirectionalLight` "sun" with shadows. Keep references to all three
  so the sun slider can drive them.

## 2. Walls with real openings
```js
function buildWall(w, baseY, H, openings, grp){
  // build a THREE.Shape of the wall's vertical rectangle (length × H), punch each opening (sill→sill+h) as a hole,
  // ExtrudeGeometry by thickness t, position/rotate to the wall's plan line. Add glass quads in window holes.
}
```
`openingsFor(wall, list)` filters doors/windows that lie on this wall (same line, within span) and returns `{u0,u1,sill,h}` along
the wall. This gives genuine cut openings, not decals.

## 3. Slabs & voids
```js
function buildSlab(yTopMM, thickMM, holes, mat, grp){ /* Shape of the outer polygon, subtract hole polygons, extrude down */ }
```
Use a hole for a double-height void (second light). Floor slab at y0; ceiling/attic slab at the top; raise floor slabs per storey.

## 4. Edges + ambient occlusion (so white reads)
- Add `EdgesGeometry` line contours on every box/wall — white-on-white is invisible without them.
- Add a **GTAOPass** to the composer for soft corner shading. Without AO and edges a minimalist white model looks like a flat blob.

## 5. First-person walkthrough
- Two modes: orbit (OrbitControls, FOV ~45) and first-person (FOV ~74, eye height 1.6 m). A room menu teleports the camera to a
  room centroid and faces it inward. FP look = drag to yaw/pitch; WASD to walk; Esc back to orbit.

## 6. Performance (do all of these — naive loops overheat laptops)
- **Render on demand:** a `dirty` flag; the loop renders only when something changed (`controls` "change" event, slider moves,
  layer toggles, FP movement). In rest the GPU idles. This is the single biggest win.
- **Freeze shadows** after the first frame: `renderer.shadowMap.autoUpdate=false`; set `shadowMap.needsUpdate=true` only when
  lights/layers change (sun slider, toggling a floor/roof). Re-computing shadow maps every frame is what cooks the machine.
- **pixelRatio ≤ 1.5**, **shadow map 1024**, and **size the shadow camera frustum to the building**, not the whole yard — a huge
  frustum wastes shadow resolution and looks worse.
- **GTAO is the heaviest pass.** Keep it, but if a weak machine struggles expose a "quality" toggle that drops GTAO.
- **Static scene built once:** create geometry/materials at startup; never build meshes per frame. **Share materials** (one
  `wallMat`, one `edgeMat`, etc.) and reuse geometries where possible.
- **Don't cast shadows from far/minor decor** (distant trees, fence): `castShadow=false`. They're outside the shadow frustum
  anyway and only add cost.
- Net effect: idle = ~0% GPU; interaction = one render per change. A full 2-storey house + site + furniture stays smooth and cool.

## 7. Per-floor furniture — the `fb()` base-height pattern (IMPORTANT)
Furniture heights are absolute. If you place 2nd-floor furniture at heights 0–2200 it lands on the **ground floor**. Use a base:
```js
let FB = 0;                              // 0 = ground floor, 3000 = first floor, ...
const fb = (x0,z0,x1,z1,y0,y1,m) => box(x0,z0,x1,z1, y0+FB, y1+FB, m, FB?furn2:furn);
// helpers (bed, nstand, wardrobe, deskBox, chairBox, shelfUnit) all call fb() so they respect FB.
FB = 0;    /* ...ground-floor pieces... */
FB = 3000; /* ...first-floor pieces... */
FB = 0;
```
Keep **furniture groups per floor** and parent the upper group to that floor's group (`g2.add(furn2)`) so toggling a floor's
visibility hides its furniture too. A separate "Furniture" toggle controls both.

## 8. Sun by latitude (physically correct)
Don't fake an arc. Use the building's latitude φ and a season declination δ (−23.45°…+23.45°, 0 = equinox). At noon the sun is in
the **south** (N hemisphere), max elevation = 90−φ+δ (e.g. at 40°N: ~73° summer, ~50° equinox, ~26° winter — NOT 90°).
```js
const H = (hour-12)*15*Math.PI/180;                               // hour angle
const el = Math.asin(sinφ*sinδ + cosφ*cosδ*Math.cos(H));          // elevation
const g  = Math.atan2(Math.sin(H), Math.cos(H)*sinφ - Math.tan(δ)*cosφ);  // azimuth from SOUTH (+ toward west)
// place sun toward south=-z, with east/west on ±x as the user's orientation dictates (flip the x sign to match their compass)
```
Drive sun intensity/colour (warm low, white high), hemisphere/ambient, tone-mapping exposure, and sky colour from the elevation;
call `shadowMap.needsUpdate=true` on change. Expose a **time-of-day slider** and a **season slider**. Critical: the sun must rise
on the side the user calls *east* — confirm and flip the azimuth's x-component if needed.

## 9. Pitched roof — two real technologies, not just a colour
A toggle should switch **construction**, because tile and metal differ:
- **Tile (ceramic):** steeper pitch (~30°), water-shed by overlapping **horizontal courses**; render terracotta with thin
  horizontal course lines across each slope, thicker profile.
- **Standing-seam metal:** much lower pitch OK (~15° down to ~1:12), **vertical seams** ridge→eave; render sleek grey metallic
  with thin raised ribs running up each slope.
Build each as its own group (different ridge height + ribs), show one at a time, button toggles. Close gable ends with solid
(extruded) wall triangles, and close any notch end-wall (e.g. where a slope stops at a balcony) — open gable triangles read as
holes. Leave genuinely open areas (an uncovered balcony) open, but wall off the *roof's* exposed ends.

## 10. Site, levels, ramp, steps, terrace, balcony
- **Plot:** a lawn plane sized to the lot, a thin boundary line, a perimeter fence (low boxes) with a gate gap at the street,
  driveway + path, trees (trunk cylinder + low-poly icosahedron canopy; rows/bands; vary size deterministically).
- **Raised floor (+0.5 m):** lower ground to −0.5; add a plinth slab between −0.5 and 0; a tilted box **ramp** at the garage gate
  and **steps** (boxes from grade to floor) at entrances; the **terrace** is a platform whose top = floor level (flush with the
  back door) with steps down to the lawn.
- **Balcony:** a slab at the upper floor over a notch, with a parapet, reached by a door cut into the wall (add it to the door
  array so the opening is real).

## 11. Quick test hashes (temporary)
Add throwaway `location.hash` handlers for verification cameras/states (`#open` no roof, `#cut` ground floor only, `#fpN` enter
room N, plus ad-hoc ones like a top-down or a façade view), render, then **delete the temporary ones**. Keep only the stable
`#open`/`#cut`/`#fpN`.
