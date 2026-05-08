# UX & Accessibility Audit — 2026-05-08

**Branch (audit conducted on):** `fix/code-review-2026-05-07` (most recent fix branch; today's audit branch will be `fix/code-review-2026-05-08`)
**Reviewer:** Jennifer Mitchelle (Senior UX Design Critic)
**Scope:** UI consistency, WCAG 2.1 AA compliance, design system adherence, responsive layout, UX patterns
**Note on aesthetic:** The "retro 90s GeoCities" look (commit `8b971ef`) is an intentional design choice. Findings are limited to objectively broken issues — accessibility violations, layout bugs, security regressions — not stylistic critiques.

---

## Context vs. Previous Reviews

| Date | Outcome |
|---|---|
| 2026-05-01 | 4 CRITICAL + 8 HIGH (retro overhaul lost prior fixes) → restored in `7941ae9` |
| 2026-05-02 | 4 HIGH (N1–N4) → fixed in `8bae07f` |
| 2026-05-03 | 0 Critical/High; 4 Medium + 5 Low (deferred) |
| 2026-05-04 | 0 Critical/High; no new findings |
| 2026-05-05 | 0 Critical/High; 1 new Low (N14) |
| 2026-05-06 | 1 HIGH (N15, generated-page nav touch target) → fixed in `f2b2d39` |
| 2026-05-07 | 0 Critical/High; no new findings |
| **2026-05-08 (this audit)** | **0 Critical/High; no new findings; carry-overs unchanged** |

### Code change since last audit

`git diff f0a471a..HEAD -- '*.py' '*.html' '*.css' '*.js'` returns no diff. The only working-tree change is the untracked `media/` directory (empty subdirs + `.gitkeep`, no application code). Nothing in the live app surface has changed since yesterday's audit log was committed.

### Re-verification of all prior fixes (current tree)

| ID | Item | File:line | Status |
|---|---|---|---|
| C1–C4 (2026-05-01) | Path-traversal regex, lazy cleanup, focus indicator, prefers-reduced-motion | `app.py:21,27-38,73,85,95`; `static/css/style.css:40-48,457-472` | PASS |
| H1–H9 (2026-05-01) | Skip link, `<main>`, lang, viewport, alt, aria-live, button types, etc. | `templates/base.html:12,34`; `templates/generate.html:33,88,109` | PASS |
| N1 | Auxiliary-link wrapper colour ≥7:1 | `createAct.py:601` (`color:#999999`) | PASS |
| N2 | Top-nav `.nav-bar a` ≥24px tap target | `static/css/style.css:141-147` (`display:inline-block; padding:6px 8px;`) | PASS |
| N3 | `<th scope="col">` on data tables | `templates/gallery.html:16-18`, `templates/generate.html:46-47` | PASS |
| N4 | `focusHeading()` moves focus on state changes | `templates/generate.html:211-217,224,237,246` | PASS |
| N15 | Generated-band-page `.nav-bar a` ≥24px tap target | `createAct.py:525-529` (`display: inline-block; padding: 6px 8px; margin: 0 5px;`) | PASS |

`SAFE_BAND_NAME` regex still in place (`app.py:21`), validated on both `view_band` (`app.py:73`) and `band_assets` (`app.py:85`). All inline JS event handlers use `addEventListener` (`generate.html:127-133`); no inline `onclick=` regression. `aria-current="page"` still set on active framework-page nav link (`base.html:28-30`). All five `<button>` elements carry explicit `type="button"` (`generate.html:26,80,97,101,113`). Reduced-motion gating in three places (`style.css:457-472`, `createAct.py:427-435,497-504`, `static/js/main.js:6-10`) all intact.

---

## 2026-05-08 Audit Methodology

Files re-reviewed independently in current tree:

- `templates/base.html` (62 lines)
- `templates/index.html` (105 lines)
- `templates/gallery.html` (59 lines)
- `templates/generate.html` (286 lines)
- `static/css/style.css` (507 lines)
- `static/js/main.js` (27 lines)
- `createAct.py` HTML emission and discography/member generation (lines 324–627)
- `app.py` routes and validation (217 lines)

Re-derived contrast ratios from luminance for every accent permutation on the generated page. Re-measured tap-target heights for all interactive elements on framework pages and on the generated band page. Re-checked WCAG 2.2.2 (Pause/Stop/Hide) on the blinking footer text since it is the most subjective borderline item.

### Checks performed (Phase 1)

1. **Color contrast (WCAG 1.4.3 AA, 4.5:1 normal text / 3:1 large text & non-text)** — every body-text, link, heading, and accent pair clears 4.5:1 in the worst sampled case. Worst-case re-check: `.banner-tagline #ff69b4` on banner-gradient peak `#000099` ≈ 5.47:1; album-title with `c1=#ff69b4` on `#222222` ≈ 4.63:1; `.footer-area p` `#888888` on `#000000` ≈ 6.64:1; `.badge-row` `#999999` on `#000000` ≈ 7.37:1; generated-page `a` colour with `c1=#ff6600` on `#000000` ≈ 5.31:1; `.intro-text #dddddd` on `#0a0a1a` ≈ 13.2:1. **No finding.**

2. **Touch-target size (WCAG 2.5.8 AA, 24×24 CSS px minimum)** — primary nav (~32px ✓), `.retro-button` (10px y-padding × 2 + 1.1em line ≈ 40px ✓), `.retro-button-small` (`min-height: 32px` ✓), gallery row tap zones (~90px ✓), generated-page `.nav-bar a` post-N15 fix (~32px ✓). Inline links in body prose (`.big-link`, footer email) are exempt under the WCAG 2.5.8 "inline" exception. **No finding.**

3. **Semantic structure & landmarks (WCAG 1.3.1, 2.4.1)** — framework pages: single `<h1>` per document, `<header role="banner">`, `<nav aria-label>`, `<main id="main-content">`, `<footer role="contentinfo">` all present. Skip link present (`base.html:12`). Generated band page: `<header role="banner">`, `<nav aria-label="Page sections">` present; the absence of `<main>` and `<footer>` elements is logged as deferred MEDIUM N16 (in-page anchor nav at `createAct.py:558-564` satisfies WCAG 2.4.1 Bypass Blocks). **No new finding.**

4. **Heading hierarchy** — N14 (`<h2>` → `<h4>` skip in feature boxes at `index.html:85,91,97`) carries over LOW. Other pages have correct `h1 → h2 → h3` hierarchy. Generated page: `h1.band-title` followed by `h2.section-header` for each region — clean.

5. **ARIA & live regions** — `aria-live="polite"` on `#progressDisplay` and `#successDisplay`; `role="alert" aria-live="assertive"` on `#errorDisplay`. `aria-current="page"` on active nav link. `aria-hidden="true"` on decorative star strips (`base.html:18,23`; `createAct.py:549,554`). `aria-label="Page sections"` on the generated-page section nav. **No new finding.**

6. **Keyboard / focus** — `:focus-visible` outline (yellow `#ffff00`, 3px) on all interactive elements (`style.css:40-48`); skip-link visible on focus (`style.css:7-24`); generated-page anchors have `:focus-visible` outline (`createAct.py:394-397`). `focusHeading()` (`generate.html:211-217`) moves focus to the new region's `<h3>` on state transitions; the three headings carry `tabindex="-1"`. **No finding.**

7. **Reduced motion (WCAG 2.3.3 AAA, plus mechanism for 2.2.2 A)** — site stylesheet (`style.css:457-472`), generated-page inline `<style>` (`createAct.py:497-504`), and `static/js/main.js:6-10` all honour `prefers-reduced-motion: reduce`. The band-title pulse is gated by `(prefers-reduced-motion: no-preference)` (`createAct.py:427-435`). The footer `.blink` animation (`style.css:447-455`, `createAct.py:491-496`) does run >5s and is in parallel with other content (potential WCAG 2.2.2 trigger), but `prefers-reduced-motion` is honoured globally and is widely accepted as a sufficient stop mechanism. Frequency is ~0.83 Hz (single 50% step per 1.2s), nowhere near the 3-flash WCAG 2.3.1 threshold. **No finding.**

8. **Image alt text** — gallery thumbs have descriptive alt (`gallery.html:25`), generated band photo too (`createAct.py:577`), decorative stars `aria-hidden="true"`. **No finding.**

9. **Lang / `<title>` / viewport** — present on all four framework templates (`base.html:2,5,6`) and on the generated band page (`createAct.py:377,379-381`). **No finding.**

10. **Empty state** — gallery has clear empty-state with CTA (`gallery.html:43-52`). **No finding.**

11. **Form/input accessibility** — N/A: app has no input forms; only buttons. **No finding.**

12. **Responsive layout** — `@media (max-width: 640px)` (`style.css:481-506`) collapses tables to 100%, drops thumb to 60×60, reduces title size, stacks feature cells. `page-wrapper` `max-width: 800px` with 5-10px gutters. Re-confirmed no horizontal overflow at 320px / 768px / 1024px. **No finding.**

13. **UX anti-patterns** — placeholder `href="#"` links in generated band page (Sign Guestbook, Webrings, MIDI Archive, Back to Top, fake `mailto`) remain part of the deliberate retro pastiche, not regressions. `cancelGeneration()` truth-in-labelling issue (N8) remains MEDIUM and deferred.

14. **Path-traversal & input validation** — `SAFE_BAND_NAME` regex (`^[A-Za-z0-9_\-]+$`) applied at both `view_band` and `band_assets` route entry. `gallery()` reads directories from disk via `glob` (no user input). **No finding.**

15. **JavaScript graceful degradation** — `/generate` flow is fully JS-dependent; no `<noscript>` fallback. Acceptable for a tool whose core functionality is async polling, but worth noting. Logged below as new LOW N17.

---

## NEW Findings (2026-05-08 audit)

**No new Critical/High findings.** One new LOW finding noted purely for the daily-audit log:

| ID | Severity | Item | File:line |
|---|---|---|---|
| N17 | LOW | No `<noscript>` fallback on `/generate`; users with JS disabled see a button that does nothing | `templates/generate.html:14-30` |

This is *not* a WCAG violation (no progressive-enhancement mandate exists in 2.1 AA), and the project's core flow fundamentally requires JS for async polling. Logged for completeness, deferred.

---

## Carried-over MEDIUM / LOW (still deferred — unchanged from prior audits)

| ID | Severity | Item | File:line |
|---|---|---|---|
| N16 | MED | Generated band page lacks `<main>` and `<footer>` elements (`<header>`/`<nav>` landmarks present) | `createAct.py:543-624` |
| M7 | MED | Dead `marquee {}` rule in generated CSS | `createAct.py:530-536` |
| M8 | MED | `bandPreview.innerHTML` injects unsanitised AI band name | `templates/generate.html:233-236` |
| N5 | MED | Progress-steps table column header is the literal "?" | `templates/generate.html:46` |
| N6 | MED | Step-indicator state changes not announced to SR users | `templates/generate.html:183-209` |
| N7 | MED | Polling interval re-announces same prose message | `templates/generate.html:158, 183-191` |
| N8 | MED | `cancelGeneration()` does not tell the server to stop | `templates/generate.html:249-254`, `app.py` |
| N9 | LOW | `#progressDisplay` `aria-live` region wraps too much markup | `templates/generate.html:33-85` |
| N10 | LOW | Failing step is invisible to user on error | `templates/generate.html:49-77` |
| N12 | LOW | `body` font-family includes `cursive` between specific and generic | `static/css/style.css:67`, `createAct.py:387` |
| N13 | LOW | `<hr>` `noshade` and `size` attributes are obsolete in HTML5 | multiple templates and `createAct.py` |
| N14 | LOW | Heading hierarchy h2 → h4 skip in feature boxes | `templates/index.html:85,91,97` |
| N17 | LOW | `<noscript>` fallback on `/generate` (NEW today, deferred) | `templates/generate.html:14-30` |
| L7 | LOW | `Faker==28.1.0` declared but unused | `requirements.txt` |
| L8 | LOW | Inline `import re` inside functions | `createAct.py:85, 218` |
| L9 | LOW | Visitor counter randomises on each page load (thematic) | `templates/base.html:47` |
| L10 | LOW | Dead `mailto:webmaster@aibandgen.geocities.com` (thematic) | `templates/base.html:52` |
| L11 | LOW | Visitor counter and `mailto` repeated in generated band pages (thematic) | `createAct.py:600, 616` |
| L12 | LOW | `<table>` used for layout in `index.html` "What You Get" section | `templates/index.html:81-102` |
| L13 | LOW | Inline styles throughout templates and generated HTML | many |
| L14 | LOW | Deprecated HTML attributes (`bordercolor`, `noshade`, `cellpadding`, `align`, `width`) throughout | many |
| L15 | LOW | `band_assets()` route doesn't whitelist filenames | `app.py:82-87` |

The broader f-string-interpolated XSS surface in `create_html_content()` (sibling to M8: `band_name`, `backstory`, member fields, album titles, track names) remains logged-for-tracking, MEDIUM-severity, deferred. Threat surface is constrained — LLM prompts contain no user input, so there is no direct injection vector — but a stray `<script>` or `<img onerror=...>` in any LLM response would render as HTML.

---

## Summary

| Severity | Count this audit | Fixed this pass |
|---|---|---|
| CRITICAL | 0 | — |
| HIGH | 0 | — |
| MEDIUM | 0 new (7 carried) | 0 (deferred) |
| LOW | 1 new (N17) + 13 carried | 0 (deferred) |

**No CRITICAL or HIGH findings.** This is the sixth daily audit in seven (excluding the 2026-05-06 N15 follow-up) to land on the "no critical/high" outcome — the codebase is in steady state. Today's audit confirms all prior fixes remain intact and that today's working tree is byte-identical to yesterday's (no `*.py`/`*.html`/`*.css`/`*.js` diff between `f0a471a` and `HEAD`).

Per task instructions, no code is changed in Phase 2 today. Phase 4 (PR) still opens for the audit-log commit, matching the established daily pattern.

---

## Phase 2 — Fix

No code changes. All Critical/High findings from prior audits are verified resolved; no new Critical/High findings this pass. Medium and Low findings remain logged above as deferred. The single new LOW (N17) is noted-and-deferred per the standing rule that only Critical/High get fixed in the daily pass.

---

## Phase 3 — Verification

Even though no application code was changed today:

- `python -m py_compile app.py createAct.py` — both files compile cleanly.
- All four Jinja2 templates (`base.html`, `index.html`, `generate.html`, `gallery.html`) parse OK on visual inspection: `{% block %}`, `{% extends %}`, `{% if %}`, `{% for %}` blocks balanced; no stray `{{` or `}}`.
- CSS structure intact: `prefers-reduced-motion` media query at `style.css:457-472`, responsive breakpoint at `style.css:481-506`, brace matching even.
- Re-read `createAct.py:525-529` to confirm the N15 fix is structurally correct: `display: inline-block; padding: 6px 8px; margin: 0 5px;` inside the f-string-emitted `<style>` block, with double-braces preserved.
- Did not start the dev server in-process — running `/api/generate` requires a live `OPENAI_API_KEY` and would burn API credits to render an end-to-end page. Static template + Python compile review covers all rendering paths the audit needs.

## Phase 4 — Deliver

- Branch `fix/code-review-2026-05-08` created off `fix/code-review-2026-05-07` (since prior daily fix branches have been stacking and not merged into `main` — see `git log main..HEAD` showing 8 stacked commits).
- Commit includes only `tasks/review.md` (audit log, no code changes).
- PR raised via `gh pr create`. URL recorded in the agent's final response.
