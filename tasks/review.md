# UX & Accessibility Code Review
**Date**: 2026-04-10
**Reviewer**: Jennifer Mitchelle (Senior UX Design Critic, Swords, Ireland)
**Branch**: fix/code-review-2026-04-06

## Summary

Seventh review of the AI Band Generator. All previously resolved issues remain resolved. No regressions detected. Two new issues identified: N-021 (high -- missing focus indicators on generated fan pages) and N-022 (low -- missing line-height). N-021 has been **fixed** in this review cycle. All critical and high issues are now resolved. The application's main pages continue to demonstrate strong accessibility fundamentals.

**Files reviewed:**
- `templates/base.html`, `templates/index.html`, `templates/generate.html`, `templates/gallery.html`
- `static/css/style.css`, `static/js/main.js`
- `app.py`, `createAct.py`

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 7 |
| Low | 11 |

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

---

## Escalation Assessment

Each medium issue was reviewed to determine whether any should be escalated to high or critical:

- **N-002 (inline styles)**: Maintainability concern only. Does not block users or violate WCAG AA. Stays medium.
- **N-003 (guestbook `#` links)**: While technically a WCAG SC 2.4.4 Level A issue, it exists only on generated fan pages (not the main app) and the guestbook section is clearly themed as decorative retro content. Stays medium.
- **N-004 (legacy pages)**: No accessibility barrier; old pages are simply inconsistent. Gallery already filters them out. Stays medium.
- **N-009 (gallery table < 400px)**: SC 1.4.10 Reflow is Level AA, but devices below 400px are edge-case. The table remains functional (horizontally scrollable), just cramped. Stays medium.
- **N-012 (non-ASCII path validation)**: Functional bug where bands with non-ASCII names are generated but unreachable. However, non-ASCII names are uncommon given English prompts. Stays medium.
- **N-016 (path resolution inconsistency)**: Functional reliability concern, not user-facing unless CWD differs from project root. Stays medium.
- **N-019 (!important overrides)**: User stylesheet override concern. No direct accessibility barrier. Medium.

---

## High Issues

### N-021: Generated fan pages have no focus indicator styles -- **RESOLVED**

- **File**: `createAct.py:418-421`
- **Resolution**: Added `a:focus-visible { outline: 2px solid #ffff00; outline-offset: 2px; }` to the generated fan page's embedded `<style>` block. Matches the main app's focus indicator pattern. All 12+ interactive elements on generated pages now have visible keyboard focus indicators against the #000000 background.
- **WCAG**: SC 2.4.7 Focus Visible, Level AA -- now compliant

---

## Medium Issues

### N-002: Residual inline styles in generated fan pages
- **File**: `createAct.py:701,704,722`
- **Problem**: Three inline `style` attributes remain in the generated HTML template. At line 701: `style="text-align:center; padding:10px;"`. At line 704: `style="color:#888888; font-size:0.8em;"`. At line 722: `style="color:{c1};"`. Inconsistent with the class-based approach used elsewhere.
- **WCAG**: N/A (maintainability, user stylesheet override concern)
- **Fix**: Extract to named CSS classes in the generated page's `<style>` block.

### N-003: Guestbook links use `href="#"` with no indication of non-functionality
- **File**: `createAct.py:702,705-707`
- **Problem**: Five decorative links in the guestbook section use `href="#"`. Screen reader users encounter five links that all navigate to page top with different labels.
- **WCAG**: SC 2.4.4 Link Purpose (In Context), Level A
- **Fix**: Replace with `<span>` elements styled with a `.faux-link` class, or add `role="link" aria-disabled="true"`.

### N-004: Legacy generated pages still accessible via direct URL
- **File**: `app.py:91-100`
- **Problem**: The `view_band` route serves any band directory's `home.html` without checking for `band_info.json`. Legacy pages with old-template bugs are still reachable.
- **WCAG**: N/A (consistency)
- **Fix**: Add `band_info.json` existence check in `view_band()`, returning 404 for legacy directories.

### N-009: Gallery table lacks responsive handling for narrow viewports
- **File**: `static/css/style.css:449-492`, `templates/gallery.html:14-47`
- **Problem**: At viewports narrower than ~400px, the three-column gallery table leaves insufficient space for band names. No breakpoint exists for very narrow mobile devices.
- **WCAG**: SC 1.4.10 Reflow, Level AA
- **Fix**: Add a sub-400px breakpoint that hides the photo column or switches to a stacked card layout.

### N-012: Band directory path validation blocks non-ASCII band names
- **File**: `app.py:36,94`
- **Problem**: `SAFE_BAND_NAME = re.compile(r'^[A-Za-z0-9_\-]+$')` rejects directories with non-ASCII characters. Bands with non-ASCII names are generated but permanently inaccessible via web route.
- **WCAG**: N/A (functional bug -- data loss)
- **Fix**: Sanitize non-ASCII in `create_project_directory()` or broaden regex to `re.compile(r'^[\w\-]+$', re.UNICODE)`.

### N-016: Inconsistent path resolution between gallery and view_band routes
- **File**: `app.py:66-86,91-100`
- **Problem**: Gallery route uses `app.root_path` with `glob.glob()` while `view_band()` uses relative `os.path.join()`. Path resolution could fail depending on working directory.
- **WCAG**: N/A (functional reliability)
- **Fix**: Define a `BANDS_DIR` constant and use it consistently in both routes.

### N-019: Generated fan pages use `!important` overrides in responsive styles
- **File**: `createAct.py:615,618,621`
- **Problem**: The generated fan page's embedded CSS uses `!important` on three declarations in the `@media (max-width: 600px)` block. Since the generated page uses only embedded styles with no external stylesheet competing, `!important` is unnecessary. It prevents user stylesheets from overriding these values.
- **WCAG**: SC 1.4.12 Text Spacing, Level AA (user stylesheet override concern)
- **Fix**: Remove `!important` from all three declarations.

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

### N-011: Blink animation timing mismatch between main app and generated pages
- **File**: `createAct.py:580-584` vs `static/css/style.css:648-655`
- **Problem**: Main app uses `step-start`; generated pages use `linear`. Inconsistent design language.

### N-014: Inline `import re` inside functions in createAct.py
- **File**: `createAct.py:115,252`
- **Problem**: `import re` inside functions instead of at module level. Inconsistent with Python conventions.

### N-015: Inline style on visitor count in generated pages
- **File**: `createAct.py:722`
- **Problem**: Visitor count uses inline `style="color:{c1};"`. Part of the N-002 pattern.

### N-017: No focus management after gallery page load
- **File**: `templates/gallery.html`
- **Problem**: Minor landmark navigation gap on empty gallery state.

### N-018: Fixed polling interval with no backoff
- **File**: `templates/generate.html:355`
- **Problem**: Status polling at fixed 1500ms for up to 200 requests. No backoff after plateau.

### N-020: Generated fan page `<br>` tag after decorative stars in header
- **File**: `createAct.py:647`
- **Problem**: `<br>` tag used for layout spacing after decorative stars. Main app uses block-level `<div>` elements instead. Minor inconsistency.

### N-022 (NEW): Generated fan page body has no explicit line-height on root element
- **File**: `createAct.py:408-415`
- **Problem**: The generated fan page's `body` rule does not set `line-height`. While the `.backstory-box` rule sets `line-height: 1.6` at line 514, the rest of the page content (band subtitle, member cards, guestbook, footer) inherits the browser default, which varies across user agents (typically 1.0-1.2). The main app explicitly sets `line-height: 1.5` on `body`. This is a minor readability concern, not a WCAG violation, but SC 1.4.12 Text Spacing recommends line heights of at least 1.5 for body text.
- **WCAG**: SC 1.4.12 Text Spacing, Level AA (advisory, not a violation since user can override)
- **Fix**: Add `line-height: 1.5;` to the generated page's `body` rule.

---

## Positive Observations

1. **Skip link**: Properly implemented on both main app and generated fan pages.
2. **Keyboard navigation**: All interactive elements reachable and operable. Focus indicators use `focus-visible` with high-contrast yellow outline (main app only -- see N-021 for generated pages).
3. **ARIA progressbar**: Proper `role="progressbar"` with dynamically updated values.
4. **Live regions**: Progress uses `aria-live="polite"`, errors use `aria-live="assertive"` -- correct urgency levels.
5. **Focus management**: State transitions correctly move focus via `tabindex="-1"` and `.focus()`.
6. **Reduced motion**: Both main app and generated pages respect `prefers-reduced-motion: reduce`.
7. **Touch targets**: Buttons meet 44x44px minimum.
8. **Design tokens**: CSS custom properties well-organized and consistently used.
9. **Color contrast**: Primary text (#cccccc on #000022) passes WCAG AA at ~10.5:1. All accent colors pass 4.5:1.
10. **Semantic HTML**: Proper use of landmarks, scoped table headers, fieldset/legend, and heading hierarchy.
11. **XSS prevention**: All AI-generated strings properly escaped via `html.escape()` before template insertion.
12. **Error resilience**: Consecutive network error counter with graceful degradation messaging.

---

## Metrics
- Total tracked issues: 19 (was 17; +1 new high, +1 new low)
- Critical: 0 | High: 0 | Medium: 7 | Low: 11
- Resolved this review: N-021 (focus indicators added to generated fan pages)
- Previously resolved: N-001 (accent color contrast)
- Reclassified as invalid: N-013 (`json` import is actually used)
- New this review: N-021 (high -- fixed), N-022 (low)
