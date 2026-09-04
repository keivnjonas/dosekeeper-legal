# Spotify setup — Listen When Sad playlist

Everything the app needs from the Spotify dashboard, and what to say when you
ask for the quota extension.

---

## 1. The app

Dashboard → your app → **Settings**.

**Redirect URIs** — Spotify matches these character for character. A missing
trailing slash is a rejected sign-in. Register every address the page is
served from:

```
https://www.jonasbrothers.com/listenwhensadplaylist/
https://listen-when-sad-playlist.netlify.app/
https://listen-when-sad-playlist.netlify.app/index.html
http://127.0.0.1:8000/
http://127.0.0.1:5500/
```

Local testing must use `127.0.0.1`, not `localhost` — Spotify treats them as
different hosts and only the numeric form is allowed over plain HTTP.

The same list lives in `__PL.spotify.redirectUris` in the page. It is not used
to authenticate anything; it is only so the page can say *"this address is not
registered"* instead of showing a button that silently fails.

**Which APIs** — Web API only. No playback, so no Web Playback SDK.

---

## 2. Scopes, and why each one

| Scope | Why |
|---|---|
| `playlist-modify-private` | Create the playlist on the fan's account (private is the default) |
| `playlist-modify-public` | Only used if the fan ticks **public** |
| `ugc-image-upload` | Upload their disc as the playlist's cover art |

Nothing reads the fan's library, listening history, or profile beyond the user
id and display name needed to create a playlist under their account.

---

## 3. The client secret

**There isn't one in play, and there must never be.**

Auth is Authorization Code with **PKCE**, which exists precisely so a static
page with no server can sign users in. The **client ID is public by design** —
it ships in the page, as it does in every PKCE app. The **client secret is
never used by this app and must never be pasted into any file in this repo**;
anything in a static page is readable by anyone who views source.

---

## 4. Development Mode — the current cap

Until Spotify grants an extension, the app is in Development Mode:

- **25 users maximum**, each added by hand in the dashboard
  (Settings → User Management) by name and the email on their Spotify account
- anyone not on that list gets a **403** — the page explains exactly this when
  it sees one, so a tester is not left guessing

That cap is the launch blocker. Everything else is built and tested.

---

## 5. Asking for the quota extension

Spotify's extension request is a form in the dashboard. What it asks for
changes from time to time, so treat the answers below as drafts to adapt
rather than a script — read the current form before pasting anything.

**What the app does** (draft):

> A page on the official Jonas Brothers website where fans build a "Listen When
> Sad" playlist. The first track is pinned by the artist; fans search Spotify
> for the rest. The page renders their tracklist as a burned CD, and — with
> their permission — creates that playlist on their own Spotify account and
> sets the CD image as the playlist cover. It is a fan engagement piece tied to
> the single; it does not stream, download, or alter any audio.

**Points worth making explicitly:**

- Playlists are created **on the fan's own account**, only when they press the
  button, and are **private by default**
- No audio is streamed, downloaded, or cached; no metadata is altered
- Spotify is credited on the page, and every search result links back to the
  track on Spotify
- The only content the app writes is a playlist name, description, tracklist,
  and a cover image the fan made
- Expected scale: say what you actually expect — a single-linked page on the
  band's site, so a launch spike then a long tail

**Have ready:** a screen recording of the real flow — connect, search, create,
open the playlist in Spotify. Do this **after** a real end-to-end run, not
before; see below.

**Flag it early:** this is an artist's official site, so it is commercial use
by a business, not a hobby project. Say so in the request. Spotify may route
a brand or label integration through a commercial agreement rather than the
standard extension, and finding that out at the start is much cheaper than
finding it out after launch is scheduled.

---

## 6. Before you record anything: one real run

The Spotify layer has been exercised against a mock covering the whole journey
and its failure paths (`test/run.sh`), but **it has never touched the live
API** — the machine it was written on cannot reach `accounts.spotify.com`.

Do this once on the deployed page, signed in as an account on the 25-user list:

1. **Connect Spotify** → accept every permission it asks for
2. Type a song by hand → it should show **ON SPOTIFY** within a second
3. Type nonsense → it should show **NOT FOUND**
4. **Create on Spotify** → open the playlist
5. Confirm: **Listen When Sad is track 1**, the other songs follow in disc
   order, and the cover art is the disc
6. Press **Update on Spotify** → confirm it edits that same playlist rather
   than creating a second one

If step 1 fails with a 403, the account is not on the allow-list. If step 5
shows the right songs but no cover, `ugc-image-upload` was not granted — sign
out, connect again, and accept the image permission.
