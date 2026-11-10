# Quran in One Year — handoff for Codex (same as AGENTS.md)

Build an installable, offline-capable **web app (PWA)** called **"Quran in One Year"**. It reads the whole Quran in 365 days. Each day has Arabic, English transliteration and Bangla meaning for every ayah, plus a short English reading-practice summary that gets a little harder through the year.

It is a rebuild of an existing single-page app (`reference/original-index.html`). Keep **all of its features and its look**. The main change: **each user picks their own start date and name on first launch, and the whole plan's dates follow from that.** There is no server, no login, and no AI at runtime. Everything is static files.

Targets: any modern browser, **Android (Chrome install)** and **iPhone/iPad (Safari → Share → Add to Home Screen)**. Host on GitHub Pages (or Netlify / Cloudflare Pages).

---

## 1. What's in this folder

| Path | What it is |
|---|---|
| `reference/original-index.html` | The current app. Copy its design (CSS, colors, fonts, layout, icons, wording) and behavior. It was built for claude.ai, so remove all `window.claude` code. |
| `data/plan.json` | 365 items `{day, passages:[[surah, fromAyah, toAyah], ...]}`. The reading for each plan day. **No dates in it**: dates are computed from the user's start date. |
| `data/quran-data.json` | `Q[surah-1][ayah-1] = [arabic, transliteration, bangla]` for all 114 surahs (6,236 ayahs). About 4 MB. |
| `data/summaries.json` | `{"1": {...}, ..., "365": {...}}`, one summary per plan day (see §4). **Days 266–270 are missing** (see §7). |
| `data/sum/day-N.json` | The same summaries, one file per day (source of truth for editing). |
| `_source/en-days.json` | Saheeh International English for each day's ayahs: `[{day, date, ayahs:[{ref:"s:a", en}]}]`. Only needed to write or check summaries; **don't ship it in the app**. Ignore its `date` field. |
| `tools/RULES.md` | Rules for writing summaries (content, difficulty levels, format). |
| `tools/qtool.py` | `python3 tools/qtool.py show A B` prints English for days A..B; `check A B` validates `data/sum/day-N.json`. |
| `tools/build_summaries.py` | Merges `data/sum/*.json` into `data/summaries.json`. |

The surah names (`N`, English; `AR`, Arabic), `SC` (ayah count per surah) and `JUZ` (juz start points) arrays are inside `reference/original-index.html`. Move them into a JS module.

---

## 2. Features to keep (all from the original)

Four tabs in a fixed bottom tab bar, phone-first (max width 560 px), light and dark theme following the system:

1. **Today**
   - Decorative header: Basmala in Aref Ruqaa, gold ornament, "ختم القرآن", title, **"Assalamu alaikum, {name}"**.
   - Hero card: "Today · Day N · date", the passages (e.g. "Al-Baqarah 11–27"), ayah count, "about 10–15 min", a **Start reading / Read again** button, and the Arabic surah name as a watermark.
   - **Reading practice card**: level badge ("Level L · W words · about M min", M = max(1, round(W/100))), title, paragraphs each with an "Ayahs x:y-z" label, a "New words" list (word, simple meaning, Bangla), and an **"I read this summary"** toggle.
   - Tiles: day streak, days done, days left.
   - Progress ring (% of 365 done), on track / X days ahead / X days behind, "Next unread: Day N", a **Catch up** button.
   - **Ayah of the day**: the shortest ayah of 3 or more words from today's reading, in Arabic, transliteration and Bangla, with a **Listen** link to `https://quran.com/{s}/{a}`.
   - Closing line "رَبِّ زِدْنِي عِلْمًا".
2. **Read** (any day): header, the practice card, then every ayah (Arabic RTL in Amiri Quran, italic transliteration, Bangla in Noto Sans Bengali) with per-ayah and per-passage **Listen** links to quran.com. A **Mark Day N as done** toggle, ← / → day navigation, and the source credit line.
3. **Plan**: all 365 days grouped by month, each with a checkbox (done), "Day N + date", and the passage text (tap to open in Read). Today's row is highlighted and scrolled into view.
4. **Progress**: ayahs read out of 6,236, juz completed out of 30, surahs completed out of 114, streak, a 30-bar juz chart, and a 365-cell heatmap (done / not yet / today).

Keep the exact logic for streak, on-track / behind, next unread, juz and surah completion (see `vToday`, `vStats`, `streak`, `nextUnread` in the reference).

---

## 3. What's new or different

### 3.1 First-launch setup (required)
Before anything else, show a welcome screen in the same style:
- **Your name** (required, trimmed, max 30 characters). Used in "Assalamu alaikum, {name}".
- **Start date** (date picker, defaults to today, any past or future date allowed).
- Optional: **"I've already read up to Day ___"** (0–365). Marks those days done, for people switching from the old app. Default 0.
- Button: **Start my plan**.

Save `{name, startDate, createdAt}` in `localStorage` (`qy.settings`). Wrap every storage call in try/catch.

### 3.2 Dates follow the start date
- `dateOf(day) = startDate + (day − 1)` days, using **local dates** (no UTC drift; build dates with `new Date(y, m, d)`).
- `todayIndex = clamp(daysBetween(startDate, localToday), 0, 364)`. Before the start date, show Day 1 with a "Your plan starts on {date}" note. After Day 365, show a completion message ("You finished the whole Quran, MashaAllah") instead of the hero.
- Plan header: "365 days · {start} – {end}".
- **Summaries, levels and progress are keyed by plan day, never by date**, so changing the start date never breaks them.

### 3.3 Settings (new small screen)
Reach it from a gear icon on the Today header. It should let the user:
- Change name.
- Change start date (warn: "Your ticks stay on the same plan days; only the dates move").
- **Export progress** (download a JSON file) and **Import progress** (choose a file, then merge). This replaces the old cloud sync.
- **Reset everything** (with confirm).
- App version and source credits.

### 3.4 Remove
- All `window.claude.use('db')`, `use('user')` and cloud sync code.
- The "A new one is added every morning" text. Every summary is now bundled, so if one is missing, show "Summary not available for this day."

---

## 4. Data formats

Summary object (`summaries.json["N"]`):
```json
{"day":23,"level":1,"title":"One Faith, Giving, and the House at Makkah",
 "paragraphs":[{"ref":"3:84-85","text":"..."}],
 "words":150,
 "hardWords":[{"w":"repent","m":"to be sorry and stop doing wrong","bn":"তওবা করা"}]}
```
Older items might have `text` instead of `paragraphs`; support both, like the reference does.

Progress in `localStorage` key `qy.progress`:
```json
{"done":{"12":{"v":1,"t":1731200000000}}, "prac":{"12":{"v":1,"t":...}}}
```
`v` is 1 or 0, `t` is the change timestamp. Import merges by keeping the newer `t` per key (same as `mergeMeta` in the reference). On first run, also migrate the old keys `qmeta` / `qdone` / `qprac` if they exist.

Also remember the last tab (`qy.view`).

---

## 5. Tech requirements

- **Plain HTML, CSS and JS with no build step** (preferred, so it can be served as is from GitHub Pages). Small ES modules are fine. If you use Vite, output to `dist/` and add a Pages deploy workflow.
- Structure suggestion:
  ```
  index.html  app.js  plan.js  styles.css  manifest.webmanifest  sw.js
  icons/ (192, 512, maskable 512, apple-touch-icon 180)
  data/plan.json  data/quran-data.json  data/summaries.json
  ```
- **PWA**
  - `manifest.webmanifest`: name "Quran in One Year", short_name "Quran 365", `display: standalone`, `start_url: "./"`, `scope: "./"`, theme `#0f6b52`, background `#eef3f0`, icons.
  - iOS tags: `apple-mobile-web-app-capable`, `apple-mobile-web-app-status-bar-style`, `apple-touch-icon`, `viewport-fit=cover`. Keep the safe-area padding from the reference.
  - `sw.js`: pre-cache the app shell, `plan.json` and `summaries.json`. Cache `quran-data.json` and Google Fonts on first fetch (cache-first, then stale-while-revalidate). Use a versioned cache name and clean up old caches.
  - **Works fully offline after the first load.** The Listen links need internet; that's fine.
  - Show an "Install" hint: on Android use `beforeinstallprompt`; on iOS Safari show a one-time tip ("Tap Share → Add to Home Screen").
- Use **relative paths everywhere**, so it works under `https://<user>.github.io/<repo>/`.
- Fonts: same Google Fonts as the reference (Amiri, Amiri Quran, Aref Ruqaa, Noto Sans Bengali, Nunito Sans). Optionally self-host them in `fonts/` for better offline use.
- Accessibility: keep the tab roles, `lang="ar"` / `lang="bn"` on those texts, focus outlines, and `prefers-reduced-motion` handling.
- Performance: load `quran-data.json` once and show "Loading ayahs…" until it's ready. Render tabs on demand like the reference.

---

## 6. Acceptance checks

1. A fresh visit shows setup. After entering a name and start date, Today shows Day 1 on the start date with "Assalamu alaikum, {name}".
2. A start date of 10 days ago → Today shows Day 11, and the Plan dates line up (Day 11 = today).
3. A start date in the future → Day 1 with the "starts on" note.
4. Changing the start date in Settings keeps all ticks on the same day numbers.
5. Done and summary toggles survive a reload. Export, then reset, then import restores them.
6. Read tab: Day 1 shows Al-Fatihah 1–7 and Al-Baqarah 1–10, with Arabic, transliteration and Bangla.
7. A summary shows for every day that has one (spot check Days 1, 120, 240, 365).
8. Airplane mode after one full load: the app still opens and every day's text shows.
9. Lighthouse PWA "installable" passes. Add to Home Screen on iPhone opens full-screen.
10. No `window.claude` references remain.

---

## 7. Finish the missing summaries (Days 266–270)

`data/summaries.json` has 360 of 365 days. Days 266–270 still need writing:
1. Read `tools/RULES.md`.
2. Run `python3 tools/qtool.py show 266 270` to get the ayahs' English.
3. Write `data/sum/day-266.json` … `day-270.json` following the rules (Level 5: 300–350 words, 6 hardWords with Bangla). Use **only** what the English text says.
4. Run `python3 tools/qtool.py check 266 270` until it shows 0 errors.
5. Run `python3 tools/build_summaries.py` to rebuild `data/summaries.json`.

Until then, the app must show the "Summary not available" state for those days.

---

## 8. Credits (show in Read footer and in Settings)

"Text, transliteration and Bangla translation: quran-json by Risan Bagja Pradana (CC BY-SA 4.0), from QuranEnc and Tanzil. Daily summaries are based on the Saheeh International English translation." Listen links go to quran.com.
