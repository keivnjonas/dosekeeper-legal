# jonasbrothers.com as a 2006 MySpace page (concept mockup)

A mockup of **jonasbrothers.com** styled as a 2006 MySpace band profile.
Built as a pitch piece. Not a live site and not affiliated with anything.

Open `index.html` in a browser.

## What's in it

Three screens, switchable from the fake IE6 toolbar:

| Screen | MySpace analogue | What it holds |
|---|---|---|
| **Profile** | Band profile page | Identity, contact table, music player, band details, tour dates, blog, Top 8, fan comments |
| **Music** | Band music page | Latest release, discography grid, streaming links |
| **Tour** | Shows listing | Full routing, date filters, venue info |

## Glitter and flames

Five animated glitter surfaces, all drawn in canvas — no image assets:

- a **glitter graphic** header (pink) captioned as copy-paste fan art
- a **divider bar** under the marquee
- a **fan-made glitter graphic** posted in the comments (ice blue)
- the **JB crest** in the left column (red), masked from a drawn shape rather
  than text — this is the hook for swapping in real logo artwork
- the **profile wordmark** (gold), still available but currently replaced by
  the band photo slot

Behind everything: a Doom-fire flames background burning in the margins, plus a
full-page sparkle layer where glitter falls ambiently and trails the cursor,
with a burst on click. An **Effects** toolbar toggle pauses all of it at once
(leaving a static frame), and `prefers-reduced-motion` starts it paused.

Three implementation notes worth keeping if this is ever rebuilt:

- The glitter is masked with a single `destination-in` composite against **one
  combined offscreen mask**. Masking line-by-line does not work —
  `destination-in` composites against the whole canvas per call, so the second
  line intersects with the first and the text disappears.
- The grain is drawn deliberately chunky (1.4–5px). These canvases display at
  half their backing-store size, so 1px specks average away to a flat gradient.
- The fire is scaled up with smoothing left **on**. That soft upscale is what
  makes it read as a blurry tiled fire GIF instead of a crisp gradient, and the
  simulation is primed with 180 frames so the page opens already burning.

An **Annotations** toggle overlays 18 numbered markers and a notes panel
arguing the thesis: this band was made on MySpace in 2006, and a MySpace
profile already contains every module a modern artist site needs. It also
highlights every placeholder value in yellow.

## Accuracy

Real and current as of August 2026:

- *Greetings from Your Hometown* (Aug 8, 2025), the seventh studio album
- The Burning Up Tour: All Over Again — 45 North American dates
- Opening night Sep 25 at TD Garden, Boston; final night Dec 21 at
  Prudential Center, Newark
- Three Madison Square Garden shows, Aug 20–22, 2026
- Special guests: Magnus Ferrell, Franklin Jonas, All Time Low
- New single "Listen When Sad", debuted live at MSG

Placeholder (highlighted yellow when annotations are on):

- Friend counts
- The TBA routing rows between opening and closing night

Placeholder artwork — drop the real files in, no code change needed:

- **`assets/band-photo.jpg`** fills the profile photo slot automatically
- The **JB crest** is an original drawn shield, not the band's real crest.
  Swap it by pointing `SHAPE.crest` at your asset (see HANDOFF.md).

The fan comments are invented and carry a visible `SAMPLE COPY` tag.
Song titles appear as titles only — no lyrics.

## Implementation notes

- Single file, no dependencies, no external requests.
- All system typefaces (Verdana / Arial Black / Courier New / Comic Sans) —
  that's what makes it read as 2006 rather than a filter over a modern page.
- Deliberately single-theme; every color is painted explicitly.
- `prefers-reduced-motion` disables the blink and marquee animations.
- Fixed 800px page inside an `overflow-x: auto` viewport, so the document
  itself never scrolls sideways.
- No photographs are used; all avatars, album sleeves, glitter and tiles are
  drawn in CSS or canvas.
- The wordmark is original type, not the band's actual logo artwork.
