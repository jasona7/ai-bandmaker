# UX / Accessibility / Design-System Review — 2026-07-18

**Reviewer:** Jennifer Mitchelle (Senior UX Design Critic).
**Supersedes:** the prior 2026-07-17 run (audit #32). This is an independent re-derivation from source,
line-by-line; the prior file's conclusions were NOT inherited. Contrast ratios were recomputed from the
real hex values against the actual backgrounds they render on.
**Summary:** 0 CRITICAL, 1 HIGH, 1 MEDIUM, 4 LOW.
**Fix-scope applied:** the 1 HIGH was fixed (`templates/generate.html`). MEDIUM/LOW logged, not fixed.
**Scope:** `templates/base.html`, `index.html`, `generate.html`, `gallery.html`, `static/css/style.css`,
`static/js/main.js`, and `app.py` / `createAct.py` for route + template wiring and model-output escaping.
**Standard:** WCAG 2.1 AA (2.2 additions noted where relevant).

**Key divergence from the prior run:** the prior review found the same `innerHTML` model-output injection
but filed it as an "out-of-scope security observation" and changed no code. The parent's fix-scope for this
run explicitly names "un-escaped output" and "XSS/injection into the DOM." Under that scope it is an
in-scope HIGH, and it has been fixed.

**Note:** The 1996 GeoCities aesthetic (Comic Sans, `blink`, neon-on-dark, table layout, visitor counter,
under-construction banner, tiled starfield) is intentional and is NOT flagged. Contrast and motion defects
*inside* that aesthetic are still flagged.

---

## Summary of counts

| Severity | Count | Disposition |
|----------|-------|-------------|
| CRITICAL | 0 | — |
| HIGH | 1 | FIXED (`templates/generate.html`) |
| MEDIUM | 1 | LOGGED, not fixed (out of fix-scope) |
| LOW | 4 | LOGGED, not fixed (out of fix-scope) |

---

## Phase 1 — AUDIT (findings)

### HIGH

**H1 — DOM-based XSS: raw model-generated `band_name` written via `innerHTML`. (FIXED)**
`templates/generate.html` — `showSuccess()`, was lines 311–314:
```js
preview.innerHTML = '<p style="color:#00ffff; font-size:1.3em;">' +
    '~*~ ' + (data.band_name || 'Your Band') + ' ~*~</p>' +
    '<p style="color:#cccccc;">The fan page is ready!</p>';
```
- **Sink → source chain:** `data.band_name` is returned by `GET /api/status/<id>` (`app.py:230-243`,
  `PUBLIC_STATUS_FIELDS` includes `band_name`), which echoes `band_profile['Band Name']` verbatim
  (`app.py:269`). That value is **raw GPT-4o output**. It is parsed straight out of the model completion in
  `createAct.generate_band_profile()` with `re.search(r"Band Name:\s*(.*)", response)` — no escaping, no
  charset restriction (the `SAFE_BAND_NAME` gate and `slugify_band_name` apply only to the *directory*, not
  to the display name).
- **Impact:** a completion whose band name contains markup — e.g. `"><img src=x onerror=alert(document.cookie)>`
  or any `<script>`/`<img onerror>` payload — is written through `innerHTML` and executes in the visitor's
  browser on the `/generate` page. Even a benign name containing `<` or `&` corrupts the preview markup.
- **Why this is a real defect, not theoretical:** `createAct.py` itself documents that "Everything the
  language model returns is untrusted markup" and routes this exact value through `esc()` at all 14
  server-side fan-page sinks. The generate-page preview is the one place the same untrusted value reaches
  the DOM **unescaped** — an inconsistency in the app's own trust model.
- **WCAG:** not a WCAG criterion (this is security), but squarely inside the parent's stated fix-scope
  ("un-escaped output", "XSS/injection into the DOM").
- **Fix applied:** rebuilt the preview with `document.createElement` + `textContent` and
  `preview.replaceChildren(...)` instead of `innerHTML`, so the untrusted name renders as text. Mirrors the
  `esc()` discipline already used server-side. No visual/behavioral change for normal band names.

### MEDIUM

**M1 — Focus drops to `<body>` after CANCEL and GENERATE ANOTHER.**
`templates/generate.html` — `resetInterface()` (lines 347–378), reached from `cancelGeneration()` (line 334)
and the `generateAnotherBtn` handler (line 141).
- WCAG 2.4.3 Focus Order (A).
- The activating control (`#cancelBtn` / `#generateAnotherBtn`) lives inside a container that
  `resetInterface()` sets to `display:none`. Hiding the focused element reverts focus to `document.body`,
  so a keyboard / screen-reader user is silently dropped at the top of the document with no announcement.
  Every *other* transition in this file correctly calls `focusHeading(...)`
  (`showProgress`→`progressTitle`, `showError`→`errorTitle`, `showSuccess`→`successTitle`), so the two reset
  paths are a consistency gap.
- Why MEDIUM not HIGH: focus lands on `body` (a valid target), nothing is trapped, Tab still works — a
  wayfinding/consistency defect, not a blocker.
- Suggested fix (out of scope this run): after `resetInterface()` reveals `#startGeneration`, move focus to
  `#generateBtn`.

### LOW

**L1 — Pending step-indicator glyph is below 4.5:1 (decorative / duplicated).**
`static/css/style.css:369` — `.step-row .step-indicator { color:#666666 }` on the `.progress-steps-table`
background `#0a0a1a` measures ≈ **3.4:1**.
- WCAG 1.4.3 Contrast (Minimum) (AA). LOW because the `...`/`[>]`/`[X]` glyph carries `aria-hidden="true"`
  (`generate.html:55` ff.), every row also has an always-visible label in `#cccccc` (~11:1), and an
  `sr-only` "(pending/in progress/complete)" status — the low-contrast glyph is decorative and duplicated,
  never the sole information carrier. Active states `[>]` `#ffff00` and `[X]` `#00ff00` pass comfortably.
  Nudge the pending color up (e.g. `#8a8aa0`) to clear 4.5:1.

**L2 — ASCII progress bar "empty" segment is ≈1.5:1.**
`templates/generate.html:45` — `#progressBarEmpty` uses `color:#333333` on the `.retro-box` background
`#0a0a2a` ≈ **1.5:1**.
- WCAG 1.4.3 (AA), but the whole `.ascii-progress` block is `aria-hidden="true"` and the same percentage is
  carried in text by `#progressPercent` and by the step table, so the dim empty track is decorative. Filed
  LOW; could be lifted to `#555577` to read as a real track.

**L3 — Heading level skips from `<h2>` to `<h4>`.**
`templates/index.html` — "What You Get" is `<h2>` (line 78); the three feature cards directly under it are
`<h4>` (lines 85, 91, 97) with no intervening `<h3>`.
- WCAG 1.3.1 Info & Relationships (A) — heading-hierarchy best practice. Screen-reader users navigating by
  heading perceive a missing level. Fix: promote the card titles to `<h3>` (inline styling can be kept, so
  no visual change).

**L4 — Layout table not marked presentational.**
`templates/index.html:81-102` — the 3-column "What You Get" table (`border="0"`, no `<th>`) is used purely
for side-by-side layout of the feature boxes.
- WCAG 1.3.1 (A). Assistive tech announces it as a data table ("table, 1 row, 3 columns"). Fix: add
  `role="presentation"`. (The "How It Works", gallery, and progress-steps tables are genuine data tables
  with `scope="col"` headers and are correct.)

---

## Verified clean (independently checked and found sound)

| Area | File / anchor | Check | Result |
|------|---------------|-------|--------|
| Skip link | base.html:12; style.css:7–24 | Off-screen, visible on `:focus`, targets `#main-content` | Pass (2.4.1) |
| Main landmark focus | base.html:34; style.css:53–56 | `#main-content tabindex="-1"`, outline suppressed only for programmatic focus; `:focus-visible` retained | Pass |
| Nav current page | base.html:28–30 | `aria-current="page"` gated on `request.endpoint` | Pass |
| Landmarks / single h1 | base.html:17,27,34,39 | `banner`/`nav[aria-label]`/`main`/`contentinfo`; one `<h1>` | Pass (1.3.1) |
| Body text contrast | style.css:66 `#cccccc` on `#000022` | ≈ 12.8:1 | Pass (1.4.3) |
| Nav links | style.css:142 `#00ff00` on `#111122` | ≈ 13.6:1 | Pass |
| Tagline | style.css:126 `#ff69b4` on lightest gradient stop `#000099` | ≈ 5.4:1 | Pass |
| Feature card headings | index.html:85/91/97 `#00ffff`/`#ff00ff`/`#ffff00` on `#0a0a2a` | ≈6.1–18:1 (magenta worst ≈6.1) | Pass |
| Feature body text | style.css:270 `#aaaaaa` on `#0a0a2a` | ≈ 8.3:1 | Pass |
| Table header cells | `#ff00ff` on `#1a1a3a` | ≈ 5.3:1 | Pass |
| Footer badges | style.css:417–425 `#888888` on `#111111` | ≈ 5.3:1 | Pass |
| No-photo placeholder | style.css:475 `#9999bb` on `#0a0a1a` | ≈ 7.1:1 | Pass |
| Error heading | generate.html:116 `#ff4444` on `#1a0a0a` | ≈ 5.6:1 | Pass |
| Buttons | style.css:277–324 `#00ffff`/`#cccccc` on `#333366`/`#222222` | 9+:1 | Pass |
| Focus indicator | style.css:40–48 | 3px `#ffff00` via `:focus-visible` on interactive + `[tabindex]` | Pass (2.4.7) |
| `blink` motion | style.css:448–461 | `prefers-reduced-motion:reduce` → `animation:none`; 1.2s cycle ≈0.83 Hz (< 3 Hz) | Pass (2.3.1); see note |
| Star twinkle JS | main.js:6–10 | Early-returns under reduced-motion | Pass (2.3.3) |
| Fan-page title pulse | createAct.py:462–470 | Wrapped in `@media (prefers-reduced-motion: no-preference)` | Pass |
| Live region — status | generate.html:40; main.js:247–251 | Single `role="status" aria-live="polite" aria-atomic`; `setText` writes only on change | Pass (4.1.3) |
| Live region — error | generate.html:114 | `role="alert" aria-live="assertive"`, focus to heading; text set via `textContent` | Pass |
| Progress not color-only | generate.html:54–81, 264–287 | State carried by `[X]`/`[>]`/text + `sr-only` status | Pass (1.4.1) |
| Recovery path | generate.html:213–225 | `not_found`/`cancelled` stop the poller and surface recovery | Pass |
| Images alt text | gallery.html:24; createAct.py:612 | Descriptive `alt`; decorative stars `aria-hidden` | Pass (1.1.1) |
| Zoom | base.html:5; createAct.py:415 | `width=device-width, initial-scale=1.0`, no scale lock | Pass (1.4.4) |
| Language | base.html:2; createAct.py:412 | `lang="en"` | Pass (3.1.1) |
| Path-traversal gate | app.py:23,136,152,164 | `SAFE_BAND_NAME` gates `view_band`/`band_assets` + gallery listing | Pass |
| Model-output escaping (fan page) | createAct.py:357–362, 378–383, 390, 395, 605, 614 | 14 `esc()` sinks cover name/style/year/genres/nationality/members/tracks/titles/backstory/caption; `mailto` host from slug | Pass |
| Success preview escaping (generate page) | generate.html:showSuccess | **Was `innerHTML` with raw `band_name` → H1; now `textContent`** | Fixed |
| Touch targets | style.css nav/buttons | Nav links ≈32px tall; `retro-button-small min-height:32px` | Pass (2.5.8) |
| Responsive | style.css:481–506 | `<=640px`: cells stack, tables→100%, thumbs 60px; no forced horizontal scroll | Pass (1.4.10) |

**Blink note (2.2.2):** the footer "Always Under Construction" blink runs indefinitely. It is honored by
`prefers-reduced-motion` and its ~0.83 Hz rate is far below the 3 Hz seizure threshold (2.3.1). It is part
of the intentional retro aesthetic, so it is not flagged as a fix-scope defect; recorded here for
completeness only.

---

## Phase 2 — FIX

Applied to CRITICAL + HIGH only.

- **H1 (HIGH) — FIXED** in `templates/generate.html`: `showSuccess()` now builds the band-name preview with
  `document.createElement` + `textContent` + `replaceChildren(...)` instead of `innerHTML`, so untrusted
  model output can no longer inject DOM nodes/scripts.

MEDIUM (M1) and LOW (L1–L4) are logged above and intentionally left unfixed.

---

## Phase 3 — VERIFY

See the parent hand-off for exact command output. `python -c "import app"` and
`python -c "import createAct"` both import cleanly; all four Jinja templates parse; the edited
`generate.html` block was re-read and confirmed to contain no `innerHTML` sink for `band_name`.
