# UX / Accessibility / Design-System Audit — 2026-07-08

**Reviewer:** Jennifer Mitchelle (Senior UX Design Critic)
**Branch:** `fix/code-review-2026-07-08`
**Scope:** `templates/base.html`, `templates/index.html`, `templates/generate.html`, `templates/gallery.html`, `static/css/style.css`, `static/js/main.js`, **`createAct.py`**, **`app.py`**

> **Scope change — read this first.** Every audit from 2026-05-10 through 2026-07-07 declared "no critical/high findings." All 25 were scoped to `templates/` + `static/` only. `createAct.py` and `app.py` were never opened. **Both HIGH defects found today live in exactly that gap**, and one of them — a dead link on `/gallery` — has been reproducible in the browser the entire time.
>
> The streak was a scope artifact that hardened into a conclusion. The prior reports were not fabricated: their contrast arithmetic is real and 9 of 10 quoted ratios are correct to the decimal. But the prior `review.md:17` claimed "the code remains genuinely clean" while its `review.md:5` quietly excluded the file that generates the app's actual product.

**Note:** The 1996 GeoCities aesthetic (blink text, "under construction", visitor counter, table layout, neon palette, Comic Sans, tiled starfield) is intentional and is NOT flagged.

## Summary of counts

| Severity | Count | Status |
|----------|-------|--------|
| CRITICAL | 0 | — |
| HIGH | 3 | **All 3 fixed this run** |
| MEDIUM | 9 | Logged, unfixed (per scope) |
| LOW | 13 | Logged, unfixed (per scope) |

---

## CRITICAL

**None.**

---

## HIGH — all fixed in this branch

### H1 — Model output interpolated into HTML with zero escaping ✅ FIXED
**File:** `createAct.py` (13 interpolation sites in `create_html_content`)
**WCAG:** 1.1.1 Non-text Content (A). Also a stored-injection vector — these pages are served same-origin by `view_band`.

Every f-string dropped raw GPT-4o output straight into markup. `createAct.py` had **no `import html` and no escaping anywhere**. Reproduced with band name `Sun & Moon "Choir" <Live>`:

```
<img src="band_photo.jpg" alt="Promotional photo of Sun & Moon "Choir" <Live>">
```

Python's `html.parser` sees:
```
('START','img',[('src','band_photo.jpg'), ('alt','Promotional photo of Sun & Moon '), ('choir"',None), ('<live',None)])
```
The `alt` text **truncates at the first quote**; the remainder becomes junk attributes. `<h1 class="band-title">` emits a phantom `<live>` element. `<b>` in a backstory renders as live markup.

Not hypothetical: the repo contains a directory literally named `**VelvetEchoes` — the model returned markdown bold and it was written to disk. A model that emits `**` will emit `&`, `<`, and `"`.

**Fix applied:** added a module-level `esc()` (`html.escape(str(v), quote=True)`, safe for text nodes and double-quoted attributes) and applied it to all 13 sites — band name, style, year, genres, nationality, backstory, member name/instrument/bio, track titles, album titles, photo caption. The mailto host is now derived from the slug rather than the raw name.

**Verified:** ran `create_html_content` with hostile input across every field; parsed output with `html.parser`; zero injected elements (`live`, `script`, `b`, `em`), `alt` intact as a single attribute value.

### H2 — Generated directory names could never be served back; the happy path dead-ended in a 404 ✅ FIXED
**Files:** `createAct.py:create_project_directory` ←→ `app.py:21,58,73,85`
**WCAG:** 2.4.4 / general correctness.

`create_project_directory` did `''.join(word.capitalize() for word in band_name.split())` with no charset restriction. `app.py` gates every band route on `SAFE_BAND_NAME = ^[A-Za-z0-9_\-]+$`. Any name with punctuation or non-ASCII produced a directory the app **can never serve** — and `createAct.py:61-79` explicitly prompts for names that are "evocative and strange" with nationalities that are "obscure", so this is the expected case, not the edge case.

Verified live against the running app *before* the fix:
```
GET /gallery -> 200
  href /band/**VelvetEchoes/               -> 404   <- rendered to real users
  src  /band/**VelvetEchoes/band_photo.jpg -> 404   <- broken image
```
Worse: after a successful generation, `viewBand()` navigates to `/band/<dir>/` and the user lands on a bare, unstyled `"Band not found"`. The app's single primary task terminated in a 404.

```
'The Sun & Moon'    -> 'TheSun&Moon'      -> 404
"Sons of Ka'nien"   -> "SonsOfKa'nien"    -> 404
'Björk Collective'  -> 'BjörkCollective'  -> 404
```

**Fix applied:** new `slugify_band_name()` — NFKD-transliterates to ASCII (so `Björk` → `Bjork`, not `Bjrk`), strips to `[A-Za-z0-9_-]`, falls back to `UntitledBand` if empty. Used by both `create_project_directory` and the mailto host. Separately, `app.py:gallery()` now filters the glob through `SAFE_BAND_NAME` and logs a warning, so an unservable directory can never render as a link again.

**Verified:** `/gallery` now emits 6 band refs, **all 200**. `**VelvetEchoes` is filtered out. Traversal guards (`/band/../app.py`) still 404.

### H3 — Progress `aria-live` region flooded on every 1.5 s poll ✅ FIXED
**File:** `templates/generate.html` — region, ASCII bar, step table, `updateProgress()`, `setInterval` at 1.5 s
**WCAG:** 1.3.1 (A) for the glyph-only status; 4.1.3 Status Messages (AA).

`aria-live="polite" aria-atomic="false"` sat on the whole panel, and `updateProgress()` wrote `.textContent` on four nodes plus seven step indicators every 1.5 s.

The load-bearing detail: **the DOM `textContent` setter is replace-all** — it removes existing children and inserts a *new* Text node even when the assigned string is identical. So a generation stalled at 35% for 20 seconds still fired ~13 rounds of mutation records. Across a 60–90 s generation that is 40–60 announcements of `Progress: [ ==== ------- ] 35%`. The polite queue never drains, and there is no way to stop it — for the full duration of the app's only real task.

Compounding it: the status column's `<th>` was the literal string `?` (announced "question mark"), and per-step state was conveyed *only* by `...` / `[>]` / `[X]` glyphs with no text alternative.

**Fix applied:**
- Removed `aria-live`/`aria-atomic` from `#progressDisplay`.
- `aria-hidden="true"` on `.ascii-progress` and all 7 `.step-indicator` cells (decorative; percent + step table carry the same info).
- `<th>?</th>` → `<span class="sr-only">Status</span><span aria-hidden="true">?</span>`.
- Added `.sr-only step-status` spans (`(pending)` / `(in progress)` / `(complete)`) giving each step a real text status.
- Added one dedicated `#progressStatus` region (`role="status"`, `aria-live="polite"`, `aria-atomic="true"`) carrying only `"{message}, {percent}%"`.
- New `setText()` helper guards every write: `if (el.textContent !== value)`. `resetInterface()` resets the new nodes.

**Verified:** simulated 13 identical polls → **1** live-region write (was 13); a real change → 2. `node --check` clean. Markup assertions confirm 7/7 indicators hidden, 7/7 status spans present, `#progressDisplay` no longer a live region.

> Note: `.sr-only` was defined at `style.css:27` and **never used anywhere** — evidence someone planned this fix and never landed it. It is now used.

---

## MEDIUM — logged, not fixed

| # | File | Issue |
|---|---|---|
| M1 | `templates/generate.html` `resetInterface()` | **`resetInterface()` destroys keyboard focus.** `cancelBtn` (inside `#progressDisplay`) and `generateAnotherBtn` (inside `#successDisplay`) both hide their own focused ancestor; focus reverts to `<body>` and the next Tab restarts from the document top. WCAG 2.4.3 (A). The asymmetry proves oversight: `showProgress/showSuccess/showError` all call `focusHeading()`; `resetInterface()` is the only transition that doesn't. **One-line fix** (`generateBtn.focus()`) — strongest candidate for the next run. *This directly contradicts the prior audit's claim of "no focus loss into a hidden panel."* |
| M2 | `static/css/style.css:369` | `.step-indicator` `#666666` on `#0a0a1a` = **3.414:1**, below AA 4.5:1 — and it was the *sole* conveyor of per-step status (mitigated by H3's sr-only spans, but the visual still fails). Suggest `#8a8a99` (≈4.7:1). WCAG 1.4.3 (AA). |
| M3 | `templates/generate.html` `checkStatus()` | `status === 'not_found'` never handled → poller runs **forever** at 0% showing "Generation not found". `cleanup_old_generations()` can purge a still-running entry, and `debug=True` restarts drop the dict. The `.catch` only calls `console.error`. |
| M4 | `templates/generate.html` `cancelGeneration()` | **"CANCEL" cancels nothing.** Clears the client interval; the daemon thread keeps running, keeps burning OpenAI calls, and the band still lands on disk. No cancel route exists. Nielsen #1/#3. |
| M5 | `templates/index.html:85,91,97` | Heading level skipped h2 → h4. WCAG 1.3.1 (A). (Carried over from prior audits — still unfixed.) |
| M6 | `app.py:97` | `generation_id` uses `strftime("%Y%m%d_%H%M%S")` — 1-second resolution. Two concurrent POSTs collide; users see each other's band. Use `uuid4().hex` (note this also breaks the lexicographic prune at `:34`). |
| M7 | `createAct.py` backstory box | Backstory `\n\n` paragraph breaks are discarded; every fan page is one wall of Comic Sans. Split → `<p>` (safe now that H1 escapes). |
| M8 | `index.html:81`, `createAct.py` members table | Layout table without `role="presentation"`; members table is a real *data* table with zero `<th>`/`scope`. WCAG 1.3.1 (A). |
| M9 | `app.py:74,79,86` | Both 404 paths unstyled with no way back — `abort(404)` (Flask default) and bare `"Band not found"` coexist. Add one `@app.errorhandler(404)` extending `base.html`. |

---

## LOW — logged, not fixed

| # | File | Issue |
|---|---|---|
| L1 | `generate.html` ascii bar | `#333333` dashes on `#0a0a2a` = 1.525:1. Genuinely decorative; now `aria-hidden` via H3. Lift to `#777777`. |
| L2 | `style.css:50-56` | Comment claims `:focus-visible` still applies — **false**. `h3[tabindex]:focus` (0,2,1) beats `[tabindex]:focus-visible` (0,2,0). Conversely `main:focus` (0,1,1) *loses*, so `main` does get an outline. Both halves of the comment are wrong. |
| L3 | `gallery.html:31` | Band-name link `display:inline`, line box ≈23.1px — under WCAG 2.5.8's 24×24. Saved by the *spacing* exception, not the inline one. |
| L4 | `gallery.html:36` | `[ VIEW ]` × N with no per-band accessible name. Passes 2.4.4; fails 2.4.9 (AAA). |
| L5 | `style.css:27` | ~~`.sr-only` defined but never used~~ — **now used by H3.** |
| L6 | `createAct.py` css block | A `marquee {}` CSS rule exists but no `<marquee>` is ever emitted. Dead rule. |
| L7 | `createAct.py` css block | `img`/`.backstory-box` lack `box-sizing` → 8px/4px overhang into the wrapper's 10px padding. Off-center but **no horizontal scrollbar**. Cosmetic. |
| L8 | `createAct.py` slugify | `str.capitalize()` lowercases the tail: `"MGMT Revival"` → `MgmtRevival`. (Preserved deliberately in the H2 fix to keep the change minimal.) |
| L9 | `main.js:6-10` | `prefers-reduced-motion` sampled once at `DOMContentLoaded`; no `change` listener. |
| L10 | `createAct.py` guestbook | Five `href="#"` no-op links. Arguably part of the pastiche. |
| L11 | `generate.html` `showSuccess()` | Reveals → writes `innerHTML` → moves focus: three announcements of the same box. Populate before revealing. |
| L12 | `generate.html` `showError()` | `showError(data.error)` with a missing key renders the literal string **"undefined"**. |
| L13 | `style.css` | No `:root` custom properties; neon palette repeated as magic hex across CSS *and* inline template styles. |

---

## Data follow-up (not a code change)

The on-disk directory `**VelvetEchoes/` is now correctly hidden from `/gallery` rather than rendering a dead link. It remains unreachable. It appears to duplicate `TheVelvetEchoes/`. **Left untouched** — renaming or deleting generated content is a data decision for the maintainer, not the reviewer.

---

## Verified clean

Recomputed **42** contrast pairs from relative luminance (sRGB → linear → `0.2126R + 0.7152G + 0.0722B`), including all four random palettes in `createAct.py`. Exactly **two** failures exist in the whole codebase (M2, L1); everything else clears 4.5:1. Worst pair in any generated page: `#ff4444` on `#000066` = 5.170:1.

- **`prefers-reduced-motion`: coverage is correct and complete.** `.blink` gated by `animation:none` + a global `*` override; the starfield twinkle uses inline `style.opacity` (a CSS `*` override *cannot* stop it) and is correctly handled by the JS early-return, belt-and-braced by `.banner-stars { opacity: 1 !important }` — an author `!important` declaration does beat a non-`!important` inline style. Someone reasoned this through. Only gap: L9.
- **2.3.1 Three Flashes:** `.blink` at 1.2 s = 0.83 Hz, well under 3 Hz. Passes.
- **2.2.2 Pause, Stop, Hide:** `prefers-reduced-motion` is a user-agent mechanism, which the WCAG definition explicitly permits. Compliant.
- **No horizontal overflow at 320px** anywhere — box model checked on `.page-wrapper`, `.retro-box`, all three tables, `.ascii-progress`, and the 41-asterisk banner.
- Skip link + `#main-content` target valid; no keyboard traps; focus order follows DOM; `aria-current="page"` correct; decorative star rows `aria-hidden`; 1.4.1 Use of Color passes (step status changes glyph *and* color); Jinja autoescaping on in templates; `send_from_directory` blocks traversal.

## Corrections to the prior audit's record

- Prior `review.md:30` / `:108` — "focus management … all present and correct", "no focus loss into a hidden panel" is **false**, and false *inside its own declared scope*. See M1. The reviewer read `focusHeading()`'s three call sites and generalized without enumerating the fourth transition.
- Prior `review.md:26` — "`#ff69b4` on `#000022` ≈ **10+:1**". Actual: **7.753:1**. Still a comfortable AA pass, but it is the only wrong number in a list of ten, and it errs in the flattering direction, in a document opening with "every pair was recomputed from relative luminance."
- Prior L1 rated the `...`/`[>]`/`[X]` glyph "non-essential text" to justify LOW. It was the *only* content of the status column — reasoning backwards from the desired severity. Now genuinely non-essential, because H3 added a text alternative.
- Prior M2 (the `aria-live` finding) was correctly diagnosed but under-rated at MEDIUM, and its mechanism was incomplete — it missed that `textContent` is replace-all. Promoted to HIGH and fixed.
</content>
