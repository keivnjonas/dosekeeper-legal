# jonasbrotbers.com — 2006 MySpace redesign (concept)

A full-site redesign concept for **jonasbrotbers.com**, styled as a 2006 MySpace
profile. Built as a pitch artifact for the team.

Open `index.html` in a browser, or view the published version.

## What's in it

Three screens, switchable from the fake IE6 toolbar:

| Screen | MySpace analogue | Job it does |
|---|---|---|
| **Profile** | Personal profile page | Homepage — identity, contact actions, changelog, feature grid, testimonials |
| **Products** | Browse / friends list | Product index + featured product spec |
| **Support** | Blog entries | FAQ + privacy summary |

An **Annotations** toggle overlays 15 numbered markers and a pitch-notes panel
explaining what each 2006 module maps to in a modern marketing site. It also
highlights every placeholder value in yellow.

## Content sourcing

Live `jonasbrotbers.com` does not resolve from the build environment and
`dosekeeper.com` is blocked by the network egress proxy, so copy was written
from the verified material in this repo:

- Product features, support answers, and the contact address come from
  `SUPPORT.md` and `PRIVACY_POLICY.md` — these are accurate.
- Company facts (founded year, location, user count, ship date) are
  **placeholders**. They render with a yellow highlight when annotations are on.
- The testimonial block is marked `SAMPLE COPY` and needs real, permissioned
  quotes before any production use.

## Implementation notes

- Single file, no dependencies, no external requests.
- All system typefaces (Verdana / Arial Black / Courier New / Comic Sans) —
  that's what makes it read as 2006 rather than a filter over a modern page.
- Deliberately single-theme; every color is painted explicitly.
- `prefers-reduced-motion` disables the blink and marquee animations.
- Fixed 800px page inside an `overflow-x: auto` viewport, so the document
  itself never scrolls sideways.
- No photographs of real people were used; all avatars and product tiles are
  CSS-drawn.
