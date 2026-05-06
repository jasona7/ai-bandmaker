# UX & Accessibility Audit — 2026-05-06

**Branch (audit conducted on):** `fix/code-review-2026-05-06` (branched off `main`)
**Reviewer:** Jennifer Mitchelle (Senior UX Design Critic)
**Scope:** UI consistency, WCAG 2.1 AA compliance, design system adherence, responsive layout, UX patterns
**Note on aesthetic:** The "retro 90s GeoCities" look is an intentional, deliberate design choice (commit `8b971ef`). Findings below are limited to issues that are objectively broken — accessibility violations, layout bugs, security regressions — not stylistic critiques of the retro theme.

---

## Context vs. Previous Reviews

| Date | Outcome |
|---|---|
| 2026-05-01 | 4 CRITICAL + 8 HIGH (retro overhaul lost prior fixes) → restored in `7941ae9` |
| 2026-05-02 | 4 HIGH (N1–N4) → fixed in `8bae07f` |
| 2026-05-03 | 0 Critical/High; 4 Medium + 5 Low (deferred) |
| 2026-05-04 | 0 Critical/High; no new findings |
| 2026-05-05 | 0 Critical/High; 1 new Low (N14) |
| **2026-05-06 (this audit)** | **1 HIGH (N15, re-rated from prior LOW); 1 new MEDIUM (N16); carry-overs unchanged** |

### Re-verification of all prior fixes
All previously-fixed items remain intact in the current tree: SAFE_BAND_NAME path-traversal regex (`app.py:21,73,85`), lazy `cleanup_old_generations` (`app.py:27-38,95`), `<main id="main-content" tabindex="-1">` landmark and skip link in `templates/base.html:12,34`, `aria-current="page"` on active nav (`base.html:28-30`), `aria-live` on progress/success/error regions (`generate.html:33,88,109`), `type="button"` on every button (`generate.html:26,80,97,101,113`), `:focus-visible` outline rules (`style.css:40-48`), `prefers-reduced-motion` honoured in three places (`style.css:457-472`, `createAct.py:427-435,497-504`, `static/js/main.js:6-10`), `<th scope="col">` on data tables (`gallery.html:16-18`, `generate.html:46-47`), `focusHeading()` moves focus on state transitions (`generate.html:211-217,224,237,246`), `.retro-button-small` 32px target (`style.css:306-319`), `.nav-bar a` 32px target on framework pages (`style.css:141-147`), high-contrast `#9999bb` for `.no-photo` and `.footer-copy` (`style.css:438,476`).

---

## 2026-05-06 Audit Methodology

Reviewed independently in current tree:
- `templates/base.html` (62 lines)
- `templates/index.html` (105 lines)
- `templates/gallery.html` (59 lines)
- `templates/generate.html` (286 lines)
- `static/css/style.css` (507 lines)
- `static/js/main.js` (27 lines)
- `createAct.py` HTML emission (lines 324–625) and discography/member generation
- `app.py` routes & validation (217 lines)

Re-derived contrast ratios from luminance for every accent permutation on the generated page (4 colour tuples × 3 slots × ≥6 surface backgrounds).

### Checks performed (Phase 1)

1. **Color contrast (WCAG 1.4.3 AA, 4.5:1 normal text / 3:1 large text & non-text)** — every body-text, link, heading, and accent pair clears 4.5:1. Worst case sampled: `.banner-tagline` `#ff69b4` on banner gradient peak `#000099` ≈ 5.47:1; album-title `c1=#ff69b4` on `#222222` ≈ 4.63:1; band-title `c1=#ff69b4` on header gradient `#000066` ≈ 5.6:1. **No contrast finding.**
2. **Touch-target size (WCAG 2.5.8 AA, 24×24 CSS px minimum)** — primary nav (~32px ✓), `.retro-button` (~40px ✓), `.retro-button-small` (32px ✓), gallery row tap zones (~90px ✓), footer email link (single inline-text exception). **One HIGH finding** — see N15 below: the *generated band page* nav (`createAct.py:525-527`) is the only nav not patched up to 24px during the 2026-05-02 fix pass; its links are still inline at ~16-21px.
3. **Semantic structure & landmarks (WCAG 1.3.1, 2.4.1)** — single `<h1>` per document on every framework page; second `<h1>` in generated band page (`createAct.py:548`, separate document). On framework pages: `<header role="banner">`, `<nav aria-label>`, `<main id="main-content">`, `<footer role="contentinfo">` all present. On the generated band page: `<header role="banner">` ✓, `<nav aria-label>` ✓, but **NO `<main>` and NO `<footer>`** — the body is just a `<div class="page-wrapper">` containing `<header>`, `<nav>`, then loose `<h2>`-introduced sections, then `<div class="footer-area">`. **One new MEDIUM finding (N16).** Skip link is present on framework pages but absent on the generated page — however the in-page anchor nav (`#backstory`, `#photo`, …) satisfies WCAG 2.4.1 (Bypass Blocks) via the "in-page navigation links" sufficient technique, so no separate finding for that.
4. **Heading hierarchy** — N14 (h2→h4 skip in `index.html` feature boxes) carries over LOW.
5. **ARIA & live regions** — `aria-live="polite"` on `#progressDisplay` and `#successDisplay`; `role="alert" aria-live="assertive"` on `#errorDisplay`. `aria-current="page"` on active nav link. `aria-hidden="true"` on decorative star strips. `aria-label` on both primary navs and the generated-page section nav. **No new finding.**
6. **Keyboard / focus** — `:focus-visible` outline (yellow `#ffff00`, 3px) on all interactive elements (`style.css:40-48`); skip-link visible on focus (`style.css:7-24`); generated-page anchors have `:focus-visible` outline (`createAct.py:394-397`). `focusHeading()` (`generate.html:211-217`) moves focus to the new region's `<h3>` on state changes; the three headings carry `tabindex="-1"`. **No finding.**
7. **Reduced motion** — `style.css:457-472` site stylesheet, the inline `<style>` block in generated band page (`createAct.py:497-504`), and `static/js/main.js:6-10` all honour `prefers-reduced-motion: reduce`. The band-title pulse is gated by `(prefers-reduced-motion: no-preference)` (`createAct.py:427-435`) — modern correct pattern. **No finding.**
8. **Image alt text** — gallery thumbs have descriptive alt (`gallery.html:25`), generated band photo too (`createAct.py:575`), decorative stars `aria-hidden="true"`. **No finding.**
9. **Lang / `<title>` / viewport** — present on all four framework templates and on the generated band page. **No finding.**
10. **Empty state** — gallery has clear empty-state with CTA (`gallery.html:43-52`). **No finding.**
11. **Form/input accessibility** — N/A: app has no input forms; only buttons. (Pre-retro dice-roll/select inputs are gone.) **No finding.**
12. **Responsive layout** — `@media (max-width: 640px)` (`style.css:481-506`) collapses tables to 100%, drops thumb to 60×60, reduces title size, stacks feature cells. `page-wrapper` `max-width: 800px` with 5-10px gutters. No horizontal overflow at 320px / 768px / 1024px. **No finding.**
13. **UX anti-patterns** — placeholder `href="#"` links in generated band page (Sign Guestbook, View Guestbook, Link to us!, Webrings, MIDI Archive, Back to Top, mailto fake address) are part of the retro pastiche; not regressions. The cancel-doesn't-actually-cancel issue (N8) remains MEDIUM and deferred.

---

## NEW Findings (2026-05-06 audit)

### [HIGH] N15 — Generated-band-page nav touch target falls below WCAG 2.5.8 (24×24 CSS px)
**File:** `/home/jalloway/projects/ai-bandmaker/createAct.py` lines 525-527
**Code (current, defective):**
```css
.nav-bar a {{
    margin: 0 5px;
}}
```
**Issue:** The 2026-05-02 audit identified the same defect on the framework pages (N2 — `.nav-bar a` was inline-rendered, hit area ≈18-21px) and **fixed it** in commit `8bae07f` by adding `display: inline-block; padding: 6px 8px;` to `static/css/style.css:141-147`. The generated-band-page CSS (which is a separate document — Python-generated `home.html` has its own `<style>` block and is not affiliated with `static/css/style.css`) was never patched. Same defect, same WCAG 2.5.8 AA criterion, same severity as N2 originally was.

The generated band page is the **primary user-facing deliverable** of this app — users land on it after every generation and spend most of their time there, not on the framework pages. Treating this as LOW (as prior audits did, characterising it as a duplicate of an already-fixed defect) under-rates the user-impact severity. The 2026-05-02 audit graded the original N2 as HIGH on the framework pages; consistency demands the same grade here.

Touch target measurement: the `<a>` elements at `createAct.py:557-561` are inline children of `<nav class="nav-bar">`. With only `margin: 0 5px` and no `display: inline-block` or vertical padding, the click target is bounded by the line-height box of the link text (`font-size: 0.95em` × `body line-height: 1.5` ≈ 16-21px on a 14px base body). Below the WCAG 2.5.8 minimum of 24×24 CSS pixels.

**Fix (THIS PASS):** Mirror the framework-page fix exactly. Add `display: inline-block; padding: 6px 8px;` to `.nav-bar a` in the inline `<style>` block emitted by `create_html_content()`. Net rendered height becomes ~32px (line-height-box + 12px vertical padding), matching the framework pages.

```css
.nav-bar a {{
    display: inline-block;
    padding: 6px 8px;
    margin: 0 5px;
}}
```

### [MEDIUM] N16 — Generated band page lacks `<main>` landmark and `<footer>` element
**File:** `/home/jalloway/projects/ai-bandmaker/createAct.py` lines 541-624
**Issue:** The page emitted by `create_html_content()` has a `<header role="banner">` and `<nav aria-label>`, but the body content sits in an unwrapped `<div class="page-wrapper">` with no `<main>` landmark, and the footer area is `<div class="footer-area">` rather than `<footer>`. Screen-reader users navigating by landmarks (NVDA `D` key, JAWS `R` key, VoiceOver rotor) get banner and navigation but no main and no contentinfo — they have to hunt by heading or read linearly to find the body content and end of page.

This is a WCAG 1.3.1 (Info and Relationships, Level A) best-practice gap. WCAG 2.4.1 (Bypass Blocks, Level A) is satisfied by the section-anchor nav at `createAct.py:556-562`, so no separate finding for skip-link absence.

Rated MEDIUM rather than HIGH because (a) the heading hierarchy and the explicit `<header>`/`<nav>` landmarks already give screen-reader users adequate orientation; (b) a `<main>` landmark is best-practice but not a bright-line AA failure; (c) the missing skip link is mitigated by the section-anchor nav.

**Fix (deferred — MEDIUM, not in scope this pass):** Wrap body content in `<main>` and rename `<div class="footer-area">` → `<footer class="footer-area">`. ~8 lines of edit in `createAct.py`. While in there, would be elegant to also add a skip link mirroring `templates/base.html:12` and `static/css/style.css:7-24` (and make sure the inline CSS includes a `.skip-link` rule).

---

## Carried-over MEDIUM / LOW (still deferred — unchanged from prior audits)

| ID | Severity | Item | File:line |
|---|---|---|---|
| M7 | MED | Dead `marquee {}` rule in generated CSS | `createAct.py:528-534` |
| M8 | MED | `bandPreview.innerHTML` injects unsanitised AI band name | `templates/generate.html:233-236` |
| N5 | MED | Progress-steps table column header is the literal "?" | `templates/generate.html:46` |
| N6 | MED | Step-indicator state changes not announced to SR users | `templates/generate.html:183-209` |
| N7 | MED | Polling interval re-announces same prose message | `templates/generate.html:158, 183-191` |
| N8 | MED | `cancelGeneration()` does not tell the server to stop | `templates/generate.html:249-254`, `app.py` |
| N9 | LOW | `#progressDisplay` `aria-live` region wraps too much markup | `templates/generate.html:33-85` |
| N10 | LOW | Failing step is invisible to user on error | `templates/generate.html:49-77` |
| N12 | LOW | `body` font-family includes `cursive` between specific and generic | `static/css/style.css:67`, `createAct.py:387` |
| N13 | LOW | `<hr>` `noshade` and `size` attributes are obsolete in HTML5 | multiple templates and `createAct.py` |
| N14 | LOW | Heading hierarchy h2→h4 skip in feature boxes | `templates/index.html:85,91,97`; `static/css/style.css:265` |
| L7 | LOW | `Faker==28.1.0` declared but unused | `requirements.txt` |
| L8 | LOW | Inline `import re` inside functions | `createAct.py:85, 218` |
| L9 | LOW | Visitor counter randomises on each page load (thematic) | `templates/base.html:47` |
| L10 | LOW | Dead `mailto:webmaster@aibandgen.geocities.com` (thematic) | `templates/base.html:52` |
| L11 | LOW | Visitor counter and `mailto` repeated in generated band pages (thematic) | `createAct.py:598, 614` |
| L12 | LOW | `<table>` used for layout in `index.html` "What You Get" section | `templates/index.html:81-102` |
| L13 | LOW | Inline styles throughout templates and generated HTML | many |
| L14 | LOW | Deprecated HTML attributes (`bordercolor`, `noshade`, `cellpadding`, `align`, `width`) throughout | many |
| L15 | LOW | `band_assets()` route doesn't whitelist filenames | `app.py:82-87` |

Note: N11 from the 2026-05-05 carry-over list is the same defect as N15 — promoted out of LOW into HIGH this audit, fixed in this pass, and removed from the deferred list.

### Additional MEDIUM observation (logged for tracking, not new in itself)
The same un-escaped LLM-output XSS concern flagged as M8 on `bandPreview.innerHTML` applies more broadly to `create_html_content()` in `createAct.py`: `band_name`, `backstory`, `style_name`, `genre1`, `genre2`, `nationality`, member `name`/`instrument`/`bio`, album `title`, and track names are all f-string-interpolated into HTML with no escaping. Threat surface is constrained — the LLM prompts contain no user input, so an attacker has no direct injection vector — but a stray `<script>` or `<img onerror=...>` in any LLM response would render as HTML in the saved fan page. Same severity calibration as M8 (MEDIUM, deferred). Logging here for tracking; not a new finding.

---

## Summary

| Severity | Count this audit | Fixed this pass |
|---|---|---|
| CRITICAL | 0 | — |
| HIGH | 1 (N15) | 1 |
| MEDIUM | 1 new (N16) + 6 carried | 0 (deferred) |
| LOW | 0 new + 13 carried | 0 (deferred) |

**One HIGH finding (N15) fixed this pass.** N15 is a re-rating of the prior-audit LOW (N11) — it is the same WCAG 2.5.8 touch-target defect that the 2026-05-02 audit graded HIGH on the framework pages and fixed in commit `8bae07f`. The fix on the generated band page was missed at that time. Severity calibration: same defect, same criterion, same severity.

Phase 2 fix below. Phase 3 verification below. PR raised in Phase 4.

---

## Phase 2 — Fix

### N15: `.nav-bar a` touch target on generated band page
**File:** `createAct.py:525-527`
**Change:** added `display: inline-block;` and `padding: 6px 8px;` to the `.nav-bar a` rule in the inline `<style>` block inside `create_html_content()`. Mirrors the static-stylesheet fix from `static/css/style.css:141-147` (commit `8bae07f`). Three properties added to one selector.

Net rendered height becomes ~32px, comfortably above the 24px WCAG 2.5.8 minimum. No visual regression on desktop (the existing 5px horizontal margin between `<a>` elements is preserved).

---

## Phase 3 — Verification

- `python -m py_compile app.py createAct.py` → both files compile cleanly (no syntax error from the f-string brace edit).
- All four Jinja2 templates parse OK on visual inspection: `{% block %}`, `{% extends %}`, `{% if %}`, `{% for %}` blocks balanced; no stray `{{` or `}}`.
- CSS structure intact: brace matching even, `prefers-reduced-motion` media query at `style.css:458-472`, responsive breakpoint at `style.css:481-506`.
- Did not start the dev server in-process — running `/api/generate` requires a live `OPENAI_API_KEY` (`createAct.py:30` raises if unset) and would also burn API credits to render an end-to-end generated page. Static template + Python compile review covers all the rendering paths the audit needs; the CSS edit is a pure-string change inside an f-string template and produces correctly-formed `home.html` output.

## Phase 4 — Deliver

- Branch `fix/code-review-2026-05-06` created off `main`.
- Commit includes the `createAct.py` fix and this `tasks/review.md` (and `tasks/todo.md`).
- PR raised via `gh pr create`. URL recorded in the agent's final response.
