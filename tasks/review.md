# UX & Accessibility Code Review
**Date**: 2026-04-07
**Reviewer**: Jennifer Mitchelle (UX Design Critic)
**Branch**: fix/code-review-2026-04-06

## Summary

Fourth review of the AI Band Generator. The two fix commits (51ca7ca, a45fa18) resolved 7 of 10 previous critical/high issues fully and 2 partially. No critical issues remain. One high-priority color contrast issue persists. Five medium and six low issues logged.

**Files reviewed:**
- `templates/base.html`, `templates/index.html`, `templates/generate.html`, `templates/gallery.html`
- `static/css/style.css`, `static/js/main.js`
- `app.py`, `createAct.py`
- Legacy band directories (spot checks)

---

## Status of Previous Critical/High Issues

| Prior ID | Issue | Status |
|---|---|---|
| C-001/C-002 | Legacy pages with fixed footer / raw Markdown | Partially fixed -- hidden from gallery but still served via direct URL |
| C-003 | Layout table in generated fan page header | Fixed |
| C-004 | Discography tables lack semantics | Fixed |
| H-001 | Color contrast in accent tuples | Partially fixed -- see N-001 |
| H-002 | No error recovery for polling failures | Fixed |
| H-003 | Inline styles in generated fan pages | Mostly fixed -- residual inline styles remain (see N-002) |
| H-004 | Gallery band name derivation fragile | Fixed |
| H-005 | Star twinkle ignores prefers-reduced-motion | Fixed |
| H-006 | Back to Top link uses href="#" | Fixed |

---

## High Issues

### N-001: Color contrast failure in accent color tuple
- **File**: `createAct.py:354`
- **Code**: `("#ffff00", "#00ffff", "#ff6666")`
- **Problem**: `#ff6666` on `#000000` background achieves approximately 4.35:1 contrast ratio, which fails WCAG 2.1 AA for normal text (requires 4.5:1). The fix comment claims compliance but the math does not support it.
- **Fix**: Replace `#ff6666` with `#ff7777` (~5.0:1 on black).
- **WCAG**: SC 1.4.3 Contrast (Minimum), Level AA

---

## Medium Issues

### N-002: Residual inline styles in generated fan pages
- **File**: `createAct.py:701,704,722`
- **Problem**: Three inline `style` attributes remain after the H-003 fix. Inconsistent with the refactored CSS class approach used elsewhere in the template.
- **WCAG**: N/A (maintainability, user stylesheet override concern)

### N-003: Guestbook links use `href="#"` with no indication of non-functionality
- **File**: `createAct.py:702,708`
- **Problem**: Five decorative links in the guestbook section still use `href="#"`. Screen reader users encounter five links that all navigate to page top with different labels.
- **WCAG**: SC 2.4.4 Link Purpose (In Context), Level A

### N-004: Legacy generated pages still accessible via direct URL
- **File**: `app.py:91-100`
- **Problem**: The `view_band` route serves any band directory's `home.html` without checking for `band_info.json`. Legacy pages with old-template bugs are still reachable via direct navigation.
- **WCAG**: N/A (consistency)

### N-009: Gallery table lacks responsive handling for narrow viewports
- **File**: `static/css/style.css:449-492`, `templates/gallery.html:14-47`
- **Problem**: At viewports narrower than ~400px, the three-column gallery table leaves insufficient space for band names. No breakpoint exists for very narrow mobile devices.
- **WCAG**: SC 1.4.10 Reflow (Level AA)

### N-012: Band directory path validation blocks non-ASCII band names
- **File**: `app.py:36,94`
- **Problem**: The `SAFE_BAND_NAME` regex `^[A-Za-z0-9_\-]+$` blocks directories with non-ASCII characters (e.g., `ChaoDeCorais`). Such bands are generated successfully but permanently inaccessible via web route.
- **WCAG**: N/A (functional bug -- data loss)

---

## Low Issues

### N-005: `<hr>` elements use deprecated HTML attributes
- **File**: `createAct.py:668,675,688,695,700`
- **Problem**: `color`, `size`, and `noshade` attributes on `<hr>` are deprecated in HTML5.

### N-006: Feature grid boxes lack equal height content alignment
- **File**: `static/css/style.css:288-306`
- **Problem**: `height: 100%` on `.feature-box` is redundant with flexbox. Content alignment is unbalanced when text lengths differ.

### N-007: `role="form"` on `<form>` element is redundant
- **File**: `templates/generate.html:18`
- **Problem**: `<form>` already has implicit `form` role. Also, redundant `onsubmit="return false;"` alongside JS `preventDefault()`.

### N-008: No `<meta name="description">` on any page
- **File**: `templates/base.html:3-8`
- **Problem**: Affects SEO and link previews.

### N-010: Generated fan page nav bar pipe separators not hidden from assistive tech
- **File**: `createAct.py:656-662`
- **Problem**: Pipe characters between nav links are announced by screen readers. Main app's nav bar correctly uses `<span aria-hidden="true">` but the generated page does not.

### N-011: Blink animation in generated fan pages uses `linear` timing
- **File**: `createAct.py:580-584`
- **Problem**: Main app uses `step-start` timing; generated pages use `linear`, creating a gradual fade instead of instant on/off.

---

## Metrics
- Total issues: 12
- Critical: 0 | High: 1 | Medium: 5 | Low: 6
- Previously fixed: 7 fully, 2 partially
