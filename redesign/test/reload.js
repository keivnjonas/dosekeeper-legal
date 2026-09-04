/* Third suite: the mix must survive leaving the page and coming back, which
   is what connecting Spotify does - and must NOT survive into a fresh visit.
   Runs the page in an iframe so it can be navigated for real rather than
   assumed. Not shipped. */
(function(){
  var log = [];
  function ok(n, c){ log.push((c ? 'PASS ' : 'FAIL ') + n); }
  function until(fn, ms){
    ms = ms || 10000;
    var t0 = Date.now();
    return new Promise(function(res, rej){
      (function tick(){
        var v; try { v = fn(); } catch(e){ v = null; }
        if(v) return res(v);
        if(Date.now() - t0 > ms) return rej(new Error('timeout'));
        setTimeout(tick, 40);
      })();
    });
  }
  function finish(err){
    if(err) log.push('FAIL harness: ' + err.message);
    var bad = log.filter(function(l){ return l.indexOf('FAIL') === 0; });
    document.title = (bad.length ? 'FAILED ' + bad.length : 'ALL PASS') + ' :: ' + log.join(' | ');
  }

  var frame = document.getElementById('f');
  function win(){ return frame.contentWindow; }
  function doc(){ return frame.contentDocument; }

  function load(url){
    return new Promise(function(res){
      frame.onload = function(){ res(); };
      frame.src = url;
    }).then(function(){
      return until(function(){ return win().__PL_API; });
    });
  }

  (async function(){
    try {
      var PLAIN = 'plain.html';

      await load(PLAIN);
      ok('first visit starts blank',
         win().__PL_API.state.tracks.every(function(t){ return !(t.t || '').trim(); }));

      var rows = doc().querySelectorAll('#tracks .tr');
      var t = rows[1].querySelector('.t'), a = rows[1].querySelector('.a');
      t.value = 'Lovebug'; t.dispatchEvent(new (win().Event)('input', {bubbles:true}));
      a.value = 'Jonas Brothers'; a.dispatchEvent(new (win().Event)('input', {bubbles:true}));
      doc().getElementById('pl-by').value = 'kevin';
      doc().getElementById('pl-by').dispatchEvent(new (win().Event)('input', {bubbles:true}));
      await until(function(){ return win().__PL_API.filled().length === 1; });

      /* Leaving and coming back is exactly what the Spotify redirect does. */
      await load(PLAIN + '?code=fake-auth-code');
      ok('mix survives the Spotify round trip',
         win().__PL_API.filled().length === 1 &&
         win().__PL_API.state.tracks[0].t === 'Lovebug');
      ok('maker name survives it too', win().__PL_API.state.by === 'kevin');

      /* A plain reload is the same tab, so it keeps it too. */
      await load(PLAIN);
      ok('mix survives a reload', win().__PL_API.filled().length === 1);

      /* Clear is the fan's own reset. */
      doc().getElementById('clear').click();
      await until(function(){ return win().__PL_API.filled().length === 0; });
      await load(PLAIN);
      ok('Clear wipes it for good', win().__PL_API.filled().length === 0);

      /* And nothing was ever left in localStorage for the next visitor. */
      ok('nothing persisted to localStorage',
         !win().localStorage.getItem('jb-playlist-v2') &&
         !win().localStorage.getItem('jb-sp-tok'));

      finish();
    } catch(e){ finish(e); }
  })();
})();
