# PROJECT-detail.md — Skill #232: Micro Urban Agriculture Design & Management

---

## Executive Summary

Skill #232 (`micro-urban-agriculture-design`) is a structured analytical harness for designing, scoring, and continuously improving micro-scale urban farm systems built on soilless growing methods — primarily hydroponics (NFT, DWC, Kratky) and aeroponics. It accepts a user's physical space profile, location/climate data, target crop list, budget, and experience level, then produces a complete professional design package: system layout, lighting plan (DLI-calculated), water and nutrient schedule (EC/pH-calibrated), structural assessment, and a scored improvement roadmap anchored to FAO Urban Agriculture guidelines, VPD physics, and water-use efficiency standards. A crawl4ai knowledge pipeline keeps the embedded SECOND-KNOWLEDGE-BRAIN.md current with the latest research from MDPI Horticulturae, ArXiv, FAO, and RUAF.

---

## Problem Statement

Urban food production at micro scale (balcony: 2–15 m², rooftop: 10–100 m²) is technically accessible but practically challenging:

1. **Light constraints:** Urban structures shadow growing spaces at unpredictable angles and times. Without Daily Light Integral (DLI) calculations anchored to local latitude and weather, growers choose the wrong crops and experience chronic underperformance.
2. **Water and nutrient complexity:** Soilless systems require precise EC (electrical conductivity) and pH management per crop species. Over- or under-dosing causes rapid crop failure and wastes resources in nutrient solutions that cannot be easily discarded without environmental impact.
3. **System selection paralysis:** NFT, DWC, Aeroponics, and Kratky each suit different crops, space shapes, budgets, and skill levels. No single resource guides the selection decision with scored tradeoffs.
4. **Climate coupling:** VPD (Vapor Pressure Deficit) — the primary driver of transpiration, nutrient uptake, and disease pressure — varies daily with real temperature/humidity. Generic grow guides ignore this relationship.
5. **Knowledge fragmentation:** Best-practice literature spans FAO reports, MDPI Horticulturae journal articles, USDA ARS publications, and RUAF briefs. A self-updating knowledge base aggregating these sources is currently unavailable to the average urban grower.

This skill solves all five problems in a single structured workflow.

---

## Target Users & Use Cases

### Primary Users
- Urban apartment dwellers (balcony growers, beginner–intermediate)
- Rooftop farm designers (community/commercial, intermediate–advanced)
- Agricultural extension officers advising urban clients
- Urban farming NGOs building replicable pilot models

### Specific Trigger Examples

| User Says | Skill Does |
|-----------|-----------|
| "I have a 3 m × 1.5 m south-facing balcony in Ho Chi Minh City and want to grow lettuce and herbs" | Runs sub-profile-intake → sub-system-designer (Kratky/NFT recommendation) → sub-scoring-engine → sub-improvement-roadmap → full design PDF-ready report |
| "My Bangkok rooftop is 20 m² with partial shade from a water tank. What system should I choose?" | Intake collects shade pattern → system-designer calculates effective DLI after obstruction → scores NFT vs DWC vs Aeroponics → recommends with rationale |
| "My hydroponic lettuce keeps yellowing after week 2. EC is 1.4 mS/cm" | Scores against optimal EC range (1.2–2.0 mS/cm for lettuce) → checks pH range → improvement roadmap flags likely iron deficiency or root zone temperature issue |
| "I want to grow strawberries on my 5 m² terrace in Seoul" | Validates DLI requirements for strawberries (12–16 mol/m²/day) against Seoul latitude + season → recommends supplemental LED if DLI insufficient → calculates energy cost |
| "Design a zero-budget aquaponics setup on my rooftop" | Flags aquaponics as out of scope (sub-system-designer redirects to NFT Kratky low-cost variant) → produces budget-optimized design |

---

## Harness Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   micro-urban-agriculture-design (main.md)              │
│                              HARNESS ENTRY                              │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │   sub-profile-intake    │
                    │  (space, crops, climate,│
                    │   budget, experience)   │
                    └────────────┬────────────┘
                                 │ Profile JSON
                    ┌────────────▼────────────┐
                    │   sub-system-designer   │
                    │  (DLI calc, VPD check,  │
                    │   system selection,     │
                    │   nutrient schedule,    │
                    │   water/energy budget)  │
                    └────────────┬────────────┘
                                 │ Design Spec
                    ┌────────────▼────────────┐
                    │   sub-scoring-engine    │
                    │  (FAO/DLI/VPD/EC-pH/   │
                    │   water-use/yield/      │
                    │   structural safety)    │
                    └────────────┬────────────┘
                                 │ Scored Design
                    ┌────────────▼────────────┐
                    │   Devil's Advocate       │
                    │  (Challenge assumptions, │
                    │   surface failure modes) │
                    └────────────┬────────────┘
                                 │ Validated Design
                    ┌────────────▼────────────┐
                    │  sub-improvement-roadmap│
                    │  (Ranked improvements,  │
                    │   effort×impact matrix, │
                    │   milestone schedule)   │
                    └────────────┬────────────┘
                                 │ Roadmap
                    ┌────────────▼────────────┐
                    │   FINAL DELIVERABLE     │
                    │  (Professional Design   │
                    │   Report + Action Plan) │
                    └─────────────────────────┘
```

---

## Full Sub-Skill Catalog

### sub-profile-intake
- **Purpose:** Collect all inputs needed to design the system
- **Inputs:** User's conversational description of their space and goals
- **Outputs:** Structured profile JSON (space_m2, orientation, latitude/longitude, city, target_crops[], budget_usd, experience_level, preferred_system, shading_description, local_climate_zone)
- **Tools Used:** WebSearch (weather API for location climate), Read (SECOND-KNOWLEDGE-BRAIN.md fallback)
- **Quality Gate:** All required fields populated; latitude/longitude resolved; at least one target crop specified

### sub-system-designer
- **Purpose:** Produce a complete technical system design
- **Inputs:** Profile JSON from sub-profile-intake
- **Outputs:** Design Specification (system_type, layout_diagram, container_specs, grow_medium, lighting_plan_with_DLI_calc, nutrient_schedule_with_EC_pH, water_budget_L_per_week, energy_budget_kWh_per_week, planting_density, expected_yield_g_per_week)
- **Tools Used:** WebSearch (OpenWeatherMap for local solar irradiance, humidity), WebFetch (DLI tables from USDA, VPD charts), Read (SECOND-KNOWLEDGE-BRAIN.md)
- **Quality Gate:** DLI target met or supplemental lighting specified; EC/pH within crop-appropriate range; water budget calculated; system selection justified against alternatives

### sub-scoring-engine
- **Purpose:** Multi-dimensional scoring of the design against world-renowned standards
- **Inputs:** Design Specification
- **Outputs:** Scored Report (7-dimension score matrix, overall composite score /100, top 3 strengths, top 3 weaknesses, benchmark citations)
- **Tools Used:** Read (SECOND-KNOWLEDGE-BRAIN.md — frameworks section), WebFetch (FAO guidelines, MDPI papers)
- **Quality Gate:** All 7 dimensions scored; each score anchored to a named framework; overall score computed; strengths and weaknesses cited

### sub-improvement-roadmap
- **Purpose:** Translate scoring gaps into a prioritized, actionable improvement plan
- **Inputs:** Scored Report, Profile JSON
- **Outputs:** Improvement Roadmap (ranked improvement items: priority rank, improvement title, effort estimate, expected yield-impact %, cost estimate, implementation timeline, framework citation)
- **Tools Used:** Read (SECOND-KNOWLEDGE-BRAIN.md), WebSearch (supplemental LED pricing, nutrient solution costs)
- **Quality Gate:** At least 5 improvements listed; each with effort AND impact quantified; ranked by impact/effort ratio; all claims cited

---

## Skill File Format Specification

### Frontmatter Schema (all skill files)
```yaml
---
name: micro-urban-agriculture-design   # or sub-skill slug
description: One-line summary for /help and skill picker
---
```

### Required Sections (main.md)
1. `## Role & Persona` — who Claude becomes
2. `## Workflow` — numbered step-by-step harness flow
3. `## Sub-skills Available` — list of sub-skill files
4. `## Tools` — tools used with purpose
5. `## Output Format` — exact structure of final deliverable
6. `## Quality Gates` — pass/fail checklist before output

### Required Sections (sub-*.md)
1. `## Purpose`
2. `## Inputs`
3. `## Workflow` (numbered steps)
4. `## Outputs`
5. `## Quality Gate`

---

## E2E Execution Flow

```
1. User invokes /micro-urban-agriculture-design
2. Harness greets user, explains what data it needs
3. sub-profile-intake runs:
   a. Prompts for space (dimensions, orientation, floor type)
   b. Prompts for location (city or lat/lon)
   c. WebSearch → fetch local climate zone, average monthly solar irradiance, humidity
   d. Prompts for target crops (species list)
   e. Prompts for budget (USD) and experience level (beginner/intermediate/advanced)
   f. Prompts for preferred system (if any preference)
   g. Produces Profile JSON → quality gate check
4. sub-system-designer runs:
   a. Calculates DLI for each crop species at user's latitude + season
   b. Checks VPD range against local temperature/humidity (WebSearch weather API)
   c. Selects optimal system type (NFT/DWC/Kratky/Aeroponics) with justification matrix
   d. Designs layout (plant positions, reservoir size, pump specs if needed)
   e. Builds nutrient schedule (week-by-week EC/pH targets per crop stage)
   f. Calculates water budget (L/week) and energy budget (kWh/week)
   g. Estimates yield (g/week/m²) based on DLI + system efficiency benchmarks
   h. Quality gate → missing data triggers graceful degradation to SECOND-KNOWLEDGE-BRAIN fallback
5. sub-scoring-engine runs:
   a. Scores against 7 dimensions (see Quality Gates)
   b. Looks up benchmark values from SECOND-KNOWLEDGE-BRAIN.md + live WebFetch
   c. Produces score matrix + top 3 strengths + top 3 weaknesses
6. Devil's Advocate phase (inline, not a sub-skill):
   a. Challenge: "What if local solar irradiance is lower than API average due to air pollution?"
   b. Challenge: "What if user's water source has high chlorine/fluoride affecting pH?"
   c. Challenge: "What if structural load of full reservoirs exceeds balcony load limit?"
   d. Integrate responses into design adjustments
7. sub-improvement-roadmap runs:
   a. Maps score gaps to specific improvement actions
   b. Estimates effort (hours + USD cost) per improvement
   c. Quantifies expected yield-impact (%)
   d. Ranks by impact/effort ratio (Pareto principle)
   e. Produces milestone timeline (Week 1 / Month 1 / Month 3 / Year 1)
8. Harness synthesizes final deliverable:
   a. Executive summary (5 bullet points)
   b. System design specification (full technical detail)
   c. Score card (7-dimension matrix)
   d. Improvement roadmap (ranked table)
   e. Appendix: DLI calculation, VPD chart, EC/pH schedule, water budget
9. Quality gates checked → output presented
```

**Error Handling:**
- WebSearch/WebFetch unavailable → fall back to SECOND-KNOWLEDGE-BRAIN.md, flag limitation in output header
- Location not found → request manual lat/lon entry; use USDA Plant Hardiness Zone lookup fallback
- Budget = 0 → route to Kratky (passive, zero-infrastructure) design path
- Crop DLI requirement impossible at location → flag incompatibility, suggest indoor LED supplement or crop substitution

---

## SECOND-KNOWLEDGE-BRAIN Integration

The `SECOND-KNOWLEDGE-BRAIN.md` file is referenced at every sub-skill stage as the primary offline knowledge source. When WebSearch/WebFetch are available, they supplement and update this base. The crawl pipeline (`tools/knowledge_updater.py`) runs weekly and appends new entries, ensuring the knowledge base reflects the current state of the art.

**Crawl Configuration:**
- Sources: MDPI Horticulturae RSS, ArXiv q-bio.QM, FAO UA news, RUAF newsletters, USDA ARS publications
- Keywords: hydroponics, aeroponics, DLI, NFT, DWC, Kratky, urban agriculture, soilless cultivation, nutrient solution, VPD, EC pH
- Frequency: Weekly (recommended cron: `0 6 * * 1` — Monday 06:00 UTC)
- Append format: Markdown table row in Key Research Papers section + text snippet in State-of-the-Art Methods

---

## Supporting Tools Specification

### `tools/knowledge_updater.py`
- **Inputs:** None (self-contained; reads config from top-level constants)
- **Outputs:** Appended rows to `SECOND-KNOWLEDGE-BRAIN.md` sections: Key Research Papers table, State-of-the-Art Methods, Knowledge Update Log
- **Dependencies:** `crawl4ai`, `feedparser`, `requests`, `hashlib`, `datetime`, `pathlib`
- **Schedule:** Weekly cron
- **Deduplication:** SHA-256 hash of (DOI or URL) stored in a local `.knowledge_index.json`; duplicate hashes skip append
- **Relevance scoring:** Title + abstract keyword match against domain keyword list; minimum score 0.3 to include

---

## Quality Gates

Final output is blocked until ALL of the following pass:

| # | Gate | Pass Criterion |
|---|------|---------------|
| 1 | DLI Compliance | Every target crop's DLI requirement is either met by natural light at the user's location/season OR a supplemental LED plan is specified with wattage and photoperiod |
| 2 | VPD Range | Calculated VPD at user's location falls within the optimal range for target crops OR HVAC/misting recommendations are provided |
| 3 | Nutrient Schedule | EC and pH targets specified per crop species per growth stage (seedling / vegetative / fruiting/harvest) |
| 4 | Water Budget | Weekly water consumption (L) calculated and compared to local water cost and availability |
| 5 | System Justification | Chosen system type (NFT/DWC/Kratky/Aeroponics) justified against at least 2 alternatives with scored comparison |
| 6 | Score Completeness | All 7 scoring dimensions have numeric scores; no dimension left blank |
| 7 | Roadmap Quantification | Every improvement item has: effort (hours + USD), expected yield-impact (%), and timeline (week/month) |
| 8 | Citation Coverage | Every claim references either: (a) a named framework (FAO, DLI table, VPD chart, ISO), (b) a paper in SECOND-KNOWLEDGE-BRAIN.md, or (c) a live WebFetch result |
| 9 | Safety Check | Structural load assessment flag checked; electrical load for lighting/pumps within standard residential circuit limits |
| 10 | Graceful Degradation Flag | If any web resource was unavailable, output header clearly states which data points are from internal knowledge base only |

---

## Test Scenarios

See `tests/test-scenarios.md` for full scenarios. Summary:

1. Beginner balcony grower, tropical city, lettuce + basil
2. Intermediate rooftop grower, temperate city, strawberries + cherry tomatoes
3. Advanced commercial rooftop, subtropical, mixed leafy greens at scale
4. Zero-budget grower, equatorial, single crop (spinach), Kratky path
5. Edge case: north-facing balcony with <2 DLI natural light — full LED dependency
6. Edge case: salt water region (high TDS tap water) — water treatment requirement
7. Crop incompatibility: user requests tropical and cold-climate crops simultaneously

---

## Key Design Decisions

1. **DLI as primary design driver:** DLI (Daily Light Integral, mol/m²/day) is the single most impactful variable for yield in soilless systems. All system recommendations derive from DLI compatibility first, then EC/pH, then water use.
2. **Real weather data over averages:** The skill fetches real local solar irradiance and humidity data rather than relying on generic climate zone averages, dramatically improving DLI and VPD accuracy.
3. **System selection is scored, not opinionated:** NFT vs DWC vs Kratky vs Aeroponics is resolved by a scored comparison matrix (5 criteria: cost, skill required, maintenance, crop compatibility, water efficiency) — not a single recommendation.
4. **Budget paths:** The harness has explicit routing for zero/low/medium/high budget, ensuring Kratky/passive designs are first-class outputs, not afterthoughts.
5. **Safety gates are mandatory:** Structural load and electrical safety checks are non-optional quality gates — urban rooftop farming has caused structural failures in unassessed buildings.
6. **Aquaponics out of scope:** Fish system management adds a biological variable that requires a separate skill (flagged as future extension). The skill notes this boundary and redirects.
7. **Offline-first design:** SECOND-KNOWLEDGE-BRAIN.md seeds enough domain knowledge that the skill produces useful output even when all web tools are unavailable.
8. **Weekly crawl over continuous:** crawl4ai pipeline runs weekly (not real-time) to respect API rate limits, avoid duplicate noise, and produce a stable knowledge base between updates.
