# SkillBridge — Figma Design System & Dev Handoff Specification

**Brand Name:** SkillBridge  
**Tagline:** "Bridging Skills to Opportunity"  
**Target Platform:** Flask + Jinja2 + TailwindCSS Responsive Web Application (Mobile 375px, Tablet 768px, Desktop 1440px)  
**Target Demographics:** India's blue-collar workforce (electricians, plumbers, drivers, cooks, painters, carpenters, security guards) & employers  

---

## 1. Design System Foundations

### 1.1 Color Tokens & Palettes

| Token Name | Light Mode Value | Dark Mode Value | Usage / Intent |
| :--- | :--- | :--- | :--- |
| `--sk-primary` | `#D97706` (Saffron 600) | `#F59E0B` (Saffron 500) | Primary CTA, Hero accent, Voice search mic |
| `--sk-primary-hover` | `#B45309` (Saffron 700) | `#FBBF24` (Amber 400) | Hover state for primary buttons |
| `--sk-primary-light` | `#FEF3C7` (Amber 100) | `rgba(245,158,11,0.15)` | Active category card background, badges |
| `--sk-secondary` | `#0D9488` (Teal 600) | `#14B8A6` (Teal 500) | Verified badges, Quick Call CTAs, Income uplift |
| `--sk-bg-body` | `#FAF8F5` (Warm Sand 50) | `#0F172A` (Slate 900) | Global body background (reduces glare outdoors) |
| `--sk-bg-surface` | `#FFFFFF` | `#1E293B` (Slate 800) | Cards, Modals, Drawers |
| `--sk-bg-surface-subtle` | `#F3F0EA` | `#334155` | Input backgrounds, tag chips |
| `--sk-border` | `#E5E0D8` | `#334155` | Dividers, card borders |
| `--sk-text-main` | `#1F2937` (Slate 800) | `#F8FAFC` (Slate 50) | High contrast outdoor readability |
| `--sk-text-muted` | `#6B7280` (Slate 500) | `#94A3B8` (Slate 400) | Subtitles, timestamps, distance tags |

---

### 1.2 Typography System

SkillBridge pairs **Plus Jakarta Sans** (Latin text) with **Noto Sans Devanagari** (Hindi script) to guarantee crisp character rendering across low-resolution budget Android screens.

- **Hindi Devanagari Mode:** Activated dynamically via `html[lang="hi"]`. Line height is scaled to `1.5` to prevent Devanagari vowel mark clipping.

| Scale Token | Font Size | Line Height | Weight | Tailwind Equivalent |
| :--- | :--- | :--- | :--- | :--- |
| `Display XL` | `48px / 3rem` | `1.15` | `800 / Black` | `text-4xl lg:text-5xl font-black` |
| `Heading LG` | `30px / 1.875rem` | `1.2` | `800 / Black` | `text-2xl sm:text-3xl font-black` |
| `Heading MD` | `24px / 1.5rem` | `1.3` | `700 / Bold` | `text-xl sm:text-2xl font-extrabold` |
| `Body Large` | `18px / 1.125rem` | `1.5` | `500 / Medium` | `text-lg font-medium` |
| `Body Normal`| `15px / 0.9375rem`| `1.5` | `400 / Regular`| `text-base` |
| `Caption / Badge`| `12px / 0.75rem`| `1.4` | `700 / Bold` | `text-xs font-bold uppercase` |

---

### 1.3 Radii & Elevation Tokens

- `--sk-radius-sm`: `8px` (Chips, small badges)
- `--sk-radius-md`: `12px` (Inputs, standard buttons)
- `--sk-radius-lg`: `16px` (Job cards, category tiles)
- `--sk-radius-xl`: `24px` (Hero containers, voice modal)
- `--sk-radius-full`: `9999px` (Pills, user avatars)

**Elevation Shadows:**
- `Shadow SM`: `0 1px 2px 0 rgba(0,0,0,0.05)`
- `Shadow MD`: `0 4px 6px -1px rgba(0,0,0,0.07)`
- `Shadow LG`: `0 10px 25px -5px rgba(217, 119, 6, 0.1)`
- `Shadow Glow`: `0 0 20px rgba(217, 119, 6, 0.25)`

---

## 2. Reusable Component Specs

### 2.1 Buttons (`.sk-btn`)

1. **Primary Button (`.sk-btn-primary`):**
   - **Background:** `linear-gradient(135deg, #D97706, #C2410C)`
   - **Text:** White (`#FFFFFF`), `font-weight: 700`
   - **Min Height:** `48px` (Touch target compliance for mobile)
   - **Hover Effect:** `translateY(-1px)`, shadow glow increase

2. **Secondary Call Button (`.sk-btn-secondary`):**
   - **Background:** `#0D9488` (Teal 600)
   - **Icon:** Telephone SVG / Call icon
   - **Text:** White (`#FFFFFF`)

3. **Language Toggle Pill (`data-lang-btn`):**
   - **Active State:** Background `#D97706`, Text `#FFFFFF`
   - **Inactive State:** Background `#F3F0EA` / `#1E293B`, Text `#4B5563`

---

### 2.2 Job Cards (`.sk-card-hover`)

- **Anatomy:**
  - Top Image Banner (Height `176px`) with category backdrop image.
  - Overlay Badges: Top-Left Verified Badge (`sk-badge-verified`), Top-Right Heart Toggle button (`♡` / `♥`).
  - Title & Employer: 1-line truncation with 4.8★ rating badge.
  - Transparent Wage Container: High-contrast pill displaying guaranteed wage (e.g. `₹600 / day`).
  - Action Footer: 1-Tap "Call Employer Now" button (`#0D9488`).

---

### 2.3 Voice Search Recording Modal (`#sk-voice-modal`)

- **State 1 (Idle):** Hero search bar microphone icon (`#voice-search-btn`).
- **State 2 (Active Recording):** Dark glass overlay (`rgba(15, 23, 42, 0.7)`), center card with glowing red mic indicator (`.sk-mic-recording`), animated audio wave bars (`.sk-wave-bar`), live transcript status text in Hindi & English.
- **State 3 (Transcribing / Complete):** Auto populates search input and submits form.

---

## 3. Responsive Page Layout Blueprints

### Page 1: Home / Search (`index.html`)
- **Mobile (375px):** Single column. Sticky top header with brand logo, voice search hero bar with mic trigger, 2-column icon category grid, job card stack, 1-tap call triggers.
- **Tablet (768px):** 3-column category grid, 2-column job listing grid.
- **Desktop (1440px):** Max-width `1280px`. Left 1-column sticky filter sidebar (Category dropdown, Location select, Verified only toggle) + Right 3-column job card grid.

### Page 2: Job Detail (`job_detail.html`)
- **Mobile (375px):** Full-width job card, wage banner, skills tag cloud, Google Maps embed, **Sticky Mobile Bottom Bar** featuring Call Now (`tel:`) and WhatsApp (`chat`) buttons.
- **Desktop (1440px):** 2-Column layout: Left 2 columns containing job specifications, perks, map; Right 1 column containing sticky employer card & contact CTAs.

### Page 3: Post a Job (`make_jobs.html`)
- **Mobile & Desktop:** Structured 3-step progress bar (1. Job Specs -> 2. Pay & Location -> 3. Contact & Publish). Interactive trade category selection grid (Electrician, Plumber, Painter, Carpenter, Driver, Other) + Wage quick preset chips (`₹600/day`, `₹850/day`, `₹18,000/mo`). Work site photo drag-and-drop box.

### Page 4: Worker Profile (`profile.html`)
- **Layout:** Top header card with user photo, Aadhaar Verified badge, 4.9★ rating summary, trade skill tags. Tabbed section for "Posted Jobs & Activity", quick delete action, edit profile modal toggle.

### Page 5: Career Growth Dashboard (`career_growth.html`)
- **Layout:** Dark & Light mode compatible AI upskilling path navigator. Includes interactive quiz form, career transition hero (Electrician → Solar Panel Technician), ROI calculator (`14.0x ROI`), payback period (`0.8 months`), skill match radial chart, unlocked roles list, and Gemini AI plain-language advice card.

### Page 6: Shared Base Shell (`base.html`)
- **Components:** Glassmorphism sticky header (`sk-header`), global language switcher (`EN / हिंदी`), dark mode toggle button, slide-over mobile navigation drawer (`#sk-mobile-drawer`), voice search modal, toast alert container, and accessible footer with worker helpline `1800-SKILL-BRIDGE`.

---

## 4. State Specifications

- **Empty Search State:** Rendered when no jobs match filter query; displays friendly magnifying glass graphic, helpful query suggestion pill, and "Clear All Filters" button.
- **Loading State:** Shimmer skeleton cards (`.sk-skeleton`) matching job card geometry.
- **Microphone Error State:** Fallback text alert when mic permission is denied or browser lacks `MediaRecorder` support.
