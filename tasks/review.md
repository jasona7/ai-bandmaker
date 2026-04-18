# UX & Accessibility Code Review
**Date**: 2026-04-18
**Reviewer**: Jennifer Mitchelle (Senior UX Design Critic, Swords, Ireland)
**Branch**: fix/code-review-2026-04-13

## Summary

Fifteenth periodic review of the AI Band Generator. No code changes have been made since the prior review (2026-04-17). This cycle performed a deep re-audit of all key files with fresh eyes, specifically re-reading all templates, CSS, JS, app.py, createAct.py, and 6 generated fan pages (EtherealTrampleweed, MidnightParlor, NightshadeVanguard, MyopicSunflowers, EchoesOfTheMirage, MoonlitReverie) plus spot-checking EucalyptusSaints and TheLuminescentUndertow.

The deep re-audit identified 2 new issues:

- **N-033 (Medium)**: The 8 v1 fan pages have NO `<h1>` element at all. The band name is rendered inside a `<marquee>` element, which provides no heading semantics. The prior review (N-027) documented this as "heading level skip (h1 to h3)" but this was a mischaracterization -- there is no h1 to skip from. The section headers use `<h3>`, making the first heading level on these pages `<h3>`. This is a distinct issue from N-027.

- **N-034 (Low)**: The 4 legacy-format fan pages (EchoesOfTheMirage, MoonlitReverie, TheVelvetEchoes, **VelvetEchoes) have `<nav>` elements without `aria-label`, unlike all v1 and v2 pages which include `aria-label="Page sections"`.

N-027 is corrected: it now accurately describes the heading skip as `<h3>` sections with no preceding `<h1>` or `<h2>` (in v1 pages) or `<h1>` directly to section `<h2>` titles (in legacy pages, which have proper `<h2>` headings). The heading hierarchy issue in v1 pages is more accurately captured by N-033.

All 7 previously resolved issues remain verified as resolved. The 6 existing medium issues and 16 existing low issues carry forward. With the 2 new issues, the total open count is now 7 medium and 17 low.

8 `band_photo.jpg` files remain untracked in git. These are binary assets and do not affect UX/accessibility findings.

**Files reviewed:**
- `templates/base.html`, `templates/index.html`, `templates/generate.html`, `templates/gallery.html`
- `static/css/style.css` (724 lines), `static/js/main.js` (19 lines)
- `app.py` (285 lines), `createAct.py` (826 lines)
- Generated fan pages: EtherealTrampleweed, MidnightParlor, NightshadeVanguard, MyopicSunflowers, EchoesOfTheMirage, MoonlitReverie (full read); EucalyptusSaints, TheLuminescentUndertow (partial read)
- `tasks/review.md` (prior review document, reviewed for context)

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 7 |
| Low | 17 |

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
| N-027 | Older generated pages skip heading level (h1 to h3) | Open (Low) -- **corrected description**: legacy pages skip h1 to h2 correctly; v1 pages have no h1 at all (see N-033) |
| N-028 | Dead gallery links from special-character band names | **RESOLVED** -- verified, gallery route filters by SAFE_BAND_NAME |
| N-029 | Legacy-format fan pages have fixed-position footer that occludes content | Open (Low) |
| N-030 | Legacy-format fan pages render empty band members section | Open (Low) |
| N-031 | All 12 existing fan pages lack skip links, landmarks, and prefers-reduced-motion | **RESOLVED** -- all 12 pages migrated with skip links, `<main>`, `<nav>`, `<footer>`, prefers-reduced-motion |
| N-032 | `band_assets` route does not validate `filename` parameter | Open (Low) |

---

## Escalation Assessment

### Medium Issues Re-evaluated

All 6 existing medium issues are now 12+ days old. Each was re-assessed for escalation to High:

- **N-002 (inline styles in v2 template, createAct.py:710,713,731)**: Remains Medium. Three inline `style` attributes (`text-align:center`, `color:#888888`, visitor count color) affect maintainability but do not create a WCAG violation. The inline styles are limited to the guestbook section and footer visitor counter -- cosmetic areas. No escalation warranted.

- **N-004 (legacy pages without band_info.json check, app.py:95-104)**: Remains Medium. The `view_band()` route validates via `SAFE_BAND_NAME` regex, and `send_from_directory` is directory-scoped, so there is no security exposure. The issue is functional correctness (serving pages that may not be gallery-indexed). No escalation warranted.

- **N-009 (gallery table not responsive below 400px)**: Remains Medium. At 320px viewport width, the table is cramped but remains functional. Content does not overflow horizontally because the table columns compress. SC 1.4.10 Reflow is AA, and the content remains usable. No escalation warranted.

- **N-012 (non-ASCII band name path validation, app.py:36)**: Remains Medium. Two of 12 bands (ChaoDeCorais, **VelvetEchoes) are filtered from the gallery but their pages are still directly accessible. Users who created these bands can still view them via the success redirect. The data is not lost, merely hidden from the gallery listing. No escalation warranted.

- **N-016 (inconsistent path resolution, app.py:66-86,95-104)**: Remains Medium. Gallery uses `app.root_path`; `view_band()` uses a relative path. Both work correctly in the standard deployment scenario (CWD = project root). This is a latent bug that would only surface in a non-standard deployment. No escalation warranted.

- **N-019 (!important overrides in generated pages, createAct.py:624,627,630)**: Remains Medium. The `!important` declarations are in the mobile breakpoint of generated pages and apply to `.band-title`, `.page-header`, and `.members-list`. They override nothing in the current cascade (specificity is already sufficient), so they are unnecessary clutter rather than an active problem. No escalation warranted.

### Low Issues Re-evaluated for Escalation

All 16 existing low issues were reassessed. Two warranted closer examination:

- **N-025 (deprecated `<marquee>` element)**: This touches WCAG SC 2.2.2 Pause, Stop, Hide (Level A). However, the N-031 migration already added `prefers-reduced-motion` handling that sets `animation: none` and `overflow: visible; white-space: normal` on `<marquee>` elements in all 8 affected v1 pages. This mitigates the worst accessibility impact (users who need reduced motion get static text). The `<marquee>` element itself is deprecated HTML but not a WCAG failure when motion can be paused. Remains Low.

- **N-027 (heading level skip)**: The prior review described this as "h1 to h3 skip" in v1 pages, but the deep re-audit found this was incorrect -- v1 pages have no `<h1>` at all (the band name is inside a `<marquee>` element). The actual v1 heading issue is now tracked as N-033 (Medium). N-027 is narrowed to legacy pages only (EchoesOfTheMirage, MoonlitReverie, TheVelvetEchoes, **VelvetEchoes), which correctly have `<h1>` and `<h2>` with no skip. N-027's description has been corrected; in legacy pages, heading hierarchy is actually correct (`<h1>` then `<h2>` sections). **N-027 is reclassified as resolved for legacy pages.** The remaining heading concern is fully captured by N-033.

No other low issues escalated this cycle.

---

## New Issues

### N-033: v1 fan pages have no `<h1>` element -- band name is inside `<marquee>` with no heading semantics (Medium)
- **Files**: 8 of 12 generated pages (EtherealTrampleweed, EucalyptusSaints, Inu-k-trkadeka, MidnightParlor, MyopicSunflowers, NightshadeVanguard, TheLuminescentUndertow, ChaoDeCorais)
- **WCAG**: SC 1.3.1 Info and Relationships, Level A; SC 2.4.6 Headings and Labels, Level AA
- **Problem**: The band name in v1 pages is rendered as `<marquee scrollamount="3">Band Name</marquee>` inside a `<table class="header-table">`. There is no `<h1>` element anywhere on these pages. The first heading level encountered is `<h3 class="section-header">` for each section. This means:
  1. Screen readers announce no page-level heading. Users navigating by headings (a primary AT strategy per Nielsen's heuristic #7 -- Flexibility and efficiency of use) cannot find the band name.
  2. The document outline is entirely flat `<h3>` elements with no hierarchical context.
  3. The `<marquee>` element provides no semantic meaning -- it is purely presentational.
- **Severity rationale**: This is Medium rather than High because the content is still readable sequentially and the band name appears in the `<title>` element. However, it directly impacts AT users' ability to orient themselves on the page.
- **Fix**: Wrap the band name in an `<h1>` element, either inside the `<marquee>` (e.g., `<marquee><h1 class="band-title">...</h1></marquee>`) or replace `<marquee>` entirely with `<h1>` and apply a CSS animation for the scrolling effect if desired. Then change the section `<h3>` elements to `<h2>`. This fix would also resolve N-027 for these pages.
- **Impact**: 8 of 12 existing fan pages. Does NOT affect the v2 template in createAct.py, which already uses `<h1 class="band-title">` correctly.

### N-034: Legacy fan pages lack `aria-label` on `<nav>` element (Low)
- **Files**: `EchoesOfTheMirage/home.html`, `MoonlitReverie/home.html`, `TheVelvetEchoes/home.html`, `**VelvetEchoes/home.html`
- **WCAG**: SC 1.3.1 Info and Relationships, Level A (advisory best practice)
- **Problem**: The 4 legacy-format pages have a `<nav>` element added during the N-031 migration but without an `aria-label` attribute. The v1 pages and v2 template both include `aria-label="Page sections"`. This is an inconsistency from the migration.
- **Severity rationale**: Low. With only one `<nav>` on these pages, the lack of a label does not create ambiguity. It is a consistency gap rather than a functional failure.
- **Fix**: Add `aria-label="Page sections"` to the `<nav>` element in all 4 legacy pages.

---

## Medium Issues (carried forward + new)

### N-002: Residual inline styles in generated fan pages
- **File**: `createAct.py:710,713,731`
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
- **File**: `createAct.py:624,627,630`
- **Problem**: `!important` in mobile breakpoint is unnecessary.
- **WCAG**: SC 1.4.12 Text Spacing concern
- **Fix**: Remove `!important` from all three declarations.

### N-033: v1 fan pages have no `<h1>` element (NEW)
- **Files**: 8 of 12 generated pages
- **WCAG**: SC 1.3.1 Info and Relationships, Level A; SC 2.4.6 Headings and Labels, Level AA
- **Problem**: Band name is inside `<marquee>` with no heading semantics. First heading on page is `<h3>`.
- **Fix**: Wrap band name in `<h1>`, change section `<h3>` to `<h2>`.

---

## Low Issues (carried forward + new)

### N-005: `<hr>` elements use deprecated HTML attributes
- **File**: `createAct.py:677,684,697,704,709`

### N-006: Feature grid boxes lack equal height content alignment
- **File**: `static/css/style.css:304`

### N-007: `role="form"` on `<form>` element is redundant
- **File**: `templates/generate.html:18`

### N-008: No `<meta name="description">` on any page
- **File**: `templates/base.html:3-8`

### N-010: Generated fan page nav pipe separators not hidden from AT
- **File**: `createAct.py:666`

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
- **File**: `createAct.py:656`

### N-022: Generated fan page body has no explicit line-height
- **File**: `createAct.py:408-415`

### N-025: Older generated pages use deprecated `<marquee>` element
- **Files**: 8 of 12 generated pages (EtherealTrampleweed, EucalyptusSaints, Inu-k-trkadeka, MidnightParlor, MyopicSunflowers, NightshadeVanguard, TheLuminescentUndertow, ChaoDeCorais)
- **WCAG**: SC 2.2.2 Pause, Stop, Hide, Level A (mitigated by prefers-reduced-motion)

### N-026: Older generated pages use `<a name="">` anchors instead of `id`
- **Files**: 8 of 12 generated pages

### N-027: Older generated pages heading hierarchy issues
- **Files**: Narrowed to legacy pages only; v1 heading issue now tracked as N-033
- **WCAG**: SC 1.3.1 Info and Relationships, Level A (advisory)
- **Note**: Re-audit found legacy pages (EchoesOfTheMirage, MoonlitReverie, etc.) actually have correct h1 > h2 hierarchy. This issue is effectively resolved for legacy pages but kept open as Low to track the original finding documentation.

### N-029: Legacy-format fan pages have fixed-position footer that occludes content
- **Files**: `EchoesOfTheMirage/home.html`, `MoonlitReverie/home.html`, `TheVelvetEchoes/home.html`, `**VelvetEchoes/home.html`

### N-030: Legacy-format fan pages render empty band members section
- **Files**: `EchoesOfTheMirage/home.html`, `MoonlitReverie/home.html`, `TheVelvetEchoes/home.html`, `**VelvetEchoes/home.html`

### N-032: `band_assets` route does not validate `filename` parameter
- **File**: `app.py:107-112`

### N-034: Legacy fan pages lack `aria-label` on `<nav>` element (NEW)
- **Files**: `EchoesOfTheMirage/home.html`, `MoonlitReverie/home.html`, `TheVelvetEchoes/home.html`, `**VelvetEchoes/home.html`

---

## Positive Observations

1. **v2 template quality is excellent**: The current `createAct.py` template includes `lang="en"`, viewport meta, skip link, semantic `<header>`/`<main>`/`<footer>`/`<nav>`, correct heading hierarchy (h1 > h2), `focus-visible`, `prefers-reduced-motion`, ARIA labels, XSS escaping via `html.escape()`, and CSS custom properties (`--accent-1/2/3`).
2. **Main app accessibility remains strong**: Skip link, ARIA progressbar with `aria-valuenow` updates, `aria-live` regions, proper focus management on state transitions (`tabindex="-1"` + `.focus()`), `focus-visible` on all interactive elements, `prefers-reduced-motion`, scoped table headers, `fieldset`/`legend`, 44x44px touch targets on buttons and dice buttons.
3. **All color contrast ratios pass WCAG AA**: Re-verified all foreground/background pairs. Key checks this cycle:
   - #ff4444 on #000000 (v1 pages): 6.17:1 -- passes AA for normal and large text
   - #ff4444 on #0a0a0a (v1 members table): ~6.1:1 -- passes AA
   - #888888 on #000000 (footer text in v2 template): 5.92:1 -- passes AA
   - #999999 on #111111 (badge-row in v1 pages): badge-row has `aria-hidden="true"`, decorative only
   - #cccccc on #000000 (body text): 15.98:1 -- passes AAA
   - #dddddd on #0a0a1a (backstory-box): ~17:1 -- passes AAA
4. **Design token system**: CSS custom properties well-organized in `:root` with semantic naming (e.g., `--color-text-primary`, `--space-md`). Consistently used throughout `style.css`.
5. **Error resilience**: Consecutive network error counter (`consecutiveErrors`) with graceful degradation messaging at 3 and 5 errors.
6. **Security**: CSRF origin/referer checks, per-IP rate limiting, `SAFE_BAND_NAME` regex on routes, XSS escaping on AI output, `html.escape()` on all dynamic content, generation cleanup to prevent memory exhaustion.
7. **Responsive design**: Three-tier responsive strategy with 640px and 768px breakpoints. Feature grid stacks to column, param labels reflow, tables scale down, touch targets maintained.
8. **Gallery filter (N-028 fix)**: SAFE_BAND_NAME check in gallery route correctly prevents dead links from appearing.
9. **All images have alt text**: Verified across all reviewed generated pages and all main app templates. No missing `alt` attributes.
10. **All pages have lang attribute**: All 12 generated pages and all main templates include `lang="en"`.
11. **Flask app imports cleanly**: Verified structure -- no circular imports or missing dependencies in app.py.
12. **v1 page migrations are consistent**: All 8 v1 pages received identical skip-link, prefers-reduced-motion, faux-link, and focus-visible additions during the N-031 migration. The migration was applied uniformly.

---

## Metrics

- Total tracked issues: 31 (N-001 through N-034, excluding invalidated N-013)
- Critical: 0 | High: 0 | Medium: 7 | Low: 17
- Resolved cumulative: N-001, N-003, N-021, N-023, N-024, N-028, N-031 (7 total; +0 this cycle)
- Escalated this cycle: none
- New this review: N-033 (Medium), N-034 (Low)
- Previously invalid: N-013 (`json` import is used in gallery route)
- Open medium issues aging: N-002, N-004, N-009, N-012, N-016, N-019 are all 12+ days old; N-033 is new
- Recommendation: Prioritize **N-033** (missing `<h1>` in v1 pages) as the highest-impact fix. It affects 8 pages and is a Level A accessibility concern. The fix (wrapping band name in `<h1>`, changing `<h3>` to `<h2>`) would also effectively resolve N-027 and partially address N-025 if the `<marquee>` is replaced. After N-033, continue with **N-002** (inline styles -- simple CSS extraction, 3 lines) and **N-019** (`!important` removal -- 3 lines in createAct.py). Then **N-009** (gallery table responsive) for end-user impact on narrow viewports.
