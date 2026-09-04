/* ------------------------------------------------------------------
   A fake Spotify, good enough to drive every branch of the real layer.

   The live API is unreachable from the machine this was built on, so this
   stands in for it: it records every call, answers to the documented shapes,
   and can be told to fail on purpose (401 once, 429 once) so the retry and
   refresh paths get exercised rather than assumed.

   Injected BEFORE the page's own scripts. Not shipped to production.
   ------------------------------------------------------------------ */
window.MOCK = (function(){
  var calls = [];
  var fail = {};                       /* one-shot failures, by key */
  function track(id, name, who){
    return {uri:'spotify:track:' + id, name:name, artists:[{name:who}],
            external_urls:{spotify:'https://open.spotify.com/track/' + id}};
  }
  var CATALOGUE = [
    track('sucker',   'Sucker',               'Jonas Brothers'),
    track('cake',     'Cake By The Ocean',    'DNCE'),
    track('burnin',   "Burnin' Up",           'Jonas Brothers'),
    track('lovebug',  'Lovebug (Remastered)', 'Jonas Brothers'),
    track('year3000', 'Year 3000',            'Jonas Brothers')
  ];

  function res(status, bodyObj, headers){
    var text = bodyObj === undefined ? '' :
               (typeof bodyObj === 'string' ? bodyObj : JSON.stringify(bodyObj));
    return Promise.resolve({
      ok: status >= 200 && status < 300,
      status: status,
      headers: {get: function(k){ return (headers || {})[k.toLowerCase()] || null; }},
      text: function(){ return Promise.resolve(text); },
      json: function(){ return Promise.resolve(text ? JSON.parse(text) : null); }
    });
  }

  function matches(q){
    /* Understands both track:"x" artist:"y" and a plain phrase. */
    var t = (q.match(/track:"([^"]+)"/) || [])[1];
    var a = (q.match(/artist:"([^"]+)"/) || [])[1];
    var plain = (!t && !a) ? q : null;
    function n(x){ return String(x||'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim(); }
    return CATALOGUE.filter(function(tr){
      var name = n(tr.name), who = n(tr.artists[0].name);
      if(plain){
        var p = n(plain);
        return p.split(' ').filter(Boolean).every(function(w){
          return name.indexOf(w) !== -1 || who.indexOf(w) !== -1;
        });
      }
      if(t && name.indexOf(n(t)) === -1 && n(t).indexOf(name) === -1) return false;
      if(a && who.indexOf(n(a)) === -1) return false;
      return true;
    });
  }

  var playlists = {};
  var nextId = 1;

  window.fetch = function(url, opts){
    opts = opts || {};
    var u = String(url);
    var method = opts.method || 'GET';
    calls.push({url: u, method: method, body: opts.body, headers: opts.headers || {}});

    if(u.indexOf('accounts.spotify.com/api/token') !== -1){
      if(fail.refresh){ fail.refresh = false; return res(400, {error:'invalid_grant'}); }
      return res(200, {access_token:'AT-' + (++nextId), refresh_token:'RT-1', expires_in:3600});
    }

    var path = u.replace(/^https:\/\/api\.spotify\.com\/v1/, '');

    if(fail.once401){ fail.once401 = false; return res(401, {error:{status:401}}); }
    if(fail.once429){ fail.once429 = false; return res(429, '', {'retry-after':'1'}); }
    if(fail.once500){ fail.once500 = false; return res(503, 'upstream'); }
    if(fail.forbid){ return res(403, {error:{status:403, message:'Forbidden'}}); }

    if(path === '/me') return res(200, {id:'fan1', display_name:'Test Fan'});

    if(path.indexOf('/search') === 0){
      var q = new URLSearchParams(path.split('?')[1]).get('q') || '';
      return res(200, {tracks:{items: matches(q)}});
    }

    var mkPl = path.match(/^\/users\/([^/]+)\/playlists$/);
    if(mkPl && method === 'POST'){
      var id = 'PL' + (++nextId);
      var b = JSON.parse(opts.body);
      playlists[id] = {id:id, name:b.name, public:b.public, description:b.description, uris:[], image:null};
      return res(201, {id:id, external_urls:{spotify:'https://open.spotify.com/playlist/' + id}});
    }

    var trk = path.match(/^\/playlists\/([^/]+)\/tracks$/);
    if(trk){
      var pl = playlists[trk[1]];
      if(!pl) return res(404, {error:{status:404, message:'Not found'}});
      var body = JSON.parse(opts.body);
      if(method === 'POST'){ pl.uris = pl.uris.concat(body.uris); return res(201, {snapshot_id:'s1'}); }
      if(method === 'PUT'){ pl.uris = body.uris.slice(); return res(200, {snapshot_id:'s2'}); }
    }

    var img = path.match(/^\/playlists\/([^/]+)\/images$/);
    if(img && method === 'PUT'){
      var p2 = playlists[img[1]];
      if(!p2) return res(404, {error:{status:404}});
      p2.image = opts.body;
      return res(202, undefined);
    }

    var det = path.match(/^\/playlists\/([^/]+)$/);
    if(det && method === 'PUT'){
      var p3 = playlists[det[1]];
      if(!p3) return res(404, {error:{status:404}});
      Object.assign(p3, JSON.parse(opts.body));
      return res(200, undefined);
    }

    return res(404, {error:{status:404, message:'mock has no route for ' + method + ' ' + path}});
  };

  return {
    calls: calls,
    playlists: playlists,
    fail: fail,
    reset: function(){ calls.length = 0; },
    find: function(re, method){
      return calls.filter(function(c){ return re.test(c.url) && (!method || c.method === method); });
    }
  };
})();
