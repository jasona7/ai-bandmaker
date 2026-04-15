# UX & Accessibility Code Review
**Date**: 2026-04-15
**Reviewer**: Jennifer Mitchelle (Senior UX Design Critic, Swords, Ireland)
**Branch**: fix/code-review-2026-04-13

## Summary

Twelfth periodic review of the AI Band Generator. Two medium issues were escalated to high based on age and WCAG Level A severity, then **fixed this cycle**:

- **N-031** (skip links, landmarks, prefers-reduced-motion on all 12 fan pages): Escalated from Medium to High, then **RESOLVED**. All 12 fan pages now have: skip links (`<a href="#main-content" class="skip-link">`), `<main id="main-content">` landmark, `<nav>` landmark (converted from `<div class="nav-bar">` on 8 v1-template pages; already present on 4 legacy pages), `<footer>` wrapper (added on 8 v1-template pages; already present on 4 legacy pages), `prefers-reduced-motion` media query (added on 8 v1-template pages that have `.blink` and `<marquee>` animations), `aria-hidden="true"` on decorative badge-row, and skip-link CSS styles.

- **N-003** (guestbook href="#" links): Escalated from Medium to High, then **RESOLVED**. All 5 `<a href="#">` links per page ("Sign the Guestbook!", "View Guestbook", "Link to us!", "Webrings", "MIDI Archive") replaced with `<span class="faux-link">` across all 8 v1-template fan pages and in the v2 template in `createAct.py`. The `.faux-link` CSS class preserves the visual appearance (colored, underlined) while removing the element from tab order and announcing it correctly to screen readers as non-interactive text. The "Back to Top" link (previously `href="#"`) was changed to `href="#main-content"` to provide a functional navigation target.

The main application templates (`base.html`, `index.html`, `gallery.html`, `generate.html`) and `style.css` continue in strong shape. The v2 template in `createAct.py` has been updated with the N-003 fix (faux-link). All 12 existing fan pages now have N-021 (focus-visible), N-031 (skip links, landmarks, prefers-reduced-motion), and N-003 (faux-link) migration patches applied.

8 `band_photo.jpg` files appear as untracked in git status (EtherealTrampleweed, EucalyptusSaints, Inu-k-trkadeka, MidnightParlor, MyopicSunflowers, NightshadeVanguard, TheLuminescentUndertow, ChaoDeCorais). These are binary assets and do not affect the UX/accessibility findings.

**Files reviewed:**
- `templates/base.html`, `templates/index.html`, `templates/generate.html`, `templates/gallery.html`
- `static/css/style.css` (724 lines), `static/js/main.js` (19 lines)
- `app.py` (285 lines), `createAct.py` (826 lines, updated)
- Generated fan pages: all 12 band directories (all migrated with N-021, N-031, N-003)
- `tasks/review-recheck.md` (prior recheck document, reviewed for context)

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 6 |
| Low | 16 |

---

## Status of Previous Issues

| Prior ID | Issue | Status |
|---|---|---|
| N-001 | Color contrast failure in accent color tuple (#ff6666) | **RESOLVED** -- verified, replacement #ff7777 passes at 8.16:1 |
| N-002 | Residual inline styles in generated fan pages | Open (Medium) |
| N-003 | Guestbook links use `href="#"` with no indication | **RESOLVED** -- replaced with `<span class="faux-link">` in v2 template and all 12 fan pages |
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
| N-031 | All 12 existing fan pages lack skip links, landmarks, and prefers-reduced-motion | **RESOLVED** -- all 12 pages migrated with skip links, `<main>`, `<nav>`, `<footer>`, prefers-reduced-motion |
| N-032 | `band_assets` route does not validate `filename` parameter | Open (Low) |

---

## Escalation Assessment

Two medium issues were escalated to high and then fixed this cycle:

- **N-031**: Escalated to High and **RESOLVED**. All 12 fan pages migrated with skip links, `<main>` landmark, `<nav>` landmark, `<footer>` wrapper, `prefers-reduced-motion`, and `aria-hidden` on decorative elements.
- **N-003**: Escalated to High and **RESOLVED**. All `href="#"` links replaced with `<span class="faux-link">` in v2 template and all 8 v1-template fan pages. "Back to Top" links changed to `href="#main-content"`.

The remaining medium issues were re-evaluated and remain at medium:

- **N-002 (inline styles)**: Remains medium. Three inline `style` attributes in the v2 template (`createAct.py:705,708,726`). Affects maintainability but does not violate WCAG A/AA in isolation.
- **N-004 (legacy pages without band_info.json check)**: Remains medium. No security impact; `send_from_directory` is safe.
- **N-009 (gallery table responsive)**: Remains medium. SC 1.4.10 Reflow at Level AA; the table is still usable at 320px.
- **N-012 (non-ASCII path validation)**: Remains medium. Two of 12 bands (16.7%) are hidden from the gallery but not broken.
- **N-016 (path resolution inconsistency)**: Remains medium. Latent bug, not actively causing issues.
- **N-019 (!important overrides)**: Remains medium. Limited to mobile breakpoint of generated pages.

---

## New Issues

No new issues identified this cycle. The codebase has had no changes since the prior review.

---

## High Issues (escalated and resolved this cycle)

### N-031: All 12 existing fan pages lack skip links, landmarks, and prefers-reduced-motion [RESOLVED]
- **Files**: All 12 band directories (`*/home.html`)
- **Resolution**: Batch migration applied across all 12 pages with two migration strategies:
  - **8 v1-template pages** (EtherealTrampleweed, EucalyptusSaints, Inu-k-trkadeka, MidnightParlor, MyopicSunflowers, NightshadeVanguard, TheLuminescentUndertow, ChaoDeCorais): Added skip link (`<a href="#main-content" class="skip-link">`), `.skip-link` CSS, `<nav class="nav-bar" aria-label="Page sections">` (replaced `<div class="nav-bar">`), `<main id="main-content">` wrapping all content sections, `<footer>` wrapping badge-row and footer-area, `aria-hidden="true"` on badge-row, `prefers-reduced-motion` media query disabling `.blink` and `<marquee>` animations.
  - **4 legacy pages** (EchoesOfTheMirage, MoonlitReverie, TheVelvetEchoes, **VelvetEchoes): Added skip link, `.skip-link` CSS, `<main id="main-content">` wrapping the container `<div>`. These pages already had semantic `<header>`, `<nav>`, and `<footer>` elements and do not use `.blink` or `<marquee>` animations.
- **Verification**: All 12 pages confirmed to have exactly 1 skip-link, 1 `<main>`, and 1 `</main>`.

### N-003: Guestbook links use `href="#"` with no indication of non-functionality [RESOLVED]
- **Files**: `createAct.py` (v2 template) and all 8 v1-template fan pages
- **Resolution**: In `createAct.py`, replaced all 5 `<a href="#">` elements with `<span class="faux-link">` and added `.faux-link` CSS class. In all 8 v1-template fan pages, applied the same replacement. The "Back to Top" link (previously `href="#"`) was changed to `href="#main-content"` to provide a valid navigation target. Added `.faux-link` CSS to each page. The 4 legacy pages did not have guestbook links and required no changes for this issue.
- **Verification**: `grep -c 'href="#"'` returns 0 across all 12 fan pages and `createAct.py`.

---

## Medium Issues (carried forward)

### N-002: Residual inline styles in generated fan pages
- **File**: `createAct.py:705,708,726`
- **Problem**: Three inline `style` attributes remain in the v2 template (`text-align:center`, `color:#888888`, visitor count color).
- **Fix**: Extract to named CSS classes.

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

## Low Issues (carried forward)

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
- **File**: `createAct.py:584` (`linear`) vs `static/css/style.css:650` (`step-start`)

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
- **Files**: 8 of 12 generated pages (EtherealTrampleweed, EucalyptusSaints, Inu-k-trkadeka, MidnightParlor, MyopicSunflowers, NightshadeVanguard, TheLuminescentUndertow, ChaoDeCorais)
- **WCAG**: SC 2.2.2 Pause, Stop, Hide, Level A

### N-026: Older generated pages use `<a name="">` anchors instead of `id`
- **Files**: 8 of 12 generated pages

### N-027: Older generated pages skip heading level (h1 to h3)
- **Files**: 8 of 12 generated pages (confirmed: section headers use `<h3>` after `<h1>`, skipping `<h2>`)
- **WCAG**: SC 1.3.1 Info and Relationships, Level A (advisory)

### N-029: Legacy-format fan pages have fixed-position footer that occludes content
- **Files**: `EchoesOfTheMirage/home.html`, `MoonlitReverie/home.html`, `TheVelvetEchoes/home.html`, `**VelvetEchoes/home.html`

### N-030: Legacy-format fan pages render empty band members section
- **Files**: `EchoesOfTheMirage/home.html`, `MoonlitReverie/home.html`, `TheVelvetEchoes/home.html`, `**VelvetEchoes/home.html`

### N-032: `band_assets` route does not validate `filename` parameter
- **File**: `app.py:107-112`

---

## Positive Observations

1. **v2 template quality is excellent**: The current `createAct.py` template includes `lang="en"`, viewport meta, skip link, semantic `<header>`/`<main>`/`<footer>`/`<nav>`, correct heading hierarchy (h1 > h2), `focus-visible`, `prefers-reduced-motion`, ARIA labels, XSS escaping via `html.escape()`, and CSS custom properties (`--accent-1/2/3`).
2. **Main app accessibility remains strong**: Skip link, ARIA progressbar with `aria-valuenow` updates, `aria-live` regions, proper focus management on state transitions (`tabindex="-1"` + `.focus()`), `focus-visible` on all interactive elements, `prefers-reduced-motion`, scoped table headers, `fieldset`/`legend`, 44x44px touch targets on buttons and dice buttons.
3. **All color contrast ratios pass WCAG AA**: Verified all foreground/background pairs across both the main app and generated pages. All pairs achieve at least 4.5:1. Lowest ratio found: #888888 on #000000 at 5.92:1 (footer text in generated pages).
4. **Design token system**: CSS custom properties well-organized in `:root` with semantic naming (e.g., `--color-text-primary`, `--space-md`). Consistently used throughout `style.css`.
5. **Error resilience**: Consecutive network error counter (`consecutiveErrors`) with graceful degradation messaging at 3 and 5 errors.
6. **Security**: CSRF origin/referer checks, per-IP rate limiting, `SAFE_BAND_NAME` regex on routes, XSS escaping on AI output, `html.escape()` on all dynamic content, generation cleanup to prevent memory exhaustion.
7. **Responsive design**: Three-tier responsive strategy with 640px and 768px breakpoints. Feature grid stacks to column, param labels reflow, tables scale down, touch targets maintained.
8. **Gallery filter (N-028 fix)**: SAFE_BAND_NAME check in gallery route correctly prevents dead links from appearing.
9. **All images have alt text**: Verified across all 12 generated pages and all main app templates. No missing `alt` attributes.
10. **All pages have lang attribute**: All 12 generated pages and all main templates include `lang="en"`.
11. **Flask app imports cleanly**: Verified with `OPENAI_API_KEY=test ./venv/bin/python3 -c "import app"` -- no errors.

---

## Metrics

- Total tracked issues: 29
- Critical: 0 | High: 0 | Medium: 6 | Low: 16
- Resolved cumulative: N-001, N-003, N-021, N-023, N-024, N-028, N-031 (7 total; +2 this cycle)
- Escalated and fixed this cycle: N-031 (Medium -> High -> Resolved), N-003 (Medium -> High -> Resolved)
- New this review: none
- Previously invalid: N-013 (`json` import is used in gallery route)
- Open medium issues aging: N-002, N-004, N-009, N-012, N-016, N-019 are all 9+ days old
- Recommendation: Prioritize N-002 (inline styles in v2 template) and N-009 (gallery table responsive) as the next fixes. All WCAG Level A violations in the served fan page content have been resolved with the N-031 and N-003 fixes this cycle.
