# UX & Accessibility Audit — 2026-05-01

**Branch:** `fix/code-review-2026-04-30`
**Reviewer:** Jennifer Mitchelle (Senior UX Design Critic)
**Scope:** UI consistency, WCAG 2.1 AA compliance, design system adherence, responsive layout, UX patterns
**Note on aesthetic:** The "retro 90s GeoCities" look is an intentional, deliberate design choice (see commit `8b971ef`). Findings below are limited to issues that are objectively broken — accessibility violations, layout bugs, security regressions — not stylistic critiques of the retro theme. Where the theme inherently conflicts with WCAG (e.g. `<marquee>`, `<blink>`, Comic Sans), I note pragmatic mitigations rather than demanding the theme be removed.

---

## Context vs. Previous Review

The recheck at `tasks/review-recheck.md` (dated 2026-04-01) describes a state where the templates contained a skip link, semantic landmarks (`<header>/<nav>/<main>/<footer>`), `<fieldset>/<label>` form structure, ARIA labels, `aria-current="page"`, `aria-live` regions, `:focus-visible` styles, `prefers-reduced-motion`, plus security hardening (`SAFE_BAND_NAME` regex and `cleanup_old_generations()`).

**The "Retro 90s overhaul" commit (`8b971ef`) discarded all of those.** The current templates and `app.py` are a fresh authoring that does not include any of those accessibility or security fixes. So this audit re-applies them where appropriate.

---

## Findings

### [CRITICAL] C1 — Missing semantic landmarks across all templates
**File:** `/home/jalloway/projects/ai-bandmaker/templates/base.html` lines 12-54
**Issue:** The page is structured entirely with `<div>` elements — no `<header>`, `<nav>`, `<main>`, or `<footer>`. Screen-reader users rely on landmark navigation (rotor / "skip to" gestures) to jump between regions. Without landmarks, the entire page is a flat list. Violates WCAG 1.3.1 (Info and Relationships) and 2.4.1 (Bypass Blocks).
**Fix:** Replace `<div class="site-banner">` with `<header role="banner">`, `<div class="nav-bar">` with `<nav aria-label="Primary">`, `<div class="main-content">` with `<main id="main-content" tabindex="-1">`, `<div class="site-footer">` with `<footer role="contentinfo">`.

### [CRITICAL] C2 — No skip-to-content link
**File:** `/home/jalloway/projects/ai-bandmaker/templates/base.html` line 11
**Issue:** Keyboard and screen-reader users have no mechanism to bypass the banner+nav and jump directly to page content. Violates WCAG 2.4.1 (Bypass Blocks, Level A).
**Fix:** Add a visually-hidden-until-focused skip link as the first focusable element: `<a class="skip-link" href="#main-content">Skip to main content</a>`. Pair with CSS that reveals it on `:focus`.

### [CRITICAL] C3 — `<marquee>` element with no pause control on band fan pages
**File:** `/home/jalloway/projects/ai-bandmaker/createAct.py` line 518
**Issue:** Generated band pages use `<marquee scrollamount="3">{band_name}</marquee>` for the band name. WCAG 2.2.2 (Pause, Stop, Hide, Level A) requires that any moving/scrolling content lasting longer than 5 seconds offer a mechanism to pause it. `<marquee>` is also a deprecated, non-standard element (removed from HTML5 spec). The band name itself is the page's primary heading — animating it harms readability for users with cognitive/vestibular conditions.
**Fix:** Replace `<marquee>{band_name}</marquee>` with a static `<h1>{band_name}</h1>`. If you want a hint of motion to preserve the retro feel, use a CSS keyframe animation gated behind `@media (prefers-reduced-motion: no-preference)` so it disables for users who request reduced motion. The band name MUST be a heading regardless — the page currently has no `<h1>`.

### [CRITICAL] C4 — No `<h1>` on the generated band fan page
**File:** `/home/jalloway/projects/ai-bandmaker/createAct.py` lines 514-525
**Issue:** The generated band page jumps from `<title>` directly to `<h3>` section headers, with the band name only appearing inside a `<marquee>` (or after C3's fix, somewhere else). Violates WCAG 1.3.1 and 2.4.6 (Headings and Labels). Screen readers report "no heading level 1" and skip-by-heading navigation is broken.
**Fix:** Make the band name a real `<h1>`. Demote section headers from `<h3>` to `<h2>` so the heading hierarchy is contiguous (h1 → h2, not h1 → h3).

### [HIGH] H1 — Path-traversal regex removed from `app.py`
**File:** `/home/jalloway/projects/ai-bandmaker/app.py` lines 54-67
**Issue:** Previous review installed `SAFE_BAND_NAME = re.compile(r'^[A-Za-z0-9_\-]+$')` and validated it in `view_band()` and `band_assets()` before calling `send_from_directory`. That validation is gone in the current code. While `send_from_directory` does some path-safety checks of its own, the explicit allow-list is a defence-in-depth measure that was deliberately added and is now missing. Not strictly a UX issue but a regression worth flagging in the audit log; leaving the fix to a security-focused pass.
**Fix:** Reinstate the `SAFE_BAND_NAME` regex check in both routes. Return 400 (or 404 to avoid leaking existence) for names that fail to match.

### [HIGH] H2 — `generation_status` dict grows unboundedly
**File:** `/home/jalloway/projects/ai-bandmaker/app.py` line 21
**Issue:** Every band-generation request adds an entry keyed by timestamp; nothing prunes old entries. In a long-running process the dict will grow without limit. Previous review introduced `cleanup_old_generations()` to remove entries older than 1 hour — that function is no longer present.
**Fix:** Reinstate a cleanup pass invoked from `api_generate()` (lazy cleanup, no extra threads). Remove entries older than ~1 hour.

### [HIGH] H3 — Form controls in `generate.html` lack explicit `type="button"`
**File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html` lines 26, 80, 97, 101, 113
**Issue:** `<button>` defaults to `type="submit"` per the HTML spec. These buttons are not currently inside a `<form>` (so the default is harmless today), but if a `<form>` ancestor is ever introduced — for example by wrapping the page during a future refactor — pressing Enter on any of them will trigger an unintended submission. Always specify `type="button"` for non-submit buttons. Trivial to fix and prevents future regressions.
**Fix:** Add `type="button"` to all five `<button>` elements: `generateBtn`, `cancelBtn`, `viewBandBtn`, `generateAnotherBtn`, `retryBtn`.

### [HIGH] H4 — Progress region not announced to screen readers
**File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html` lines 33-85
**Issue:** The `#progressDisplay` region is updated dynamically (status messages, percent, step indicators) but has no `aria-live` attribute. Screen-reader users will hear the initial state and then nothing else as generation proceeds. They have no way to know the band is being generated or when it completes. Violates WCAG 4.1.3 (Status Messages, Level AA).
**Fix:** Add `aria-live="polite"` and `aria-atomic="false"` to the `#progressMessage` element (or to a wrapping container). The success and error messages should also be in a polite live region.

### [HIGH] H5 — (not applicable to current template — placeholder kept for traceability)
**Note:** Previous review flagged missing `<label>` on `<select>` elements. The current `generate.html` has no `<select>` controls — generation is fully randomised on the server. **No action needed.**

### [HIGH] H6 — Missing `:focus-visible` styles on interactive elements
**File:** `/home/jalloway/projects/ai-bandmaker/static/css/style.css`
**Issue:** Buttons, links, and skip-link have no explicit focus indicator. Browser defaults differ; Chromium's blue ring is fine but is often clobbered by the heavy retro borders (`border: 2px outset #6666cc`). Keyboard users may lose track of focus completely on `.retro-button` because the button already looks "active" without focus. Violates WCAG 2.4.7 (Focus Visible, Level AA).
**Fix:** Add a high-contrast `:focus-visible` outline to `a`, `button`, `.retro-button`, `.retro-button-small`, `.big-link`, and `.skip-link` — e.g. `outline: 3px solid #ffff00; outline-offset: 2px;`.

### [HIGH] H7 — Animations not gated by `prefers-reduced-motion`
**File:** `/home/jalloway/projects/ai-bandmaker/static/css/style.css` lines 388-396; `/home/jalloway/projects/ai-bandmaker/static/js/main.js` lines 7-15
**Issue:** The `.blink` keyframe runs unconditionally, and `main.js` runs a `setInterval` that mutates `.banner-stars` opacity every 2 seconds. Users with vestibular disorders or photosensitive epilepsy can't opt out. The 1.2s blink cycle is below the 3-flash-per-second WCAG 2.3.1 threshold, but combined with the pulsing star opacity it harms users with motion sensitivity. Best-practice violation of WCAG 2.3.3 (Animation from Interactions, AAA) and the spirit of 2.2.2 (Pause, Stop, Hide).
**Fix:** Wrap `.blink` and the star-twinkle JS interval in `prefers-reduced-motion` checks. CSS: `@media (prefers-reduced-motion: reduce) { .blink { animation: none; } }`. JS: gate the `setInterval` behind `if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches)`.

### [HIGH] H8 — Insufficient color contrast on placeholder text and footer
**File:** `/home/jalloway/projects/ai-bandmaker/templates/gallery.html` line 27; `/home/jalloway/projects/ai-bandmaker/static/css/style.css` line 380
**Issue:**
- `[no photo]` text uses `color:#666666` on `background-color:#0a0a1a`. Contrast ratio approximately 3.4:1 — fails WCAG 1.4.3 AA (4.5:1 required for normal text).
- `.footer-copy { color: #666666; }` on the dark page background — same problem, ratio approximately 3.4:1.
- `.feature-box p { color: #aaaaaa; }` on `#0a0a2a` — ratio approximately 8.3:1, OK.
**Fix:** Bump these `#666666` values to at least `#9999bb` (approximately 6.5:1) or `#aaaaaa` (approximately 8.3:1). Footer copy can stay muted but must clear 4.5:1.

### [HIGH] H9 — Touch targets below 24x24 minimum
**File:** `/home/jalloway/projects/ai-bandmaker/static/css/style.css` lines 249-260
**Issue:** `.retro-button-small` has `padding: 4px 12px` and `font-size: 0.85em` (around 12px). Effective height around 20-22px. WCAG 2.5.5 (Target Size, AAA) recommends 44x44; WCAG 2.5.8 (Target Size Minimum, AA) requires 24x24 for non-inline targets. The gallery's `[ VIEW ]` link buttons are too small for touch users with motor impairments.
**Fix:** Bump padding to `8px 16px` and ensure a `min-height: 32px` (or use `min-height: 44px` to meet AAA).

---

## Medium / Low (logged, not fixed in this pass)

### [MEDIUM] M1 — Deprecated HTML attributes throughout generated band page
**File:** `/home/jalloway/projects/ai-bandmaker/createAct.py`
**Issue:** Generated band pages use deprecated HTML4 presentation attributes: `bordercolor=`, `color=` on `<hr>`, `noshade`, `cellpadding`, `cellspacing`, `border=` on `<table>`, `<a name="...">` anchors. They render in current browsers but are out of spec.
**Fix (deferred):** Migrate to CSS-driven equivalents while preserving the visual look. Use `id="backstory"` instead of `<a name="backstory">`, move table presentation to the `<style>` block.

### [MEDIUM] M2 — Inline styles throughout templates and generated HTML
**File:** All templates and `createAct.py`
**Issue:** Many `style="color:#xxxxxx; ..."` attributes scattered across templates. Duplicates the design system, defeats CSP `style-src` if added later.
**Fix (deferred):** Extract repeated inline styles to utility classes.

### [MEDIUM] M3 — `band_assets()` route doesn't restrict file types
**File:** `/home/jalloway/projects/ai-bandmaker/app.py` lines 64-67
**Issue:** `/band/<band_name>/<filename>` will serve any file in the band directory. Today directories only contain `home.html` and `band_photo.jpg`, but the route should whitelist filenames as defence-in-depth.
**Fix (deferred):** Restrict to known filenames.

### [MEDIUM] M4 — `<table>` used for layout in `index.html` features section
**File:** `/home/jalloway/projects/ai-bandmaker/templates/index.html` lines 81-102
**Issue:** "What You Get" three-column grid is a layout table. Screen readers announce it as tabular data when it isn't. WCAG 1.3.1.
**Fix (deferred):** Replace with a CSS grid/flex container of `<div>` cards.

### [MEDIUM] M5 — Visitor counter randomises on every page load
**File:** `/home/jalloway/projects/ai-bandmaker/templates/base.html` line 45
**Issue:** Refreshing yields a different (often smaller) number — incoherent. Pure cosmetic joke; flagged for completeness.
**Fix (deferred):** Use a stable per-session number or a real counter.

### [MEDIUM] M6 — `mailto:webmaster@aibandgen.geocities.com` is a dead address
**File:** `/home/jalloway/projects/ai-bandmaker/templates/base.html` line 50
**Issue:** GeoCities shut down in 2009. Clicking opens the user's mail client to nowhere.
**Fix (deferred):** Remove the mailto, point to a real address, or render as plain text.

### [LOW] L1 — `aria-current="page"` not set on active nav item
**File:** `/home/jalloway/projects/ai-bandmaker/templates/base.html` lines 26-28
**Fix (deferred):** Pass current route to template and set `aria-current="page"`.

### [LOW] L2 — `import json` unused in `app.py`
**File:** `/home/jalloway/projects/ai-bandmaker/app.py` line 3
**Fix (deferred):** Remove the import.

### [LOW] L3 — Inline `import re` inside functions in `createAct.py`
**File:** `/home/jalloway/projects/ai-bandmaker/createAct.py` lines 85, 218
**Fix (deferred):** Move to module-level imports.

### [LOW] L4 — `Faker==28.1.0` declared but unused
**File:** `/home/jalloway/projects/ai-bandmaker/requirements.txt`
**Fix (deferred):** Remove from requirements.

### [LOW] L5 — Comic Sans MS as primary font
**File:** `/home/jalloway/projects/ai-bandmaker/static/css/style.css` line 15
**Issue:** Intentional retro choice. Comic Sans is divisive in body copy but is acceptable here given the deliberate aesthetic and 14px size.
**Fix:** No action — intentional.

### [LOW] L6 — Banner stars opacity twinkle has no purpose
**File:** `/home/jalloway/projects/ai-bandmaker/static/js/main.js` lines 8-15
**Issue:** Pure decoration that runs `setInterval` indefinitely. Covered by H7 (gate behind reduced-motion).

---

## Summary

| Severity | Count |
|---|---|
| CRITICAL | 4 |
| HIGH | 8 (H5 not actionable for current template) |
| MEDIUM | 6 |
| LOW | 6 |

**Phase 2 plan:** Fix C1, C2, C3, C4, H1, H2, H3, H4, H6, H7, H8, H9. Skip H5 (not applicable). Leave all MEDIUM and LOW items logged but unfixed.
