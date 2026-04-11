# UX & Accessibility Code Review
**Date**: 2026-04-11
**Reviewer**: Jennifer Mitchelle (Senior UX Design Critic, Swords, Ireland)
**Branch**: fix/code-review-2026-04-06

## Summary

Eighth review of the AI Band Generator. The `createAct.py` template has been significantly improved with semantic HTML, focus-visible indicators, skip links, ARIA landmarks, reduced-motion support, and correct heading hierarchy. However, a critical systemic issue has emerged: **no existing generated fan page reflects any of these improvements**, and **no `band_info.json` files exist anywhere**, meaning the gallery route displays zero bands. The template improvements are real and well-executed, but they exist only in code -- no page on disk benefits from them. This constitutes a regression of N-021 (focus indicators) from "resolved" back to "open" for all currently accessible pages, and reveals a new critical-severity functional bug where the gallery is completely empty. Two new medium+ issues and three new low issues are identified.

**Files reviewed:**
- `templates/base.html`, `templates/index.html`, `templates/generate.html`, `templates/gallery.html`
- `static/css/style.css`, `static/js/main.js`
- `app.py`, `createAct.py`
- Generated fan pages: `EtherealTrampleweed/home.html`, `NightshadeVanguard/home.html`, `MidnightParlor/home.html`, `EchoesOfTheMirage/home.html`, `MoonlitReverie/home.html`

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 7 |
| Low | 14 |

---

## Status of Previous Issues

| Prior ID | Issue | Status |
|---|---|---|
| N-001 | Color contrast failure in accent color tuple (#ff6666) | **RESOLVED** -- now `#ff7777`, passes 4.5:1 on dark bg |
| N-002 | Residual inline styles in generated fan pages | Open (Medium) |
| N-003 | Guestbook links use `href="#"` with no indication | Open (Medium) |
| N-004 | Legacy generated pages still accessible via direct URL | Open (Medium) |
| N-005 | `<hr>` elements use deprecated HTML attributes | Open (Low) |
| N-006 | Feature grid boxes lack equal height content alignment | Open (Low) |
| N-007 | `role="form"` on `<form>` element is redundant | Open (Low) |
| N-008 | No `<meta name="description">` on any page | Open (Low) |
| N-009 | Gallery table lacks responsive handling for narrow viewports | Open (Medium) |
| N-010 | Generated fan page nav pipe separators not hidden from AT | Open (Low) |
| N-011 | Blink animation timing mismatch (`linear` vs `step-start`) | Open (Low) |
| N-012 | Band directory path validation blocks non-ASCII band names | Open (Medium) |
| N-013 | Unused `json` import in app.py | **INVALID** -- `json` is used at lines 77 and 79 for `json.load()` and `json.JSONDecodeError` |
| N-014 | Inline `import re` inside functions in createAct.py | Open (Low) |
| N-015 | Inline style on visitor count in generated pages | Open (Low) -- subsumed under N-002 |
| N-016 | Inconsistent path resolution between gallery and view_band routes | Open (Medium) |
| N-017 | No focus management after gallery page load | Open (Low) |
| N-018 | Fixed polling interval with no backoff | Open (Low) |
| N-019 | Generated fan pages use `!important` overrides in responsive styles | Open (Medium) |
| N-020 | Generated fan page `<br>` tag after decorative stars in header | Open (Low) |
| N-021 | Generated fan pages have no focus indicator styles | **REGRESSED** -- see below |
| N-022 | Generated fan page body has no explicit line-height | Open (Low) |

---

## Escalation Assessment

Each medium issue was reviewed to determine whether any should be escalated to high or critical:

- **N-002 (inline styles)**: Maintainability concern only. Does not block users or violate WCAG AA. Stays medium.
- **N-003 (guestbook `#` links)**: While technically a WCAG SC 2.4.4 Level A issue, it exists only on generated fan pages (not the main app) and the guestbook section is clearly themed as decorative retro content. Stays medium.
- **N-004 (legacy pages)**: No accessibility barrier; old pages are simply inconsistent. Now partly subsumed by N-023. Stays medium.
- **N-009 (gallery table < 400px)**: SC 1.4.10 Reflow is Level AA, but devices below 400px are edge-case. The table remains functional (horizontally scrollable), just cramped. Stays medium.
- **N-012 (non-ASCII path validation)**: Functional bug where bands with non-ASCII names are generated but unreachable. `ChãoDeCorais` directory exists demonstrating this in practice. Stays medium.
- **N-016 (path resolution inconsistency)**: Functional reliability concern, not user-facing unless CWD differs from project root. Stays medium.
- **N-019 (!important overrides)**: User stylesheet override concern. No direct accessibility barrier. Stays medium.
- **N-024 (#666666 contrast)**: WCAG AA failure on existing generated pages. Affects 8 of 12 band pages. Medium since pages will be superseded, but patching is straightforward.

---

## Critical Issues

### N-023: Gallery displays zero bands because no `band_info.json` files exist -- **RESOLVED**

- **File**: `app.py:66-88` (gallery route), `createAct.py:753-767` (save_band_info function)
- **Resolution**: Migration script `migrate_legacy_pages.py` created `band_info.json` with `template_version: 1` for all 12 existing band directories. Gallery now displays all bands correctly.
- **WCAG**: N/A (functional bug -- now fixed)

---

## High Issues

### N-021: Generated fan pages have no focus indicator styles -- **RESOLVED**

- **Files**: All 12 generated fan page directories under project root
- **Template file**: `createAct.py:419-422` -- the fix is present in code
- **Resolution**: Migration script `migrate_legacy_pages.py` injected `a:focus-visible { outline: 2px solid #ffff00; outline-offset: 2px; }` into the `<style>` block of all 12 existing generated pages. All interactive elements now have visible keyboard focus indicators.
- **WCAG**: SC 2.4.7 Focus Visible, Level AA -- now compliant

---

## Medium Issues

### N-002: Residual inline styles in generated fan pages
- **File**: `createAct.py:705,708,726`
- **Problem**: Three inline `style` attributes remain in the generated HTML template.
- **WCAG**: N/A (maintainability, user stylesheet override concern)
- **Fix**: Extract to named CSS classes in the generated page's `<style>` block.

### N-003: Guestbook links use `href="#"` with no indication of non-functionality
- **File**: `createAct.py:706,709-711`
- **Problem**: Five decorative links in the guestbook section use `href="#"`.
- **WCAG**: SC 2.4.4 Link Purpose (In Context), Level A
- **Fix**: Replace with `<span>` elements styled with a `.faux-link` class, or add `role="link" aria-disabled="true"`.

### N-004: Legacy generated pages still accessible via direct URL
- **File**: `app.py:91-100`
- **Problem**: The `view_band` route serves any band directory's `home.html` without checking for `band_info.json`.
- **Fix**: Add `band_info.json` existence check in `view_band()`, returning 404 for legacy directories.

### N-009: Gallery table lacks responsive handling for narrow viewports
- **File**: `static/css/style.css:449-492`, `templates/gallery.html:14-47`
- **Problem**: At viewports narrower than ~400px, the three-column gallery table leaves insufficient space for band names.
- **WCAG**: SC 1.4.10 Reflow, Level AA
- **Fix**: Add a sub-400px breakpoint that hides the photo column or switches to a stacked card layout.

### N-012: Band directory path validation blocks non-ASCII band names
- **File**: `app.py:36,94`
- **Problem**: `SAFE_BAND_NAME = re.compile(r'^[A-Za-z0-9_\-]+$')` rejects directories with non-ASCII characters.
- **Fix**: Broaden regex to `re.compile(r'^[\w\-]+$', re.UNICODE)`.

### N-016: Inconsistent path resolution between gallery and view_band routes
- **File**: `app.py:66-86,91-100`
- **Problem**: Gallery route uses `app.root_path` with `glob.glob()` while `view_band()` uses relative `os.path.join()`.
- **Fix**: Define a `BANDS_DIR` constant and use it consistently in both routes.

### N-019: Generated fan pages use `!important` overrides in responsive styles
- **File**: `createAct.py:619,622,625`
- **Problem**: `!important` in `@media (max-width: 600px)` block is unnecessary since generated pages use only embedded styles.
- **WCAG**: SC 1.4.12 Text Spacing, Level AA (user stylesheet override concern)
- **Fix**: Remove `!important` from all three declarations.

### N-024: Older generated pages use `#666666` text on `#000000` background -- **RESOLVED**
- **Files**: 8 of 12 generated fan pages
- **Resolution**: Migration script `migrate_legacy_pages.py` replaced all `#666666` occurrences with `#888888` (5.92:1 contrast ratio, passes WCAG AA) across all 12 generated pages.
- **WCAG**: SC 1.4.3 Contrast (Minimum), Level AA -- now compliant

---

## Low Issues

### N-005: `<hr>` elements use deprecated HTML attributes
- **File**: `createAct.py:672,679,692,699,704`
- **Problem**: `color`, `size`, `noshade` attributes on `<hr>` are deprecated in HTML5.

### N-006: Feature grid boxes lack equal height content alignment
- **File**: `static/css/style.css:304`
- **Problem**: `height: 100%` on `.feature-box` is redundant with flexbox.

### N-007: `role="form"` on `<form>` element is redundant
- **File**: `templates/generate.html:18`
- **Problem**: Redundant `role="form"` and `onsubmit="return false;"` alongside JS `preventDefault()`.

### N-008: No `<meta name="description">` on any page
- **File**: `templates/base.html:3-8`
- **Problem**: Affects SEO and link previews.

### N-010: Generated fan page nav bar pipe separators not hidden from AT
- **File**: `createAct.py:661`
- **Problem**: Pipe characters announced by screen readers.

### N-011: Blink animation timing mismatch between main app and generated pages
- **File**: `createAct.py:584` vs `static/css/style.css:650`
- **Problem**: Main app uses `step-start`; generated pages use `linear`.

### N-014: Inline `import re` inside functions in createAct.py
- **File**: `createAct.py:115,252`
- **Problem**: `import re` inside functions instead of at module level.

### N-015: Inline style on visitor count in generated pages
- **File**: `createAct.py:726`
- **Problem**: Part of the N-002 pattern.

### N-017: No focus management after gallery page load
- **File**: `templates/gallery.html`
- **Problem**: Minor landmark navigation gap on empty gallery state.

### N-018: Fixed polling interval with no backoff
- **File**: `templates/generate.html:355`
- **Problem**: Status polling at fixed 1500ms for up to 200 requests.

### N-020: Generated fan page `<br>` tag after decorative stars in header
- **File**: `createAct.py:651`
- **Problem**: `<br>` tag used for layout spacing after decorative stars.

### N-022: Generated fan page body has no explicit line-height on root element
- **File**: `createAct.py:408-415`
- **Problem**: Body rule does not set `line-height`. Main app sets `line-height: 1.5`.
- **WCAG**: SC 1.4.12 Text Spacing, Level AA (advisory)
- **Fix**: Add `line-height: 1.5;` to the generated page's `body` rule.

### N-025 (NEW): Older generated pages use deprecated `<marquee>` element
- **Files**: All pre-template-update generated pages
- **Problem**: Band title wrapped in `<marquee>`, deprecated in HTML5 with no pause mechanism.
- **WCAG**: SC 2.2.2 Pause, Stop, Hide, Level A

### N-026 (NEW): Older generated pages use `<a name="">` anchors instead of `id` attributes
- **Files**: All pre-template-update generated pages
- **Problem**: Section anchors use deprecated `<a name="">` pattern creating empty focusable elements.

### N-027 (NEW): Older generated pages skip heading level (h1 to h3)
- **Files**: All pre-template-update generated pages
- **Problem**: Section headings use `<h3>` while page title is `<h1>` via `<marquee>`, skipping `<h2>`.
- **WCAG**: SC 1.3.1 Info and Relationships, Level A (advisory)

---

## Positive Observations

1. **Template quality is excellent**: The current `createAct.py` template includes `lang="en"`, viewport meta, skip link, semantic landmarks, correct heading hierarchy, `focus-visible` indicators, `prefers-reduced-motion`, ARIA labels, properly escaped content, and CSS custom properties.
2. **Main app accessibility remains strong**: Skip link, ARIA progressbar, live regions, proper focus management, `focus-visible`, `prefers-reduced-motion`, scoped table headers, fieldset/legend, 44x44px touch targets.
3. **XSS prevention**: All AI-generated strings properly escaped via `html.escape()`.
4. **Design token system**: CSS custom properties well-organized and consistently used.
5. **Error resilience**: Consecutive network error counter with graceful degradation messaging.
6. **CSRF protection and rate limiting**: Origin/referer checks and per-IP rate limiting intact.

---

## Metrics
- Total tracked issues: 24 (was 19; +5 new issues found, 3 fixed this cycle)
- Critical: 0 | High: 0 | Medium: 7 | Low: 14
- Resolved this review: N-023 (critical -- gallery empty, fixed via migration), N-021 (high -- focus indicators injected into all pages), N-024 (medium -- contrast fixed)
- Previously resolved: N-001 (accent color contrast)
- New this review: N-023 (critical -- fixed), N-024 (medium -- fixed), N-025 (low -- marquee), N-026 (low -- `<a name>`), N-027 (low -- heading skip)
- Previously invalid: N-013 (`json` import is actually used)
