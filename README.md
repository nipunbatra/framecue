# 🎬 Video Subtitle Overlay

Play a local video with **synced subtitles** and a **constant metadata overlay**, all rendered
inside a single self-contained HTML file. Built for **sharing a Chrome tab** over Google Meet,
Zoom, or any screen share — because the subtitles and metadata are drawn into the page, they
show up in the shared view (unlike OS-level captions or a separate window).

**▶️ Live app:** https://nipunbatra.github.io/video-subtitle-overlay/app.html
**📖 Docs:** https://nipunbatra.github.io/video-subtitle-overlay/

## Demo

A ~37-second **linear-regression explainer** narrated with **Gemini TTS**, with synced subtitles and a constant metadata overlay, lives in [`demo/`](demo/). It ships in **three background styles** — all sharing the same narration/subtitles — so you can see how the subtitle overlay reads on different content:

- `demo-lecture.mp4` — dark [Manim](https://www.manim.community/) animation (3Blue1Brown-style)
- `demo-lecture-light.mp4` — the same animation on a **light** background
- `demo-lecture-slides.mp4` — a **light lecture-slides** montage

On the **[live page](https://nipunbatra.github.io/video-subtitle-overlay/#demo)** you can switch between them and cycle the **subtitle background** (`g`) — the effect is most visible on the light clips. Or open any `demo/*.mp4` (with its sibling `.vtt`/`.json`) in the app.

https://github.com/nipunbatra/video-subtitle-overlay/raw/main/demo/demo-lecture.mp4

## Features

- **Auto-matched files** — pick a folder; each video finds its same-named `.vtt`/`.srt` subtitles and `.json`/`.txt` metadata.
- **YouTube links too** — paste a link (or drag one onto the page); the video plays in an embedded player with the same overlays drawn on top.
- **Constant metadata overlay** — title, date, or any fields stay on screen for the whole clip.
- **Synced subtitles** — custom WebVTT/SRT renderer, resizable and repositionable for a shared screen.
- **Live timecode** — always-visible `current / duration` readout.
- **Presentation mode** — one key hides the UI so the video fills the tab.
- **100% local & private** — no uploads, no server, no dependencies. *(YouTube items naturally stream from YouTube — everything else stays on your machine.)*

## Usage

Name files with the **same base name** and put them in a folder:

```
my-folder/
├── talk.mp4      ← the video
├── talk.vtt      ← subtitles  (optional, or talk.srt)
└── talk.json     ← metadata overlay  (optional, or talk.txt)
```

`talk.json` renders as `key: value` lines:

```json
{
  "Lecture": "Linear Regression — Introduction to ML",
  "Topic": "Fitting a line to data",
  "Date": "30 Jun 2026"
}
```

A plain `talk.txt` is shown verbatim.

> **Don't want to hand-write JSON?** Click **✎ New metadata** in the app — add fields with a live preview, then download a ready-to-use `.json` (named to match your video) or apply it to the current clip instantly.

### YouTube links

Click **▶ YouTube link** and paste a URL — or just drag one from the address bar onto the page. The video plays in an embedded YouTube player with the same subtitle/metadata/timecode overlays drawn on top, so they still show up in a shared tab.

A YouTube item's *base name* is its **video ID**, so the usual same-name matching applies:

- **Metadata** — easiest: **✎ New metadata → Apply to current** (and **Download .json** to keep it for next time). Or add a `<video-id>.json` (e.g. `dQw4w9WgXcQ.json`) via **Pick files** / drag & drop.
- **Subtitles** — add a `<video-id>.vtt` the same way. (YouTube's own captions aren't accessible from an embed, so bring your own `.vtt`.)

Notes:

- Works on the **[hosted app](https://nipunbatra.github.io/video-subtitle-overlay/app.html)** or any http-served copy. YouTube refuses to play inside a page opened as a **local file** (`file://` sends no referrer → YouTube error 153) — if you downloaded `app.html`, serve it first: `python3 -m http.server`, then open `http://localhost:8000/app.html`. Local videos are unaffected either way.
- Videos whose owner disabled embedding won't play (YouTube error 150/101).
- Keyboard shortcuts work while the embedded player isn't focused.

Then:

1. Open the app and click **Pick folder** (or drag a folder onto the page).
2. Click a video in the sidebar — subtitles and metadata load automatically.
3. Share the **Chrome Tab** in Meet/Zoom and tick **“Also share tab audio.”**

> Playback uses the browser's codecs — **MP4 (H.264)** and **WebM** are safe. `.mkv`/`.avi` may not decode in Chrome.

## Keyboard shortcuts

| Key | Action |
|-----|--------|
| `Space` | Play / pause |
| `m` | Metadata on / off |
| `s` | Subtitles on / off |
| `t` | Timecode on / off |
| `b` | Subtitles bottom / top |
| `g` | Overlay background — subtitles, metadata & timecode (box → lighter → faint → frosted → no-box) |
| `+` / `−` | Subtitle size |
| `]` / `[` | Metadata size |
| `.` / `,` | Scale all overlays up / down |
| `v` | Move mode — drag any overlay anywhere (double-click to reset) |
| `p` | Presentation mode |
| `⇧→` / `⇧←` | Next / previous video |

## Run locally — just download one file

There's nothing to install and **nothing is ever uploaded** — your videos stay on your machine. The whole app is the single file [`app.html`](https://raw.githubusercontent.com/nipunbatra/video-subtitle-overlay/main/app.html). Download it, open it in Chrome, done.

**1. Download `app.html`**

- **macOS / Linux:**
  ```bash
  curl -O https://raw.githubusercontent.com/nipunbatra/video-subtitle-overlay/main/app.html
  ```
- **Windows (PowerShell):**
  ```powershell
  iwr https://raw.githubusercontent.com/nipunbatra/video-subtitle-overlay/main/app.html -OutFile app.html
  ```
- **Or no command line:** open the [raw file](https://raw.githubusercontent.com/nipunbatra/video-subtitle-overlay/main/app.html), then **Save Page As… → `app.html`**.

**2. Open it in Chrome**

- **macOS:** `open -a "Google Chrome" app.html`
- **Linux:** `google-chrome app.html`  *(or `xdg-open app.html`)*
- **Windows:** `start chrome app.html`  *(or just double-click the file)*

> A Chromium browser (Chrome, Edge, Brave) is recommended — **Pick folder** and **"share tab audio"** work best there.

Then point the app at a folder of videos (see [Usage](#usage)). It all runs inside the browser tab: no server, no sign-up, no upload.

*Developers:* you can still `git clone` the repo if you want the source, demo files and tests. The test suite (pytest + Playwright driving your installed Chrome, YouTube API mocked) runs with:

```bash
uv run --with pytest --with playwright pytest tests/ -q          # full suite
uv run --with pytest --with playwright pytest tests/ -q --live   # + real YouTube embed
```

## Roadmap

- **Open from Google Drive** — point the app at a shared Drive folder instead of a local one, so the same videos/subtitles/metadata can be played without downloading them first. *(Planned — today everything is strictly local.)*

## License

MIT © Nipun Batra
