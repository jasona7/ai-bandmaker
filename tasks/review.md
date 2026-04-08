# UX & Accessibility Code Review
**Date**: 2026-04-08
**Reviewer**: Jennifer Mitchelle (UX Design Critic)
**Branch**: fix/code-review-2026-04-06

## Summary

Fifth review of the AI Band Generator. The previous high-priority issue (N-001: accent color contrast) has been resolved. No critical or high issues remain. Six medium and ten low issues are logged. One new medium issue (N-016: path inconsistency) and four new low issues were discovered.

**Files reviewed:**
- `templates/base.html`, `templates/index.html`, `templates/generate.html`, `templates/gallery.html`
- `static/css/style.css`, `static/js/main.js`
- `app.py`, `createAct.py`

---

## Status of Previous Issues

| Prior ID | Issue | Status |
|---|---|---|
| N-001 | Color contrast failure in accent color tuple (#ff6666) | **RESOLVED** — now `#ff7777`, passes 4.5:1 on dark bg |
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

---

## Medium Issues

### N-002: Residual inline styles in generated fan pages
- **File**: `createAct.py:701,704,722`
- **Problem**: Three inline `style` attributes remain after the H-003 fix. Inconsistent with the refactored CSS class approach used elsewhere in the template.
- **WCAG**: N/A (maintainability, user stylesheet override concern)
- **Fix**: Extract to named CSS classes in the generated page's `<style>` block.

### N-003: Guestbook links use `href="#"` with no indication of non-functionality
- **File**: `createAct.py:702,705-707`
- **Problem**: Five decorative links in the guestbook section use `href="#"`. Screen reader users encounter five links that all navigate to page top with different labels.
- **WCAG**: SC 2.4.4 Link Purpose (In Context), Level A
- **Fix**: Replace with `<span>` elements styled as `.faux-link`, or add `aria-disabled="true"` with explanatory labels.

### N-004: Legacy generated pages still accessible via direct URL
- **File**: `app.py:91-100`
- **Problem**: The `view_band` route serves any band directory's `home.html` without checking for `band_info.json`. Legacy pages with old-template bugs are still reachable.
- **WCAG**: N/A (consistency)
- **Fix**: Add a `band_info.json` existence check in `view_band()`, returning 404 for legacy directories.

### N-009: Gallery table lacks responsive handling for narrow viewports
- **File**: `static/css/style.css:449-492`, `templates/gallery.html:14-47`
- **Problem**: At viewports narrower than ~400px, the three-column gallery table leaves insufficient space for band names. No breakpoint exists for very narrow mobile devices.
- **WCAG**: SC 1.4.10 Reflow, Level AA
- **Fix**: Add a sub-400px breakpoint that hides the photo column or switches to a stacked card layout.

### N-012: Band directory path validation blocks non-ASCII band names
- **File**: `app.py:36,94`
- **Problem**: The `SAFE_BAND_NAME` regex `^[A-Za-z0-9_\-]+$` blocks directories with non-ASCII characters. Such bands are generated but permanently inaccessible via web route.
- **WCAG**: N/A (functional bug — data loss)
- **Fix**: Sanitize non-ASCII in `create_project_directory()` or broaden regex to `^[\w\-]+$` with `re.UNICODE`.

### N-016 (NEW): Inconsistent path resolution between gallery and view_band routes
- **File**: `app.py:66-86,91-100`
- **Problem**: Gallery route uses `app.root_path` with `glob.glob()` while `view_band()` uses relative `os.path.join()`. Path resolution could fail depending on working directory when server starts.
- **WCAG**: N/A (functional reliability)
- **Fix**: Define a `BANDS_DIR` constant and use it consistently in both routes.

---

## Low Issues

### N-005: `<hr>` elements use deprecated HTML attributes
- **File**: `createAct.py:668,675,688,695,700`
- **Problem**: `color`, `size`, `noshade` attributes on `<hr>` are deprecated in HTML5.

### N-006: Feature grid boxes lack equal height content alignment
- **File**: `static/css/style.css:288-306`
- **Problem**: `height: 100%` on `.feature-box` is redundant with flexbox. Content alignment unbalanced.

### N-007: `role="form"` on `<form>` element is redundant
- **File**: `templates/generate.html:18`
- **Problem**: Redundant `role="form"` and `onsubmit="return false;"` alongside JS `preventDefault()`.

### N-008: No `<meta name="description">` on any page
- **File**: `templates/base.html:3-8`
- **Problem**: Affects SEO and link previews.

### N-010: Generated fan page nav bar pipe separators not hidden from AT
- **File**: `createAct.py:656-662`
- **Problem**: Pipe characters announced by screen readers. Main app correctly uses `aria-hidden="true"` but generated pages do not.

### N-011: Blink animation in generated fan pages uses `linear` timing
- **File**: `createAct.py:580-584`
- **Problem**: Main app uses `step-start`; generated pages use `linear`. Inconsistent design language.

### N-013 (NEW): Unused `json` import in app.py
- **File**: `app.py:3`
- **Problem**: `import json` is present but never used in `app.py`.

### N-014 (NEW): Inline `import re` inside functions in createAct.py
- **File**: `createAct.py:115,252`
- **Problem**: `import re` inside functions instead of at module level. Inconsistent with Python style.

### N-015 (NEW): Inline style on visitor count in generated pages
- **File**: `createAct.py:722`
- **Problem**: Visitor count uses inline `style="color:{c1};"`. Part of the N-002 pattern.

### N-017 (NEW): No focus management after gallery page load
- **File**: `templates/gallery.html`
- **Problem**: Minor landmark navigation gap on empty gallery state.

### N-018 (NEW): Fixed polling interval with no backoff
- **File**: `templates/generate.html:355`
- **Problem**: Status polling at fixed 1500ms for up to 200 requests. No backoff after plateau.

---

## Metrics
- Total issues: 16
- Critical: 0 | High: 0 | Medium: 6 | Low: 10
- Previously resolved: N-001 (accent color contrast)
