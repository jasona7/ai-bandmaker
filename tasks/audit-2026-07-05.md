# UX / Accessibility / Design-System Audit — 2026-07-05

**Reviewer:** Jennifer Mitchelle (Senior UX Design Critic)
**Branch:** `fix/code-review-2026-05-11`
**Scope:** `templates/base.html`, `templates/index.html`, `templates/generate.html`, `templates/gallery.html`, `static/css/style.css`, `static/js/main.js`
**Note:** The 1996 GeoCities aesthetic (blink text, "under construction", visitor counter, table layouts, neon palette) is intentional and is NOT flagged. Findings below are genuine user-impacting or maintainability issues only.

## Summary of counts

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH | 0 |
| MEDIUM | 2 |
| LOW | 6 |

Overall the code is genuinely clean. Contrast on all essential body and interactive text passes WCAG AA by a wide margin (body `#cccccc` on `#000022` ≈ 12.8:1; nav links `#00ff00` on `#111122` ≈ 13.7:1; magenta table headers `#ff00ff` on `#1a1a3a` ≈ 5.4:1; hot-pink footer link `#ff69b4` on `#000022` ≈ 7.7:1; progress percent `#ff00ff` on `#0a0a2a` ≈ 6.1:1). Skip link, focus-visible indicators, `prefers-reduced-motion` handling, aria-current, aria-labels, informative-image alt text, and focus management on dynamic state transitions are all present and correct. No forms/inputs exist, so there are no label violations. No keyboard traps, no destructive actions, no missing error states.

---

## CRITICAL

**None.**

## HIGH

**None.**

---

## MEDIUM

### M1 — Heading hierarchy skips from h2 to h4
**File:** `templates/index.html` lines 85, 91, 97 (feature-box `<h4>` under the `<h2>` "~ What You Get ~" at line 78)
**Problem:** The document goes `h1` (site title) → `h2` (section headers) → `h4` (feature boxes) with no intervening `h3`. Screen-reader users navigating by heading level encounter a broken outline and may assume content is missing.
**WCAG:** 1.3.1 Info and Relationships (A).
**Fix:** Change the three feature-box headings from `<h4 style="...">` to `<h3 class="feature-heading">` (move the inline color to a class if desired). No visual change is required — style the new `h3` to match the current h4 sizing.

### M2 — `aria-live` region scope is too broad; screen readers announce cryptic ASCII on every poll
**File:** `templates/generate.html` line 33 (`<div id="progressDisplay" ... aria-live="polite">`) wrapping the ASCII bar (lines 39-42) and the step table (lines 44-77); driven by `updateProgress()` in the inline script (lines 183-209), polled every 1.5 s.
**Problem:** Because the whole progress panel is a polite live region and its ASCII decorations mutate every 1.5 s, assistive tech re-announces the changed nodes each poll — the fill string (`====`), the empty string (`----`), and step indicators toggling `...` → `[>]` → `[X]`. That produces noisy, meaningless announcements ("equals equals equals", "bracket X bracket") instead of a clear status.
**WCAG:** 4.1.3 Status Messages (AA) / 1.3.1 (announcements do not convey meaning).
**Fix:** Mark the decorative ASCII/indicator nodes `aria-hidden="true"` (the `.ascii-progress` block and each `.step-indicator` cell), and move the human-readable status into a single dedicated `sr-only` polite live region that announces only `progressMessage` + percent (e.g. "Writing backstory, 35%"). Keep `#progressMessage` visible but let one concise live region carry the spoken update.

---

## LOW

### L1 — Pending step indicator has sub-AA contrast (decorative placeholder)
**File:** `static/css/style.css` line 369 (`.step-row .step-indicator { color: #666666; }`) on table bg `#0a0a1a`.
**Problem:** `#666666` on `#0a0a1a` ≈ **3.4:1**, below the 4.5:1 AA threshold for normal text. Impact is limited: the glyph is only the `...` "pending" placeholder, the adjacent step label is readable `#cccccc`, and active states switch to bright green/yellow.
**WCAG:** 1.4.3 (borderline; non-essential text).
**Fix:** Lift the pending color to about `#8a8a99` (≈ 4.7:1) to clear AA without changing the retro feel.

### L2 — Empty ASCII progress dashes fail contrast (decorative)
**File:** `templates/generate.html` line 40 (`<span id="progressBarEmpty" style="color:#333333;">`) on retro-box `#0a0a2a`.
**Problem:** `#333333` on `#0a0a2a` ≈ **1.5:1**. This is the unfilled remainder of the bar; the essential progress value is conveyed by the `#ff00ff` percent text (passes) and `#00ff00` fill, so real impact is minimal.
**WCAG:** 1.4.3 (non-essential decoration).
**Fix:** Raise the empty-segment color to ~`#777777`, or (preferred) `aria-hidden` the whole bar per M2 and treat it as pure decoration.

### L3 — No CSS custom properties; neon palette repeated as magic values
**File:** `static/css/style.css` throughout (e.g. `#00ffff`, `#ff00ff`, `#0a0a2a`, `#0a0a1a`, `#333366` each appear many times) plus numerous inline `style="color:#..."` in templates.
**Problem:** Design-system maintainability, not user-facing. Palette changes require hunting duplicated hex literals across CSS and inline styles.
**Fix:** Define tokens in `:root` (e.g. `--neon-cyan`, `--neon-magenta`, `--panel-bg`) and reference them; migrate inline color styles to utility classes over time.

### L4 — Inconsistent button font-family stacks
**File:** `static/css/style.css` line 282 (`.retro-button`: `'Comic Sans MS','Trebuchet MS',cursive,sans-serif`) vs line 312 (`.retro-button-small`: `'Comic Sans MS', cursive`).
**Problem:** Component inconsistency; the small button lacks the same fallback chain, so rendering can diverge where Comic Sans is unavailable.
**Fix:** Share one font stack (a variable per L3) across both button classes.

### L5 — Inline styles scattered across templates reduce consistency
**File:** `templates/index.html` (lines 16, 35-62, 66-70, 81-99), `templates/generate.html` (lines 15-16, 33, 35-41, 79, 88-111), `templates/gallery.html` (lines 22, 30-36).
**Problem:** Repeated inline color/spacing/font-size values make the button/spacing system harder to keep consistent and are easy to drift. Not user-harming today.
**Fix:** Promote recurring inline patterns (table-cell number styling, section spacing, heading colors) to classes.

### L6 — Motion is pausable only via OS `prefers-reduced-motion` (acceptable mitigation — noted for completeness)
**File:** `static/css/style.css` lines 448-472 (`.blink` + reduced-motion block); `static/js/main.js` lines 12-25 (star twinkle `setInterval`).
**Problem:** The footer `.blink` and the JS star twinkle run indefinitely (> 5 s, in parallel with content) with no on-page pause control; the only stop mechanism is the OS reduced-motion preference. Both animations are on decorative / `aria-hidden` content, blink frequency (~0.83 Hz) is well under the 3 Hz seizure threshold, and neither wraps essential content — so this is broadly compliant.
**WCAG:** 2.2.2 Pause, Stop, Hide (A) — `prefers-reduced-motion` is a widely accepted mitigation; 2.3.1 Three Flashes passes.
**Fix:** None required. Optional enhancement: an on-page "stop animations" toggle for users who cannot set an OS preference.

---

## Positive observations (verified, not issues)

- Skip link (`base.html` line 12) is correctly offscreen and reveals on `:focus` with a visible outline (style.css 7-24).
- Every informative image has meaningful alt text (`gallery.html` line 25); the no-photo case uses readable text, not an empty image.
- `aria-current="page"` on the active nav item (base.html 28-30); `aria-hidden` on decorative star rows.
- Dynamic state transitions move focus to the new region heading (`focusHeading()` in generate.html 211-247) — correct focus management, no focus loss.
- Error state exists with `role="alert"` + assertive live region (generate.html 109-117); appropriate, not a double-announcement problem in practice.
- Responsive: `max-width` wrapper, tables reflow to 100% width and feature cells stack (`display:block`) at ≤640px; viewport meta present; no fixed pixel widths that force horizontal scroll at 320px.
- Touch targets meet WCAG 2.5.8 (24×24 CSS px): `.retro-button` ≈ 38px tall, `.retro-button-small` `min-height:32px`, nav links ≈ 27-30px.
