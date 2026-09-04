#!/usr/bin/env python3
"""Render the link-preview image (og.png, 1200x630) from playlist.html.

The preview is a picture of the real thing, composed by the page's own card
code rather than a separate mock-up, so it cannot drift from what fans make.

The page composes the PNG itself and hands back a data URL, which this script
decodes. Screenshotting was the obvious approach and the wrong one: a canvas
scaled down by CSS rasterises unreliably in headless Chrome, and the bottom of
the card came out clipped while every measurement of the element said it was
the right size. Compositing in-page removes the guesswork - what the code draws
is exactly what is saved.

Usage:  python3 build-og.py [output.png]      ($CHROME to pick a browser)
"""
import base64, io, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'og.png')

SRC = None
for name in ('playlist.html', 'index.html'):
    if os.path.exists(os.path.join(HERE, name)):
        SRC = os.path.join(HERE, name)
        break
if not SRC:
    sys.exit('no playlist.html or index.html here')

CHROME = os.environ.get('CHROME', '/opt/pw-browsers/chromium')
if not os.path.exists(CHROME):
    sys.exit('no headless Chrome at %s - set $CHROME' % CHROME)

SONGS = [('Sucker', 'Jonas Brothers'),
         ('Cake By The Ocean', 'DNCE'),
         ('Year 3000', 'Jonas Brothers')]

COMPOSE = """
<div id="out" style="display:none"></div>
<script>
(function(){
  var songs = %s;
  var W = 1200, H = 630;

  function until(fn){ return new Promise(function(r){ (function t(){ fn()?r():setTimeout(t,40); })(); }); }

  function compose(){
    var card = document.getElementById('disc');
    var cv = document.createElement('canvas');
    cv.width = W; cv.height = H;
    var c = cv.getContext('2d');

    var bg = c.createLinearGradient(0, 0, 0, H);
    bg.addColorStop(0, '#111116');
    bg.addColorStop(1, '#08080B');
    c.fillStyle = bg; c.fillRect(0, 0, W, H);

    /* the card, whole, at the height the slot allows */
    var ch = H - 30, cw = ch * (card.width / card.height);
    c.drawImage(card, 74, 15, cw, ch);

    var x = 74 + cw + 78;
    c.textAlign = 'left';

    c.fillStyle = '#E8368F';
    c.font = '700 15px "Helvetica Neue",Arial,sans-serif';
    var kicker = 'J O N A S   B R O T H E R S';
    c.fillText(kicker, x, 214);

    c.fillStyle = '#FFFFFF';
    c.font = '400 50px "Rock Salt","Permanent Marker",cursive';
    c.fillText('Listen When Sad', x, 285);

    c.fillStyle = '#A09AA4';
    c.font = '400 21px "Helvetica Neue",Arial,sans-serif';
    c.fillText('Pin the song. Build the rest.', x, 345);
    c.fillText('Burn it to a disc.', x, 379);

    c.fillStyle = '#6E6E78';
    c.font = '700 15px "Helvetica Neue",Arial,sans-serif';
    c.fillText('J O N A S B R O T H E R S . C O M', x, 425);

    document.getElementById('out').textContent = cv.toDataURL('image/png');
    document.title = 'READY';
  }

  until(function(){ return document.querySelectorAll('#tracks .tr').length > songs.length; })
    .then(function(){
      var rows = document.querySelectorAll('#tracks .tr');
      songs.forEach(function(s, i){
        var row = rows[i+1];
        var t = row.querySelector('.t'), a = row.querySelector('.a');
        t.value = s[0]; t.dispatchEvent(new Event('input', {bubbles:true}));
        a.value = s[1]; a.dispatchEvent(new Event('input', {bubbles:true}));
      });
      /* wait for the marker faces, or the headline sets in a fallback serif */
      var fonts = document.fonts && document.fonts.ready
        ? document.fonts.ready : Promise.resolve();
      return fonts.then(function(){ return new Promise(function(r){ setTimeout(r, 400); }); });
    })
    .then(compose);
})();
</script>
"""

page = io.open(SRC, encoding='utf-8').read()
# A stored mix would show through, so start from a clean slate every time.
page = page.replace('<body>',
                    '<body>\n<script>try{sessionStorage.clear();localStorage.clear();}catch(e){}</script>', 1)
page = page.replace('</body>',
                    COMPOSE % repr(SONGS).replace("'", '"').replace('(', '[').replace(')', ']')
                    + '\n</body>', 1)

tmp = tempfile.mkdtemp()
src = os.path.join(tmp, 'og-compose.html')
io.open(src, 'w', encoding='utf-8').write(page)

dom = subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-sandbox',
                      '--user-data-dir=' + os.path.join(tmp, 'ud'),
                      '--virtual-time-budget=30000', '--window-size=1400,900',
                      '--dump-dom', 'file://' + src],
                     check=True, capture_output=True).stdout.decode('utf-8', 'replace')

m = re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)', dom)
if not m:
    sys.exit('the page did not produce an image - is the card rendering?')
io.open(OUT, 'wb').write(base64.b64decode(m.group(1)))
print('wrote %s (%d bytes)' % (OUT, os.path.getsize(OUT)))
