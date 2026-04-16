# UX & Accessibility Code Review
**Date**: 2026-04-16
**Reviewer**: Jennifer Mitchelle (Senior UX Design Critic, Swords, Ireland)
**Branch**: fix/code-review-2026-04-13

## Summary

Thirteenth periodic review of the AI Band Generator. No code changes have been made since the prior review (2026-04-15). All 7 previously resolved issues remain verified as resolved. The 6 open medium issues and 16 open low issues carry forward unchanged. No new issues were identified this cycle.

All 6 medium issues have now been open for 10+ days. Two low issues -- N-025 (deprecated `<marquee>` element, a WCAG Level A concern) and N-027 (heading level skip, a WCAG Level A advisory) -- were re-evaluated for escalation but remain at their current severity (see Escalation Assessment).

The legacy fan pages (EchoesOfTheMirage, TheVelvetEchoes, MoonlitReverie, **VelvetEchoes) continue to present the most concentrated cluster of issues: fixed-position footer occluding content (N-029), empty band members section (N-030), fixed-width 600px band photo with no responsive breakpoints, and no responsive breakpoints. These pages also use a `max-width: 1200px` container versus the 800px used by v1 and v2 templates, creating a visual inconsistency.

8 `band_photo.jpg` files appear as untracked in git status (EtherealTrampleweed, EucalyptusSaints, Inu-k-trkadeka, MidnightParlor, MyopicSunflowers, NightshadeVanguard, TheLuminescentUndertow, ChaoDeCorais). These are binary assets and do not affect the UX/accessibility findings.

**Files reviewed:**
- `templates/base.html`, `templates/index.html`, `templates/generate.html`, `templates/gallery.html`
- `static/css/style.css` (724 lines), `static/js/main.js` (19 lines)
- `app.py` (285 lines), `createAct.py` (826 lines)
- Generated fan pages: all 12 band directories (spot-checked across v1 and legacy templates)
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
| N-003 | Guestbook links use `href="#"` with no indication | **RESOLVED** -- verified, 0 matches across all 12 pages and createAct.py |
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

### Medium Issues Re-evaluated

All 6 medium issues are now 10+ days old. Each was re-assessed for escalation to High:

- **N-002 (inline styles in v2 template, createAct.py:705,708,726)**: Remains Medium. Three inline `style` attributes (`text-align:center`, `color:#888888`, visitor count color) affect maintainability but do not create a WCAG violation. The inline styles are limited to the guestbook section and footer visitor counter -- cosmetic areas. No escalation warranted.

- **N-004 (legacy pages without band_info.json check, app.py:95-104)**: Remains Medium. The `view_band()` route validates via `SAFE_BAND_NAME` regex, and `send_from_directory` is directory-scoped, so there is no security exposure. The issue is functional correctness (serving pages that may not be gallery-indexed). No escalation warranted.

- **N-009 (gallery table not responsive below 400px)**: Remains Medium. At 320px viewport width, the table is cramped but remains functional. Content does not overflow horizontally because the table columns compress. SC 1.4.10 Reflow is AA, and the content remains usable. No escalation warranted.

- **N-012 (non-ASCII band name path validation, app.py:36)**: Remains Medium. Two of 12 bands (ChaoDeCorais, **VelvetEchoes) are filtered from the gallery but their pages are still directly accessible. Users who created these bands can still view them via the success redirect. The data is not lost, merely hidden from the gallery listing. No escalation warranted.

- **N-016 (inconsistent path resolution, app.py:66-86,95-104)**: Remains Medium. Gallery uses `app.root_path`; `view_band()` uses a relative path. Both work correctly in the standard deployment scenario (CWD = project root). This is a latent bug that would only surface in a non-standard deployment. No escalation warranted.

- **N-019 (!important overrides in generated pages, createAct.py:619,622,625)**: Remains Medium. The `!important` declarations are in the mobile breakpoint of generated pages and apply to `.band-title`, `.page-header`, and `.members-list`. They override nothing in the current cascade (specificity is already sufficient), so they are unnecessary clutter rather than an active problem. No escalation warranted.

### Low Issues Re-evaluated for Escalation

All 16 low issues were reassessed. Two warranted closer examination:

- **N-025 (deprecated `<marquee>` element)**: This touches WCAG SC 2.2.2 Pause, Stop, Hide (Level A). However, the N-031 migration already added `prefers-reduced-motion` handling that sets `animation: none` and `overflow: visible; white-space: normal` on `<marquee>` elements in all 8 affected v1 pages. This mitigates the worst accessibility impact (users who need reduced motion get static text). The `<marquee>` element itself is deprecated HTML but not a WCAG failure when motion can be paused. Remains Low.

- **N-027 (heading level skip, h1 to h3)**: SC 1.3.1 Info and Relationships (Level A) -- however, heading level skips are an advisory technique (G141), not a normative requirement. Screen readers handle skipped levels gracefully. Remains Low.

No low issues escalated this cycle.

---

## New Issues

No new issues identified this cycle. The codebase has had no changes since the prior review.

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
- **Problem**: `SAFE_BAND_NAME` regex blocks `ChaoDeCorais` (non-ASCII tilde) and `**VelvetEchoes` (asterisks). Both are filtered from gallery (N-028 fix) so they are hidden, but the underlying data is inaccessible via gallery.
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
- **WCAG**: SC 2.2.2 Pause, Stop, Hide, Level A (mitigated by prefers-reduced-motion)

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
11. **Flask app imports cleanly**: Verified with `OPENAI_API_KEY=test python3 -c "import app"` -- no errors.

---

## Metrics

- Total tracked issues: 29 (N-001 through N-032, excluding invalidated N-013)
- Critical: 0 | High: 0 | Medium: 6 | Low: 16
- Resolved cumulative: N-001, N-003, N-021, N-023, N-024, N-028, N-031 (7 total; +0 this cycle)
- Escalated this cycle: none
- New this review: none
- Previously invalid: N-013 (`json` import is used in gallery route)
- Open medium issues aging: N-002, N-004, N-009, N-012, N-016, N-019 are all 10+ days old
- Recommendation: Prioritize **N-002** (inline styles in v2 template -- simple CSS extraction, 3 lines) and **N-019** (`!important` removal -- 3 lines in createAct.py) as the next fixes. Both are low-effort changes that improve maintainability. After those, **N-009** (gallery table responsive) is the most impactful remaining Medium issue for end users on narrow viewports.
