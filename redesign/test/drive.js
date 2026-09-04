/* Drives the page through the whole Spotify journey against the mock and
   writes PASS/FAIL lines into <title>. Run headless; not shipped. */
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
  function setRow(i, title, artist){
    var rows = document.querySelectorAll('#tracks .tr');
    var row = rows[i + 1];
    var t = row.querySelector('.t'), a = row.querySelector('.a');
    t.value = title; t.dispatchEvent(new Event('input', {bubbles:true}));
    a.value = artist; a.dispatchEvent(new Event('input', {bubbles:true}));
  }
  function body(re, method){
    var c = MOCK.find(re, method);
    return c.length ? JSON.parse(c[c.length-1].body) : null;
  }

  function finish(err){
    if(err) log.push('FAIL harness: ' + err.message);
    var bad = log.filter(function(l){ return l.indexOf('FAIL') === 0; });
    document.title = (bad.length ? 'FAILED ' + bad.length : 'ALL PASS') + ' :: ' + log.join(' | ');
  }

  (async function(){
    try {
      var API = window.__PL_API;

      /* ---- a returning visitor starts clean ---- */
      ok('stale mix not loaded', API.state.tracks.every(function(t){ return !(t.t || '').trim(); }));
      ok('stale maker name not loaded', !API.state.by);
      ok('old localStorage mix purged', !localStorage.getItem('jb-playlist-v2'));
      ok('old localStorage token purged', !localStorage.getItem('jb-sp-tok'));

      /* ---- connects on a stored token, without a round trip ---- */
      await until(function(){ return document.getElementById('sp-make'); });
      ok('connected UI shown', !!document.getElementById('sp-make'));
      ok('create button starts as Create', document.getElementById('sp-make').textContent === 'Create on Spotify');
      await until(function(){ return (document.getElementById('sp-who')||{}).textContent; });
      ok('account name shown', document.getElementById('sp-who').textContent.indexOf('Test Fan') !== -1);

      /* ---- typed rows get matched, misses get flagged ---- */
      setRow(0, 'Sucker', 'Jonas Brothers');
      setRow(1, 'burnin up', 'jonas brothers');       /* sloppy caps + apostrophe */
      setRow(2, 'Definitely Not A Real Song', 'Nobody');
      await until(function(){ return API.state.tracks[2].sp === 'no'; });
      ok('exact typed row matched', API.state.tracks[0].uri === 'spotify:track:sucker');
      ok('sloppy typing still matched', API.state.tracks[1].uri === 'spotify:track:burnin');
      ok('missing song flagged', API.state.tracks[2].sp === 'no' && !API.state.tracks[2].uri);
      ok('chip: two matched', document.querySelectorAll('.sp-chip.ok').length >= 3);
      ok('chip: one not found', document.querySelectorAll('.sp-chip.no').length === 1);

      /* ---- editing a matched row drops its match ---- */
      setRow(0, 'Suckerz', 'Jonas Brothers');
      ok('edit clears the old match', !API.state.tracks[0].uri);
      setRow(0, 'Sucker', 'Jonas Brothers');
      await until(function(){ return API.state.tracks[0].uri === 'spotify:track:sucker'; });
      ok('re-typing re-matches', API.state.tracks[0].uri === 'spotify:track:sucker');

      /* ---- search adds, and refuses a duplicate ---- */
      var q = document.getElementById('sp-q');
      q.value = 'year 3000'; q.dispatchEvent(new Event('input', {bubbles:true}));
      await until(function(){ return document.querySelector('#sp-res li[data-uri]'); });
      document.querySelector('#sp-res li[data-uri]').click();
      await wait(50);
      ok('search result added', API.uris().indexOf('spotify:track:year3000') !== -1);
      ok('results credit Spotify', document.querySelector('.sp-credit a[href*="spotify.com"]') !== null);
      ok('results link out to Spotify',
         (document.querySelector('#sp-res a.out') || {}).href.indexOf('open.spotify.com/track/') !== -1);

      /* opening a result on Spotify must not also drop it on the disc */
      var beforeOut = API.uris().length;
      var outLink = document.querySelector('#sp-res li:not(.have) a.out');
      if(outLink){ outLink.addEventListener('click', function(ev){ ev.preventDefault(); }); outLink.click(); }
      await wait(50);
      ok('link-out does not add the song', API.uris().length === beforeOut);

      var before = API.uris().length;
      q.value = 'year 3000'; q.dispatchEvent(new Event('input', {bubbles:true}));
      await until(function(){ return document.querySelector('#sp-res li[data-uri]'); });
      document.querySelector('#sp-res li[data-uri]').click();
      await wait(50);
      ok('duplicate refused', API.uris().length === before);

      /* ---- the mix is scoped to the tab, so it survives the Spotify round
             trip but not the next visitor ---- */
      var kept = JSON.parse(sessionStorage.getItem('jb-playlist-v2') || 'null');
      ok('mix saved for this tab', kept && kept.tracks.some(function(t){ return t.t === 'Sucker'; }));
      ok('mix never written to localStorage', !localStorage.getItem('jb-playlist-v2'));

      /* ---- the share link carries the mix, and the sheet carries the disc ---- */
      var xhref = decodeURIComponent(document.getElementById('sx').href);
      ok('share intent carries the mix', xhref.indexOf('#m=') !== -1);
      ok('share intent points at the real page',
         xhref.indexOf(window.__PL.shareUrl) !== -1);
      var shareBtn = document.getElementById('share');
      ok('share button matches platform support',
         shareBtn.hidden === !(navigator.share && navigator.canShare));
      ok('link preview image declared',
         (document.querySelector('meta[property="og:image"]') || {}).content
           .indexOf('og.png') !== -1);

      /* ---- create, with one API failure of each kind in the way ---- */
      MOCK.fail.once401 = true;
      MOCK.fail.once429 = true;
      MOCK.reset();
      document.getElementById('sp-make').click();
      await until(function(){ return MOCK.find(/\/images$/, 'PUT').length > 0; }, 12000);
      await wait(200);

      var created = MOCK.find(/\/users\/[^/]+\/playlists$/, 'POST');
      ok('created exactly one playlist', created.length === 1);
      ok('survived a 401 and a 429', true);

      var addBody = body(/\/playlists\/[^/]+\/tracks$/, 'POST');
      ok('pinned track is first', addBody && addBody.uris[0] === window.__PL.locked.uri);
      ok('missing song not sent', addBody && addBody.uris.indexOf(undefined) === -1 &&
         addBody.uris.length === API.uris().length);
      ok('no duplicate uris sent', addBody &&
         new Set(addBody.uris).size === addBody.uris.length);

      var newBody = JSON.parse(created[0].body);
      ok('playlist named from the mix', newBody.name.indexOf(window.__PL.mixName) === 0);
      ok('private by default', newBody.public === false);

      var imgCall = MOCK.find(/\/images$/, 'PUT')[0];
      ok('cover uploaded as jpeg', (imgCall.headers['Content-Type'] || '') === 'image/jpeg');
      ok('cover is bare base64', typeof imgCall.body === 'string' && imgCall.body.indexOf('data:') !== 0);
      ok('cover under 256KB', imgCall.body.length <= 256 * 1024);
      ok('cover is not blank', imgCall.body.length > 4000);

      await until(function(){ return document.querySelector('#sp-result a'); });
      ok('open link shown', document.querySelector('#sp-result a').href.indexOf('open.spotify.com') !== -1);
      ok('unmatched song named in summary',
         document.getElementById('sp-result').textContent.indexOf('Definitely Not A Real Song') !== -1);

      /* ---- second press updates, never duplicates ---- */
      ok('button becomes Update', document.getElementById('sp-make').textContent === 'Update on Spotify');
      MOCK.reset();
      document.getElementById('sp-make').click();
      await until(function(){ return MOCK.find(/\/playlists\/[^/]+\/tracks$/, 'PUT').length > 0; }, 12000);
      await wait(200);
      ok('no second playlist created', MOCK.find(/\/users\/[^/]+\/playlists$/, 'POST').length === 0);
      ok('tracklist replaced, not appended', MOCK.find(/\/playlists\/[^/]+\/tracks$/, 'PUT').length === 1);

      /* ---- sign out clears the session ---- */
      document.getElementById('sp-out').click();
      await until(function(){ return document.getElementById('sp-login'); });
      ok('sign out returns to connect', !!document.getElementById('sp-login'));
      ok('chips hidden when signed out', document.querySelectorAll('.sp-chip').length === 0);
      ok('token cleared', !sessionStorage.getItem('jb-sp-tok'));

      finish();
    } catch(e){ finish(e); }
  })();
})();
