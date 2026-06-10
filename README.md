# 🐻‍❄️ YouTube No Autoplay

A minimal Chrome extension that prevents YouTube videos from auto-playing when you restore tabs or sync them across devices.

**Videos play only when you click play.**

---

## The problem

When Chrome restores your previous session, or when a YouTube tab syncs from another device, the video starts playing automatically — often with sound. This extension stops that.

## How it works

The extension listens for the browser's native `play` event on YouTube video pages. If the event fires without a real user interaction (a click or keypress), it immediately pauses the video. That's all it does.

## Features

- Blocks autoplay on tab restore and cross-device sync
- On/Off toggle in the Chrome toolbar popup
- Zero data collection — no servers, no tracking, no analytics
- ~20 lines of JavaScript

## Install

**From the Chrome Web Store** *(coming soon)*

**Manually (developer mode):**

1. Clone this repo
2. Go to `chrome://extensions/`
3. Enable **Developer mode**
4. Click **Load unpacked** → select the `extension/` folder

## Privacy

This extension collects nothing. The only data stored locally is whether the toggle is on or off.  
→ [Full privacy policy](https://robkasta.github.io/youtube-no-autoplay/privacy-policy.html)

## License

MIT — free to use, modify, and share.
