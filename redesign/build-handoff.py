#!/usr/bin/env python3
"""Build the team handoff bundle from redesign/index.html.

index.html is authored as a single self-contained file because that is what
the published artifact needs. Developers want real project files, so this
script splits that one file into index.html + assets/, keeping both in sync
from one source. Re-run it after any edit to redesign/index.html.

    python3 redesign/build-handoff.py [outdir]

Produces outdir/jonasbrothers-myspace-mockup/ and a .zip beside it.
"""
import base64, io, os, re, sys, shutil, zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'index.html')
NAME = 'jonasbrothers-myspace-mockup'
STANDALONE = 'jonasbrothers-myspace.html'
GLITTER_MARK = '  /* ================= GLITTER ENGINE'

APP_HEADER = """/* ------------------------------------------------------------------
   app.js - screen switching + the pitch annotations layer.
   No dependencies. Safe to load in any order alongside glitter.js.
   ------------------------------------------------------------------ */
"""

GLITTER_HEADER = """/* ------------------------------------------------------------------
   glitter.js - the 2006 glitter engine.

   Renders an animated glitter field on <canvas> and masks it into
   letterforms, which is how the glitter-text generators of the era
   worked. Drives four surfaces plus a full-page sparkle layer.

   Add a new glitter surface with markup alone:
     <canvas class="glitcv" width="880" height="200"
             data-glit="banner" data-pal="pink"></canvas>

   data-glit  keys into SPEC below for the text lines. A canvas whose
              key has no SPEC entry renders as a plain glitter bar.
   data-pal   keys into PAL: gold | pink | ice.

   TWO THINGS THAT WILL BITE YOU IF YOU REFACTOR THIS:

   1. All text lines are masked in ONE 'destination-in' composite
      against a single combined offscreen mask. Masking line by line
      does NOT work: 'destination-in' composites against the whole
      canvas per call, so line two intersects with line one and the
      text disappears entirely.

   2. The grain is drawn chunky (1.4-5px) on purpose. These canvases
      display at half their backing-store size, so 1px specks average
      away into a flat gradient.
   ------------------------------------------------------------------ */
"""


def build(outdir):
    src = io.open(SRC, encoding='utf-8').read()

    # Single self-contained file: styles, scripts and artwork all inline, no
    # relative paths at all. This is the copy to email around - forwarding it
    # without a folder cannot break it.
    standalone = os.path.join(outdir, STANDALONE)
    title_m = re.search(r'<title>(.*?)</title>', src, re.S)
    io.open(standalone, 'w', encoding='utf-8').write(
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '</head>\n<body>\n\n%s\n\n</body>\n</html>\n' % src)
    print('built %s (%d KB, self-contained)'
          % (standalone, os.path.getsize(standalone) // 1024))
    dest = os.path.join(outdir, NAME)
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    os.makedirs(os.path.join(dest, 'assets'))

    written_assets = {}
    src = extract_assets(src, dest, written_assets)

    title = re.search(r'<title>(.*?)</title>', src, re.S).group(1).strip()
    css = re.search(r'<style>(.*?)</style>', src, re.S).group(1).strip()
    # Must not span an earlier <script> (the __ASSETS block sits above this
    # one), so the captured body is forbidden from containing a closing tag.
    script_tag = re.search(r'<script>((?:(?!</script>)[\s\S])*)</script>\s*$', src)
    js = script_tag.group(1).strip()

    body = src.replace(script_tag.group(0), '')
    body = re.sub(r'<title>.*?</title>\s*', '', body, flags=re.S)
    body = re.sub(r'<style>.*?</style>\s*', '', body, flags=re.S).strip()

    if GLITTER_MARK not in js:
        sys.exit('glitter marker missing - did index.html change shape?')
    app_part, glit_part = js.split(GLITTER_MARK, 1)
    glit_part = GLITTER_MARK + glit_part

    # each half is self-contained, so give each its own IIFE
    app_part = app_part.replace('(function(){', '', 1).rstrip()
    glit_part = glit_part.rsplit('})();', 1)[0].rstrip()

    write(dest, 'assets/styles.css', css + '\n')
    write(dest, 'assets/app.js', '%s(function(){\n%s\n})();\n' % (APP_HEADER, app_part))
    write(dest, 'assets/glitter.js', '%s(function(){\n%s\n})();\n' % (GLITTER_HEADER, glit_part))
    write(dest, 'index.html', (
        '<!doctype html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>%s</title>\n'
        '<link rel="stylesheet" href="assets/styles.css">\n'
        '</head>\n<body>\n\n%s\n\n'
        '<script src="assets/app.js"></script>\n'
        '<script src="assets/glitter.js"></script>\n'
        '</body>\n</html>\n' % (title, body)))

    readme = os.path.join(ROOT, 'HANDOFF.md')
    if os.path.exists(readme):
        shutil.copy(readme, os.path.join(dest, 'README.md'))

    archive = os.path.join(outdir, NAME + '.zip')
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(dest):
            for f in sorted(files):
                full = os.path.join(base, f)
                z.write(full, os.path.relpath(full, outdir))
    if written_assets:
        print('extracted assets: %s' % ', '.join(sorted(written_assets.values())))
    print('built %s' % archive)


EXT = {'image/webp': '.webp', 'image/png': '.png',
       'image/jpeg': '.jpg', 'image/gif': '.gif', 'image/svg+xml': '.svg'}


def extract_assets(src, dest, written):
    """Turn the inlined __ASSETS data URIs back into real files.

    index.html carries the artwork inline so the published page stays a single
    self-contained file. Developers want actual image files, so each data URI
    is decoded into assets/ and the block is rewritten to point at the paths.
    """
    block = re.search(r'<script>[^<]*?window\.__ASSETS\s*=.*?</script>', src, re.S)
    if not block:
        return src

    paths = {}
    for name, uri in re.findall(r'(\w+)\s*:\s*"(data:[^"]+)"', block.group(0)):
        head, b64 = uri.split(',', 1)
        mime = head[5:].split(';')[0]
        fname = {'crest': 'jb-crest', 'photo': 'band-photo'}.get(name, name)
        fname += EXT.get(mime, '.bin')
        with open(os.path.join(dest, 'assets', fname), 'wb') as fh:
            fh.write(base64.b64decode(b64))
        paths[name] = 'assets/' + fname
        written[name] = fname

    if not paths:
        return src

    lines = ',\n'.join('  %s: "%s"' % (k, v) for k, v in sorted(paths.items()))
    return src.replace(block.group(0),
        '<script>\n/* Real artwork, kept as files in assets/. */\n'
        'window.__ASSETS = {\n%s\n};\n</script>' % lines)


def write(dest, rel, text):
    io.open(os.path.join(dest, rel), 'w', encoding='utf-8').write(text)


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else os.getcwd())
