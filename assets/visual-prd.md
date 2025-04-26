# ArtGen UI Refresh – *Light‑Scope* PRD (Visual Only)

**Version:** 2.0   **Last Updated:** 26 Apr 2025

> **Scope Note**  This iteration is **purely cosmetic**. We will not add, remove, or refactor any features or JavaScript logic. The goal is to make the existing single‑page interface feel polished, modern, and delightful while keeping the DOM structure and API calls untouched.

---
## 1 Objectives
1. **Elevate visual appeal** to a world‑class standard inspired by Midjourney but suited for a lightweight FastAPI demo.
2. **Improve readability & hierarchy** without changing content or functionality.
3. **Maintain simplicity**: zero new controls, fields, pop‑ups, or data flows.

Success = “Wow, it looks amazing!” while the codebase and user flow stay identical.

---
## 2 Design Principles
| Principle | Implementation Hint |
|-----------|---------------------|
|Minimal & Bold|Plenty of white/dark space, one strong accent gradient for CTAs|
|Glassmorphism Touches|Subtle frosted panels (backdrop‑filter: blur(12px); background: rgba(255,255,255,0.06))|
|Soft Motions|Fade/slide‑up 200 ms on load; button pulse on hover (CSS only)|
|Consistent Tokens|8‑pt spacing; 2 rem border‑radius for cards; Inter font|
|Contrast & Accessibility|AA contrast for text; focus rings with outline‑offset 2 px|

---
## 3 Style Guide
### 3.1 Colors
| Token | Hex | Usage |
|-------|-----|-------|
|`bg-base`|`#0d0d10`|Page background (dark theme default)|
|`fg-primary`|`#ffffff`|Body text|
|`accent-grad`|linear‑grad 90deg from `#eb5cff` via `#9f6eff` to `#4bbdff`|Buttons, active elements|
|`surface`|rgba(255,255,255,0.04)|Panel backgrounds |
|`border-subtle`|rgba(255,255,255,0.12)|1 px card borders |

### 3.2 Typography
- **Font:** Inter, system‑fallback.
- **Sizes:** H1 2.5 rem / H2 1.5 rem / body 1 rem / small 0.875 rem.
- **Letter‑spacing:** ‑0.01 em for headings for dense tech look.

### 3.3 Components
| Element | Visual Treatment |
|---------|------------------|
|Header|Full‑width frost bar, logo in bold gradient text, subtitle lighter 500 weight|
|Control Panel|Glass card max‑width 320 px; stacked 16 px gap; labels in small caps; textarea auto‑shadow on focus|
|Details tag|Custom arrow icon rotates 90° on open (CSS transform)|
|Generate Button|Accent gradient background, white text, shadow‑md, hover: translateY(‑2 px) + shadow‑xl|
|Results Panel|Scroll container with fade‑in images & light 1 px border;
small caption row (`status`) under heading|
|Image container|Rounded‑xl, overflow hidden; hover overlay (gradient‑to‑transparent top→bottom) showing download icon|
|Spinner|SVG circle 40 px, stroke‑dasharray 100, CSS @keyframes rotate 1.2 s linear infinite|
|Toast|Fixed bottom‑right stack, blur‑behind, slide‑in 250 ms|

---
## 4 CSS Implementation
We will drop **`/static/css/styles.css`** and rebuild with **TailwindCSS 3** (CDN mode to avoid build toolchain). Advantages: speed, consistent tokens, minimal hand‑rolled CSS.

```html
<!‑‑ in <head> ‑‑>
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@3.4.4/dist/tailwind.min.css" rel="stylesheet">
<style>
  /* custom vars */
  :root {
    --accent-grad: linear-gradient(90deg,#eb5cff,#9f6eff 50%,#4bbdff);
  }
  .glass { backdrop-filter: blur(12px); background: rgba(255,255,255,0.04); }
</style>
```

All classes below are illustrative; devs can map them into the existing HTML without changing IDs/classes used in JS.

### Key Mappings
| Section | Old class | New Tailwind classes |
|---------|-----------|----------------------|
|`<header>`|`.container`|`max‑w‑5xl mx‑auto px‑6 py‑8 flex flex‑col gap‑1`|
|`h1`| |`text‑3xl font‑bold bg‑clip‑text text‑transparent [background:var(--accent-grad)]`|
|Control Panel|`.control-panel`|`glass p‑6 rounded‑2xl w‑[320px] flex flex‑col gap‑4`|
|Button|`.btn.btn-primary`|`bg‑[var(--accent-grad)] text‑white py‑3 rounded‑xl font‑medium shadow transition hover:shadow‑xl active:scale‑95`|
|Results Panel|`.results-panel`|`flex‑1 min‑h‑[480px] pl‑8`|
|Image Container|`.image-container`|`relative rounded‑2xl overflow‑hidden group`|
|Overlay|`.image-actions`|`absolute inset‑0 bg‑gradient‑to‑b from‑black/0 via‑black/40 to‑black/70 opacity‑0 group‑hover:opacity‑100 transition`|

---
## 5 Animation Specs (CSS‑only)
| Element | Trigger | Keyframes |
|---------|---------|-----------|
|Page load|on DOM ready|`@keyframes fadeSlideUp` 0→1 opacity, +12 px translation|
|Button pulse|hover|scale 1→1.04→1 (150 ms)|
|Spinner|continuous|rotate infinite 360°|
|Toast|create|translateX(100%) → 0 (200 ms) & fade in|

---
## 6 File Changes Matrix
| File | Change |
|------|--------|
|`index.html`|Add Tailwind CDN link & `style` block; swap most class names to TW (no structural change)|
|`styles.css`|Can be removed or kept only for custom spinner & toast animations if preferred|
|`app.js`|No modifications required |

---
## 7 Timeline (Visual‑only)
- **Day 0** — Agree on palette & token values.
- **Day 1** — Implement Tailwind classes + CSS variables; polish header, control panel, button.
- **Day 2** — Style gallery, hover overlays, spinner, toast; responsive tweak.
- **Day 3** — Lighthouse pass (accessibility/contrast), handover.

---
## 8 Out‑of‑Scope Items (Explicit)
- New controls (prompt history, user auth, likes…)  ❌
- WebSocket or progress bar integration           ❌
- Backend / API changes                           ❌

---
## 9 Deliverables
1. Updated `index.html` with Tailwind classes & gradient tokens.
2. `custom.css` (if any) for glass, spinner, toast.
3. Screenshot set (desktop & mobile) for sign‑off.

---
### End of Document

