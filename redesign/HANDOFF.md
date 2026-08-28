# jonasbrothers.com as a 2006 MySpace page

A concept mockup: the band's site rebuilt as a MySpace profile, circa 2006.
Made as a pitch piece. **Not a live site, not production code, not affiliated
with anything.**

## Two copies, pick the right one

**Sharing it with people to look at?** Send `jonasbrothers-myspace.html` — one
file with the styles, scripts and artwork all inline. Nothing to keep next to
it, so forwarding it through email or chat cannot break it. This is the copy to
send for review.

**Working on the code?** Use this folder. `index.html` plus `assets/`, split
into real files.

Do not send the folder's `index.html` on its own: it points at `assets/` for the
photo, the crest, the CSS and the scripts, and mail clients routinely forward
the file without the folder. That is what makes the images disappear.

## Run it

Double-click either HTML file. That's the whole setup.

No build step, no package manager, no dependencies, no network requests.
It works from `file://`, from any static host, or dropped into an existing
site as a route.

```
index.html            the three screens, as markup
assets/styles.css     all styling — single theme, no framework
assets/glitter.js     the glitter engine + flames (canvas)
assets/app.js         screen switching + annotations layer
assets/band-photo.jpg YOU ADD THIS — see below
preview.png           what it should look like
```

## The artwork

Both real assets ship in this bundle:

```
assets/jb-crest.webp    the JB crest, transparent, 588x793
assets/band-photo.jpg   band photo, 600x400
assets/flames-bg.webp   the flames background, 500x500, tiled
```

They are wired through a single `window.__ASSETS` block near the bottom of
`index.html`. Change a path there and both the page and the glitter engine pick
it up — nothing else references the files directly.

**The crest keeps its own artwork.** Rather than masking our glitter field into
its silhouette, the engine draws the real logo and composites an animated
sparkle layer on top with `source-atop`, at 55% opacity. You get the actual red
glitter texture of the asset, with live twinkle over it. If the image ever fails
to load, it falls back to `SHAPE.crest`, an original drawn shield.

**The photo** renders at 150x150 with `object-fit: cover` and
`object-position: 50% 26%`, which frames the three faces rather than the
reaching hand. Swap in any crop; the slot handles any aspect ratio.

**Note on the single-file version.** The published page carries both images
inline as data URIs so it stays one self-contained file. `build-handoff.py`
decodes them back into `assets/` and rewrites the `__ASSETS` block to paths,
which is how this bundle got its image files. Edit `redesign/index.html`, re-run
the script, and both forms stay in sync.


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
- **Effects** — pauses every animation at once (glitter, cursor sparkles and the
  flames) and leaves a static frame, so you can talk over the page without it
  moving behind you.

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

## The survey

A fourth screen: the `listenwhensad. :]` survey, working. Fill it in, add a
photo, and it renders a shareable card.

Everything is driven by `__DATA.survey` — sections and questions, each with a
unique `id` that doubles as its localStorage key. Add, cut or reword questions
there and the form, the card and the copy-as-text output all follow.

How it behaves:

- **Answers** persist per-browser in `localStorage`, wrapped in try/catch so a
  private window or blocked storage degrades to a form that still works.
- **The photo** is read with `FileReader` and never leaves the device. It is
  cover-cropped into the card via a clipped `drawImage`.
- **The card** is drawn in canvas at 1080px wide with a measure pass first, so
  the height matches the content exactly and long answers wrap instead of
  clipping. Only answered questions are drawn.
- **Copy As Text** puts the filled survey on the clipboard — the way these
  actually spread in 2006, pasted into bulletins.
- **Share** opens X, Facebook, Tumblr and Reddit intents prefilled from the
  answers.

**Saving the image needs a runtime capability.** A published artifact cannot
start its own download, so the Save button calls the `downloads` capability
(`claude.use('downloads')`) and is **hidden unless that resolves**. The card
image always renders inline regardless, so a viewer without the capability can
still long-press or right-click it. If you host this yourself outside the
artifact runtime, swap that call for an `<a download>` and drop the capability
declaration.

## The flames

Supplied artwork, tiled along the bottom with `repeat-x` and
`background-size: auto 100%`, so it scales to the layer height and repeats
sideways however wide the window gets. The art's left and right edges are close
enough in value to tile without a visible seam.

A second copy sits on top, mirrored horizontally, blended with `screen` and
slowly drifting. That is what keeps a static image from reading as frozen, and
the mirroring further disguises the repeat. Both the drift and its opacity
flicker park when Effects is switched off, and under `prefers-reduced-motion`
the second layer holds still at a fixed opacity.

This replaced a generated fire simulation; the artwork reads better, and it
removed about 40 lines of per-frame canvas work from the render loop.

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
