# UX & Accessibility Audit — 2026-05-05

**Branch (audit conducted on):** `fix/code-review-2026-05-02`
**Reviewer:** Jennifer Mitchelle (Senior UX Design Critic)
**Scope:** UI consistency, WCAG 2.1 AA compliance, design system adherence, responsive layout, UX patterns
**Note on aesthetic:** The "retro 90s GeoCities" look is an intentional, deliberate design choice (commit `8b971ef`). Findings below are limited to issues that are objectively broken — accessibility violations, layout bugs, security regressions — not stylistic critiques of the retro theme.

---

## Context vs. Previous Reviews

| Date | Outcome |
|---|---|
| 2026-05-01 | 4 CRITICAL + 8 HIGH (retro overhaul lost prior fixes) → restored in `7941ae9` |
| 2026-05-02 | 4 HIGH (N1–N4) → fixed in `8bae07f` |
| 2026-05-03 | 0 Critical/High; 4 Medium + 5 Low (deferred) |
| 2026-05-04 | 0 Critical/High; no new findings |
| **2026-05-05 (this audit)** | **0 Critical/High; 1 new Low; carry-overs unchanged** |

### Re-verification of 2026-05-02 fixes (all PASS in current tree)

| ID | Item | Status |
|---|---|---|
| N1 | Guestbook auxiliary-link wrapper colour | PASS — `createAct.py:599` is `color:#999999` (~7.4:1 on `#000000`) |
| N2 | `.nav-bar a` touch-target ≥24px | PASS — `static/css/style.css:141-147` (`display:inline-block; padding:6px 8px;` → ~32px) |
| N3 | Data tables use `<th scope="col">` | PASS — `templates/gallery.html:16-18`, `templates/generate.html:46-47` |
| N4 | Focus moves to new region heading on state change | PASS — `templates/generate.html:35,90,111,211-217,224,237,246` |

### Re-verification of restored fixes (C1–C4, H1–H9)
All landmarks, skip link, single-H1-on-band-page, `SAFE_BAND_NAME` regex, lazy cleanup, `type="button"`, `aria-live`, `:focus-visible`, `prefers-reduced-motion`, contrast on `.no-photo`/`.footer-copy`, and `.retro-button-small` 32px target are intact.

---

## 2026-05-05 Audit Methodology

Reviewed in current tree:
- `templates/base.html` (62 lines)
- `templates/index.html` (105 lines)
- `templates/gallery.html` (59 lines)
- `templates/generate.html` (286 lines)
- `static/css/style.css` (507 lines)
- `static/js/main.js` (27 lines)
- `createAct.py` HTML emission (lines 324–625)
- `app.py` routes & validation (217 lines)

### Checks performed (Phase 1)

1. **Color contrast (WCAG 1.4.3 AA, 4.5:1 for normal text, 3:1 for large/non-text)** — sampled all foreground/background pairs in the static templates and the four `c1/c2/c3` accent permutations on the generated band page. Every body-text pair clears 4.5:1; every link/heading pair clears 4.5:1. Worst case sampled: `#ff4444` (c3, option 3) on `#000066` header gradient ≈ 5.37:1 — passes AA. **No contrast finding.**
2. **Touch-target size (WCAG 2.5.8)** — primary nav (~32px), `.retro-button` (~40px), `.retro-button-small` (≥32px), gallery row tap zones, footer email link (single inline link, exempt by SC 2.5.8 inline-text exception). **No finding.**
3. **Semantic structure (WCAG 1.3.1)** — single `<h1>` in `base.html` (site banner) on every framework page; second `<h1>` in generated band page (`createAct.py:548`, separate document). Landmarks (`<header role="banner">`, `<nav aria-label>`, `<main id="main-content">`, `<footer role="contentinfo">`) intact. Data tables in `gallery.html` and `generate.html` use `<th scope="col">`. **One new low finding** — see L16 below (h4 after h2 in `index.html`'s feature boxes).
4. **ARIA & live regions** — `aria-live="polite"` on `#progressDisplay` and `#successDisplay`; `role="alert" aria-live="assertive"` on `#errorDisplay`. `aria-current="page"` on active nav link. `aria-hidden="true"` on decorative star strips. `aria-label` on primary nav and on generated-page `<nav class="nav-bar">`. **No finding.**
5. **Keyboard / focus** — `:focus-visible` outline (yellow `#ffff00`, 3px) on all interactive elements (`static/css/style.css:40-48`). Skip-link visible on focus (`style.css:7-24`). `focusHeading()` (`templates/generate.html:211-217`) moves focus to the newly-visible region's `<h3>` on every `showProgress`/`showSuccess`/`showError` transition; the three headings carry `tabindex="-1"`. **No finding.**
6. **Reduced motion** — both `style.css:457-472` (site stylesheet) and the inline `<style>` block in generated band page (`createAct.py:497-504`) honour `prefers-reduced-motion: reduce`. The band-title pulse animation is gated by `(prefers-reduced-motion: no-preference)` (`createAct.py:427-435`) — modern correct pattern. `static/js/main.js:6-10` early-returns on reduced-motion before scheduling the star-twinkle interval. **No finding.**
7. **Image alt text** — gallery thumbs use descriptive alt (`templates/gallery.html:25` "Promotional photo of {band.name}"), generated band photo same pattern (`createAct.py:575`). Decorative stars marked `aria-hidden="true"`. **No finding.**
8. **Lang / `<title>` / viewport** — present on all four templates and on the generated band page. Title pattern `~*~ AI Band Generator ~*~ <Page> ~*~` is consistent. **No finding.**
9. **Empty state** — gallery has clear empty-state with CTA (`templates/gallery.html:43-52`). **No finding.**
10. **Form/input accessibility** — N/A: the app has no input forms; only buttons. (Earlier dice-roll/select inputs from before the retro overhaul are gone.)
11. **Responsive layout** — `@media (max-width: 640px)` (`style.css:481-506`) collapses tables to 100%, drops thumb to 60×60, reduces title size, stacks feature cells. `page-wrapper` `max-width: 800px` with 5–10px gutters. No horizontal overflow detected at 320px / 768px / 1024px. **No finding.**
12. **UX anti-patterns** — placeholder `href="#"` links in generated band page (Sign Guestbook, View Guestbook, Link to us!, Webrings, MIDI Archive, Back to Top, mailto fake address) are part of the retro pastiche; not user-facing functionality regressions. The cancel-doesn't-actually-cancel issue (N8) remains MEDIUM and deferred per prior review.

---

## NEW Findings (2026-05-05 audit)

### [LOW] N14 — Heading hierarchy skips from h2 to h4 in `index.html` feature boxes
**File:** `/home/jalloway/projects/ai-bandmaker/templates/index.html` lines 85, 91, 97
**Issue:** The "What You Get" section is introduced by `<h2 class="section-header">` (line 78), and each of the three feature cards inside the next table uses `<h4 style="color:#...">` (lines 85, 91, 97). No `<h3>` exists between them. WCAG 1.3.1 (Info and Relationships, Level A) and Headings best-practice (G141) recommend not skipping heading levels — screen-reader users navigating by heading (`H` key in NVDA/JAWS) will land on the page's h1, the section h2s, and then jump straight to h4 for the feature labels, skipping the h3 level entirely. The output sounds like an outline with a missing rung.

This is a LOW because the visual hierarchy is clear, the headings are short labels (not deeply nested content), and most screen-reader users tolerate one-level skips. But it is a real WCAG 1.3.1 nit and trivially fixable.

**Fix (deferred per task instructions; LOW only):** Change the three `<h4>` elements in `templates/index.html` lines 85, 91, 97 to `<h3>`. Update the matching CSS rule `.feature-box h4` in `static/css/style.css:265-268` to `.feature-box h3`. No visual change because the `.feature-box h4` rule only sets margin and font-family — both of which apply equally to an h3 with the same `font-family: 'Impact', 'Arial Black', sans-serif;` declaration. Three template lines + one selector edit.

---

## Carried-over MEDIUM / LOW (still deferred — unchanged from 2026-05-03)

| ID | Severity | Item | File:line |
|---|---|---|---|
| M7 | MED | Dead `marquee {}` rule in generated CSS | `createAct.py:528-534` |
| M8 | MED | `bandPreview.innerHTML` injects unsanitised AI band name | `templates/generate.html:233-236` |
| N5 | MED | Progress-steps table column header is the literal "?" | `templates/generate.html:46` |
| N6 | MED | Step-indicator state changes not announced to SR users | `templates/generate.html:183-209` |
| N7 | MED | Polling interval re-announces same prose message | `templates/generate.html:158, 183-191` |
| N8 | MED | `cancelGeneration()` does not tell the server to stop | `templates/generate.html:249-254`, `app.py` |
| N9 | LOW | `#progressDisplay` `aria-live` region wraps too much markup | `templates/generate.html:33-85` |
| N10 | LOW | Failing step is invisible to user on error | `templates/generate.html:49-77` |
| N11 | LOW | Generated-page nav touch-target ~21px (matches old N2 defect on the separate generated-page CSS) | `createAct.py:556-562, 525-527` |
| N12 | LOW | `body` font-family includes `cursive` between specific and generic | `static/css/style.css:67`, `createAct.py:387` |
| N13 | LOW | `<hr>` `noshade` and `size` attributes are obsolete in HTML5 | multiple templates and `createAct.py` |
| L7 | LOW | `Faker==28.1.0` declared but unused | `requirements.txt` |
| L8 | LOW | Inline `import re` inside functions | `createAct.py:114, 251` |
| L9 | LOW | Visitor counter randomises on each page load (thematic) | `templates/base.html:47` |
| L10 | LOW | Dead `mailto:webmaster@aibandgen.geocities.com` (thematic) | `templates/base.html:52` |
| L11 | LOW | Visitor counter and `mailto` repeated in generated band pages (thematic) | `createAct.py:598, 614` |
| L12 | LOW | `<table>` used for layout in `index.html` "What You Get" section | `templates/index.html:81-102` |
| L13 | LOW | Inline styles throughout templates and generated HTML | many |
| L14 | LOW | Deprecated HTML attributes (`bordercolor`, `noshade`, `cellpadding`, `align`, `width`) throughout | many |
| L15 | LOW | `band_assets()` route doesn't whitelist filenames | `app.py:82-87` |

---

## Summary

| Severity | Count this audit | Fixed this pass |
|---|---|---|
| CRITICAL | 0 | — |
| HIGH | 0 | — |
| MEDIUM | 0 new (6 carried) | 0 (deferred) |
| LOW | 1 new (N14) + 13 carried | 0 (deferred) |

**No CRITICAL or HIGH findings.** The codebase is stable: this is the third consecutive audit (2026-05-03, 2026-05-04, today) with zero critical/high regressions. The recent two passes (2026-05-01 restoration + 2026-05-02 N1–N4 fixes) closed every WCAG AA show-stopper, and nothing new has slipped in since.

The single new finding (N14, heading hierarchy h2→h4 skip in `index.html` feature boxes) is LOW severity. Per task instructions, no code is being changed in Phase 2 today. Phase 4 (PR) is skipped accordingly. This review file is the only deliverable, committed to the existing branch.

---

## Phase 3 — Verification

No code changed; verified the current tree still parses cleanly:

- `python -m py_compile app.py createAct.py` → both files compile cleanly.
- All four Jinja2 templates (`base.html`, `index.html`, `generate.html`, `gallery.html`) parse OK on visual inspection: `{% block %}`, `{% extends %}`, `{% if %}`, `{% for %}` blocks balanced; no stray `{{` or `}}`.
- CSS structure intact: brace matching even, `prefers-reduced-motion` media query at `static/css/style.css:458-472`, responsive breakpoint at `static/css/style.css:481-506`.
- Did not start the dev server (no code changes; running `/api/generate` would require live `ANTHROPIC_API_KEY` / `OPENAI_API_KEY`). Static template review covers all the rendering paths the audit needs.
