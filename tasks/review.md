# UX & Accessibility Audit -- AI Band Generator
**Date:** 2026-04-04
**Reviewer:** Jennifer Mitchelle (UX Design Critic)

**Files reviewed:**
- `/home/jalloway/projects/ai-bandmaker/templates/base.html`
- `/home/jalloway/projects/ai-bandmaker/templates/index.html`
- `/home/jalloway/projects/ai-bandmaker/templates/generate.html`
- `/home/jalloway/projects/ai-bandmaker/templates/gallery.html`
- `/home/jalloway/projects/ai-bandmaker/static/css/style.css`
- `/home/jalloway/projects/ai-bandmaker/static/js/main.js`
- `/home/jalloway/projects/ai-bandmaker/app.py`
- `/home/jalloway/projects/ai-bandmaker/createAct.py` (generated fan page HTML)

---

## Summary

This retro 90s-themed Flask application is an AI-powered band generator with a strong visual identity and a solid accessibility foundation. The developer has already implemented many best practices: a skip-link, semantic `<nav>` with `aria-label`, `aria-current="page"` on active links, `aria-live` regions, `scope="col"` table headers, labelled form controls with `<fieldset>`/`<legend>`, `prefers-reduced-motion` support on the blink animation, `focus-visible` outlines on interactive elements, and a well-structured CSS custom property system. Touch targets on dice buttons meet the 44x44px WCAG 2.5.5 minimum. Path validation on band routes prevents directory traversal.

However, several critical issues remain. The generated fan pages (produced by `createAct.py` and served as static HTML) are the largest risk area: they interpolate AI-generated strings without HTML escaping (stored XSS), lack skip links and `<main>` landmarks, use deprecated `<marquee>`, and have no `prefers-reduced-motion` support. In the main application, colour contrast failures on muted text, an inaccessible progress bar, and unmanaged focus during view transitions are the top concerns.

This audit identified **41 issues**: 7 Critical, 20 High, 13 Medium, and 1 Low.

---

## Critical Issues (must fix)

### C-001 -- XSS vulnerability in generated fan page HTML
- **File:** `/home/jalloway/projects/ai-bandmaker/createAct.py`, lines 357-633
- **Category:** UX / Security
- **Description:** The `create_html_content()` function interpolates AI-generated strings directly into HTML via f-strings with no escaping. `{band_name}` appears in `<title>`, `<marquee>`, headings, and `mailto:` links. `{backstory}` is injected into a `<div>`. `{member.get('name')}` and `{member.get('bio')}` go into table cells. Track names flow through `{tracks_html}`. If the AI generates content containing `<script>`, `onclick`, or other HTML constructs, they render as executable markup. This is a stored XSS vector.
- **Fix:** Apply `html.escape()` to all interpolated strings. Better yet, serve generated bands through a Flask route that renders a shared Jinja2 template (which auto-escapes), reading band data from a JSON sidecar file. This would also fix C-004, C-005, C-006, and C-007 below.

### C-002 -- Colour contrast failures on muted text (WCAG 1.4.3)
- **File:** `/home/jalloway/projects/ai-bandmaker/static/css/style.css`, lines 13, 316, 431-434, 466, 604-606, 622-624
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html`, line 190 (inline style)
- **Category:** Accessibility
- **Description:** Multiple text/background combinations fail the 4.5:1 minimum contrast ratio:

  | Element | Foreground | Background | Approx. Ratio | Verdict |
  |---|---|---|---|---|
  | `.badge` text | `#999999` | `#111111` | ~4.0:1 | **Fail** |
  | `.step-indicator` (default) | `#999999` | `#0a0a1a` | ~4.3:1 | **Fail** |
  | `.gallery-no-photo` | `#999999` | `#0a0a1a` | ~4.3:1 | **Fail** |
  | `.feature-box p` | `#aaaaaa` | `#0a0a2a` | ~4.2:1 | **Fail** |
  | Progress bar empty dashes | `#333333` (inline) | `#0a0a2a` | ~1.5:1 | **Fail** |

  The progress bar empty dashes at `#333333` are essentially invisible against the dark surface.
- **Fix:** Raise `--color-text-muted` to `#b0b0b0` (~6.0:1 against `#0a0a1a`). Raise `.feature-box p` colour to `#bbbbbb`. Change progress bar empty dash colour from `#333333` to `#666688` and extract to a CSS class using a design token.

### C-003 -- Progress bar has no accessible semantics (WCAG 1.3.1, 4.1.3)
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html`, lines 188-192
- **Category:** Accessibility
- **Description:** The ASCII progress bar is built from `=` and `-` characters inside `<span>` elements with no ARIA role. Screen readers announce literal strings of equals signs and dashes. There is no `role="progressbar"`, no `aria-valuenow`, `aria-valuemin`, or `aria-valuemax`. The `#progressMessage` has `aria-live="polite"` which helps, but the bar itself is invisible to assistive technology.
- **Fix:** Add ARIA progressbar semantics to the container and update dynamically:
  ```html
  <div class="ascii-progress" role="progressbar" aria-valuenow="0"
       aria-valuemin="0" aria-valuemax="100" aria-label="Band generation progress">
  ```
  In `updateProgress()`:
  ```js
  document.querySelector('.ascii-progress').setAttribute('aria-valuenow', pct);
  ```

### C-004 -- Generated fan pages lack skip link and main landmark (WCAG 2.4.1)
- **File:** `/home/jalloway/projects/ai-bandmaker/createAct.py`, lines 539-633
- **Category:** Accessibility
- **Description:** Generated band fan pages have no skip-to-content link and no `<main>` element. Keyboard and screen reader users must tab through the header and navigation on every page load.
- **Fix:** Add `<a href="#main" class="skip-link">Skip to main content</a>` after `<body>` and wrap the content area in `<main id="main">`.

### C-005 -- Generated fan pages use deprecated `<marquee>` element (WCAG 2.2.2)
- **File:** `/home/jalloway/projects/ai-bandmaker/createAct.py`, line 547
- **Category:** Accessibility
- **Description:** The `<marquee>` element produces continuously scrolling text that users cannot pause, stop, or hide. This violates WCAG 2.2.2 (Pause, Stop, Hide). Screen readers may read the text multiple times or skip it entirely.
- **Fix:** Replace with a static heading. If the retro aesthetic demands motion, use a CSS animation with a visible pause control and `prefers-reduced-motion: reduce` support.

### C-006 -- Generated fan pages missing `prefers-reduced-motion` for blink animation (WCAG 2.3.1)
- **File:** `/home/jalloway/projects/ai-bandmaker/createAct.py`, lines 497-502
- **Category:** Accessibility
- **Description:** The main app CSS (style.css line 640) correctly disables the blink animation for `prefers-reduced-motion`. The generated fan pages define their own `.blink` animation at line 498 without this media query. Users with vestibular disorders or photosensitive epilepsy are at risk.
- **Fix:** Add `@media (prefers-reduced-motion: reduce) { .blink { animation: none; } }` to the generated page styles.

### C-007 -- Focus is not managed during view transitions
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html`, lines 402-433 (showProgress, showSuccess, showError functions)
- **Category:** Accessibility
- **Description:** When the user clicks "Generate Band", the start panel hides and the progress panel shows via `display:none`/`display:block` toggling. Focus remains on the now-hidden generate button. Screen reader and keyboard users are stranded in a hidden DOM region. The same problem occurs on transitions to success and error states. This violates WCAG 2.4.3 (Focus Order).
- **Fix:** After each view transition, move focus to the heading of the newly visible section. Add `tabindex="-1"` to each target heading so it can receive programmatic focus:
  ```js
  function showProgress() {
      // ... existing display toggles ...
      document.getElementById('progressTitle').focus();
  }
  function showSuccess(data) {
      // ... existing display toggles ...
      document.querySelector('#successDisplay h3').focus();
  }
  function showError(message) {
      // ... existing display toggles ...
      document.querySelector('#errorDisplay h3').focus();
  }
  ```

---

## High Issues (should fix)

### H-001 -- Inline JS colour assignments bypass design tokens (WCAG 1.4.3)
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html`, lines 392-397
- **Category:** Accessibility / Code Quality
- **Description:** Step indicator colours are set via `indicator.style.color = '#00ff00'` and `indicator.style.color = '#ffff00'`, bypassing the CSS custom property system. If tokens are updated for contrast compliance, these inline values will not follow.
- **Fix:** Replace with CSS class toggling:
  ```css
  .step-indicator--active { color: var(--color-accent-yellow); }
  .step-indicator--complete { color: var(--color-accent-green); }
  ```
  ```js
  indicator.classList.remove('step-indicator--active', 'step-indicator--complete');
  indicator.classList.add(pct >= (thresholds[i + 1] || 100) ? 'step-indicator--complete' : 'step-indicator--active');
  ```

### H-002 -- Cancel button does not stop server-side generation
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html`, lines 435-444
- **File:** `/home/jalloway/projects/ai-bandmaker/app.py` (no cancel endpoint)
- **Category:** UX
- **Description:** The cancel button stops client-side polling and shows a `confirm()` dialog saying "The server will continue processing in the background." The server thread continues making expensive OpenAI API calls (GPT-4o, DALL-E 3). Users expect "Cancel" to actually cancel.
- **Fix:** Implement a cancellation flag in `generation_status`. Add a `/api/cancel/<generation_id>` endpoint. Check the flag between each step in `generate_band_async()` and bail out before the DALL-E call. Alternatively, rename the button to "Go Back" with messaging that sets correct expectations.

### H-003 -- Generation ID timestamp has race condition
- **File:** `/home/jalloway/projects/ai-bandmaker/app.py`, line 98
- **Category:** UX / Code Quality
- **Description:** `generation_id = datetime.now().strftime("%Y%m%d_%H%M%S")` has only second-level precision. Two users generating in the same second get the same ID. The second request silently overwrites the first in `generation_status`, corrupting both sessions.
- **Fix:** Use `uuid.uuid4().hex[:12]` or append a random suffix.

### H-004 -- No CSRF protection on generation API
- **File:** `/home/jalloway/projects/ai-bandmaker/app.py`, line 92
- **Category:** Code Quality / Security
- **Description:** The `/api/generate` POST endpoint has no CSRF token. An external site could trigger generation from a user's browser, consuming OpenAI API credits.
- **Fix:** Add Flask-WTF CSRF protection or a custom token validated server-side.

### H-005 -- No rate limiting on generation endpoint
- **File:** `/home/jalloway/projects/ai-bandmaker/app.py`, line 92
- **Category:** Code Quality / Security
- **Description:** No rate limiting exists. A user could trigger dozens of concurrent generations, each making multiple expensive API calls.
- **Fix:** Add Flask-Limiter or a simple in-memory limit (e.g., max 1 concurrent generation per IP, max 5 per hour).

### H-006 -- Thread safety issue with `generation_status` dict
- **File:** `/home/jalloway/projects/ai-bandmaker/app.py`, lines 22, 110, 150-223
- **Category:** Code Quality
- **Description:** `generation_status` is a plain `dict` read and written from both Flask request threads and background generation threads without locking. The cleanup function's iterate-and-delete pattern (lines 32-40) is not thread-safe.
- **Fix:** Use `threading.Lock()` around all access to `generation_status`. For production, consider a task queue (Celery, RQ).

### H-007 -- Gallery glob depends on working directory
- **File:** `/home/jalloway/projects/ai-bandmaker/app.py`, line 60
- **Category:** Code Quality
- **Description:** `glob.glob("*/home.html")` uses a relative path. If Flask runs from a different directory or behind a WSGI server that changes cwd, the gallery finds nothing.
- **Fix:** Use `glob.glob(os.path.join(app.root_path, "*/home.html"))`.

### H-008 -- Gallery image alt text is generic (WCAG 1.1.1)
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/gallery.html`, line 25
- **Category:** Accessibility
- **Description:** `alt="{{ band.name }}"` repeats the band name without describing the image content. Screen reader users cannot distinguish this from the adjacent text link.
- **Fix:** Change to `alt="Promotional photo of {{ band.name }}"`.

### H-009 -- Gallery VIEW links lack accessible labels (WCAG 2.4.4)
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/gallery.html`, line 36
- **Category:** Accessibility
- **Description:** Each gallery row has a generic `[ VIEW ]` link. Screen readers listing all links on the page hear "VIEW, VIEW, VIEW..." with no context about which band each link relates to.
- **Fix:** Add `aria-label="View {{ band.name }} fan page"` to each VIEW link.

### H-010 -- Progress steps table header column says "?" (WCAG 1.3.1)
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html`, line 196
- **Category:** Accessibility
- **Description:** The first column header is `?`, which screen readers announce as "question mark" -- semantically meaningless.
- **Fix:** Use `<th scope="col"><span class="sr-only">Status</span><span aria-hidden="true">?</span></th>` or simply change the visible text to "Status".

### H-011 -- Generated fan pages use deprecated `<a name="">` anchors (WCAG 4.1.1)
- **File:** `/home/jalloway/projects/ai-bandmaker/createAct.py`, lines 566, 574, 588, 598, 602
- **Category:** Accessibility
- **Description:** Uses `<a name="backstory">` instead of `id` attributes on section headings. This is deprecated HTML that some assistive technologies may not navigate correctly.
- **Fix:** Replace `<a name="backstory"></a><h3 ...>` with `<h3 id="backstory" class="section-header">`.

### H-012 -- Inline styles override CSS system in multiple templates
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/index.html`, lines 30, 67
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html`, lines 171, 190, 191
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/gallery.html`, lines 16, 17, 30, 54
- **Category:** Code Quality
- **Description:** The stylesheet uses a well-structured custom property system, but inline `style=""` attributes bypass it. Notable examples: `style="width:50px;"` on table column, `style="color:#333333;"` and `style="color:#ff00ff;"` on progress bar spans, `style="width:120px;"` on gallery columns, `style="margin-bottom:10px;"` on button, `style="font-size:1.2em;"` on CTA text.
- **Fix:** Extract each to named CSS classes: `.step-number-col { width: 50px; }`, `.progress-empty { color: var(--color-border-subtle); }`, `.progress-pct { color: var(--color-accent-magenta); }`, `.gallery-col-photo { width: 120px; }`, etc.

### H-013 -- No `<form>` element wrapping band parameters
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html`, lines 14-180
- **Category:** Accessibility / UX
- **Description:** The band parameter controls and generate button are not wrapped in a `<form>`. Pressing Enter in a select does not submit (broken keyboard expectation). Assistive technology does not announce the region as a form landmark.
- **Fix:** Wrap `#startGeneration` content in `<form role="form" aria-label="Band generation parameters">`. Add a `submit` event listener with `preventDefault()` that triggers `startGeneration()`. Change the generate button to `type="submit"`.

### H-014 -- No loading indicator between button click and API response
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html`, lines 317-339
- **Category:** UX
- **Description:** The generate button is disabled on click but shows no visual loading state. On slow connections, the user sees a frozen greyed-out button with no feedback for potentially several seconds. Violates Nielsen's heuristic #1 (Visibility of System Status).
- **Fix:** Change button text to "Starting..." immediately on click, or add a CSS spinner next to the button.

### H-015 -- Error retry does not return user to form
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html`, lines 259-267, 281
- **Category:** UX
- **Description:** The "TRY AGAIN" button calls `startGeneration()` directly, re-submitting with the same parameters. The user has no way to change selections before retrying.
- **Fix:** Add a "[ CHANGE PARAMETERS ]" button alongside "[ TRY AGAIN ]", where the former calls `resetInterface()`.

### H-016 -- Error state does not re-enable generate button
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html`, lines 427-433
- **Category:** UX
- **Description:** `showError()` hides/shows panels but does not clear running intervals/timeouts or re-enable the generate button. If the user navigates back to the form manually, the button remains disabled.
- **Fix:** Have `showError()` call cleanup logic: clear intervals, clear timeouts, set `generateBtn.disabled = false`.

### H-017 -- Gallery displays parsed directory names instead of stored band names
- **File:** `/home/jalloway/projects/ai-bandmaker/app.py`, lines 62-63
- **Category:** UX
- **Description:** `display_name = re.sub(r'([A-Z])', r' \1', band_name).strip()` is fragile CamelCase splitting. "MyopicSunflowers" becomes " Myopic Sunflowers" (leading space). Band names with numbers, hyphens, or non-ASCII characters will display incorrectly.
- **Fix:** Write a JSON sidecar file (e.g., `band_meta.json`) to each band directory during generation containing the original band name and metadata. Read that file in the gallery view.

### H-018 -- Gallery table missing `<thead>` and `<tbody>` (WCAG 1.3.1)
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/gallery.html`, lines 14-42
- **Category:** Accessibility
- **Description:** The gallery table uses `<th scope="col">` (good) but lacks explicit `<thead>` and `<tbody>` grouping, which degrades screen reader table navigation.
- **Fix:** Wrap the header row in `<thead>` and the data rows in `<tbody>`.

### H-019 -- Form parameter rows overflow on narrow screens
- **File:** `/home/jalloway/projects/ai-bandmaker/static/css/style.css`, lines 496-514
- **Category:** Layout
- **Description:** `.param-row` uses `display: flex` with an 80px label, 260px max-width select, and 44px dice button. Total minimum width is approximately 400px, which overflows a 320px viewport. No responsive rules exist for this component.
- **Fix:** Add to the 640px media query:
  ```css
  .param-row { flex-wrap: wrap; }
  .param-label { width: 100%; text-align: left; margin-bottom: var(--space-xs); }
  .retro-select { max-width: none; }
  ```

### H-020 -- Gallery VIEW button touch targets are undersized (WCAG 2.5.5)
- **File:** `/home/jalloway/projects/ai-bandmaker/static/css/style.css`, lines 359-379
- **Category:** Layout / Accessibility
- **Description:** `.retro-button-small` has `padding: 4px 12px` with `font-size: 0.85em` (~12px). The resulting touch target is approximately 32x20px -- well below the 44x44px minimum for mobile touch targets.
- **Fix:** Add `min-height: 44px; min-width: 44px;` to `.retro-button-small`, or increase padding to at least `10px 16px`.

---

## Medium Issues (nice to fix)

### M-001 -- Navigation uses decorative brackets that screen readers announce
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/base.html`, lines 28-31
- **Category:** Accessibility
- **Description:** Nav items include literal `[`, `]`, and `|` characters as visual separators. Screen readers announce these as "left bracket, Home, right bracket, pipe..." creating a noisy, confusing experience.
- **Fix:** Wrap decorative characters in `<span aria-hidden="true">`:
  ```html
  <li><span aria-hidden="true">[ </span><a href="...">Home</a><span aria-hidden="true"> ]</span></li>
  ```

### M-002 -- Banner stars are announced by screen readers
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/base.html`, lines 17, 22
- **Category:** Accessibility
- **Description:** The `.banner-stars` divs contain `* * * * * * * * * * * * * * * * * * * * *` which screen readers read as a long string of "asterisk" or "star" announcements. These are purely decorative.
- **Fix:** Add `aria-hidden="true"` to both `.banner-stars` divs.

### M-003 -- Visitor counter announced as meaningful content
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/base.html`, lines 47-49
- **Category:** Accessibility
- **Description:** The visitor counter generates a random number on each page load. Screen readers announce "You are visitor number 47293" which is misleading since the value is random. Assistive technology users may take it literally.
- **Fix:** Add `aria-hidden="true"` to the counter paragraph, or wrap the number in `<span aria-hidden="true">` with a visually hidden note: `<span class="sr-only">(this counter is decorative)</span>`.

### M-004 -- Only one breakpoint -- tablets unaddressed
- **File:** `/home/jalloway/projects/ai-bandmaker/static/css/style.css`, line 652
- **Category:** Layout
- **Description:** A single `@media (max-width: 640px)` breakpoint handles mobile. Tablets (641px-800px) use the desktop layout, which creates cramped three-column feature grids and tight gallery tables.
- **Fix:** Add an intermediate breakpoint at `max-width: 768px` to stack the feature grid and widen gallery columns.

### M-005 -- Feature grid has no minimum width or wrap behaviour
- **File:** `/home/jalloway/projects/ai-bandmaker/static/css/style.css`, lines 288-298
- **Category:** Layout
- **Description:** `.feature-grid` uses `display: flex` with `flex: 1` children. Between 400px and 640px (above the mobile breakpoint), the three boxes get squeezed to approximately 100px each, making text unreadable. No `flex-wrap: wrap` or `min-width` exists.
- **Fix:** Add `flex-wrap: wrap` and `min-width: 200px` to `.feature-box`, or lower the stacking breakpoint.

### M-006 -- Button class hierarchy is non-composable
- **File:** `/home/jalloway/projects/ai-bandmaker/static/css/style.css`, lines 322-379
- **Category:** Code Quality
- **Description:** Three button variants exist: `.retro-button` (primary), `.retro-button-secondary` (modifier), `.retro-button-small` (standalone). `.retro-button-small` duplicates every property from `.retro-button` instead of extending it. On generate.html line 171, `retro-button-secondary retro-button-small` are combined, but secondary's hover colours are not overridden by small, producing an accidental hover state.
- **Fix:** Refactor to a composable BEM system: `.btn` (base), `.btn--primary`, `.btn--secondary`, `.btn--sm` (size modifier only).

### M-007 -- `<br>` and `&nbsp;` used for layout spacing
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html`, line 174 (`<br>`), line 250 (`&nbsp;&nbsp;`)
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/gallery.html`, line 47 (`<br>`)
- **Category:** Code Quality / Accessibility
- **Description:** `<br>` tags create visual spacing between buttons. `&nbsp;&nbsp;` separates the View and Generate Another buttons. These are presentational misuses that screen readers may announce and that provide no consistent spacing control.
- **Fix:** Remove `<br>` tags and `&nbsp;` entities. Use CSS margin or flexbox gap:
  ```css
  .button-area--spaced { display: flex; justify-content: center; gap: var(--space-md); flex-wrap: wrap; }
  ```

### M-008 -- Focus style inconsistency between `:focus` and `:focus-visible`
- **File:** `/home/jalloway/projects/ai-bandmaker/static/css/style.css`, lines 528-532 vs 340, 377, 557
- **Category:** Accessibility
- **Description:** `.retro-select` uses `:focus` (visible on all interactions), while buttons and links use `:focus-visible` (visible only on keyboard). Mouse users see a focus ring on dropdowns but not on buttons. The inconsistency may confuse users.
- **Fix:** Standardise on `:focus-visible` across all interactive elements, or keep `:focus` on all form controls. Pick one strategy and apply uniformly.

### M-009 -- 5-minute timeout with no elapsed time display
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html`, lines 343-347
- **Category:** UX
- **Description:** The 300-second timeout has no user-facing time indicator. Users may assume the process is stuck when the DALL-E step takes 30-60 seconds. Violates Nielsen's heuristic #1 (Visibility of System Status).
- **Fix:** Show elapsed time near the progress bar (e.g., "Generating for 2m 15s...") and set expectations: "This usually takes 2-3 minutes."

### M-010 -- No `beforeunload` warning during generation
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html`
- **Category:** UX
- **Description:** If the user navigates away or closes the tab during generation, there is no warning. The generation continues server-side but the user loses status tracking.
- **Fix:** Add a `beforeunload` event listener while generation is in progress and remove it on completion/error/cancel.

### M-011 -- JavaScript uses global scope
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/generate.html`, lines 273-477
- **Category:** Code Quality
- **Description:** All functions and variables (`currentGenerationId`, `statusCheckInterval`, `startGeneration`, etc.) are declared in global scope, polluting `window` and risking collisions.
- **Fix:** Wrap in an IIFE: `(function() { ... })();`.

### M-012 -- `main.js` star twinkle interval lacks cleanup and reduced-motion check
- **File:** `/home/jalloway/projects/ai-bandmaker/static/js/main.js`, lines 8-14
- **Category:** Code Quality / Accessibility
- **Description:** The `setInterval` for star twinkle runs every 2 seconds indefinitely, even when scrolled off-screen, and does not respect `prefers-reduced-motion`.
- **Fix:** Gate behind `window.matchMedia('(prefers-reduced-motion: reduce)')` and consider using `IntersectionObserver` to start/stop when the banner is in viewport.

### M-013 -- Design tokens not used consistently in stylesheet
- **File:** `/home/jalloway/projects/ai-bandmaker/static/css/style.css`
- **Category:** Code Quality
- **Description:** The `:root` block defines 18 custom properties, but raw hex values still appear: `#1a1a3a` (line 269), `#111133` (line 452), `#aaaaaa` (line 316), and others.
- **Fix:** Create additional tokens (`--color-bg-table-header`, etc.) or use existing ones where appropriate.

---

## Low Issues (optional)

### L-001 -- Visitor counter randomises on every page load
- **File:** `/home/jalloway/projects/ai-bandmaker/templates/base.html`, line 48
- **Category:** UX
- **Description:** The visitor counter changes on every load. This is a charming retro touch but may briefly confuse users who notice the number changing. Purely cosmetic.
- **Fix:** No action required. If desired, store a session-based value so the number is consistent within a visit.

---

## Previously Fixed Issues (Acknowledged)

The following items from prior reviews have been correctly resolved:

| Issue | Resolution |
|---|---|
| Missing `<label>` elements on form controls | Proper `<label for="">` on all selects |
| Nav was `<div>` not `<nav>` | Now `<nav>` with `aria-label="Main navigation"` |
| Layout tables for features/params | Features now flexbox; params now fieldset |
| No skip-to-content link (main app) | Skip link present, correctly styled |
| Table headers not semantic `<th>` | Now use `<th scope="col">` |
| No aria-live on progress messages | `aria-live="polite"` on progress, `aria-live="assertive"` on error |
| Dice buttons had no accessible text | `aria-label` present on all dice buttons |
| No `<main>` landmark (main app) | `<main>` element present with `id="main-content"` |
| Footer/header were `<div>` | Now `<footer>` and `<header>` |
| No CSS custom properties | 18 design tokens defined in `:root` |
| Heading hierarchy skip (h2 to h4) | Feature boxes now use `<h3>` correctly |
| Blink animation no reduced-motion (main app) | `prefers-reduced-motion: reduce` query present |
| XSS via innerHTML on band preview | Uses `textContent` |
| No path validation on band routes | `SAFE_BAND_NAME` regex guard present |
| No cancel confirmation | `confirm()` dialog added |
| No polling timeout | 5-minute timeout implemented |
| No disabled state on generate button | Button disabled on click |
| No active page indication in nav | `aria-current="page"` and `.nav-active` class |
| Raw exceptions exposed to users | Generic user-friendly error messages |

---

## Recommended Priority Order

### Immediate (Critical -- fix before any deploy)
1. **C-001:** Escape all AI-generated strings in `create_html_content()` with `html.escape()`
2. **C-002:** Raise `--color-text-muted` to `#b0b0b0`; fix progress bar empty dash colour
3. **C-003:** Add `role="progressbar"` and ARIA value attributes to progress display
4. **C-004:** Add skip link and `<main>` to generated fan pages
5. **C-005:** Replace `<marquee>` with static or CSS-animated heading
6. **C-006:** Add `prefers-reduced-motion` to generated page styles
7. **C-007:** Manage focus on view transitions in generate page

### Next sprint (High)
8. **H-003:** Replace timestamp generation ID with UUID
9. **H-004:** Add CSRF protection to `/api/generate`
10. **H-005:** Add rate limiting to generation endpoint
11. **H-006:** Add threading lock around `generation_status`
12. **H-007:** Use absolute path for gallery glob
13. **H-001:** Replace inline JS colour with CSS class toggling
14. **H-002:** Implement server-side generation cancellation
15. **H-013:** Wrap parameters in `<form>` element
16. **H-019:** Add responsive rules for form parameter rows
17. **H-020:** Increase touch target size on small buttons
18. **H-014:** Add loading state feedback on generate button
19. **H-015/H-016:** Fix error state cleanup and add "Change Parameters" option
20. **H-017:** Store and read band metadata from JSON sidecar files
21. **H-008/H-009/H-010/H-011/H-018:** Fix remaining accessibility gaps
22. **H-012:** Extract remaining inline styles to CSS classes

### Backlog (Medium/Low)
23. All M-series and L-series issues

---

**Totals:** Critical: 7 | High: 20 | Medium: 13 | Low: 1 | **Total: 41**
