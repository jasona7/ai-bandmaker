# UX & Accessibility Code Review
**Date**: 2026-04-13
**Reviewer**: Jennifer Mitchelle (Senior UX Design Critic, Swords, Ireland)
**Branch**: fix/code-review-2026-04-12

## Summary

Tenth periodic review of the AI Band Generator. The main application templates (`base.html`, `index.html`, `gallery.html`, `generate.html`) and `style.css` remain in strong shape with well-implemented accessibility patterns. The current `createAct.py` template (v2) includes semantic HTML, skip links, landmarks, correct heading hierarchy, `prefers-reduced-motion`, `focus-visible`, ARIA labels, and XSS escaping -- all correct.

However, a significant structural observation emerges from this audit that was not surfaced in prior reviews: **all 12 existing fan pages are template v1 (migrated legacy), and no v2 pages have ever been generated.** The only migration patch applied was focus-visible injection (N-021). This means all 12 served fan pages lack skip links, `<main>` landmarks, `<header>`/`<footer>` landmarks, `prefers-reduced-motion`, `aria-hidden` on decorative elements, and proper `<nav>` elements. These are not new code defects -- the v2 template is correct -- but they represent a gap in the deployed user experience that warrants a new consolidated issue.

One new medium issue and one new low issue are identified. All previously open issues remain open. No regressions found in previously resolved items.

**Files reviewed:**
- `templates/base.html`, `templates/index.html`, `templates/generate.html`, `templates/gallery.html`
- `static/css/style.css` (724 lines), `static/js/main.js` (19 lines)
- `app.py` (285 lines), `createAct.py` (822 lines)
- Generated fan pages: all 12 band directories (all template_version 1, all migrated)

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 8 |
| Low | 16 |

---

## Status of Previous Issues

| Prior ID | Issue | Status |
|---|---|---|
| N-001 | Color contrast failure in accent color tuple (#ff6666) | **RESOLVED** -- verified, replacement #ff7777 passes at 6.16:1 |
| N-002 | Residual inline styles in generated fan pages | Open (Medium) |
| N-003 | Guestbook links use `href="#"` with no indication | Open (Medium) |
| N-004 | Legacy generated pages still accessible via direct URL without band_info.json check | Open (Medium) |
| N-005 | `<hr>` elements use deprecated HTML attributes | Open (Low) |
| N-006 | Feature grid boxes lack equal height content alignment | Open (Low) |
| N-007 | `role="form"` on `<form>` element is redundant | Open (Low) |
| N-008 | No `<meta name="description">` on any page | Open (Low) |
| N-009 | Gallery table lacks responsive handling for narrow viewports | Open (Medium) |
| N-010 | Generated fan page nav pipe separators not hidden from AT | Open (Low) |
| N-011 | Blink animation timing mismatch (`linear` vs `step-start`) | Open (Low) |
| N-012 | Band directory path validation blocks non-ASCII band names | Open (Medium) |
| N-014 | Inline `import re` inside functions in createAct.py | Open (Low) |
| N-015 | Inline style on visitor count in generated pages | Open (Low) -- subsumed under N-002 |
| N-016 | Inconsistent path resolution between gallery and view_band routes | Open (Medium) |
| N-017 | No focus management after gallery page load | Open (Low) |
| N-018 | Fixed polling interval with no backoff | Open (Low) |
| N-019 | Generated fan pages use `!important` overrides in responsive styles | Open (Medium) |
| N-020 | Generated fan page `<br>` tag after decorative stars in header | Open (Low) |
| N-021 | Generated fan pages have no focus indicator styles | **RESOLVED** -- verified, all 12 pages have `a:focus-visible` rule |
| N-022 | Generated fan page body has no explicit line-height | Open (Low) |
| N-023 | Gallery displays zero bands because no `band_info.json` files exist | **RESOLVED** -- verified, all 12 directories have band_info.json |
| N-024 | Older generated pages use `#666666` text | **RESOLVED** -- verified, no #666666 found in any served page |
| N-025 | Older generated pages use deprecated `<marquee>` element | Open (Low) |
| N-026 | Older generated pages use `<a name="">` anchors instead of `id` | Open (Low) |
| N-027 | Older generated pages skip heading level (h1 to h3) | Open (Low) |
| N-028 | Dead gallery links from special-character band names | **RESOLVED** -- verified, gallery route filters by SAFE_BAND_NAME |
| N-029 | Legacy-format fan pages have fixed-position footer that occludes content | Open (Low) |
| N-030 | Legacy-format fan pages render empty band members section | Open (Low) |

---

## Escalation Assessment

Each open medium issue was reviewed to determine whether any should be escalated to high:

- **N-002 (inline styles)**: Remains medium. Affects maintainability and user stylesheet overriding, but does not block functionality or violate WCAG A/AA requirements in isolation.
- **N-003 (guestbook href="#")**: Remains medium. SC 2.4.4 Link Purpose is Level A, but these are clearly themed as retro-decorative within the fan page context and do not mislead users into thinking they will navigate somewhere useful. A screen reader user would hear "Sign the Guestbook, link" and tab away. No data loss or broken flow.
- **N-004 (legacy pages without band_info.json check)**: Remains medium. Direct-URL access to legacy pages is a minor consistency issue; no security impact since `send_from_directory` is safe.
- **N-009 (gallery table responsive)**: Remains medium. SC 1.4.10 Reflow at Level AA, but the table is still usable at 320px -- just cramped, not broken.
- **N-012 (non-ASCII path validation)**: Remains medium. Two bands (ChaoDeCorais, **VelvetEchoes) are filtered from gallery by SAFE_BAND_NAME, so they are hidden but not broken links. The data exists but is inaccessible.
- **N-016 (path resolution inconsistency)**: Remains medium. Latent bug that would only manifest if the Flask working directory changes, which is uncommon in typical deployment.
- **N-019 (!important overrides)**: Remains medium. SC 1.4.12 Text Spacing concern, but only affects the three declarations in the mobile breakpoint of generated pages.
- **N-031 (NEW -- see below)**: Assessed at medium. All 12 served fan pages lack skip links, landmarks, and `prefers-reduced-motion`. These are WCAG Level A (SC 2.4.1 Bypass Blocks) and Level AAA (SC 2.3.3) concerns. However, because the v2 template is correct and will apply to all future generations, and the existing pages are static artifacts, this is a migration gap rather than a systemic defect. Stays medium.

No escalations warranted this cycle.

---

## New Issues

### N-031 (NEW, Medium): All 12 existing fan pages lack skip links, landmarks, and prefers-reduced-motion

- **Files**: All 12 band directories (`*/home.html`), all template_version 1
- **Problem**: The v2 template in `createAct.py` includes skip links, `<main>` landmark, semantic `<header>`/`<footer>`/`<nav>` elements, `prefers-reduced-motion` for the blink animation, and `aria-hidden` on decorative stars. However, all 12 existing fan pages were generated with the v1 template and only received the N-021 focus-visible migration patch. Specifically, all 12 pages are missing:
  - Skip link (`<a href="#main" class="skip-link">`) -- 0 of 12 have it
  - `<main>` landmark -- 0 of 12 have it
  - `<header>` landmark (8 use `<table class="header-table">` for layout, 4 use `<header>` but no `<main>`)
  - `<footer>` landmark (8 use `<div class="footer-area">`, 4 use `<footer>` but with `position: fixed` bug)
  - `<nav>` element (8 use `<div class="nav-bar">`, 4 legacy pages use `<nav>`)
  - `prefers-reduced-motion` (0 of 12 have it, yet all have `.blink` animation)
  - `aria-hidden` on decorative badge-row and visitor counter (0 of 12)
- **WCAG**: SC 2.4.1 Bypass Blocks (Level A -- skip links), SC 1.3.1 Info and Relationships (Level A -- landmarks), SC 2.3.3 Animation from Interactions (Level AAA -- prefers-reduced-motion advisory)
- **Impact**: Users navigating these 12 pages with assistive technology cannot skip to main content, cannot use landmark navigation, and cannot disable the blinking animation via OS preferences.
- **Fix**: Extend the migration script to inject skip links, wrap content in `<main>`, replace `<div class="nav-bar">` with `<nav>`, add `prefers-reduced-motion` media query to the blink animation, and add `aria-hidden="true"` to decorative badge-row and visitor counter. This is a batch operation across 12 files.

### N-032 (NEW, Low): Generated fan page `band_assets` route does not validate the `filename` parameter

- **File**: `app.py:107-112`
- **Problem**: The `band_assets()` route validates `band_name` against `SAFE_BAND_NAME` but does not validate `filename`. While Flask's `send_from_directory` internally uses `safe_join` to prevent directory traversal, defense-in-depth would suggest validating `filename` as well (e.g., restrict to known extensions like `.jpg`, `.json`, `.html`). A malicious request to `/band/ValidBand/../../etc/passwd` would be blocked by Flask, but an explicit allowlist is more robust.
- **Fix**: Add a filename validation check: `if not re.match(r'^[\w\-]+\.(jpg|json|html)$', filename): return "Invalid filename", 400`

---

## Medium Issues (carried forward)

### N-002: Residual inline styles in generated fan pages
- **File**: `createAct.py:705,708,726`
- **Problem**: Three inline `style` attributes remain in the v2 template (`text-align:center`, `color:#888888`, visitor count color).
- **Fix**: Extract to named CSS classes.

### N-003: Guestbook links use `href="#"` with no indication of non-functionality
- **File**: `createAct.py:706,709-711`
- **Problem**: Five decorative links use `href="#"`. Screen reader users encounter these as actionable links that navigate nowhere meaningful.
- **WCAG**: SC 2.4.4 Link Purpose (In Context), Level A
- **Fix**: Replace with `<span>` styled as `.faux-link`, or add `aria-disabled="true"`.

### N-004: Legacy generated pages still accessible via direct URL without band_info.json check
- **File**: `app.py:95-104`
- **Problem**: `view_band()` serves any directory's `home.html` without checking for `band_info.json`.
- **Fix**: Add `band_info.json` existence check to `view_band()`.

### N-009: Gallery table lacks responsive handling for narrow viewports
- **File**: `static/css/style.css:449-492`, `templates/gallery.html:14-47`
- **Problem**: Below ~400px, the three-column gallery table is cramped.
- **WCAG**: SC 1.4.10 Reflow, Level AA
- **Fix**: Add sub-400px breakpoint hiding photo column or switch to card layout.

### N-012: Band directory path validation blocks non-ASCII and special-character band names
- **File**: `app.py:36`
- **Problem**: `SAFE_BAND_NAME` regex blocks `ChaoDeCorais` (non-ASCII tilde) and `**VelvetEchoes` (asterisks). Both are filtered from gallery (N-028 fix) so they are hidden, but the underlying data is inaccessible.
- **Fix**: Broaden regex for Unicode support or sanitize names at generation time.

### N-016: Inconsistent path resolution between gallery and view_band routes
- **File**: `app.py:66-86,95-104`
- **Problem**: Gallery uses `app.root_path`; `view_band()` uses relative path. Would fail if CWD differs from project root.
- **Fix**: Use `app.root_path` consistently.

### N-019: Generated fan pages use `!important` overrides in responsive styles
- **File**: `createAct.py:619,622,625`
- **Problem**: `!important` in mobile breakpoint is unnecessary.
- **WCAG**: SC 1.4.12 Text Spacing concern
- **Fix**: Remove `!important` from all three declarations.

---

## Low Issues (carried forward + new)

### N-005: `<hr>` elements use deprecated HTML attributes
- **File**: `createAct.py:672,679,692,699,704`

### N-006: Feature grid boxes lack equal height content alignment
- **File**: `static/css/style.css:304`

### N-007: `role="form"` on `<form>` element is redundant
- **File**: `templates/generate.html:18`

### N-008: No `<meta name="description">` on any page
- **File**: `templates/base.html:3-8`

### N-010: Generated fan page nav pipe separators not hidden from AT
- **File**: `createAct.py:661`

### N-011: Blink animation timing mismatch between main app and generated pages
- **File**: `createAct.py:584` vs `static/css/style.css:650`

### N-014: Inline `import re` inside functions in createAct.py
- **File**: `createAct.py:115,252`

### N-015: Inline style on visitor count in generated pages
- **File**: Subsumed under N-002

### N-017: No focus management after gallery page load
- **File**: `templates/gallery.html`

### N-018: Fixed polling interval with no backoff
- **File**: `templates/generate.html:355`

### N-020: Generated fan page `<br>` tag after decorative stars
- **File**: `createAct.py:651`

### N-022: Generated fan page body has no explicit line-height
- **File**: `createAct.py:408-415`

### N-025: Older generated pages use deprecated `<marquee>` element
- **Files**: 8 of 12 generated pages
- **WCAG**: SC 2.2.2 Pause, Stop, Hide, Level A

### N-026: Older generated pages use `<a name="">` anchors instead of `id`
- **Files**: 8 of 12 generated pages

### N-027: Older generated pages skip heading level (h1 to h3)
- **Files**: 8 of 12 generated pages
- **WCAG**: SC 1.3.1 Info and Relationships, Level A (advisory)

### N-029: Legacy-format fan pages have fixed-position footer that occludes content
- **Files**: `EchoesOfTheMirage/home.html`, `MoonlitReverie/home.html`, `TheVelvetEchoes/home.html`, `**VelvetEchoes/home.html`

### N-030: Legacy-format fan pages render empty band members section
- **Files**: `EchoesOfTheMirage/home.html`, `MoonlitReverie/home.html`, `TheVelvetEchoes/home.html`, `**VelvetEchoes/home.html`

### N-032 (NEW): `band_assets` route does not validate `filename` parameter
- **File**: `app.py:107-112`

---

## Positive Observations

1. **v2 template quality is excellent**: The current `createAct.py` template includes `lang="en"`, viewport meta, skip link, semantic `<header>`/`<main>`/`<footer>`/`<nav>`, correct heading hierarchy (h1 > h2), `focus-visible`, `prefers-reduced-motion`, ARIA labels, XSS escaping via `html.escape()`, and CSS custom properties (`--accent-1/2/3`).
2. **Main app accessibility remains strong**: Skip link, ARIA progressbar with `aria-valuenow` updates, `aria-live` regions, proper focus management on state transitions (`tabindex="-1"` + `.focus()`), `focus-visible` on all interactive elements, `prefers-reduced-motion`, scoped table headers, `fieldset`/`legend`, 44x44px touch targets on buttons and dice buttons.
3. **All color contrast ratios pass WCAG AA**: Verified all foreground/background pairs across both the main app and generated pages. All pairs achieve at least 4.5:1. Lowest ratio found: 5.82:1 (#555 on #F0E68C in the EchoesOfTheMirage legacy page).
4. **Design token system**: CSS custom properties well-organized in `:root` with semantic naming (e.g., `--color-text-primary`, `--space-md`). Consistently used throughout `style.css`.
5. **Error resilience**: Consecutive network error counter (`consecutiveErrors`) with graceful degradation messaging at 3 and 5 errors.
6. **Security**: CSRF origin/referer checks, per-IP rate limiting, `SAFE_BAND_NAME` regex on routes, XSS escaping on AI output, `html.escape()` on all dynamic content, generation cleanup to prevent memory exhaustion.
7. **Responsive design**: Three-tier responsive strategy with 640px and 768px breakpoints. Feature grid stacks to column, param labels reflow, tables scale down, touch targets maintained.
8. **Gallery filter (N-028 fix)**: SAFE_BAND_NAME check in gallery route correctly prevents dead links from appearing.

---

## Metrics

- Total tracked issues: 29 (was 27; +2 new, 0 resolved this cycle)
- Critical: 0 | High: 0 | Medium: 8 | Low: 16
- Resolved cumulative: N-001, N-021, N-023, N-024, N-028 (5 total)
- New this review: N-031 (medium -- all 12 served pages lack skip links/landmarks/prefers-reduced-motion), N-032 (low -- filename parameter not validated in band_assets route)
- Previously invalid: N-013 (`json` import is used in gallery route)
- Open medium issues aging: N-002, N-003, N-004, N-009, N-012, N-016, N-019 are all 6+ days old
- Recommendation: Prioritize N-031 (migration script extension) and N-003 (guestbook links) as the most impactful next fixes
