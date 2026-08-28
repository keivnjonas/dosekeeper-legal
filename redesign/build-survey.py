#!/usr/bin/env python3
"""Extract the survey from index.html into a standalone page.

The survey is authored once, inside the site mockup. This pulls its CSS,
markup, data and script out into redesign/survey.html so it can be tested
and deployed on its own URL without keeping a second copy by hand.
Re-run after editing the survey in index.html.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'index.html')
OUT = os.path.join(ROOT, 'survey.html')


def slice_between(text, start, end, what):
    i = text.find(start)
    if i < 0:
        sys.exit('marker missing: ' + what)
    j = text.find(end, i + len(start))
    if j < 0:
        sys.exit('end marker missing: ' + what)
    return text[i:j]


def balanced(text, start_marker, open_ch, close_ch, what):
    """Return start_marker plus text through its matching closing bracket."""
    i = text.find(start_marker)
    if i < 0:
        sys.exit('marker missing: ' + what)
    j = text.find(open_ch, i)
    depth, k = 0, j
    while k < len(text):
        if text[k] == open_ch:
            depth += 1
        elif text[k] == close_ch:
            depth -= 1
            if depth == 0:
                return text[i:k + 1]
        k += 1
    sys.exit('unbalanced: ' + what)


def build():
    src = io.open(SRC, encoding='utf-8').read()

    css = slice_between(src,
                        '/* ---------- survey ---------- */',
                        '/* ---------- scrollable show list ---------- */', 'css')

    # divs need real nesting counting, not bracket matching
    i = src.find('<div class="sv">')
    depth, k, end = 0, i, None
    for m in re.finditer(r'<(/?)div\b[^>]*>', src[i:]):
        if not m.group(1):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                end = i + m.end()
                break
    if end is None:
        sys.exit('could not close .sv markup')
    markup = src[i:end]
    markup = re.sub(r'<span class="anno">\d+</span>', '', markup)   # pitch marker

    data = balanced(src, '  survey: {', '{', '}', 'survey data')
    data = data[data.find('{'):]

    js = slice_between(src, '  /* ==================== SURVEY ====================', '\n  })();', 'js')
    js += '\n  })();'

    page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>listenwhensad. :]</title>
<style>
*{box-sizing:border-box;}
body{
  margin:0;padding:22px 12px 44px;background:#DCE6F2;
  font-family:"Andale Mono","Lucida Console","Courier New",monospace;
  font-size:13px;color:#000000;
}
a{color:#0A2ED6;}
a:focus-visible,button:focus-visible{outline:2px solid #FF6600;outline-offset:1px;}
%s
</style>
</head>
<body>

%s

<script>
window.__DATA = { survey: %s };
</script>
<script>
(function(){
%s
})();
</script>
</body>
</html>
""" % (css, markup, data, js)

    io.open(OUT, 'w', encoding='utf-8').write(page)
    print('built %s (%d KB)' % (OUT, os.path.getsize(OUT) // 1024))


if __name__ == '__main__':
    build()
