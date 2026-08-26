# jonasbrothers.com as a 2006 MySpace page

A concept mockup: the band's site rebuilt as a MySpace profile, circa 2006.
Made as a pitch piece. **Not a live site, not production code, not affiliated
with anything.**

## Run it

Double-click `index.html`. That's the whole setup.

No build step, no package manager, no dependencies, no network requests.
It works from `file://`, from any static host, or dropped into an existing
site as a route.

```
index.html            the three screens, as markup
assets/styles.css     all styling — single theme, no framework
assets/glitter.js     the glitter engine (canvas)
assets/app.js         screen switching + annotations layer
preview.png           what it should look like
```

## What's in it

Three screens, switchable from the fake IE6 toolbar:

| Screen | MySpace analogue | Holds |
|---|---|---|
| **Profile** | Band profile | Identity, contact table, music player, band details, tour dates, blog, Top 8, fan comments |
| **Music** | Band music page | Latest release, discography grid, streaming links |
| **Tour** | Shows listing | Full routing, date filters, venue info |

Two toolbar toggles:

- **Annotations** — overlays 18 numbered markers and a notes panel mapping each
  MySpace module to the job a modern artist site gives it. This is the thing to
  present from. It also highlights every placeholder value in yellow.
- **Glitter** — pauses all animation and leaves a static frame, so you can talk
  over the page without it shimmering behind you.

## Before this goes anywhere public

**Accurate as of August 2026** — safe to keep:

- *Greetings from Your Hometown* (Aug 8, 2025), the seventh studio album
- The Burning Up Tour: All Over Again — 45 North American dates
- Opening night Sep 25, TD Garden Boston; final night Dec 21, Prudential Center Newark
- Three Madison Square Garden shows, Aug 20–22, 2026
- Special guests: Magnus Ferrell, Franklin Jonas, All Time Low
- New single "Listen When Sad", debuted live at MSG

**Placeholder — needs real data.** Highlighted yellow when annotations are on:

- Profile view and friend counts
- The TBA routing rows between opening and closing night

**Invented — replace or remove:**

- All fan comments. They carry a visible `SAMPLE COPY` tag. Real quotes need
  real permission.
- The wordmark is original type, **not the band's actual logo artwork**. If you
  want the real logo, see "Swapping in the real logo" below.

Song titles appear as titles only. No lyrics, no photographs — every avatar,
album sleeve and sparkle is drawn in code.

## Notes for whoever picks this up

**It's deliberately single-theme.** A 2006 screen has one look. Every color is
painted explicitly rather than inherited, so it holds on any background.

**Accessibility is real, not decorative.** Focus states are visible,
`prefers-reduced-motion` starts the glitter paused, canvases carry labels, and
the fixed 800px page sits inside an `overflow-x: auto` viewport so the document
never scrolls sideways.

**Two glitter gotchas** — both are commented in `glitter.js`, and both will
silently break the effect if you refactor past them:

1. All text lines are masked in **one** `destination-in` composite against a
   single combined offscreen mask. Masking line by line does not work:
   `destination-in` composites against the whole canvas per call, so line two
   intersects with line one and the text vanishes entirely.
2. The grain is drawn **chunky** (1.4–5px) on purpose. These canvases display at
   half their backing-store size, so 1px specks average away to a flat gradient.

**Adding a glitter surface** takes markup only:

```html
<canvas class="glitcv" width="880" height="200"
        data-glit="banner" data-pal="pink"></canvas>
```

`data-glit` keys into `SPEC` for the text lines; a key with no `SPEC` entry
renders as a plain glitter bar. `data-pal` keys into `PAL` — `gold`, `pink`,
or `ice`.

### Swapping in the real logo

The engine masks glitter into any shape, not just text. To use real logo
artwork, replace the body of `maskFor()` so it draws your asset instead of
`fillText` — a transparent PNG or an SVG path both work:

```js
function maskFor(cv, lines){
  if(cv._mask) return cv._mask;
  var m = document.createElement('canvas');
  m.width = cv.width; m.height = cv.height;
  m.getContext('2d').drawImage(logoImage, 0, 0, cv.width, cv.height);
  cv._mask = m;
  return m;
}
```

Everything else — the animated field, the glow, the toggle — keeps working
unchanged. Note the mask is cached per canvas, so make sure the image has
loaded before the first draw.
