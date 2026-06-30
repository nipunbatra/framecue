# 🎬 Video Subtitle Overlay

Play a local video with **synced subtitles** and a **constant metadata overlay**, all rendered
inside a single self-contained HTML file. Built for **sharing a Chrome tab** over Google Meet,
Zoom, or any screen share — because the subtitles and metadata are drawn into the page, they
show up in the shared view (unlike OS-level captions or a separate window).

**▶️ Live app:** https://nipunbatra.github.io/video-subtitle-overlay/app.html
**📖 Docs:** https://nipunbatra.github.io/video-subtitle-overlay/

## Features

- **Auto-matched files** — pick a folder; each video finds its same-named `.vtt` subtitles and `.json`/`.txt` metadata.
- **Constant metadata overlay** — title, date, or any fields stay on screen for the whole clip.
- **Synced subtitles** — custom WebVTT renderer, resizable and repositionable for a shared screen.
- **Live timecode** — always-visible `current / duration` readout.
- **Presentation mode** — one key hides the UI so the video fills the tab.
- **100% local & private** — no uploads, no server, no dependencies.

## Usage

Name files with the **same base name** and put them in a folder:

```
my-folder/
├── talk.mp4      ← the video
├── talk.vtt      ← subtitles  (optional)
└── talk.json     ← metadata overlay  (optional, or talk.txt)
```

`talk.json` renders as `key: value` lines:

```json
{
  "Lecture": "Introduction to Machine Learning, 14",
  "Lecture Date": "20 Feb 2024"
}
```

A plain `talk.txt` is shown verbatim.

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
| `+` / `−` | Subtitle size |
| `]` / `[` | Metadata size |
| `p` | Presentation mode |
| `⇧→` / `⇧←` | Next / previous video |

## Run locally

No build step:

```bash
git clone https://github.com/nipunbatra/video-subtitle-overlay
open video-subtitle-overlay/app.html   # macOS
```

## License

MIT © Nipun Batra
