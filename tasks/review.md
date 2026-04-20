# UX & Accessibility Code Review
**Date**: 2026-04-20
**Reviewer**: Jennifer Mitchelle (Senior UX Design Critic, Swords, Ireland)
**Branch**: fix/code-review-2026-04-13

## Summary

Seventeenth periodic review of the AI Band Generator. No code changes have been made since the prior review (2026-04-19). This cycle performed a fresh deep re-audit of all key files, re-reading all templates, CSS, JS, app.py, createAct.py, and rotating the fan-page spot-check set to a different subset (EucalyptusSaints, Inu-k-trkadeka, MidnightParlor, TheLuminescentUndertow, ChãoDeCorais) with targeted grep checks across all 12 pages and cross-verification against the 4 legacy pages.

The deep re-audit identified 1 new issue:

- **N-036 (Low)**: `resetInterface()` and `cancelGeneration()` paths in `generate.html` do not explicitly move focus back to a visible element after hiding the progress/success/error panels and re-showing the start-generation form. Keyboard focus is left on the now-hidden button the user just activated (cancel / retry / change-params / generate-another), so the next Tab press falls back to the beginning of the document instead of continuing from a sensible position. WCAG SC 2.4.3 Focus Order (Level A) is an advisory concern here -- focus is not lost entirely, but the UX is suboptimal.

All 7 previously resolved issues remain verified as resolved. The 7 existing medium issues and 18 existing low issues (including the new N-035 from last cycle) carry forward. With the 1 new issue, the total open count is now 7 medium and 19 low.

8 `band_photo.jpg` files remain untracked in git. These are binary assets and will be included in this cycle's review commit.

**Files reviewed:**
- `templates/base.html`, `templates/index.html`, `templates/generate.html`, `templates/gallery.html`
- `static/css/style.css` (724 lines), `static/js/main.js` (19 lines)
- `app.py` (285 lines), `createAct.py` (828 lines)
- Generated fan pages (this cycle's rotation): EucalyptusSaints, Inu-k-trkadeka, MidnightParlor, TheLuminescentUndertow, ChãoDeCorais (full read); EchoesOfTheMirage (spot-read lines 1-100, 130-159) for legacy-format cross-check
- Grep verification across all 12 pages for: skip-link, a:focus-visible, prefers-reduced-motion, marquee presence, #666666 text, href="#" residuals, #ff6666 accent residual, `<a name=>` anchors
- `tasks/review.md` (prior review document, reviewed for context)

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 7 |
| Low | 19 |

---

## Status of Previous Issues

| Prior ID | Issue | Status |
|---|---|---|
| N-001 | Color contrast failure in accent color tuple (#ff6666) | **RESOLVED** -- verified, 0 occurrences of `ff6666` across py/html/css |
| N-002 | Residual inline styles in generated fan pages | Open (Medium) |
| N-003 | Guestbook links use `href="#"` with no indication | **RESOLVED** -- verified, 0 matches of `href="#"` across all 12 pages |
| N-004 | Legacy generated pages still accessible via direct URL without band_info.json check | Open (Medium) |
| N-005 | `<hr>` elements use deprecated HTML attributes | Open (Low) |
| N-006 | Feature grid boxes lack equal height content alignment | Open (Low) |
| N-007 | `role="form"` on `<form>` element is redundant | Open (Low) -- re-verified at generate.html:18 |
| N-008 | No `<meta name="description">` on any page | Open (Low) -- re-verified, 0 matches in templates/*.html |
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
| N-024 | Older generated pages use `#666666` text | **RESOLVED** -- verified, 0 matches of `#666666` in any served page |
| N-025 | Older generated pages use deprecated `<marquee>` element | Open (Low) -- 8 of 12 pages still have it |
| N-026 | Older generated pages use `<a name="">` anchors instead of `id` | Open (Low) -- 8 pages x 5 anchors = 40 occurrences confirmed |
| N-027 | Older generated pages heading hierarchy issues | Open (Low) -- narrowed to legacy pages; v1 heading issue tracked as N-033 |
| N-028 | Dead gallery links from special-character band names | **RESOLVED** -- verified, gallery route filters by SAFE_BAND_NAME |
| N-029 | Legacy-format fan pages have fixed-position footer that occludes content | Open (Low) |
| N-030 | Legacy-format fan pages render empty band members section | Open (Low) |
| N-031 | All 12 existing fan pages lack skip links, landmarks, and prefers-reduced-motion | **RESOLVED** -- all 12 pages have skip links; prefers-reduced-motion in the 8 v1 pages (legacy pages don't use blink/marquee so the media query is N/A for them) |
| N-032 | `band_assets` route does not validate `filename` parameter | Open (Low) |
| N-033 | v1 fan pages have no `<h1>` element -- band name inside `<marquee>` | Open (Medium) |
| N-034 | Legacy fan pages lack `aria-label` on `<nav>` element | Open (Low) -- re-verified, EchoesOfTheMirage `<nav>` has no aria-label |
| N-035 | Legacy fan pages have fixed-width band photo that overflows on narrow viewports | Open (Low) |

---

## Escalation Assessment

### Medium Issues Re-evaluated

All 7 medium issues were re-assessed for escalation to High. N-002, N-004, N-009, N-012, N-016, N-019 are now 14+ days old; N-033 is 2 days old.

- **N-002 (inline styles in v2 template, createAct.py:710,713,731)**: Remains Medium. Three inline `style` attributes (`text-align:center`, `color:#888888`, visitor count color) affect maintainability but do not create a WCAG violation. These are cosmetic guestbook and footer areas. No escalation warranted. Worth noting that v1 pages contain substantially more inline styles (on members table `<td>`, album `<ol>` and `<li>`, guestbook `<p>`), but those are frozen historical content -- won't be regenerated -- so they fall under legacy-page tech debt, not active bugs. Not escalating.

- **N-004 (legacy pages without band_info.json check, app.py:95-104)**: Remains Medium. The `view_band()` route validates via `SAFE_BAND_NAME` regex, and `send_from_directory` is directory-scoped, so there is no security exposure. The issue is functional correctness (serving pages not gallery-indexed). No escalation warranted.

- **N-009 (gallery table not responsive below 400px)**: Remains Medium. At 320px viewport width, the table is cramped but remains functional. Content does not overflow horizontally because columns compress. No escalation warranted.

- **N-012 (non-ASCII band name path validation, app.py:36)**: Remains Medium. `SAFE_BAND_NAME = r'^[A-Za-z0-9_\-]+$'` filters `ChãoDeCorais` and `**VelvetEchoes` from the gallery. Users who created these bands can still view them via the success redirect if the path happens to hit the legacy dash tolerance. Data is not lost, merely hidden. No escalation warranted.

- **N-016 (inconsistent path resolution, app.py:66-86,95-104)**: Remains Medium. Latent bug only surfaces in non-standard deployment (CWD != project root). No escalation warranted.

- **N-019 (!important overrides in generated pages, createAct.py:624,627,630)**: Remains Medium. The three `!important` declarations in the 600px mobile breakpoint override nothing in the cascade (specificity is already sufficient). Unnecessary clutter rather than an active problem. No escalation warranted.

- **N-033 (no `<h1>` in v1 fan pages, 8 pages)**: Remains Medium. Band name is inside `<marquee>` with no heading semantics; first heading on page is `<h3>`. WCAG SC 1.3.1 Level A concern. Content is still readable sequentially and band name appears in `<title>`. Impact is on AT users navigating by headings. Not escalating this cycle; flagged as the top-priority Medium for the next remediation pass.

### Low Issues Re-evaluated for Escalation

All 18 existing low issues were reassessed. None warranted escalation:

- **N-025 (deprecated `<marquee>`, 8 pages)**: Mitigated by `prefers-reduced-motion` media query in all 8 v1 pages. Remains Low.
- **N-029 (fixed footer in legacy pages)**: Confirmed only the 4 legacy pages use `position: fixed` on `footer`; the 8 v1 pages only use `position: fixed` on `.skip-link:focus` (correct usage). Remains Low.
- **N-035 (fixed-width band photo in legacy pages)**: Unchanged since introduction last cycle. These are legacy frozen pages. Remains Low.
- All other low issues are unchanged from prior assessment.

No escalations this cycle.

---

## New Issues

### N-036: Focus is not moved to a visible element after resetInterface / cancelGeneration (Low)
- **File**: `templates/generate.html:471-511` (`cancelGeneration`, `resetInterface`)
- **WCAG**: SC 2.4.3 Focus Order, Level A (advisory); SC 3.2.2 On Input, Level A
- **Problem**: When a user activates "Cancel", "Try Again", "Change Parameters", or "Generate Another", `resetInterface()` hides the currently visible panel (`progressDisplay` / `errorDisplay` / `successDisplay`) and re-shows `startGeneration`. Focus management is not performed: the keyboard focus remains on the now-hidden button the user just pressed. Because that button is inside a `display:none` ancestor, most browsers invalidate the focus target and focus falls back to `<body>`. The next Tab press then jumps to the first focusable element in the document (the skip-link), which is disorienting for keyboard users who expected to continue their flow on the parameter form.
- **Severity rationale**: Low. Focus is not permanently lost (Tab still works), the reset is user-initiated (not unexpected context change), and sighted mouse users are unaffected. The transition into progress/success/error states *does* move focus correctly (`progressTitle.focus()`, `#successDisplay h3` focus, `#errorDisplay h3` focus) -- this is specifically about the return path.
- **Fix**: After the style display swaps in `resetInterface()`, focus a meaningful element in the restored `startGeneration` panel. The `<h2 class="section-header">~ Generate Your AI Band ~</h2>` at the top of the generate-page content is a natural target if given `tabindex="-1"`, or alternatively focus the first `retro-select` (`#genre1`) so the user can immediately continue making parameter choices. Preferred implementation:
  ```js
  // at end of resetInterface()
  const genre1 = document.getElementById('genre1');
  if (genre1) genre1.focus();
  ```
  This honours the user's likely next action (adjusting parameters) and keeps them in context.

---

## Medium Issues (carried forward)

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
- **Problem**: `SAFE_BAND_NAME` regex blocks `ChãoDeCorais` (non-ASCII) and `**VelvetEchoes` (asterisks).
- **Fix**: Broaden regex for Unicode support or sanitize names at generation time.

### N-016: Inconsistent path resolution between gallery and view_band routes
- **File**: `app.py:66-86,95-104`
- **Problem**: Gallery uses `app.root_path`; `view_band()` uses relative path.
- **Fix**: Use `app.root_path` consistently.

### N-019: Generated fan pages use `!important` overrides in responsive styles
- **File**: `createAct.py:624,627,630`
- **Problem**: `!important` in mobile breakpoint is unnecessary -- specificity is already sufficient.
- **Fix**: Remove `!important` from all three declarations.

### N-033: v1 fan pages have no `<h1>` element
- **Files**: 8 of 12 generated pages (EtherealTrampleweed, EucalyptusSaints, Inu-k-trkadeka, MidnightParlor, MyopicSunflowers, NightshadeVanguard, TheLuminescentUndertow, ChãoDeCorais)
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
- **File**: `createAct.py:666` (v2 template); same pattern in all 8 v1 pages

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
- **Files**: 8 of 12 generated pages (EtherealTrampleweed, EucalyptusSaints, Inu-k-trkadeka, MidnightParlor, MyopicSunflowers, NightshadeVanguard, TheLuminescentUndertow, ChãoDeCorais)
- **WCAG**: SC 2.2.2 Pause, Stop, Hide, Level A (mitigated by prefers-reduced-motion)

### N-026: Older generated pages use `<a name="">` anchors instead of `id`
- **Files**: 8 of 12 generated pages; 5 anchors per page x 8 pages = 40 occurrences

### N-027: Older generated pages heading hierarchy issues
- **Files**: Narrowed to legacy pages only; v1 heading issue tracked as N-033
- **Note**: Re-audit confirms legacy pages (EchoesOfTheMirage, MoonlitReverie, etc.) have correct h1 > h2 hierarchy.

### N-029: Legacy-format fan pages have fixed-position footer that occludes content
- **Files**: `EchoesOfTheMirage/home.html`, `MoonlitReverie/home.html`, `TheVelvetEchoes/home.html`, `**VelvetEchoes/home.html`

### N-030: Legacy-format fan pages render empty band members section
- **Files**: `EchoesOfTheMirage/home.html`, `MoonlitReverie/home.html`, `TheVelvetEchoes/home.html`, `**VelvetEchoes/home.html`

### N-032: `band_assets` route does not validate `filename` parameter
- **File**: `app.py:107-112`

### N-034: Legacy fan pages lack `aria-label` on `<nav>` element
- **Files**: `EchoesOfTheMirage/home.html`, `MoonlitReverie/home.html`, `TheVelvetEchoes/home.html`, `**VelvetEchoes/home.html`

### N-035: Legacy fan pages have fixed-width band photo that overflows on narrow viewports
- **Files**: `EchoesOfTheMirage/home.html`, `MoonlitReverie/home.html`, `TheVelvetEchoes/home.html`, `**VelvetEchoes/home.html`
- **WCAG**: SC 1.4.10 Reflow, Level AA
- **Fix**: Change `.band-photo { width: 600px; }` to `.band-photo { width: 100%; max-width: 600px; }`.

### N-036: Focus is not moved to a visible element after resetInterface / cancelGeneration (NEW)
- **File**: `templates/generate.html:471-511`
- **WCAG**: SC 2.4.3 Focus Order, Level A (advisory)
- **Fix**: Focus `#genre1` (or the page's section header) at the end of `resetInterface()`.

---

## Positive Observations

1. **v2 template quality is excellent**: The current `createAct.py` template includes `lang="en"`, viewport meta, skip link, semantic `<header>`/`<main>`/`<footer>`/`<nav>`, correct heading hierarchy (h1 > h2), `focus-visible`, `prefers-reduced-motion`, ARIA labels, XSS escaping via `html.escape()`, and CSS custom properties (`--accent-1/2/3`).
2. **Main app accessibility remains strong**: Skip link, ARIA progressbar with `aria-valuenow` updates, `aria-live` regions, proper focus management on *forward* state transitions (progress/success/error), `focus-visible` on all interactive elements, `prefers-reduced-motion`, scoped table headers, `fieldset`/`legend`, 44x44px touch targets on buttons and dice buttons.
3. **All color contrast ratios pass WCAG AA**: Key pairs re-verified:
   - #ff4444 on #000000 (v1 pages): 6.17:1 -- passes AA
   - #888888 on #000000 (footer text in v2 template): 5.92:1 -- passes AA
   - #cccccc on #000000 (body text): 15.98:1 -- passes AAA
   - #dddddd on #0a0a1a (backstory-box): ~17:1 -- passes AAA
   - `#999999` on `#111111` (badge-row): badge-row has `aria-hidden="true"`, decorative only
4. **Design token system**: CSS custom properties well-organized in `:root` with semantic naming (e.g., `--color-text-primary`, `--space-md`). Consistently used throughout `style.css`.
5. **Error resilience**: Consecutive network error counter (`consecutiveErrors`) with graceful degradation messaging at 3 and 5 errors; timer cleanup in `showError()` prevents leaked intervals.
6. **Security**: CSRF origin/referer checks, per-IP rate limiting, `SAFE_BAND_NAME` regex on routes, XSS escaping on AI output, `html.escape()` on all dynamic content, generation cleanup to prevent memory exhaustion, thread-safe `generation_lock`.
7. **Responsive design**: Three-tier responsive strategy with 640px and 768px breakpoints. Feature grid stacks to column, param labels reflow, tables scale down, touch targets maintained.
8. **Gallery filter (N-028 fix)**: `SAFE_BAND_NAME` check in gallery route correctly prevents dead links from appearing.
9. **All images have alt text**: Verified across all reviewed generated pages and all main app templates.
10. **All pages have lang attribute**: All 12 generated pages and all main templates include `lang="en"`.
11. **Flask app imports cleanly**: Verified `import app` and `import createAct` both succeed (with a dummy `OPENAI_API_KEY` set to bypass the module-level env-var guard at createAct.py:31).
12. **v1 page migrations are consistent**: All 8 v1 pages have identical skip-link markup, `prefers-reduced-motion`, `.faux-link`, and `a:focus-visible` blocks from the N-031 migration. Spot-checked on the rotated subset (EucalyptusSaints, Inu-k-trkadeka, MidnightParlor, TheLuminescentUndertow, ChãoDeCorais) -- all identical.

---

## Metrics

- Total tracked issues: 33 (N-001 through N-036, excluding invalidated N-013)
- Critical: 0 | High: 0 | Medium: 7 | Low: 19
- Resolved cumulative: N-001, N-003, N-021, N-023, N-024, N-028, N-031 (7 total; +0 this cycle)
- Escalated this cycle: none
- New this review: N-036 (Low)
- Previously invalid: N-013 (`json` import is used in gallery route)
- Open medium issues aging: N-002, N-004, N-009, N-012, N-016, N-019 are all 14+ days old; N-033 is 2 days old
- Recommendation: Prioritize **N-033** (missing `<h1>` in v1 pages) as the highest-impact fix. It affects 8 pages and is Level A. The fix (wrap band name in `<h1>`, change section `<h3>` to `<h2>`) would also effectively resolve N-027 for v1 pages and partially address N-025 if `<marquee>` is replaced. After N-033, continue with **N-002** (inline styles -- 3 CSS extractions), **N-019** (`!important` removal -- 3 lines in createAct.py), then **N-036** (single-line focus fix in generate.html), then **N-009** (gallery table responsive).
