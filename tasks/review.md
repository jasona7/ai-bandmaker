# UX & Accessibility Audit — 2026-05-02

**Branch:** `fix/code-review-2026-05-01` (audit re-run; new fix branch will be `fix/code-review-2026-05-02`)
**Reviewer:** Jennifer Mitchelle (Senior UX Design Critic)
**Scope:** UI consistency, WCAG 2.1 AA compliance, design system adherence, responsive layout, UX patterns
**Note on aesthetic:** The "retro 90s GeoCities" look is an intentional, deliberate design choice (commit `8b971ef`). Findings below are limited to issues that are objectively broken — accessibility violations, layout bugs, security regressions — not stylistic critiques of the retro theme.

---

## Context vs. Previous Review (2026-05-01)

The 2026-05-01 audit (preserved in git history of this file) found 4 CRITICAL and 8 actionable HIGH issues caused by the retro-90s overhaul (`8b971ef`) discarding earlier accessibility/security fixes. Commit `7941ae9` ("Restore accessibility, security & UX fixes lost in retro overhaul") restored them.

**Verification of yesterday's fixes (all PASS):**

| ID | Item | Status |
|---|---|---|
| C1 | Semantic landmarks (`<header>/<nav>/<main>/<footer>`) | PRESENT — `templates/base.html:17,27,34,39` |
| C2 | Skip-to-content link | PRESENT — `templates/base.html:12` + CSS `static/css/style.css:7-24` |
| C3 | `<marquee>` removed from generated band page | REMOVED — `createAct.py:548` now uses `<h1 class="band-title">` |
| C4 | `<h1>` on generated band page; section headers `<h2>` | FIXED — `createAct.py:548,565,572,582,589,594` |
| H1 | `SAFE_BAND_NAME` regex on `view_band` and `band_assets` | RESTORED — `app.py:21,73-74,85-86` |
| H2 | `cleanup_old_generations()` lazy pruning | RESTORED — `app.py:27-38, 95` |
| H3 | `type="button"` on all five `<button>` elements | RESTORED — `templates/generate.html:26,80,97,101,113` |
| H4 | `aria-live` on dynamic regions | RESTORED — `templates/generate.html:33,88,109` |
| H6 | `:focus-visible` on interactive elements | PRESENT — `static/css/style.css:40-48` |
| H7 | Animations gated behind `prefers-reduced-motion` | PRESENT — `static/css/style.css:449-464`, `static/js/main.js:6-10` |
| H8 | Contrast on placeholder/footer | FIXED — `.no-photo` and `.footer-copy` now `#9999bb` (~7:1) |
| H9 | Touch targets ≥24x24 on `.retro-button-small` | FIXED — `min-height: 32px` + `padding: 8px 16px` |

The yesterday's pass is intact. This audit catches additional issues that survived (or were missed by) yesterday's pass.

---

## NEW Findings (2026-05-02 audit)

### [HIGH] N1 — Color contrast failure on guestbook auxiliary links wrapper in generated band page
**File:** `/home/jalloway/projects/ai-bandmaker/createAct.py` line 599
**Issue:** `<p style="color:#666666; font-size:0.8em;">` wraps the small "Link to us! | Webrings | MIDI Archive" links on every generated band page. The wrapper text is set on the page's `#000000` body background. Computed contrast: **3.66:1** — fails WCAG 1.4.3 (Contrast (Minimum), Level AA, requires 4.5:1 for normal text). The 0.8em text is ~11px, which is well below the "large text" threshold. The pipe separators ("|") between the links use this color and are effectively invisible to low-vision users.
**Fix:** Bump the wrapper color to `#999999` (computes 7.37:1 on black) or `#aaaaaa` (8.84:1). The pattern matches the colors used elsewhere on the same generated page, so this is a one-character edit.

### [HIGH] N2 — Top-level navigation links fail WCAG 2.5.8 minimum target size
**File:** `/home/jalloway/projects/ai-bandmaker/static/css/style.css` lines 138-145
**Issue:** `.nav-bar a` declares `margin: 0 3px` and inherits `font-size: 0.95em` (~13.3px). Effective click/touch target height is roughly the line-height box (~20-22px). WCAG 2.5.8 (Target Size (Minimum), Level AA) requires non-inline interactive targets to be at least 24×24 CSS pixels (with documented exceptions). Mobile users with motor impairments will struggle to tap accurately, especially since the three nav links sit on a single line separated only by literal `|` characters.
**Fix:** Add vertical padding to the nav links to bring the touch target above 24px. Smallest surgical edit: `padding: 6px 8px; display: inline-block;` on `.nav-bar a`. This raises height to ~32px and gives each link its own discrete target zone.

### [HIGH] N3 — Data tables use `<td>` for header rows instead of `<th scope="col">`
**Files:**
- `/home/jalloway/projects/ai-bandmaker/templates/gallery.html` lines 15-19
- `/home/jalloway/projects/ai-bandmaker/templates/generate.html` lines 45-48 (progress-steps table)

**Issue:** Both data tables have a "header row" styled visually but constructed entirely with `<td>` elements wrapped in `<strong>`. Screen readers will not associate these as column headers. When navigating the gallery table cell-by-cell (NVDA's `Ctrl+Alt+Arrow`, JAWS table navigation), the user gets no spoken context like "Photo: [thumbnail of Velvet Echoes]" or "Band Name: Velvet Echoes". Violates WCAG 1.3.1 (Info and Relationships, Level A). The `info-table` in `index.html` and the "What You Get" three-column table are layout tables (already flagged as M4); this finding is for the genuine data tables only.
**Fix:** Replace the `<td><strong>X</strong></td>` cells in the header rows of `gallery.html` and `generate.html` with `<th scope="col">X</th>`. This is also one of the items the previous (`tasks/review-recheck.md`) review confirmed had been added before the retro overhaul wiped it out.

### [HIGH] N4 — Dynamic-state changes do not move focus, causing keyboard users to lose orientation
**File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html` lines 211-236
**Issue:** When `showProgress()`, `showSuccess()`, or `showError()` swap the visible region, focus remains on the now-hidden trigger button. For keyboard users, pressing Tab next focuses an element far from the new content; for screen-reader users, although the `aria-live` polite announcement plays, they cannot easily reach the new buttons (`viewBandBtn`, `retryBtn`, `cancelBtn`) without traversing the whole page. WCAG 2.4.3 (Focus Order) and 3.2.4 (Consistent Identification) implications. Best-practice for SPA-like state transitions: move focus to the new region's heading.
**Fix:** Each show* function should programmatically focus the heading (or a `tabindex="-1"` wrapper) of the newly-visible region. Add `tabindex="-1"` to the three section heading elements (`progressTitle`, the success `<h3>`, and the error `<h3>`) and call `.focus()` on them inside the corresponding show function.

### [MEDIUM] M7 — Dead `marquee {}` CSS rule remains in generated band page CSS
**File:** `/home/jalloway/projects/ai-bandmaker/createAct.py` lines 528-534
**Issue:** The generated band page's `<style>` block still declares a rule for the `marquee` element even though the marquee was removed in commit `7941ae9` (band name is now `<h1>`). Cosmetic dead code; no functional impact; deferred since it doesn't break anything.
**Fix (deferred):** Remove the `marquee { ... }` block.

### [MEDIUM] M8 — `bandPreview.innerHTML` injects unsanitised AI-generated band name
**File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html` lines 224-227
**Issue:** `preview.innerHTML = '<p ...>~*~ ' + (data.band_name || 'Your Band') + ' ~*~</p>...'` interpolates the band name returned from the status API directly into innerHTML. The band name comes from a ChatGPT response and is therefore not strictly user-controlled, but a creative model output containing `<script>` or HTML markup would be executed. Defense-in-depth recommendation: use textContent on a child element instead of innerHTML on the parent.
**Fix (deferred):** Build the preview using DOM APIs (`document.createElement`, `el.textContent = data.band_name`).

### [MEDIUM] M9 — `import json` still unused in `app.py`
**File:** `/home/jalloway/projects/ai-bandmaker/app.py` line 2 (note: line shifted since prior review)
**Issue:** Wait — checking current state, `import json` is no longer present in app.py (the retro overhaul cleaned this). **No action — already resolved.**

### [LOW] L7 — `Faker==28.1.0` declared but unused (carried over from L4)
**File:** `/home/jalloway/projects/ai-bandmaker/requirements.txt`
**Fix (deferred):** Remove from requirements.

### [LOW] L8 — Inline `import re` inside functions in `createAct.py` (carried over from L3)
**File:** `/home/jalloway/projects/ai-bandmaker/createAct.py` lines 85, 218
**Fix (deferred):** Move to module-level import.

### [LOW] L9 — Visitor counter randomises on every page load (carried over from M5)
**File:** `/home/jalloway/projects/ai-bandmaker/templates/base.html` line 47
**Fix (deferred):** Pure cosmetic 90s joke; not a real defect.

### [LOW] L10 — `mailto:webmaster@aibandgen.geocities.com` is a dead address (carried over from M6)
**File:** `/home/jalloway/projects/ai-bandmaker/templates/base.html` line 52
**Fix (deferred):** Cosmetic / thematic; not a real defect.

### [LOW] L11 — Visitor counter and `mailto` repeated in generated band pages
**File:** `/home/jalloway/projects/ai-bandmaker/createAct.py` lines 598, 614
**Fix (deferred):** Same as above — thematic.

### [LOW] L12 — `<table>` used for layout in `index.html` "What You Get" section (carried over from M4)
**File:** `/home/jalloway/projects/ai-bandmaker/templates/index.html` lines 81-102
**Fix (deferred):** Replace with CSS grid of `<div>` cards.

### [LOW] L13 — Inline styles throughout templates and generated HTML (carried over from M2)
**Fix (deferred):** Extract repeated inline styles to utility classes; will conflict with CSP if added later.

### [LOW] L14 — Deprecated HTML attributes (`bordercolor`, `noshade`, `cellpadding`, `align=`, `width=`) throughout (carried over from M1)
**Fix (deferred):** Migrate to CSS-driven equivalents while preserving the visual look.

### [LOW] L15 — `band_assets()` route doesn't whitelist filenames (carried over from M3)
**File:** `/home/jalloway/projects/ai-bandmaker/app.py` lines 82-87
**Fix (deferred):** Whitelist `home.html` and `band_photo.jpg` (and any future known assets) for defense-in-depth.

---

## Phase 2 plan

Fix N1, N2, N3, N4 (one HIGH-severity contrast issue, one HIGH-severity touch-target issue, one HIGH-severity table-semantics issue, one HIGH-severity focus-management issue). Skip MEDIUM/LOW per task instructions.

---

## Summary

| Severity | Count | Fixed in this pass |
|---|---|---|
| CRITICAL | 0 | — |
| HIGH | 4 (N1–N4) | 4 |
| MEDIUM | 2 (M7, M8) | 0 (deferred) |
| LOW | 9 (L7–L15) | 0 (deferred) |

No CRITICAL issues. The yesterday's pass closed all the show-stoppers; today's pass finds four HIGH-severity issues that were not in scope yesterday (or were simply missed): one numeric contrast failure on the generated band page, one touch-target failure on the global nav, one data-table semantics regression, and one focus-management gap on the generate flow.

---

# UX & Accessibility Audit — 2026-05-04

**Branch:** `fix/code-review-2026-05-02` (audit re-run; audit-only commit on this branch since no Critical/High found)
**Reviewer:** Jennifer Mitchelle (Senior UX Design Critic)
**Scope:** UI consistency, WCAG 2.1 AA compliance, design system adherence, responsive layout, UX patterns

## Verification of prior fixes (2026-05-02 audit, N1–N4)

| ID | Item | Status |
|---|---|---|
| N1 | Generated band-page guestbook auxiliary-link wrapper bumped from `#666666` to `#999999` (~7.4:1 on `#000000`) | PASS — `createAct.py:599` now `color:#999999` |
| N2 | `.nav-bar a` padded to give ≥24px touch target | PASS — `static/css/style.css:143-145` (`display: inline-block; padding: 6px 8px;` → ~32px height) |
| N3 | `<th scope="col">` on data tables in gallery and progress-steps | PASS — `templates/gallery.html:16-18` and `templates/generate.html:46-47` |
| N4 | Focus moves to new region heading on state transitions | PASS — `templates/generate.html:211-217` (`focusHeading()`) called from `showProgress`, `showSuccess`, `showError` (lines 224, 237, 246); `tabindex="-1"` present on all three section `<h3>` headings (lines 35, 90, 111) |

All four 2026-05-02 fixes are intact in current source.

## NEW Findings (2026-05-04 audit)

### Methodology
Reviewed: `templates/base.html`, `templates/index.html`, `templates/gallery.html`, `templates/generate.html`, `static/css/style.css`, `static/js/main.js`, `createAct.py` (HTML emission, lines 324–625), `app.py` (routes & validation).

Checks performed:
1. **Color contrast (WCAG 1.4.3)** — sampled all foreground/background pairs across base templates and generated band page. Primary body text (`#cccccc` on `#000022` ≈ 11.7:1, `#cccccc` on `#000000` ≈ 12.6:1). Footer text `#888888` on `#000000` ≈ 5.36:1, badge `#999999` on `#111111` ≈ 6.5:1, intro text `#dddddd` on `#0a0a1a` ≈ 13.5:1, `.no-photo` `#9999bb` on `#0a0a1a` ≈ 7.6:1, `.feature-box p` `#aaaaaa` on `#0a0a2a` ≈ 8.7:1, footer-copy `#9999bb` ≈ 7.6:1. All accent c1/c2/c3 swatches verified ≥ 4.5:1 on `#000000`. No new contrast violations.
2. **Touch-target size (WCAG 2.5.8)** — primary nav (~32px), `.retro-button` (~40px), `.retro-button-small` (≥32px), gallery row tap zones — all PASS.
3. **Semantic structure (WCAG 1.3.1)** — H1 site-title in `base.html` (line 19), single-H1-per-page rule preserved on generated band page (`<h1 class="band-title">` line 548). Gallery and progress tables use `<th scope="col">`. Landmarks (`<header role="banner">`, `<nav aria-label>`, `<main>`, `<footer role="contentinfo">`) intact.
4. **ARIA & live regions** — `aria-live="polite"` on progress/success, `role="alert" aria-live="assertive"` on error. `aria-current="page"` on active nav link. `aria-hidden="true"` on decorative star strips. PASS.
5. **Keyboard / focus** — skip-link visible on focus (`style.css:19-24`), `:focus-visible` outline on interactive elements (`style.css:40-48`), `focusHeading()` moves focus on state transitions. PASS.
6. **Reduced motion** — both `style.css:457-472` and the generated band page's inline `<style>` (`createAct.py:497-504`) honor `prefers-reduced-motion: reduce`. The band-title pulse animation is gated on `(prefers-reduced-motion: no-preference)` (`createAct.py:427-435`) — modern correct pattern. `static/js/main.js:6-10` early-returns on reduced-motion. PASS.
7. **Image alt text** — gallery thumbs and generated band photo both have descriptive alt. PASS.
8. **Lang attribute / `<title>` / viewport** — present on all four templates and on the generated band page. PASS.
9. **Empty state** — gallery has clear empty-state with CTA (`templates/gallery.html:43-52`). PASS.
10. **Form/input accessibility** — N/A (the app has no input forms; only buttons).

### Result

**No Critical, High, Medium, or Low findings new to today.** The carry-over Medium and Low items from the 2026-05-02 audit (M7 dead `marquee` CSS rule, M8 `bandPreview.innerHTML` interpolation, L7 unused `Faker` dep, L8 inline `import re`, L9–L11 thematic 90s artifacts, L12 layout table on index "What You Get", L13 inline styles, L14 deprecated HTML attributes, L15 `band_assets` whitelist) remain explicitly deferred as already noted; their status is unchanged. None rise to High under the project's stated retro-90s aesthetic exception.

## Summary

| Severity | Count | Fixed in this pass |
|---|---|---|
| CRITICAL | 0 | — |
| HIGH | 0 | — |
| MEDIUM | 0 new (2 carried) | 0 (deferred) |
| LOW | 0 new (9 carried) | 0 (deferred) |

Per task instructions: no Critical/High → no fix branch, no PR. Audit findings appended to this review file and committed on the current branch (`fix/code-review-2026-05-02`).

## Phase 3 verification evidence

- `python -c "import ast; ast.parse(open('app.py').read()); ast.parse(open('createAct.py').read())"` → `OK app.py and createAct.py parse`
- Jinja2 template compile-check across all four templates (`base.html`, `index.html`, `gallery.html`, `generate.html`) → all OK.

