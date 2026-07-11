# UX / Accessibility / Design-System Review — AI Band Generator

**Reviewer:** Jennifer Mitchelle (Senior UX Design Critic)
**Date:** 2026-07-11
**Scope:** `templates/base.html`, `index.html`, `generate.html`, `gallery.html`, `static/css/style.css`, `static/js/main.js`, and the template-facing parts of `app.py`.
**Framing:** The 1996 GeoCities aesthetic (Comic Sans, blink, neon-on-dark, ASCII bar, star field, under-construction) is treated as an intentional design language. Findings judge usability, WCAG 2.1 AA conformance, internal consistency, responsiveness, and UX anti-patterns **within** that theme. No finding says "this looks dated."

---

## Summary (counts by severity)

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High     | 1 |
| Medium   | 3 |
| Low      | 6 |
| **Total** | **10** |

**Overall:** This is a genuinely well-hardened front end. Contrast across the neon palette is excellent (see Verification notes), the skip link / `sr-only` live region / `aria-current` / focus management on state entry / `prefers-reduced-motion` are all present and correct, images have real alt text, and the status indicators use symbol-plus-color rather than color alone. The remaining issues cluster in the generate.html state machine — a CANCEL control that doesn't cancel, focus lost on the reset/cancel transitions, and unbounded polling — plus low-severity polish.

---

## High

### H1 — CANCEL is a false affordance: it stops the client but never stops the server  — ✅ FIXED (2026-07-11)
**Category:** UX anti-pattern (Nielsen #1 Visibility of system status, #3 User control & freedom)
**File:** `templates/generate.html` lines 282–287 (`cancelGeneration`); `app.py` (no cancel route exists)

**Fix applied (Phase 2):** Implemented a real server-side stop rather than the relabel fallback.
- `app.py`: added `POST /api/cancel/<generation_id>` (`api_cancel`) that sets a `cancelled` flag on the status entry (404 for unknown ids, no-op for already-terminal runs); added a `GenerationCancelled` exception, a `raise_if_cancelled()` helper called at every step boundary in `generate_band_async`, and `cleanup_partial_output()` to `shutil.rmtree` the aborted run's partial directory. `'cancelled'` added to `TERMINAL_STATUSES` so entries prune normally.
- `templates/generate.html`: `cancelGeneration()` now `POST`s to `/api/cancel/<id>` (best-effort, capturing the id before reset) so the worker actually stops; the poll loop short-circuits on a `cancelled` status.
- **Verified** end-to-end with the paid generators mocked: cancelling mid-run flips status to `cancelled`, the later DALL·E/page-save steps never execute, the partial directory is removed, unknown-id → 404, and already-finished → `already_finished`. All 6 checks passed.

**What's wrong:** `cancelGeneration()` only does `clearInterval(statusCheckInterval)` and `resetInterface()`. There is no `fetch()` to the server and no `/api/cancel` route in `app.py`. The worker thread `generate_band_async` runs to completion regardless: it still calls the profile/backstory/discography generators and DALL·E, still writes a project directory, and still flips the status entry to `complete`. The band the user "cancelled" silently appears in the Band Gallery 30–60s later.

**Why it matters:** `[ CANCEL ]` is the only "emergency exit" from the multi-step progress flow, so it sets a firm expectation that work stops. It doesn't. The user's mental model and the system state diverge (ghost bands appear), and every cancel still incurs a full paid generation (multiple GPT calls + a DALL·E image). A control that visibly contradicts its label is a top-tier usability defect, not cosmetic.

**Recommended fix:** Add a real server-side stop. Minimum viable: a `POST /api/cancel/<id>` that sets a `cancelled` flag on the status entry; have `generate_band_async` check the flag at each `update_status` boundary and bail early (cleaning up any partial directory). Have `cancelGeneration()` call it before resetting the UI. If a true stop is out of scope for Phase 2, relabel the control (e.g. `[ HIDE / START OVER ]`) and add a note that the in-flight band will still finish and appear in the gallery — so the label stops promising something the code doesn't deliver.

---

## Medium

### M1 — Focus is dropped on the CANCEL and "GENERATE ANOTHER" transitions
**Category:** Accessibility — keyboard/focus management (WCAG 2.4.3 Focus Order, Level A)
**File:** `templates/generate.html` — `cancelGeneration` (282–287) and `resetInterface` (289–315)

**What's wrong:** Every *other* state transition moves focus deliberately (`showProgress`/`showSuccess`/`showError` all call `focusHeading(...)`). But `resetInterface()` — reached from CANCEL and from the "GENERATE ANOTHER" button — hides the currently focused element (`progressTitle` after cancel, or `generateAnotherBtn` itself after success) with `display:none` and never calls `focus()` on anything. When the focused element is removed from the render tree, browsers reset focus to `<body>`. A keyboard or screen-reader user is silently dumped at the top of the document with no announcement.

**Why it matters:** Focus loss mid-flow is a documented A-level failure; the next Tab restarts from the page top and screen-reader users get no context about what happened. This is exactly the kind of gap earlier passes missed — entry transitions were handled, the two *reset* paths were not.

**Recommended fix:** After `resetInterface()` re-shows `#startGeneration`, move focus to the GENERATE button: `document.getElementById('generateBtn').focus();`. (It's a real `<button>`, already focusable.)

### M2 — Polling has no timeout ceiling and silently swallows fetch failures
**Category:** UX / error recovery (Nielsen #1 Visibility of system status)
**File:** `templates/generate.html` — `startStatusCheck` (162–164) and the `checkStatus` catch block (193–195)

**What's wrong:** Two related gaps. (1) The 1.5s poll runs unbounded — if the worker sticks in a non-terminal status (e.g. a hung DALL·E call that never raises), the bar freezes at the last percent forever. (2) The `.catch()` only does `console.error(...)` and leaves the interval running, so repeated `/api/status` 500s or network drops produce no visible feedback and no bound. The recent `not_found` handling (commit d5a50b1) covers *pruned/restarted* ids, but not a worker that is alive-but-stuck or an endpoint that is erroring.

**Why it matters:** The only escape from a frozen bar is CANCEL — which (per H1) doesn't stop the server and gives no explanation of *why* it froze. "Visibility of system status" requires telling the user when something is wrong, not just spinning.

**Recommended fix:** Track poll count / elapsed time; after a ceiling (e.g. ~3 minutes with no progress change, or N consecutive failed polls) call `showError('This is taking longer than expected — the server may be stuck. Please try again.')` and `clearInterval`. Treat a run of consecutive `.catch()` failures as an error surface rather than retrying silently forever.

### M3 — GENERATE / RETRY have no disabled state; double-submit is prevented only as a layout side effect
**Category:** UX robustness (double-submit of a costly action)
**File:** `templates/generate.html` — `generateBtn` (26), `startGeneration` (140–160), `showProgress` (252–258)

**What's wrong:** The button is never disabled or guarded by an `isGenerating` flag. Double-submission is prevented *only* because `showProgress()` sets the button's parent `#startGeneration` to `display:none` synchronously on the first click, so the second click of a fast double-click hit-tests empty space. That works today, but it couples "don't fire twice" to an unrelated layout decision. Any future refactor that keeps the button visible during progress (or moves the hide after the `fetch`) reintroduces uncontrolled double-generation — and each extra fire is a full paid generation plus an orphaned worker/directory.

**Why it matters:** Guarding an expensive, irreversible action with a rendering side effect is fragile. An explicit guard is a few lines and removes the coupling.

**Recommended fix:** Add a module-scoped `let isGenerating = false;`. At the top of `startGeneration()`: `if (isGenerating) return; isGenerating = true;`; clear it in `resetInterface`, `showError`, and `showSuccess`. Optionally set `generateBtn.disabled = true` while the request is in flight for a visible affordance.

---

## Low

### L1 — Heading level skips from h2 to h4 on the home page
**Category:** Accessibility — document structure (WCAG 1.3.1 Info and Relationships, Level A)
**File:** `templates/index.html` lines 85, 91, 97 (feature-box `<h4>`) under the `<h2>` "What You Get" (line 78)

**What's wrong:** The page runs `h1` (banner) → `h2` (section headers) → `h4` (feature titles), skipping `h3`. Heading-navigation users hit a gap. (generate.html and gallery.html are clean: `h2` → `h3`.)

**Recommended fix:** Change the three feature-box headings to `<h3>`; they keep their per-box neon colors via existing inline styles / `.feature-box`. No visual change.

### L2 — "Pending" step indicator fails AA contrast
**Category:** Accessibility — contrast (WCAG 1.4.3, Level AA)
**File:** `static/css/style.css` `.step-row .step-indicator { color:#666666 }` (367–371) on the `#0a0a1a` table background

**What's wrong:** The pending indicator (`...`) computes to **3.41:1**, below the 4.5:1 AA threshold. The in-progress (`#ffff00`) and complete (`#00ff00`) states pass; only the resting gray is low. It's `aria-hidden` (SR users get the parallel `sr-only` status text), but it is the primary *visual* status cue, so the decorative-text exemption doesn't cleanly apply for sighted low-vision users.

**Recommended fix:** Lighten to at least ~`#909090` (~4.6:1), preserving the muted "not started" look while clearing AA.

### L3 — Blinking "Under Construction" text has no stop mechanism
**Category:** Accessibility — blinking content (WCAG 2.2.2 Pause, Stop, Hide, Level A)
**File:** `templates/base.html` line 49 (`.blink`); `static/css/style.css` 447–455

**What's wrong:** The blink toggles opacity on a 1.2s infinite loop (well past the 5s threshold in 2.2.2). `prefers-reduced-motion` disables it (good, and the right thematic call), but 2.2.2 has no reduced-motion carve-out — users without that OS preference get unstoppable blinking with no pause/stop/hide control. (At ~0.8 Hz it is far below the 3-flashes/second seizure threshold of 2.3.1, so there is no photosensitivity risk — this is purely the 2.2.2 "provide a control" clause.)

**Recommended fix:** Give the animation a finite `animation-iteration-count` so it self-terminates within a few seconds (keeps the joke, satisfies the SC), or formally accept `prefers-reduced-motion` as the documented mitigation.

### L4 — `.retro-button-small` is a link dressed as a button, and duplicates the row's band-name link
**Category:** UI consistency / semantics
**File:** `templates/gallery.html` lines 31–39; `static/css/style.css` 306–324

**What's wrong:** Interactive elements are otherwise consistent (real `<button>`s for actions, `<a>` for navigation). The gallery "[ VIEW ]" is an `<a>` styled like the `.retro-button` family. Because it navigates (has `href`), link semantics are actually *correct* — but the button styling implies Space-to-activate (links respond only to Enter), a subtle affordance mismatch. Separately, each row exposes **two** links to the identical destination (band-name link on line 31, VIEW link on line 36), doubling tab stops and the screen-reader link list for no new target.

**Recommended fix:** Keep it an `<a>` (navigation is right) but either drop the redundant VIEW link, or if you want the button affordance, give it `aria-label="View {band name}"` so the two links aren't announced identically.

### L5 — Design tokens are ad-hoc: palette hexes are hardcoded inline across templates
**Category:** Design-system adherence / maintainability
**Files:** `templates/index.html` (inline `style="color:#…"` on 16, 35–61, 85, 91, 97), `templates/generate.html` (inline colors on 15, 16, 35, 36, 45, 46, 95, 116, 267–269), plus `border`/`bordercolor` HTML attributes throughout

**What's wrong:** The same ~8 neon values (`#00ffff`, `#00ff00`, `#ffff00`, `#ff00ff`, `#ff4444`, `#cccccc`, `#0a0a2a`, `#333333`) are re-typed inline dozens of times rather than centralized. There is no CSS custom-property palette, so the "system" is the stylesheet *plus* a large body of inline overrides. Global palette/contrast changes (e.g. the L2 fix, or re-theming) become error-prone and inconsistent — which is how contrast regressions can slip past template edits.

**Recommended fix:** Define the palette once as `:root` custom properties (`--neon-cyan`, `--neon-green`, …) and replace repeated inline hexes with utility classes or `var(--…)`. Maintainability only — the retro look is preserved.

### L6 — ASCII progress bar and fixed `width=` cells don't adapt on narrow screens
**Category:** Responsive layout
**Files:** `templates/generate.html` 44–47 (`.ascii-progress`); `static/css/style.css` `.ascii-progress` (344–351) and the `@media (max-width:640px)` block (481–506); fixed `width="…"` attributes in `index.html` (28), `gallery.html` (14–19), `generate.html` (49–53)

**What's wrong:** The ASCII bar is a fixed 20-char fill plus `Progress: [` / `]` / ` 100%` in 1.1em monospace with 1px letter-spacing — roughly 370px wide. Inside `.retro-box` on a ~320px viewport the usable width is ~260px, so the line wraps across 2–3 lines, breaking the single-line bar illusion. The mobile media query shrinks table fonts but never touches `.ascii-progress`. It's `aria-hidden` (percentage + step table carry the same info for AT), so this is cosmetic, not an AA failure — but it degrades the intended visual on phones. Relatedly, the HTML `width="120"/"50"/"30"` header attributes don't scale; tables avoid horizontal scroll only because CSS forces `width:100%` and the browser shrinks the flexible column, cramping the gallery band-name column.

**Recommended fix:** In the `max-width:640px` block add `.ascii-progress { font-size: 0.85em; letter-spacing: 0; white-space: nowrap; }` (consider `overflow-x: hidden` on its container), or shorten the fill to ~12 chars on small screens. For tables, prefer a CSS `min-width` on the flexible column over fixed pixel `width=` attributes.

---

## Verification notes (contrast ratios)

Ratios were computed with the WCAG 2.1 relative-luminance formula (sRGB linearization, `L = 0.2126R + 0.7152G + 0.0722B`, contrast `= (L1+0.05)/(L2+0.05)`), each against its *actual* rendered background (body `#000022`, boxes `#0a0a2a`/`#0a0a1a`, header row `#1a1a3a`, error box `#1a0a0a`, badge `#111111`). AA normal-text threshold = 4.5:1.

| Foreground | Background | Ratio | AA |
|---|---|---|---|
| `#cccccc` body text | `#000022` / `#0a0a2a` / `#0a0a1a` | 12.8 / 12.0 / 12.2 | Pass |
| `#dddddd` intro | `#0a0a1a` | 14.4 | Pass |
| `#aaaaaa` feature/footer | `#0a0a2a` / `#000022` | 8.3 / 8.8 | Pass |
| `#888888` badge | `#111111` | 5.33 | Pass |
| `#9999bb` copy/no-photo | `#000022` / `#0a0a1a` | 7.5 / 7.1 | Pass |
| `#00ffff` links/cyan | `#000022` / `#0a0a2a` | 16.4 / 15.4 | Pass |
| `#00ff00` nav/step | `#111122` / `#0a0a1a` | 13.6 / 14.3 | Pass |
| `#ffff00` yellow | `#000022` / `#0a0a2a` | 19.1 / 18.0 | Pass |
| `#ff00ff` table header | `#1a1a3a` / `#0a0a1a` | 5.34 / 6.25 | Pass |
| `#ff4444` error | `#1a0a0a` / `#000022` | 5.64 / 6.02 | Pass |
| `#ff69b4` tagline/email | `#000022` / `#000000` | 7.8 / 7.9 | Pass |
| `#cc99ff` visited link | `#000022` | 9.35 | Pass |
| button text `#00ffff`/`#ffff00`/`#cccccc` | `#333366`/`#444488`/`#222222` | 9.3 / 10.8 / 9.9 | Pass |
| **`#666666` pending step indicator** | **`#0a0a1a`** | **3.41** | **Fail (L2)** |

**Caveats:** (1) Ratios assume the flat background color; the body's sparse radial-gradient star dots (`#ffffff`, 0.3–0.5px) don't meaningfully change local text contrast. (2) `text-shadow` on `.site-title`/`.section-header` is not modeled by the formula; the underlying pairings are 17–19:1, so shadow legibility is a non-issue. (3) The only sub-4.5 result conveying information is the `#666666` pending indicator (3.41:1) — the basis for L2. The decorative `#333333` empty-bar dashes (1.53:1) sit inside the `aria-hidden`, purely-ornamental ASCII bar and carry no information, so they are exempt from 1.4.3 and are not filed. Every text color that conveys meaning passes AA.
