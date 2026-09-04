# Deploying this folder

The site already exists on Netlify:

- **Name:** `listen-when-sad-playlist`
- **Site ID:** `58a199d4-1ecd-4fb6-8492-a4207de2e9fb`
- **URL:** https://listen-when-sad-playlist.netlify.app
- **Admin:** https://app.netlify.com/projects/listen-when-sad-playlist

It has no files yet — the build environment that generated this is firewalled
off from Netlify, so the upload has to come from somewhere with network access.
Any one of these finishes it.

## A. Drag and drop (no tooling)

Open the admin link above → **Deploys** → drag this folder onto the drop zone.

## B. One command

From the repo root:

```
npx netlify-cli deploy --prod --dir=netlify-deploy --site=58a199d4-1ecd-4fb6-8492-a4207de2e9fb
```

## C. Connect the repo (best — auto-deploys on push)

Site → **Build & deploy** → link `keivnjonas/dosekeeper-legal`:

- Branch: `claude/jonasbrotbers-redesign-1aeefx`
- Build command: *(leave empty)*
- Publish directory: `netlify-deploy`

`netlify.toml` at the repo root already sets the publish directory, so only this
folder is served — the legal docs and build scripts are not.

## What lands where

| Path | Page |
|---|---|
| `/` | Playlist builder (the one to test) |
| `/survey/` | The listenwhensad survey |
| `/site/` | MySpace site mockup |

## Then, for Spotify

Add this exact string in the Spotify dashboard under Redirect URIs:

```
https://listen-when-sad-playlist.netlify.app/
```

It is already listed in the page's `redirectUris`, so once Spotify has it too,
**Connect Spotify** works and you can run the full round trip.
