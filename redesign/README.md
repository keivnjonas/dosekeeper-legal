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

An **Annotations** toggle overlays 17 numbered markers and a notes panel
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

- Profile view / friend counts
- The TBA routing rows between opening and closing night

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
- No photographs are used; all avatars, album sleeves and tiles are CSS-drawn.
