---
name: Proximity Mesh
colors:
  surface: '#0f131d'
  surface-dim: '#0f131d'
  surface-bright: '#353944'
  surface-container-lowest: '#0a0e18'
  surface-container-low: '#171b26'
  surface-container: '#1c1f2a'
  surface-container-high: '#262a35'
  surface-container-highest: '#313540'
  on-surface: '#dfe2f1'
  on-surface-variant: '#c7c4d8'
  inverse-surface: '#dfe2f1'
  inverse-on-surface: '#2c303b'
  outline: '#918fa1'
  outline-variant: '#464555'
  surface-tint: '#c3c0ff'
  primary: '#c3c0ff'
  on-primary: '#1d00a5'
  primary-container: '#4f46e5'
  on-primary-container: '#dad7ff'
  inverse-primary: '#4d44e3'
  secondary: '#4cd7f6'
  on-secondary: '#003640'
  secondary-container: '#03b5d3'
  on-secondary-container: '#00424e'
  tertiary: '#4edea3'
  on-tertiary: '#003824'
  tertiary-container: '#006e4b'
  on-tertiary-container: '#67f4b7'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e2dfff'
  primary-fixed-dim: '#c3c0ff'
  on-primary-fixed: '#0f0069'
  on-primary-fixed-variant: '#3323cc'
  secondary-fixed: '#acedff'
  secondary-fixed-dim: '#4cd7f6'
  on-secondary-fixed: '#001f26'
  on-secondary-fixed-variant: '#004e5c'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#0f131d'
  on-background: '#dfe2f1'
  surface-variant: '#313540'
typography:
  headline-xl:
    fontFamily: Geist
    fontSize: 36px
    fontWeight: '600'
    lineHeight: 44px
  headline-xl-mobile:
    fontFamily: Geist
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  headline-lg:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Geist
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  label-md:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: Geist
    fontSize: 10px
    fontWeight: '600'
    lineHeight: 12px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  margin: 1.25rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.25rem
---

## Brand & Style

The design system embodies seamless local-network collaboration: frictionless, secure, and visually calm. It captures the modern utility of peer-to-peer sharing tools like AirDrop or LocalSend while infusing an ambient, welcoming precision. The emotional experience balances instant clarity with technological confidence—reassuring the user through immediate visual feedback, spatial device awareness, and crisp state transitions.

The aesthetic blends **Modern Minimalist Surface Architecture** with **Soft Ambient Glassmorphism**. Layouts prioritize generous breathing room, ultra-subtle borders, and layered surfaces over heavy ornamentation. Visual energy is concentrated selectively into vibrant connectivity cues: soft-pulsing radars, neon cyan discovery indicators, and luminous transmission progress rings.

## Colors

The palette leverages a deep, low-luminance canvas (`#0B0F19`) accented by refined indigo and electric blue structural highlights, paired with high-clarity signaling accents.

- **Primary (`#4F46E5` / Electric Indigo):** Drives primary actions, active send flows, paired states, and core interactive anchors.
- **Secondary (`#06B6D4` / Neon Cyan):** Dedicated to peer-discovery ripples, dynamic network waves, and high-energy pairing handshakes.
- **Tertiary (`#10B981` / Emerald Green):** Signals verified device availability, secure TLS handshake completion, and successful transfer confirmations.
- **Neutral (`#0B0F19` / Deep Obsidian):** Deep slate-tinted canvas preventing harsh pure-black contrast. Paired with elevated container tiers (`#131B2E`, `#1E293B`) and crisp sub-tier borders (`rgba(255, 255, 255, 0.08)`).
- **Text & Foreground Hierarchy:** Pure White (`#F8FAFC`) for primary titles and active targets; Slate Light (`#94A3B8`) for secondary device specs and transfer speeds; Slate Dark (`#64748B`) for disabled or pending states.

## Typography

Typography relies on **Geist** throughout all UI tiers to convey engineering precision, legible data densities, and ultra-clean modern form factors. 

- **Display & Headlines:** Set with semi-bold weights (`600`) and slight negative tracking (`-0.02em`) to maintain structural tightness on dynamic device labels and throughput stats.
- **Data & Transfer Telemetry:** Real-time transfer rates (MB/s), estimated time remaining, and hash validation strings use tabular figure formatting (`tnum`) in standard body weights.
- **Labels & Micro-copy:** Uppercase tags, verification badges, and protocol indicators use `label-sm` with slightly expanded letter-spacing (`+0.04em`) to ensure legibility on high-DPI mobile screens.

## Layout & Spacing

The layout is built around a fluid single-column mobile viewport (scaling to a structured 4-to-8 column system on tablets/foldables) anchored by strict safe-area margins. 

- **Canvas Metrics:** Standard outer boundary margin is `1.25rem` (20px), ensuring touch-friendly proximity to device edges without cramped interaction zones.
- **Vertical Rhythm:** Root containers follow an 8pt architectural rhythm, with tight micro-spacings (`space-xs`, `space-sm`) inside device tiles and file queue cells, moving to generous gaps (`space-lg`, `space-xl`) between the radar discovery stage and incoming payload lists.
- **Form Factor Adaptations:**
  - *Mobile (<640px):* Centered radar zone occupying the upper 45% of the viewport; bottom sheets handle ongoing transfers and file selection.
  - *Tablet / Dual-Screen (≥640px):* Split-pane presentation with persistent multi-peer radar on the left and simultaneous multi-file streaming telemetry on the right.

## Elevation & Depth

Visual depth is communicated through dark translucent layered tiers paired with diffuse colored luminescence rather than opaque cast shadows.

- **Base Layer (Elevation 0):** Obsidian ground canvas (`#0B0F19`) providing deep black contrast.
- **Surface Layer (Elevation 1):** Device and action cards styled with `background: rgba(19, 27, 46, 0.7)`, backed by `backdrop-filter: blur(16px)` and a continuous hairline stroke of `1px solid rgba(255, 255, 255, 0.06)`.
- **Raised Interactive Layer (Elevation 2):** Active device nodes and floating transfer docks styled with `background: rgba(30, 41, 59, 0.85)` and an ambient micro-glow: `box-shadow: 0 8px 32px -4px rgba(79, 70, 229, 0.15), 0 2px 8px rgba(0, 0, 0, 0.4)`.
- **Luminous Glow States:** Active transferring devices emit a cyan-indigo soft ambient radiation: `0 0 24px rgba(6, 182, 212, 0.35)`. Verified status indicators use a self-illuminating emerald point light: `0 0 10px rgba(16, 185, 129, 0.6)`.

## Shapes

The shape system employs progressive corner curvature centered on modern squircle aesthetics (`rounded-2xl` for primary containers).

- **Cards & Device Containers:** Formed with `1rem` (16px) radius, delivering soft ergonomics that frame dense network telemetry cleanly.
- **Action Buttons & Modals:** Standardized on `1rem` to `1.25rem`, matching card contours to create continuous silhouette harmony.
- **Pill Badges & Radial Avatars:** Device avatars and status indicators utilize full roundness (`rounded-full` / 9999px) to establish visual contrast against the squircle containment architecture.

## Components

### Buttons & Interactive Triggers
- **Primary CTA:** Filled with indigo-to-blue gradient (`#4F46E5` to `#3B82F6`), `rounded-2xl` (16px), 48px height for optimal tap target. Styled with an ultra-fine inset border `inset 0 1px 0 rgba(255, 255, 255, 0.2)` and a soft ambient drop shadow `0 4px 14px rgba(79, 70, 229, 0.35)`.
- **Ghost / Subtle Secondary:** Translucent slate fill `rgba(255, 255, 255, 0.05)`, border `1px solid rgba(255, 255, 255, 0.08)`, smooth active scale effect (`scale-98`).

### Device Discovery Cards & Tiles
- Framed in `rounded-2xl` with a subtle hairline outline (`rgba(255, 255, 255, 0.08)`).
- Contains device category glyph (phone, laptop, tablet), resolved device name (`Geist label-lg`), and dynamic signal strength dots.
- Long-press triggers an expanded modal with IP, hash fingerprint, and protocol status.

### Proximity Radar Stage
- Concentric circular rings rendered with decreasing opacity (`rgba(6, 182, 212, 0.15)` to `rgba(6, 182, 212, 0.03)`).
- Core node pulses continuously with a CSS keyframe outward wave (`ping` effect) in secondary neon cyan.
- Surrounding peer nodes float dynamically along calculated distance vectors with smooth spring physics.

### Status Indicators & Badges
- **Availability Beacon:** Circular 8px dot with tertiary emerald fill (`#10B981`) enveloped by an animated 16px soft glow ring (`rgba(16, 185, 129, 0.25)`).
- **Protocol Chip:** Compact pill badge (`rounded-full`, 20px height) featuring monospace Wi-Fi Direct / Local P2P identification tags in `label-sm`.

### Transfer Progress & File Queue Items
- Card-based queue items featuring thumbnail previews, dual-line typography (`headline-sm` for file name, `body-sm` for throughput and remaining time).
- Integrated linear progress bar with neon cyan track fill (`#06B6D4`) over a dark track base (`rgba(255, 255, 255, 0.08)`), capped with a leading edge glow point.

### Inputs & Discovery Filter Fields
- Low-profile inputs set against `#131B2E`, framed by 1px border `rgba(255, 255, 255, 0.1)`. 
- Focus state activates an electric indigo glow ring: `0 0 0 2px rgba(79, 70, 229, 0.4)`.