# 🕌 Tathbeet — تثبيت | Smart Quran Memorization Tracker

A complete **Android application** for Quran memorizers to track, classify, and analyze their recitation mistakes word by word — with a built-in audio player, color-coded error system, and a personal analytics dashboard.

> **Download:** [`tathbeet.apk`](./tathbeet.apk)

---

<div style="text-align: center;">
  <img src="Gemini_Generated_Image_rt0sgfrt0sgfrt0s.png" alt="Tathbeet Logo" width="220"/>
</div>

---

## 📌 Project Overview

Tathbeet (تثبيت — meaning "to firmly establish") is a personal Quran companion app. It loads the full Quran with word-level audio timestamps, lets the user tap any word to log a mistake, and builds a visual analytics dashboard showing weak spots across all 114 surahs.

```
Word-Level Timestamps JSON (quran_timestamps.json)
        +
Quran Audio (alquran.cloud CDN)
        ↓
  Android WebView App (Capacitor + Gradle)
        ↓
  ┌─────────────────────────────────┐
  │  Splash Screen (splash.html)    │
  │  ↓                              │
  │  Quran Player + Error Logger    │
  │  ↓                              │
  │  Analytics Dashboard            │
  └─────────────────────────────────┘
```

---

## 🗂️ Project Structure

```
├── www/
│   ├── index.html              # Entry point (splash screen)
│   ├── main.html               # Main app — Quran player + dashboard
│   ├── landing.html            # Public landing page for APK download
│   ├── style.css               # Full app styling
│   ├── main.js                 # App logic — player, error tracking, charts
│   └── data/
│       └── quran_timestamps.json   # Word-level timestamps (from pipeline)
├── android/                    # Capacitor Android project (Gradle)
├── capacitor.config.json       # Capacitor configuration
├── tathbeet.apk                # ⬅️ Ready-to-install Android APK
└── Gemini_Generated_Image_rt0sgfrt0sgfrt0s.png   # App logo
```

---

## 📱 App Features

### 🔴 One-Tap Error Logging
Tap any word in the Mushaf while reviewing. A modal opens instantly — select the error type, add an optional note, and continue reciting without interruption.

### 🎨 Smart Color-Coded Classification
Three distinct error types, color-coded for instant visual recognition:

| Color | Type | Description |
|-------|------|-------------|
| 🔴 Red | نسيان / حفظ | Memorization lapse — forgot the word entirely |
| 🟠 Orange | تشكيل / لحن جلي | Tashkeel error — wrong diacritics or vowels |
| 🔵 Blue | تجويد / لحن خفي | Tajweed error — incorrect recitation rules |

### 🎵 Quran Audio Player
- Supports all 114 surahs, any aya range
- Multiple reciters via alquran.cloud CDN
- Word-by-word audio sync and highlighting
- Custom start aya selection mid-session

### 📊 Analytics Dashboard
- Donut chart — distribution of error types
- Bar chart — top 5 hardest surahs by error count
- KPI cards — total errors, per-type breakdown, hardest surah
- Error log table — last 10 errors with direct jump-to-word navigation

### 🛡️ 100% Private & Offline-Ready
All notes and errors are saved locally on the device using `localStorage`. No accounts, no servers, no ads, no subscriptions.

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript (Vanilla) |
| Charts | Chart.js |
| Fonts | Scheherazade New, Cairo (Google Fonts) |
| Audio | alquran.cloud CDN API |
| Mobile Wrapper | Capacitor 5 |
| Android Build | Gradle |
| Timestamps Data | WhisperX + wav2vec2 (from pipeline) |

---

## ⚙️ App Pages

### `index.html` — Splash Screen
Animated entry screen showing the Tathbeet logo with orbit rings, gold particles, and a loading bar. Auto-redirects to `main.html` after 2 seconds.

### `main.html` — Main Application
Two-tab layout:
- **القراءة والتسميع** — Quran reader with audio player and error logging
- **لوحة التحليل** — Analytics dashboard with charts and error history

### `landing.html` — Download Landing Page
A full Arabic landing page for sharing the APK link publicly. Includes hero section, features grid, how-it-works steps, and a direct APK download button. Designed for mobile-first sharing.

---

## 🚀 Build & Installation

### Prerequisites
- Node.js 18+
- Android Studio (with Android SDK)
- Java 17+

### Install Dependencies
```bash
npm install
```

### Sync Web Files to Android
```bash
npx cap sync android
npx cap copy android
```

### Open in Android Studio
```bash
npx cap open android
```

### Build APK
In Android Studio:
```
Build → Build Bundle(s) / APK(s) → Build APK(s)
```

Output path:
```
android/app/build/outputs/apk/debug/app-debug.apk
```

### Install Directly (USB)
```bash
npx cap run android
```

---

## 📲 Direct Install (No Build Needed)

Download the pre-built APK directly:

**[⬇️ Download tathbeet.apk](./tathbeet.apk)**

1. Transfer `tathbeet.apk` to your Android device
2. Open the file — you may need to allow **"Install from unknown sources"** in Settings → Security
3. Install and open **تثبيت**

> **Requires Android 6.0 (API 23) or higher.**

---

## 📄 Data — Word-Level Timestamps

The app uses `quran_timestamps.json` generated by a separate alignment pipeline:

- **Reciter:** Sheikh Mahmoud Khalil Al-Husary
- **Alignment model:** WhisperX + wav2vec2 Arabic
- **Coverage:** 114 surahs, 6,236 ayas, ~77,000 words
- **Format:**

```json
{
  "001": {
    "surah_number": 1,
    "surah_name": "Al-Faatiha",
    "ayat": {
      "001": {
        "aya_number": 1,
        "text": "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ",
        "words": [
          { "word": "بِسْمِ",      "start": 0.000, "end": 1.316, "score": 0.575 },
          { "word": "اللَّهِ",     "start": 1.336, "end": 1.480, "score": 0.292 },
          { "word": "الرَّحْمَنِ", "start": 1.501, "end": 1.809, "score": 0.078 },
          { "word": "الرَّحِيمِ",  "start": 1.830, "end": 5.283, "score": 0.519 }
        ]
      }
    }
  }
}
```

---

## 🙏 Acknowledgements

- Audio & Text: [alquran.cloud](https://alquran.cloud) API
- Alignment: [WhisperX](https://github.com/m-bain/whisperX)
- Compute for alignment pipeline: [Lightning.ai](https://lightning.ai) Studios (NVIDIA L4 GPU)
- App logo: Generated with Google Gemini

---

## 📜 License & Intent

This application is a **charitable work (صدقة جارية)** — built with the sole intention of serving the people of the Quran. It is free, ad-free, and open for anyone to use, learn from, or build upon.

> لا إعلانات · لا اشتراكات · لا تتبع · بياناتك على جهازك فقط
