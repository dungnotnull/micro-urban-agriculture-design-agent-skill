# test-scenarios.md — Skill #232: Micro Urban Agriculture Design & Management

Test scenarios for validating the `micro-urban-agriculture-design` skill harness. Each scenario defines the input profile, expected behavior at each sub-skill stage, expected output content, and pass/fail criteria.

---

## Scenario 1: Beginner Balcony Grower — Tropical City, Leafy Greens

**Description:** The most common beginner use case. A first-time grower in Ho Chi Minh City with a modest south-facing balcony wants to grow lettuce and basil. Budget is tight; no prior hydroponic experience.

**Input Profile:**
- Space: Balcony, 3m × 1.5m (4.5 m²), South-facing
- Location: Ho Chi Minh City, Vietnam (Lat 10.8°N)
- Shade: 20% by overhang 11am–1pm
- Target crops: Lettuce, Basil
- Budget: $80
- Experience: Beginner
- Maintenance: 2h/week available
- Water: Municipal tap (TDS ~200 ppm)
- Power: Available

**Expected Behavior:**

| Step | Sub-skill | Expected Behavior |
|------|-----------|------------------|
| 1 | sub-profile-intake | Resolves HCMC lat/lon; fetches tropical climate data; confirms 2 crops in profile JSON |
| 2 | sub-system-designer | Recommends Kratky (budget + beginner + leafy greens); calculates DLI ~28–35 mol/m²/day for tropical latitude; finds DLI adequate for both crops year-round; calculates EC 0.8–1.2 (seedling) → 1.6–2.0 (vegetative) for lettuce; water budget ~8–12 L/week; zero energy budget (passive) |
| 3 | sub-scoring-engine | D2 (DLI): 90+ (tropical DLI exceeds lettuce optimal); D4 (nutrients): 85+ (correct EC/pH); D7 (safety): 85+ (Kratky tubs are light); composite score ~83–88 |
| 4 | Devil's Advocate | Challenges: (1) Monsoon season cloud cover may reduce DLI July–September → design should flag this; (2) TDS 200 ppm → start EC already 0.2 mS/cm → adjust nutrient dosing accordingly |
| 5 | sub-improvement-roadmap | Top improvement: extend photoperiod with 20W LED in Jul–Sep cloudy months; second: add pH buffer to maintain 6.0–6.5 despite HCMC alkaline tap water tendency |

**Expected Output Content:**
- System: Kratky tubs (4×5L tubs, 20 plant sites)
- DLI analysis confirms tropical DLI 28–35 mol/m²/day — both crops well above threshold
- VPD note: 1.2–1.6 kPa in HCMC — slightly high in dry season April–May; recommend shade cloth
- Yield estimate: ~600g/week (lettuce 400g + basil 200g)
- Equipment list within $80 budget
- Composite score: 83–88

**Pass Criteria:**
- [ ] Kratky is recommended (correct system for beginner + budget + leafy)
- [ ] DLI calculation is within ±10% of 30 mol/m²/day reference for HCMC
- [ ] Monsoon DLI flag is present in the design
- [ ] EC/pH schedule covers seedling and vegetative stages for both crops
- [ ] Output is a professional report, not a conversational reply
- [ ] Total equipment cost ≤ $80

---

## Scenario 2: Intermediate Rooftop Grower — Temperate City, Mixed Fruiting + Leafy

**Description:** A grower in Seoul, South Korea has a 20 m² rooftop garden. They want cherry tomatoes and lettuce year-round. They have intermediate experience and a moderate budget. Seasonal DLI variation at 37°N is extreme.

**Input Profile:**
- Space: Rooftop, 4m × 5m (20 m²), Southeast-facing
- Location: Seoul, South Korea (Lat 37.5°N)
- Shade: 10% by water tank shadow
- Target crops: Cherry Tomato, Lettuce
- Budget: $600
- Experience: Intermediate
- Maintenance: 4h/week available
- Water: Municipal tap (TDS ~150 ppm)
- Power: Available (220V)

**Expected Behavior:**

| Step | Sub-skill | Expected Behavior |
|------|-----------|------------------|
| 1 | sub-profile-intake | Resolves Seoul lat/lon; identifies temperate continental climate; flags extreme seasonal DLI variation; notes crop incompatibility risk (tomato DLI 25–30, lettuce DLI 12–17 — different optima but manageable in separate zones) |
| 2 | sub-system-designer | Recommends NFT (intermediate + space + fruiting crops); calculates DLI: summer (June) ~35 mol/m²/day adequate for both; winter (December) ~8 mol/m²/day → far below tomato DLI minimum (20) → supplemental LED required for tomato in winter; recommends separate NFT zones for tomato and lettuce; LED: 120W for tomato zone in winter |
| 3 | sub-scoring-engine | D2 (DLI): 65 (significant winter LED gap for tomato); D6 (yield): 72 (winter tomato yield reduction); composite score ~76–80 (Good) |
| 4 | Devil's Advocate | Challenges: (1) Seoul has significant air pollution (fine dust) in spring — may reduce effective DLI 15–20% in March–April; (2) Rooftop wind exposure at 20 m² may cause high VPD in summer → misting required; (3) Winter temperatures (-5 to 0°C) may require insulation around reservoir to prevent root zone cooling |
| 5 | sub-improvement-roadmap | Priority 1: Install 120W LED for tomato zone (Dec–Feb); Priority 2: Add wind netting for VPD control; Priority 3: Install reservoir insulation for winter |

**Expected Output Content:**
- System: NFT (separate zones — 12 tomato sites, 36 lettuce sites)
- DLI deficit: November–February for tomatoes; supplemental 120W LED plan
- Seasonal crop rotation option: replace tomatoes with spinach/kale in winter (DLI 8–10)
- VPD alert: June–August outdoor VPD may reach 1.8–2.0 kPa → misting system recommended
- Winter temperature alert: root zone insulation for below-5°C nights
- Composite score: 76–80

**Pass Criteria:**
- [ ] Seasonal DLI table covers all 12 months with Korean climate data
- [ ] Supplemental LED wattage is calculated (not just mentioned)
- [ ] Crop incompatibility (DLI mismatch) is noted and resolved (separate zones)
- [ ] Winter root zone temperature risk is flagged (Devil's Advocate or design)
- [ ] NFT system is recommended over Kratky (intermediate + fruiting + space → correct)
- [ ] Composite score difference between summer and winter designs is shown

---

## Scenario 3: Advanced Commercial Rooftop — Subtropical, Mixed Leafy at Scale

**Description:** An NGO is designing a 60 m² commercial-scale rooftop hydroponics system in Bangkok (14°N, subtropical) to supply 100 households with leafy greens. They have advanced technical staff and a $3,000 budget.

**Input Profile:**
- Space: Rooftop, 10m × 6m (60 m²), South-facing
- Location: Bangkok, Thailand (Lat 13.75°N)
- Shade: 5% by stairwell housing
- Target crops: Lettuce (multi-variety), Spinach, Pak Choi
- Budget: $3,000
- Experience: Advanced
- Maintenance: 20h/week (team effort)
- Water: Municipal tap (TDS ~250 ppm)
- Power: Available (220V, 3-phase available)

**Expected Behavior:**

| Step | Sub-skill | Expected Behavior |
|------|-----------|------------------|
| 1 | sub-profile-intake | Identifies commercial-scale rooftop; Bangkok subtropical climate; flags rainy season cloud cover (July–September) reducing DLI by ~20% |
| 2 | sub-system-designer | Recommends NFT wall panel system for maximum density; calculates 200+ plant sites across 30 m² growing area; conservative 30 m² walkway/service; nutrient dosing automation recommended at commercial scale |
| 3 | sub-scoring-engine | D5 (water efficiency): 90+ (NFT recirculating, large scale); D6 (yield): 88 (good DLI + density); composite score ~87–91 |
| 4 | Devil's Advocate | Challenges: (1) Bangkok has periodic power outages — NFT pump failure kills root zone in <2h; (2) Commercial scale requires Thai food safety certification (GMP/HACCP) — FAO UA guidelines apply; (3) 60 m² rooftop structural assessment is non-optional at commercial scale |
| 5 | sub-improvement-roadmap | Priority 1: Install UPS/backup power for pumps; Priority 2: Obtain GMP certification; Priority 3: Commission professional structural engineering report |

**Expected Output Content:**
- System: NFT with 240+ plant sites, automated EC/pH dosing
- Commercial food safety compliance section citing FAO UA + Thai food safety regulations
- Structural engineering assessment flagged as mandatory (not optional)
- Yield projection: ~8–12 kg leafy greens/day (~56–84 kg/week)
- Backup power recommendation: UPS (600VA, 30-min runtime for pumps)
- Composite score: 87–91

**Pass Criteria:**
- [ ] Commercial scale triggers food safety compliance flag (D1 prominently featured)
- [ ] Structural engineering assessment flagged as mandatory
- [ ] Backup power recommendation appears in roadmap
- [ ] Yield projection is stated per day and per week (commercial format)
- [ ] Nutrient schedule is designed for multi-variety system (overlapping EC/pH ranges)
- [ ] Budget is within scope ($3,000) with detailed breakdown

---

## Scenario 4: Zero-Budget Grower — Equatorial, Single Crop, Passive System

**Description:** A student in Singapore (1.35°N, equatorial) has a 2 m² apartment windowsill / small balcony. Budget is literally $0. They want to grow spinach. This should route exclusively to the Kratky passive path.

**Input Profile:**
- Space: Balcony/windowsill, 1m × 2m (2 m²), East-facing
- Location: Singapore (Lat 1.35°N)
- Shade: 40% by adjacent building from 10am onward
- Target crops: Spinach
- Budget: $0
- Experience: Beginner
- Maintenance: 1h/week
- Water: Tap (TDS ~80 ppm — Singapore water quality is excellent)
- Power: Limited (no dedicated socket near window)

**Expected Behavior:**

| Step | Sub-skill | Expected Behavior |
|------|-----------|------------------|
| 1 | sub-profile-intake | Zero budget flag triggers Kratky path; East-facing + 40% shade → significant DLI reduction |
| 2 | sub-system-designer | Kratky is the ONLY option (zero budget, no power, beginner); calculates East-facing DLI: Singapore receives ~40 mol/m²/day clear-sky equatorial, but East-facing at 40% shade → effective ~10–12 mol/m²/day in growing window (6am–10am); spinach DLI min = 8 → barely adequate; notes growth will be slower than optimal |
| 3 | sub-scoring-engine | D2 (DLI): 62 (adequate but not optimal — East-facing shade constraint); D6 (yield): 58 (below median due to DLI limitation); D7 (safety): 95 (Kratky tubs minimal weight); composite score ~73–77 |
| 4 | Devil's Advocate | Challenges: (1) Heavy equatorial rainfall may flood uncovered Kratky tubs — recommend cover; (2) East-facing gets direct sun only in morning — check if UVA/UVB through glass (if window) reduces PAR significantly |
| 5 | sub-improvement-roadmap | Priority 1: Expose plants to more light (reposition to South-facing neighbor's balcony if possible); Priority 2: Use recycled 5L water bottles as Kratky containers (TRUE zero cost); Priority 3: If $15 becomes available, add 9W LED clip-on for afternoon supplement |

**Expected Output Content:**
- System: Kratky using recycled containers (zero-cost specification)
- DLI: East-facing constrained to ~10–12 mol/m²/day — adequate for spinach
- Yield: ~150–200g/week (slower cycle due to DLI)
- Equipment list: $0 (recycled bottles, tap water, free nutrient solution alternatives noted — e.g., compost tea, though flag hydroponics-specific limitation)
- Rainfall protection recommendation
- Composite score: 73–77

**Pass Criteria:**
- [ ] Zero budget correctly routes to Kratky (no pump, no LED recommended as primary path)
- [ ] East-facing DLI calculation is performed (not just defaulting to Singapore's peak DLI)
- [ ] Shade factor reduces DLI to East-facing morning window equivalent
- [ ] DLI is within spinach minimum threshold — design is valid (not rejected)
- [ ] Recycled container specification appears in equipment list at $0 cost
- [ ] Report acknowledges limitations clearly without being discouraging

---

## Scenario 5: Edge Case — North-Facing Balcony, <2 DLI Natural Light (Full LED Dependency)

**Description:** A user in Berlin (52.5°N) has a north-facing balcony. In December, north-facing surfaces at this latitude receive essentially zero direct sunlight. The skill must correctly identify this extreme DLI deficit and design a full LED-dependent indoor-style system.

**Input Profile:**
- Space: Balcony, 2m × 1m (2 m²), North-facing
- Location: Berlin, Germany (Lat 52.5°N)
- Shade: None (but north-facing)
- Target crops: Lettuce, Herbs
- Budget: $300
- Experience: Intermediate
- Maintenance: 3h/week
- Power: Available (220V)

**Expected Behavior:**

| Step | Sub-skill | Expected Behavior |
|------|-----------|------------------|
| 1 | sub-profile-intake | Flags: "North-facing at 52.5°N — extreme DLI limitation in winter months; supplemental LED will be required year-round for most crops" |
| 2 | sub-system-designer | Calculates winter (December) DLI: Berlin latitude ~2–3 h effective daylight north-facing; effective DLI ≈ 0.5–1.5 mol/m²/day — far below lettuce minimum (6); Summer (June) DLI may reach 6–8 mol/m²/day north-facing; therefore: full LED operation required November–March; partial LED supplement required April–October |
| 3 | sub-scoring-engine | D2 (DLI): 45 without LED plan (failing); D2: 78 with LED plan (passing); highlights that this design is fundamentally LED-dependent and energy cost is significant |
| 4 | Devil's Advocate | Challenges: (1) Berlin winter temperatures on exposed balcony: -5 to 5°C → root zone must be insulated or system moved indoors; (2) Full LED dependency means energy cost may exceed food value produced — calculate break-even |
| 5 | sub-improvement-roadmap | Priority 1: Move system indoors (window or spare room) to eliminate temperature risk; Priority 2: Full-spectrum 60W LED on 16h photoperiod; Priority 3: Insulate reservoir |

**Expected Output Content:**
- Full LED dependency design (60W LED, 16h photoperiod)
- Winter DLI from natural light: <2 mol/m²/day (clearly stated)
- Energy cost calculation: 60W × 16h × 30 days = 28.8 kWh/month (~€8–10/month at German electricity rates)
- Break-even analysis: ~500g lettuce/month vs. €0.50/500g retail → energy cost exceeds food value → flag "grow high-value herbs (basil/microgreens) to improve ROI"
- Root zone temperature warning (sub-5°C)
- Composite score: 70–75 (design is viable but constrained)

**Pass Criteria:**
- [ ] North-facing DLI at 52.5°N is correctly calculated as <2 mol/m²/day in winter (not generic European average)
- [ ] D2 score reflects DLI deficit (low without LED, improved with LED plan)
- [ ] Energy cost of LED operation is calculated in euros
- [ ] Break-even analysis appears (energy cost vs. food value)
- [ ] Root zone temperature warning is present
- [ ] High-value crop substitution (basil/microgreens) is recommended for ROI improvement
- [ ] Score without LED plan clearly distinguished from score with LED plan

---

## Scenario 6: Edge Case — High TDS Tap Water (Salt Water Region)

**Description:** A grower in a coastal area of the UAE (Dubai, 25.2°N) has high-TDS municipal water (estimated 600–800 ppm / 0.9–1.2 mS/cm). This significantly constrains nutrient addition before hitting crop EC maximums.

**Input Profile:**
- Space: Rooftop terrace, 8m × 4m (32 m²), South-facing
- Location: Dubai, UAE (Lat 25.2°N)
- Shade: None (open desert rooftop)
- Target crops: Lettuce, Basil
- Budget: $400
- Experience: Intermediate
- Water: Municipal tap (TDS ~700 ppm / EC ~1.1 mS/cm)
- Power: Available (220V)

**Expected Behavior:**

| Step | Sub-skill | Expected Behavior |
|------|-----------|------------------|
| 1 | sub-profile-intake | Flags: "Water TDS 700 ppm (EC ~1.1 mS/cm) is extremely high — this alone approaches or exceeds lettuce EC maximum before any nutrients are added. Reverse osmosis filtration is required." |
| 2 | sub-system-designer | RO filter specification included in design (mandatory, not optional); notes that without RO, nutrient addition would push EC to 2.0+ mS/cm at seedling stage → toxicity risk; Also: Dubai VPD June–September: 2.5–4.0 kPa (extreme) → shade cloth and misting essential |
| 3 | sub-scoring-engine | D1 (Food Safety): 55 without RO filter (failing — high TDS water carries unknown salinity mix); D4 (Nutrients): 40 without RO (EC incompatible with crops); D3 (VPD): 45 without misting in summer |
| 4 | Devil's Advocate | Challenges: (1) RO filter adds $80–150 to budget — does this exceed user's budget? If yes, system is not viable without either budget increase or crop change to salt-tolerant species; (2) Dubai summer temperatures (40–48°C) may cause root zone heat damage — insulated reservoir or chiller required |
| 5 | sub-improvement-roadmap | Priority 1 (MANDATORY): Install RO filter ($80–150, 1-time cost); Priority 2: Shade cloth (50% block) for summer VPD control; Priority 3: Insulate reservoir (reflective wrap) for root zone temperature |

**Expected Output Content:**
- RO filter requirement as non-negotiable design element (D1 gate would fail without it)
- Water quality warning prominently placed
- Post-RO nutrient schedule (TDS ~10–30 ppm after RO → full nutrient range available)
- Summer VPD alert: 2.5–4.0 kPa — severe; mandatory shade + misting
- Summer temperature alert: root zone >30°C degrades NFT/DWC significantly
- Composite score without RO: ~50–55 (failing); with RO: ~80–85 (Good)

**Pass Criteria:**
- [ ] High TDS is flagged in sub-profile-intake (not silently ignored)
- [ ] D1 and D4 scores reflect water quality failure without RO
- [ ] RO filter is listed as Priority 1 mandatory improvement (not optional)
- [ ] Post-RO nutrient schedule is provided
- [ ] Dubai summer VPD is calculated and flagged as extreme
- [ ] Root zone temperature warning is present
- [ ] Composite score is shown both without and with RO filter treatment

---

## Scenario 7: Crop Incompatibility — Mixed Tropical and Cool-Season Crops

**Description:** A user in a mixed-climate region (Hanoi, Vietnam, 21°N — has both hot summers and cold winters) wants to grow both cherry tomatoes (heat-loving, high DLI) and spinach (cool-season, lower DLI) in the same system simultaneously. This creates a fundamental system design conflict.

**Input Profile:**
- Space: Balcony, 3m × 2m (6 m²), South-facing
- Location: Hanoi, Vietnam (Lat 21.0°N)
- Target crops: Cherry Tomato AND Spinach (simultaneously requested)
- Budget: $200
- Experience: Beginner

**Expected Behavior:**

| Step | Sub-skill | Expected Behavior |
|------|-----------|------------------|
| 1 | sub-profile-intake | Flags incompatibility: "Cherry tomato optimal EC: 2.0–3.5 mS/cm; spinach optimal EC: 1.6–2.2 mS/cm. Tomato EC upper range exceeds spinach tolerance in fruiting stage. Additionally, tomato prefers VPD 1.0–1.5 kPa; spinach prefers cooler, higher humidity conditions. Growing simultaneously in one system requires compromise EC — recommend separate systems or seasonal rotation." |
| 2 | sub-system-designer | Two design paths presented: (A) Separate systems — small DWC for tomato + Kratky for spinach; (B) Seasonal rotation — spinach Oct–March (cool season), tomato April–September (hot season); evaluates both against budget |
| 3 | sub-scoring-engine | Simultaneous single-system design scores D4: 40 (nutrient incompatibility); Separate system design scores D4: 85; Seasonal rotation design scores D4: 90 |
| 4 | Devil's Advocate | Challenges: "Beginners rarely maintain two separate systems well. Is seasonal rotation the more realistic recommendation despite slightly lower annual yield diversity?" |
| 5 | sub-improvement-roadmap | Primary recommendation: seasonal rotation (simpler for beginner, resolves incompatibility); secondary: plan for separate Kratky tubs if user upgrades experience level |

**Expected Output Content:**
- Incompatibility clearly explained with EC/temperature data
- Two design paths with scored comparison
- Seasonal rotation plan (Hanoi: hot season April–September → tomato; cool season October–March → spinach/kale)
- Budget allocation if separate systems chosen ($120 tomato DWC + $60 spinach Kratky)
- Beginner recommendation: seasonal rotation (lower complexity)
- Composite score for each path clearly separated

**Pass Criteria:**
- [ ] Crop incompatibility is identified in sub-profile-intake (not deferred to end)
- [ ] Two design paths are presented (not a single forced choice)
- [ ] EC conflict is quantified (specific mS/cm ranges cited for both crops)
- [ ] Seasonal rotation calendar is Hanoi-specific (not generic)
- [ ] Beginner experience level influences the recommendation (rotation > dual-system)
- [ ] Both paths have separate composite scores
