/* Second pass: the paths a fan hits when things go wrong - an expired token,
   a rejected refresh, an account Spotify will not serve - plus a shared mix
   link. Runs against the mock. Not shipped. */
(function(){
  var log = [];
  function ok(name, cond){ log.push((cond ? 'PASS ' : 'FAIL ') + name); }
  function wait(ms){ return new Promise(function(r){ setTimeout(r, ms); }); }
  function until(fn, ms){
    ms = ms || 8000;
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
  function status(){ return document.getElementById('status').textContent; }
  function finish(err){
    if(err) log.push('FAIL harness: ' + err.message);
    var bad = log.filter(function(l){ return l.indexOf('FAIL') === 0; });
    document.title = (bad.length ? 'FAILED ' + bad.length : 'ALL PASS') + ' :: ' + log.join(' | ');
  }

  (async function(){
    try {
      var API = window.__PL_API;

      /* ---- the mix travelled in the link ---- */
      ok('shared mix loaded from link', API.state.tracks.length === 2 &&
         API.state.tracks[0].t === 'Lovebug' && API.state.tracks[1].t === 'Year 3000');
      ok('shared maker name loaded', API.state.by === 'Nick');
      ok('shared mix is on the disc', API.filled().length === 2);

      /* ---- a stale access token refreshes itself ---- */
      await until(function(){ return document.getElementById('sp-make'); });
      await until(function(){ return MOCK.find(/accounts\.spotify\.com\/api\/token/).length > 0; });
      ok('stale token was refreshed', MOCK.find(/accounts\.spotify\.com\/api\/token/).length >= 1);
      ok('still connected after refresh', !!document.getElementById('sp-make'));
      var tok = JSON.parse(sessionStorage.getItem('jb-sp-tok'));
      ok('new token stored with an expiry', tok && tok.access.indexOf('AT-') === 0 && tok.exp > Date.now());

      /* ---- Spotify refuses the account: the likeliest launch failure ---- */
      MOCK.fail.forbid = true;
      document.getElementById('sp-make').click();
      await until(function(){ return status().indexOf('403') !== -1; }, 12000);
      ok('403 names the Development Mode cap', status().indexOf('Development Mode') !== -1);
      ok('403 tells them what to do', status().indexOf('connect again') !== -1);
      ok('create button re-enabled after failure',
         document.getElementById('sp-make').disabled === false);
      ok('button label restored', document.getElementById('sp-make').textContent.indexOf('Spotify') !== -1);
      MOCK.fail.forbid = false;

      /* ---- a refresh token Spotify will not honour ---- */
      var t = JSON.parse(sessionStorage.getItem('jb-sp-tok'));
      t.exp = 0; sessionStorage.setItem('jb-sp-tok', JSON.stringify(t));
      MOCK.fail.refresh = true;
      document.getElementById('sp-make').click();
      await until(function(){ return document.getElementById('sp-login'); }, 12000);
      ok('dead session returns to Connect', !!document.getElementById('sp-login'));
      ok('dead session clears the token', !sessionStorage.getItem('jb-sp-tok'));
      ok('dead session says so', status().indexOf('session ended') !== -1);

      /* ---- and the disc still works with Spotify gone ---- */
      ok('disc survives sign-out', API.filled().length === 2);
      ok('no chips while signed out', document.querySelectorAll('.sp-chip').length === 0);

      finish();
    } catch(e){ finish(e); }
  })();
})();
