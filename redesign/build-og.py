#!/usr/bin/env python3
"""Render the link-preview image (og.png, 1200x630) from playlist.html.

The preview is a picture of the real thing, drawn by the page's own disc code
rather than a separate mock-up, so it cannot drift from what fans actually
make. Sample songs are typed in the same way a fan would.

Usage:  python3 build-og.py [output.png]   (needs a headless Chrome)
"""
import io, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'playlist.html')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'og.png')

CHROME = os.environ.get('CHROME', '/opt/pw-browsers/chromium')
if not os.path.exists(CHROME):
    sys.exit('no headless Chrome at %s - set $CHROME' % CHROME)

SONGS = [('Sucker', 'Jonas Brothers'),
         ('Cake By The Ocean', 'DNCE'),
         ('Year 3000', 'Jonas Brothers')]

CARD = """
<style>
  html,body{margin:0;width:1200px;height:630px;overflow:hidden;background:#0A0A0C;}
  .wrap{max-width:none;margin:0;}
  .panel,.disc-cap{display:none !important;}
  body{padding:0 !important;}
  /* The whole disc has to fit inside 630px of card height, with air. */
  .disc-stage{
    position:absolute !important;left:52px;top:29px;width:572px;height:572px;margin:0 !important;
  }
  #disc{width:572px !important;height:572px !important;}
  .og-copy{
    position:absolute;left:664px;top:0;width:492px;height:630px;
    display:flex;flex-direction:column;justify-content:center;gap:18px;
    font-family:"Helvetica Neue",Arial,sans-serif;color:#EDEDED;
  }
  .og-copy .kicker{
    font:700 15px/1 "Helvetica Neue",Arial,sans-serif;letter-spacing:.28em;
    text-transform:uppercase;color:#E8368F;
  }
  .og-copy h1{
    margin:0;font-family:"Rock Salt","Permanent Marker",cursive;font-weight:400;
    font-size:56px;line-height:1.26;color:#FFF;
  }
  .og-copy p{margin:0;font-size:20px;line-height:1.6;color:#A09AA4;}
  .og-copy .foot{font-size:15px;letter-spacing:.16em;text-transform:uppercase;color:#6E6E78;}
</style>
<div class="og-copy">
  <div class="kicker">Jonas Brothers</div>
  <h1>Listen When Sad</h1>
  <p>Pin the song. Build the rest.<br>Burn it to a disc.</p>
  <div class="foot">jonasbrothers.com</div>
</div>
<script>
(function(){
  var songs = %s;
  function until(fn){ return new Promise(function(r){ (function t(){ fn()?r():setTimeout(t,40); })(); }); }
  until(function(){ return document.querySelectorAll('#tracks .tr').length > songs.length; })
    .then(function(){
      var rows = document.querySelectorAll('#tracks .tr');
      songs.forEach(function(s, i){
        var row = rows[i+1];
        var t = row.querySelector('.t'), a = row.querySelector('.a');
        t.value = s[0]; t.dispatchEvent(new Event('input', {bubbles:true}));
        a.value = s[1]; a.dispatchEvent(new Event('input', {bubbles:true}));
      });
    });
})();
</script>
"""

page = io.open(SRC, encoding='utf-8').read()
# A stored mix would show through, so start from a clean slate every time.
page = page.replace('<body>', '<body>\n<script>try{localStorage.clear();}catch(e){}</script>', 1)
card = CARD % repr(SONGS).replace("'", '"').replace('(', '[').replace(')', ']')
page = page.replace('</body>', card + '\n</body>', 1)

tmp = tempfile.mkdtemp()
src = os.path.join(tmp, 'og-card.html')
io.open(src, 'w', encoding='utf-8').write(page)

subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-sandbox',
                '--hide-scrollbars', '--user-data-dir=' + os.path.join(tmp, 'ud'),
                '--virtual-time-budget=20000', '--window-size=1200,630',
                '--screenshot=' + OUT, 'file://' + src],
               check=True, capture_output=True)
print('wrote %s (%d bytes)' % (OUT, os.path.getsize(OUT)))
