#!/usr/bin/env python3
"""Generate the mocked test page from playlist.html.

The mock has to replace fetch BEFORE the page's own scripts run, and the
driver has to run after them, so the page is assembled rather than iframed.
Regenerate whenever playlist.html changes.
"""
import io, os, sys

here = os.path.dirname(os.path.abspath(__file__))
# In this repo the page is playlist.html; in the handoff bundle it ships as
# index.html. Take whichever is there so the tests run in both.
src = None
for name in ('playlist.html', 'index.html'):
    cand = os.path.join(here, '..', name)
    if os.path.exists(cand):
        src = cand
        break
if not src:
    sys.exit('no playlist.html or index.html next to test/')
page = io.open(src, encoding='utf-8').read()
mock = io.open(os.path.join(here, 'spotify-mock.js'), encoding='utf-8').read()
drive = io.open(os.path.join(here, 'drive.js'), encoding='utf-8').read()

# A stored token, so the page comes up already connected and the driver does
# not have to leave the origin to sign in.
boot = """<script>
try {
  localStorage.removeItem('jb-playlist-v2');
  localStorage.removeItem('jb-sp-playlist');
  localStorage.setItem('jb-sp-tok', JSON.stringify({
    access:'AT-0', refresh:'RT-0', exp: Date.now() + 3600000
  }));
} catch(e){}
</script>
<script>%s</script>""" % mock

if page.count('<body>') != 1:
    sys.exit('expected exactly one <body>')
out = page.replace('<body>', '<body>\n' + boot, 1)

# Treat the test's own file:// address as a registered redirect URI, so the
# signed-out screen offers Connect rather than the "unregistered origin"
# notice - production runs from a registered address and must be what is
# under test here.
reg = ('</script>\n<script>\n(function(){\n  var CFG = window.__PL;')
if out.count(reg) != 1:
    sys.exit('could not find the config/app script boundary')
out = out.replace(reg,
    '</script>\n<script>\n'
    'window.__PL.spotify.redirectUris.push(location.origin + location.pathname);\n'
    '</script>\n<script>\n(function(){\n  var CFG = window.__PL;', 1)

if out.count('</body>') != 1:
    sys.exit('expected exactly one </body>')
out = out.replace('</body>', '<script>%s</script>\n</body>' % drive, 1)

io.open(os.path.join(here, 'run.html'), 'w', encoding='utf-8').write(out)
print('wrote test/run.html (%d bytes)' % len(out))

# ---- second page: the failure paths -------------------------------------
# Same page, but the stored token is already stale so the first call has to
# refresh, and a different driver.
drive2 = io.open(os.path.join(here, 'drive2.js'), encoding='utf-8').read()
boot2 = boot.replace('exp: Date.now() + 3600000', 'exp: 0')
out2 = page.replace('<body>', '<body>\n' + boot2, 1)
out2 = out2.replace(reg,
    '</script>\n<script>\n'
    'window.__PL.spotify.redirectUris.push(location.origin + location.pathname);\n'
    '</script>\n<script>\n(function(){\n  var CFG = window.__PL;', 1)
out2 = out2.replace('</body>', '<script>%s</script>\n</body>' % drive2, 1)
io.open(os.path.join(here, 'run2.html'), 'w', encoding='utf-8').write(out2)

# The shared-mix link the second driver expects to have been opened with.
import base64, json
mix = json.dumps({"b": "Nick", "t": [["Lovebug", "Jonas Brothers"], ["Year 3000", "Jonas Brothers"]]},
                 separators=(',', ':'))
packed = base64.urlsafe_b64encode(mix.encode('utf-8')).decode('ascii').rstrip('=')
io.open(os.path.join(here, 'run2.hash'), 'w', encoding='utf-8').write('#m=' + packed)
print('wrote test/run2.html (%d bytes) + run2.hash' % len(out2))
