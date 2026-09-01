# Consulting-Quality Presentation Methodology

How to think about and structure a professional presentation before touching any code. Covers deck architecture, slide anatomy, storyline construction, and formatting discipline drawn from management consulting best practices (MBB-style).

Apply this methodology first (storyline → slide anatomy → evidence mapping), then return to the main SKILL.md for technical implementation.

---

## Critical Formatting Rule: No Dashes

**NEVER use em dashes or en dashes anywhere in slide content, titles, subheadings, or notes.** These characters appear inconsistently across fonts and platforms, and they look unprofessional in presentation context. Instead:

- For ranges, use "to" (e.g., "15 to 50 slides", "FY2023 to FY2025")
- For separating clauses, use a colon, semicolon, or split into two sentences
- For parenthetical asides, use commas or parentheses

This rule applies to all text generated for slides: action titles, subheadings, body content, source citations, and speaker notes.
## Workflow: Content Before Code

Follow this sequence every time. Resist the urge to start coding slides immediately.

### Step 1: Understand the audience and objective

Ask (or infer from context):
- **Who reads this?** Senior executives skim; analysts study detail. This determines density.
- **Read-deck or live-presentation?** Read-decks need self-contained slides with full evidence. Live decks can be sparser with speaker-note support.
- **Knowledge → Emotion → Action**: What should the audience *understand*, *feel*, and *do* after seeing this deck? Experts focus on the emotional lever (urgency, excitement, fear of inaction).

### Step 2: Draft the storyline (titles only)

Write action titles for every slide BEFORE building any content. The titles alone should tell the complete story. A reader skimming only the title bar of each slide must be able to:
1. Understand the main conclusions
2. Follow the logical chain of how you arrived at them

Use the **SCR framework** (see below) as the backbone. Draft in a flat list, then group into sections.

### Step 3: Outline supporting evidence per slide

For each title, note what data type proves the claim: chart, table, comparison, stat callout, process diagram, text with icons. This prevents building slides that don't support their own title.

### Step 4: Build with the pptx skill

Only after completing Steps 1 to 3, read the pptx skill and implement. Apply the formatting standards from this skill during construction.

### Step 5: QA against methodology

After building, verify: Do the action titles flow as a story? Is every slide body directly supporting its title? Are formatting standards consistent? Then run the pptx skill's visual QA process.
## Deck Architecture: Five Sections

A complete consulting-style deck follows this structure:

### 1. Front Page
Simple and clean: **title** (<8 words), optional **subtitle** for elaboration, **company/client name**, **date**. Brand the front page to match the intended positioning (client-branded if positioned as internal work; your firm's brand if external).

### 2. Executive Summary
The single most important slide, and often the one that takes the longest to write. It summarizes the key arguments, storyline, and supporting evidence of the entire body.

Structure it using **Situation-Complication-Resolution (SCR)**:
- **Situation**: Current state, context, background
- **Complication**: The challenge, gap, or threat that demands action
- **Resolution**: Your proposed solution, with key supporting evidence

The executive summary lets a busy reader extract the full story without reading further. Every claim in the exec summary must be substantiated somewhere in the body.

### 3. Body of Slides
The analytical core, often 15 to 50+ slides. Structure the overall flow using the SCR framework, and structure each individual slide using the **Slide Anatomy** rules below. Group slides into logical sections with divider slides if the deck exceeds ~15 slides.

### 4. Recommendation / Next Steps
Actionable conclusions. Three formatting rules:
- **Group** recommendations into categories (strategic, operational, financial)
- **Label/number** each group and item for easy reference in discussion
- **Active voice** with action verbs: "Grow…", "Minimize…", "Target…", "Restructure…"

Include an implementation timeline or immediate next steps where appropriate.

### 5. Appendix
Often longer than the main deck. Contains all supporting evidence, detailed analyses, methodology notes, and backup data that would clutter the main storyline but must be available for reference. Keep the main deck crisp; move everything non-essential here.
## Slide Anatomy: Three Mandatory Parts

Every content slide must have all three. If any part is missing or misaligned, the slide is incomplete.

### (a) Action Title

The title is a **complete sentence** that states the slide's key takeaway or "so-what." It is NOT a topic label.

**Bad (passive/topic title):**
> "Historical development in Revenue and Costs"

**Good (action title):**
> "Over the last 5 years, costs have grown 10% p.a., double the rate of revenue growth"

Rules:
- Maximum 2 lines, consistent font size across all slides
- Less than 15 words is ideal; never exceed ~20
- A reader should understand the slide's conclusion from the title alone without looking at the body
- The title must be provable by the slide body (nothing in the title that isn't in the body)

### (b) Subheading

A concise descriptor of the data or evidence used to prove the action title. Adds scope, units, or time frame.

**Examples:**
- "Sales of personal luxury goods, US Market, $ billions"
- "Forecasted evolution of battery cell costs by 2030 ($/kWh)"
- "Revenue breakdown by segment, FY2023 to FY2025"

### (c) Slide Body

The actual evidence: charts, tables, diagrams, stat callouts, or structured text. Rules:
- Everything in the body must directly support the action title
- Remove all data and figures that don't support the title, no matter how interesting
- Include a **source citation** in the footer for data provenance
- Include a **slide number**
## Storyline Construction: The SCR Framework

The SCR (Situation-Complication-Resolution) framework structures the overall deck flow. Variant: SCQA adds an explicit Question between Complication and Answer.

### Structure

```
SITUATION    → Context, current state, background
COMPLICATION → Challenge, gap, threat, or opportunity
RESOLUTION   → Proposed solution, evidence, recommendations
```

Alternative frameworks (use when SCR doesn't fit):
- **Past → Present → Future**: Good for transformation stories
- **Problem → Solution → Evidence**: Good for pitch decks
- **Status Quo → Disruption → New Paradigm**: Good for market/sector analysis

### How to Draft

1. Sketch overarching sections on paper (or a text document)
2. Write only action titles, one per slide
3. Print or view in Slide Sorter mode; read titles sequentially
4. The titles should read like a coherent narrative: "The market is X... but Y is happening... which means Z... therefore we recommend A, B, C"
5. Iterate titles until the story flows, THEN fill in bodies

### Horizontal Flow Test

Read all action titles in sequence. If the story has gaps, non-sequiturs, or requires the reader to look at slide bodies to follow the logic, the storyline needs work. Fix titles before building content.
## Formatting Standards

These rules produce the "consulting feel," the visual discipline that distinguishes professional decks from corporate templates.

### No Dashes (Reminder)

Never use em dashes or en dashes in any slide text. Use colons, semicolons, commas, parentheses, or "to" for ranges instead.

### Alignment (Non-Negotiable)

- Titles and subheadings occupy the **exact same position** on every slide. When flipping through slides, the title must not jump or change size.
- All repeated elements (logo, source, page number) are in identical positions throughout
- Similar elements on a slide (column headers, chart labels) are aligned to each other
- Use PowerPoint guides / consistent x,y coordinates in pptxgenjs

### Typography

- Pick ONE header font and ONE body font; use them throughout
- Recommended pairings: Georgia + Calibri (McKinsey-style), Trebuchet MS + Trebuchet MS (BCG-style), Arial Black + Arial
- Title: 28 to 36pt bold. Body: 14 to 16pt. Captions/source: 10 to 12pt muted
- Left-align body text and lists; center only slide titles and callout numbers

### Color

- Keep the palette simple: 1 primary, 1 to 2 supporting, 1 accent
- Use bright/accent colors **selectively** to draw attention to key data points
- Establish a color hierarchy and apply it **consistently** across the entire deck
- Choose colors that match the topic; don't default to generic blue

### Icons

- Icons can transform a text-heavy slide. Replace bullet points with meaningful icons where the slide is otherwise simple.
- Use icons from a **single style family** (consistent weight and style)
- Icons should carry meaning and be reusable when referring back to topics later in the deck
- In pptxgenjs, use react-icons rendered to PNG (see pptx skill's icon section)

### Slide Furniture

Every content slide must include:
- **Slide number** (bottom-right or bottom-center)
- **Source citation** (bottom-left, small font, muted color): cite the data source used on that slide

### What to Avoid

- **Dashes**: Never use em dashes or en dashes in any text on the slides
- **Animations and transitions**: Never in consulting-style decks
- **Numbered lists for non-ranked items**: Use bullets unless the numbering itself is meaningful (rankings, sequential steps)
- **Text-only slides**: Every slide needs a visual element (chart, icon, shape, image, or diagram)
- **Exceeding margins**: Never place content outside slide margins (0.5" minimum)
- **Inconsistent spacing**: Choose a gap size (0.3" or 0.5") and use it uniformly
- **Overly decorative elements**: No accent lines under titles (hallmark of AI-generated slides), no gradients for decoration, no clip art
## Slide Layout Patterns

Use these layouts to vary visual rhythm across the deck. Never repeat the same layout on consecutive slides.

### Data & Evidence Slides
- **Large stat callout**: Big number (48 to 72pt) with small label below, for KPIs, growth rates, key metrics
- **Chart + annotation**: Chart on one side, 2 to 3 bullet callouts on the other explaining the "so-what"
- **Comparison columns**: Before/after, pros/cons, Option A vs Option B, side by side
- **Timeline / process flow**: Numbered steps with arrows or connected nodes

### Content & Analysis Slides
- **Two-column**: Text/analysis left, supporting visual right (or vice versa)
- **Icon + text rows**: Icon in colored circle, bold header, description; 3 to 4 rows per slide
- **2×2 or 2×3 grid**: Cards with header + body in each cell, for frameworks, categories, segments
- **Half-bleed image**: Full-height image on left or right, content overlay on the opposite side

### Section Dividers
- Dark background with section title and number
- Minimal; just enough to signal a new chapter in the storyline
## Process Acceleration Tips

These tactics reduce deck-building time from days to hours:

1. **Always start with storyline, never with slides.** Draft the full title sequence before opening PowerPoint or writing code.
2. **Use the Slide Anatomy as a checklist.** If a slide is missing an action title, subheading, or supporting evidence, it's not ready.
3. **Build a personal library.** Save excellent slides and deck structures for reuse; categorize by type (strategy, due diligence, market sizing, etc.).
4. **Reuse section frameworks.** Business strategy, business case, market entry, and similar project types follow predictable storyline skeletons.
5. **Review on paper first.** Walk through the storyline with a colleague before building; changes at the outline stage cost minutes, changes in finished slides cost hours.
6. **Eliminate ruthlessly.** If a piece of data doesn't directly support an action title, move it to the appendix or delete it.
