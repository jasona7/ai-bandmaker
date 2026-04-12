# UX & Accessibility Code Review
**Date**: 2026-04-12
**Reviewer**: Jennifer Mitchelle (Senior UX Design Critic, Swords, Ireland)
**Branch**: fix/code-review-2026-04-06

## Summary

Ninth review of the AI Band Generator. The main application templates (`base.html`, `index.html`, `gallery.html`, `generate.html`) and CSS remain in strong shape with well-implemented accessibility patterns. The `createAct.py` template for newly generated fan pages is significantly improved with semantic HTML, skip links, landmarks, correct heading hierarchy, and `prefers-reduced-motion`. However, two new issues have surfaced: (1) the `**VelvetEchoes` directory contains literal asterisks in its name, making it unreachable via the URL route regex and creating a potential path traversal concern, and (2) the four legacy-format fan pages (EchoesOfTheMirage, MoonlitReverie, TheVelvetEchoes, **VelvetEchoes) have a fixed-position footer that permanently occludes page content. All previously open medium and low issues remain open and are carried forward. One new medium issue and two new low issues are identified.

**Files reviewed:**
- `templates/base.html`, `templates/index.html`, `templates/generate.html`, `templates/gallery.html`
- `static/css/style.css`, `static/js/main.js`
- `app.py`, `createAct.py`, `migrate_legacy_pages.py`
- Generated fan pages: all 12 band directories (`ChaoDeCorais`, `EchoesOfTheMirage`, `EtherealTrampleweed`, `EucalyptusSaints`, `Inu-k-trkadeka`, `MidnightParlor`, `MoonlitReverie`, `MyopicSunflowers`, `NightshadeVanguard`, `TheLuminescentUndertow`, `TheVelvetEchoes`, `**VelvetEchoes`)

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 7 |
| Low | 15 |

---

## Status of Previous Issues

| Prior ID | Issue | Status |
|---|---|---|
| N-001 | Color contrast failure in accent color tuple (#ff6666) | **RESOLVED** |
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
| N-012 | Band directory path validation blocks non-ASCII band names | Open (Medium) -- **expanded, see N-028** |
| N-014 | Inline `import re` inside functions in createAct.py | Open (Low) |
| N-015 | Inline style on visitor count in generated pages | Open (Low) -- subsumed under N-002 |
| N-016 | Inconsistent path resolution between gallery and view_band routes | Open (Medium) |
| N-017 | No focus management after gallery page load | Open (Low) |
| N-018 | Fixed polling interval with no backoff | Open (Low) |
| N-019 | Generated fan pages use `!important` overrides in responsive styles | Open (Medium) |
| N-020 | Generated fan page `<br>` tag after decorative stars in header | Open (Low) |
| N-021 | Generated fan pages have no focus indicator styles | **RESOLVED** |
| N-022 | Generated fan page body has no explicit line-height | Open (Low) |
| N-023 | Gallery displays zero bands because no `band_info.json` files exist | **RESOLVED** |
| N-024 | Older generated pages use `#666666` text | **RESOLVED** |
| N-025 | Older generated pages use deprecated `<marquee>` element | Open (Low) |
| N-026 | Older generated pages use `<a name="">` anchors instead of `id` | Open (Low) |
| N-027 | Older generated pages skip heading level (h1 to h3) | Open (Low) |

---

## Escalation Assessment

Each issue was reviewed to determine whether any should be escalated:

- **N-028 (new)**: The `**VelvetEchoes` directory contains literal asterisk characters. The `SAFE_BAND_NAME` regex correctly rejects this, making the band unreachable via `/band/**VelvetEchoes/`. However, the band still appears in the gallery (because `glob.glob()` discovers it and `band_info.json` exists), creating a dead link. This is a functional bug that silently breaks the gallery user experience. **Escalated to High.**
- **N-012**: `ChaoDeCorais` (non-ASCII) and `**VelvetEchoes` (special characters) are both generated, have `band_info.json`, appear in the gallery, but return 400 when clicked. Two of twelve gallery entries are broken links. N-012 scope expanded but severity stays medium since the root fix (broadening the regex) is the same.
- All other medium issues reviewed -- none warrant escalation. See previous review for detailed rationale.

---

## High Issues

### N-028: `**VelvetEchoes` directory creates dead gallery link via special characters in name — **RESOLVED 2026-04-12**

- **File**: `app.py:73-74` (gallery route filter)
- **Problem**: Band directories with names that don't match `SAFE_BAND_NAME` (e.g., `**VelvetEchoes` with asterisks, `ChãoDeCorais` with non-ASCII) appeared in gallery but returned HTTP 400 when clicked.
- **Resolution**: Added `SAFE_BAND_NAME` filter in gallery route to exclude unreachable bands from listing. Dead links eliminated.

---

## Medium Issues

### N-002: Residual inline styles in generated fan pages
- **File**: `createAct.py:705,708,726`
- **Problem**: Three inline `style` attributes remain in the template (`text-align:center`, `color:#888888`, visitor count color).
- **WCAG**: N/A (maintainability, user stylesheet override concern)
- **Fix**: Extract to named CSS classes.

### N-003: Guestbook links use `href="#"` with no indication of non-functionality
- **File**: `createAct.py:706,709-711`
- **Problem**: Five decorative links in the guestbook section use `href="#"` (Sign the Guestbook, View Guestbook, Link to us, Webrings, MIDI Archive). Screen reader users will encounter these as actionable links that navigate nowhere meaningful.
- **WCAG**: SC 2.4.4 Link Purpose (In Context), Level A
- **Fix**: Replace with `<span>` elements styled with a `.faux-link` class, or add `aria-disabled="true"` and `role="link"`.

### N-004: Legacy generated pages still accessible via direct URL
- **File**: `app.py:91-100`
- **Problem**: `view_band()` serves any directory's `home.html` without checking for `band_info.json`.
- **Fix**: Add `band_info.json` existence check.

### N-009: Gallery table lacks responsive handling for narrow viewports
- **File**: `static/css/style.css:449-492`, `templates/gallery.html:14-47`
- **Problem**: Below ~400px, the three-column gallery table is cramped.
- **WCAG**: SC 1.4.10 Reflow, Level AA
- **Fix**: Add a sub-400px breakpoint hiding the photo column or switch to a card layout.

### N-012: Band directory path validation blocks non-ASCII and special-character band names
- **File**: `app.py:36,94`
- **Problem**: `SAFE_BAND_NAME = re.compile(r'^[A-Za-z0-9_\-]+$')` blocks `ChaoDeCorais` (non-ASCII) and `**VelvetEchoes` (asterisks). Both directories exist and have valid content.
- **Fix**: For non-ASCII: broaden to `re.compile(r'^[\w\-]+$', re.UNICODE)`. For asterisks: sanitize directory names at generation time in `createAct.py` to prevent invalid characters, and filter gallery listings to exclude unreachable directories.

### N-016: Inconsistent path resolution between gallery and view_band routes
- **File**: `app.py:66-86,91-100`
- **Problem**: Gallery uses `app.root_path` with `glob.glob()`; `view_band()` uses relative `os.path.join()`. If the working directory differs from the project root, `view_band()` fails silently.
- **Fix**: Use `app.root_path` consistently in both routes.

### N-019: Generated fan pages use `!important` overrides in responsive styles
- **File**: `createAct.py:619,622,625`
- **Problem**: `!important` in `@media (max-width: 600px)` block is unnecessary since generated pages use only embedded styles with no specificity conflicts.
- **WCAG**: SC 1.4.12 Text Spacing, Level AA (user stylesheet override concern)
- **Fix**: Remove `!important` from all three declarations.

---

## Low Issues

### N-005: `<hr>` elements use deprecated HTML attributes
- **File**: `createAct.py:672,679,692,699,704`
- **Problem**: `color`, `size`, `noshade` attributes on `<hr>` are deprecated in HTML5.

### N-006: Feature grid boxes lack equal height content alignment
- **File**: `static/css/style.css:304`
- **Problem**: `height: 100%` on `.feature-box` is redundant with flexbox parent.

### N-007: `role="form"` on `<form>` element is redundant
- **File**: `templates/generate.html:18`
- **Problem**: `<form>` already has implicit `form` role. Also, `onsubmit="return false;"` is redundant with JS `preventDefault()`.

### N-008: No `<meta name="description">` on any page
- **File**: `templates/base.html:3-8`
- **Problem**: Missing meta description affects SEO and link previews.

### N-010: Generated fan page nav bar pipe separators not hidden from AT
- **File**: `createAct.py:661`
- **Problem**: Pipe characters between nav links announced by screen readers.

### N-011: Blink animation timing mismatch between main app and generated pages
- **File**: `createAct.py:584` vs `static/css/style.css:650`
- **Problem**: Main app uses `step-start`; generated pages use `linear`.

### N-014: Inline `import re` inside functions in createAct.py
- **File**: `createAct.py:115,252`
- **Problem**: Module-level import would be cleaner.

### N-017: No focus management after gallery page load
- **File**: `templates/gallery.html`

### N-018: Fixed polling interval with no backoff
- **File**: `templates/generate.html:355`
- **Problem**: 1500ms fixed interval for up to 200 requests without exponential backoff.

### N-020: Generated fan page `<br>` tag after decorative stars
- **File**: `createAct.py:651`

### N-022: Generated fan page body has no explicit line-height
- **File**: `createAct.py:408-415`
- **WCAG**: SC 1.4.12 Text Spacing, Level AA (advisory)

### N-025: Older generated pages use deprecated `<marquee>` element
- **Files**: 8 of 12 generated pages (all non-legacy-format pages)
- **WCAG**: SC 2.2.2 Pause, Stop, Hide, Level A

### N-026: Older generated pages use `<a name="">` anchors instead of `id` attributes
- **Files**: 8 of 12 generated pages

### N-027: Older generated pages skip heading level (h1 to h3)
- **Files**: 8 of 12 generated pages (EtherealTrampleweed, NightshadeVanguard, MidnightParlor, etc.)
- **WCAG**: SC 1.3.1 Info and Relationships, Level A (advisory)

### N-029 (NEW): Legacy-format fan pages have fixed-position footer that occludes content
- **Files**: `EchoesOfTheMirage/home.html:91`, `MoonlitReverie/home.html:91`, `TheVelvetEchoes/home.html:91`, `**VelvetEchoes/home.html:91`
- **Problem**: The four legacy-format pages (old template) set `footer { position: fixed; bottom: 0; width: 100%; }`. This causes the footer to permanently overlay the bottom of the page content. On longer pages, content scrolls behind the footer and is unreachable. This is a Gestalt principle violation (figure/ground confusion) and a WCAG SC 1.4.8 Visual Presentation concern.
- **Fix**: The migration script could replace `position: fixed` with `position: static` or `position: relative` in these four files.

### N-030 (NEW): Legacy-format fan pages render empty band members section
- **Files**: `EchoesOfTheMirage/home.html:143-146`, `MoonlitReverie/home.html:147-150`, `TheVelvetEchoes/home.html:137-140`, `**VelvetEchoes/home.html`
- **Problem**: These four pages display "Band Members: " as a caption followed by an empty `<div>`. The band member data was not parsed correctly during initial generation. Users see a "Band Members" section with no content -- a misleading affordance (Nielsen heuristic #2, Match Between System and Real World).
- **Fix**: Either remove the empty members section heading from these pages via migration, or re-generate the member data and inject it.

---

## Positive Observations

1. **Template quality is excellent**: The current `createAct.py` template includes `lang="en"`, viewport meta, skip link, semantic `<header>/<main>/<footer>/<nav>`, correct heading hierarchy (h1 > h2), `focus-visible`, `prefers-reduced-motion`, ARIA labels, XSS escaping, and CSS custom properties.
2. **Main app accessibility remains strong**: Skip link, ARIA progressbar, `aria-live` regions, proper focus management on state changes, `focus-visible` on all interactive elements, `prefers-reduced-motion`, scoped table headers, `fieldset`/`legend`, 44x44px touch targets.
3. **All color contrast ratios pass WCAG AA**: Verified all foreground/background pairs across both the main app and generated pages. Lowest ratio is 5.82:1 (#555 on #F0E68C in legacy pages), well above the 4.5:1 threshold.
4. **Design token system**: CSS custom properties well-organized and consistently used in main app.
5. **Error resilience**: Consecutive network error counter with graceful degradation messaging.
6. **CSRF protection and rate limiting**: Origin/referer checks and per-IP rate limiting intact.
7. **Migration script**: Well-structured and idempotent, correctly handles focus-visible injection and contrast fixes.

---

## Metrics
- Total tracked issues: 27 (was 24; +3 new, 0 resolved this cycle)
- Critical: 0 | High: 0 | Medium: 7 | Low: 15
- Resolved cumulative: N-001, N-021, N-023, N-024, N-028 (5 total)
- New this review: N-028 (high, resolved -- dead gallery links from special-character directory names), N-029 (low -- fixed footer occludes content), N-030 (low -- empty members section in legacy pages)
- Previously invalid: N-013 (`json` import is used)
