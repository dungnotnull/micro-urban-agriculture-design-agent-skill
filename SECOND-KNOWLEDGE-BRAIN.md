# SECOND-KNOWLEDGE-BRAIN.md — Skill #232: Micro Urban Agriculture Design & Management

> Self-improving domain knowledge base. Updated weekly by `tools/knowledge_updater.py`.
> Last manual seed: 2026-06-19. Next automated update: 2026-06-26.

---

## 1. Core Concepts & Frameworks

### 1.1 Daily Light Integral (DLI)

DLI measures the cumulative amount of photosynthetically active radiation (PAR, 400–700 nm) received by a plant surface over a 24-hour period.

**Formula:**
```
DLI (mol/m²/day) = PPFD (μmol/m²/s) × photoperiod (hours) × 3600 / 1,000,000
```

**DLI Requirements by Crop Category:**

| Crop | Min DLI (mol/m²/day) | Optimal DLI | Notes |
|------|---------------------|-------------|-------|
| Lettuce | 6 | 12–17 | Bolts above 20 DLI |
| Spinach | 8 | 14–16 | Shade-tolerant |
| Basil | 12 | 18–24 | Heat-sensitive above 30°C |
| Mint | 8 | 12–16 | Very shade-tolerant |
| Kale | 10 | 15–20 | — |
| Cherry Tomato | 20 | 25–30 | Requires supplemental light in most urban settings |
| Strawberry | 12 | 16–20 | Cool-season fruiting improved by chilling hours |
| Cucumber | 20 | 25–30 | High light demand |
| Chili Pepper | 18 | 22–28 | — |
| Pak Choi / Bok Choy | 8 | 12–16 | Fast-cycling crop |
| Cilantro/Coriander | 8 | 12–16 | Bolts at high temperatures |
| Green Onion/Chive | 6 | 10–14 | — |
| Swiss Chard | 8 | 14–18 | — |
| Arugula | 6 | 10–14 | Very fast cycle (21–28 days) |
| Parsley | 8 | 12–16 | Slow germination |
| Watercress | 6 | 10–12 | Aquatic/semi-aquatic — ideal for Kratky |
| Microgreens (mixed) | 10 | 16–20 | Very short cycle (7–14 days) |

**Reference solar irradiance by latitude (clear sky, summer noon peak):**

| Latitude | City Example | Peak PPFD (μmol/m²/s) | Avg Daily DLI (clear) |
|----------|-------------|----------------------|----------------------|
| 0–10°N | Singapore, Nairobi | 1800–2000 | 45–55 |
| 10–20°N | HCMC, Mumbai, Hanoi | 1600–1900 | 38–50 |
| 20–30°N | Bangkok, Guangzhou | 1400–1800 | 30–45 |
| 30–35°N | Seoul, Tokyo, Shanghai | 1200–1600 | 20–35 |
| 40–50°N | Paris, Berlin, Vancouver | 900–1400 | 12–25 (seasonal) |

Note: Urban shading reduces effective DLI by 20–60% depending on building density and obstruction angle.

---

### 1.2 Vapor Pressure Deficit (VPD)

VPD is the difference between the amount of moisture the air can hold at saturation and the amount actually present. It drives plant transpiration, nutrient uptake, and disease susceptibility.

**Formula:**
```
VPD (kPa) = SVP × (1 - RH/100)
SVP (kPa) = 0.6108 × exp(17.27 × T / (T + 237.3))   [T in °C]
```

**Optimal VPD ranges by growth stage:**

| Stage | Optimal VPD (kPa) | Risk if Too Low | Risk if Too High |
|-------|-------------------|-----------------|-----------------|
| Seedling / Clone | 0.4–0.8 | Mold / damping off | Desiccation / slow rooting |
| Vegetative | 0.8–1.2 | Mold / poor Ca uptake | Stomatal closure / wilt |
| Flowering / Fruiting | 1.0–1.5 | Bud rot, poor pollination | Blossom drop, bitterness |
| Late fruiting / harvest | 1.2–1.6 | — | Tipburn (lettuce) |

**Management interventions:**
- High VPD (hot/dry): misting, shade cloth, shade netting, timing of nutrient dosing to cooler morning hours
- Low VPD (cool/humid): increase air circulation, reduce humidity with ventilation, avoid overwatering

---

### 1.3 Nutrient Solution Management (EC/pH Standards)

**EC (Electrical Conductivity) — measures total dissolved nutrients:**

| Crop | Seedling EC (mS/cm) | Vegetative EC | Fruiting/Late EC |
|------|--------------------|-----------------|--------------------|
| Lettuce | 0.8–1.2 | 1.2–2.0 | 1.6–2.4 |
| Basil | 1.0–1.6 | 1.6–2.2 | 1.8–2.4 |
| Tomato | 1.5–2.0 | 2.0–3.5 | 2.5–3.5 |
| Strawberry | 1.0–1.4 | 1.4–1.8 | 1.8–2.4 |
| Spinach | 1.0–1.6 | 1.6–2.2 | 2.0–2.4 |
| Cucumber | 1.5–2.0 | 2.0–2.5 | 2.5–3.0 |
| Herbs (general) | 0.8–1.2 | 1.2–1.6 | 1.4–2.0 |

**pH targets:**
- Optimal range for most hydroponics: **5.8–6.5**
- Lettuce, herbs: **6.0–6.5**
- Tomatoes, peppers: **5.8–6.2**
- Strawberries: **5.5–6.0**
- pH below 5.5: risk of manganese/zinc toxicity
- pH above 7.0: iron, manganese, phosphorus lockout

**Key macronutrients (Hoagland solution reference):**

| Nutrient | Typical Concentration (ppm) |
|----------|----------------------------|
| Nitrogen (N) | 150–250 |
| Phosphorus (P) | 40–60 |
| Potassium (K) | 200–400 |
| Calcium (Ca) | 150–200 |
| Magnesium (Mg) | 40–60 |
| Sulfur (S) | 60–80 |

---

### 1.4 Soilless System Types

**Kratky Method (Passive Hydroponics)**
- No pumps, no electricity (except optional lighting)
- Reservoir sits below net pots; air gap forms as roots drink down
- Best for: leafy greens, herbs, small crops; beginners; zero/low budget
- Water use efficiency: ~90% vs. soil (no runoff)
- Maintenance: minimal (refill reservoir every 1–3 weeks)
- Yield benchmark: lettuce ~300–450 g/m²/cycle (28–35 days)

**Deep Water Culture (DWC)**
- Plants suspended in constantly aerated nutrient solution
- Requires air pump + air stones; reservoir stays full
- Best for: fast-growing leafy greens, basil; intermediate growers
- Yield benchmark: lettuce ~450–600 g/m²/cycle

**Nutrient Film Technique (NFT)**
- Thin film of nutrient solution flows continuously over roots in channels
- Requires pump, timer, channels with 1–2% slope; re-circulatory
- Best for: lettuce, herbs, strawberries; intermediate to advanced
- Most space-efficient for balconies: vertical wall systems possible
- Yield benchmark: lettuce ~500–700 g/m²/cycle

**Aeroponics**
- Roots hang in air; misted with nutrient solution at intervals (1–5 min on/off)
- Highest oxygen exposure → fastest growth; requires high-pressure pump and nozzles
- Best for: advanced growers; high-value crops; research applications
- Yield benchmark: lettuce ~600–900 g/m²/cycle
- Higher equipment cost and maintenance; failure risk if pump fails

**Comparison Matrix:**

| Criterion | Kratky | DWC | NFT | Aeroponics |
|-----------|--------|-----|-----|-----------|
| Setup Cost (USD, per m²) | $10–30 | $20–60 | $50–150 | $100–300 |
| Skill Required | Beginner | Intermediate | Intermediate | Advanced |
| Maintenance (h/week) | 0.5 | 1.0 | 1.5 | 2.5 |
| Crop Compatibility | Leafy/Herbs | Leafy/Herbs | Most crops | Most crops |
| Water Efficiency | High | High | Very High | Very High |
| Failure Risk | Very Low | Low | Medium | Medium-High |
| Scalability | Low | Medium | High | High |

---

### 1.5 Water-Energy-Food Nexus Framework

The WEF Nexus framework evaluates urban agriculture systems on three interconnected axes:
- **Water:** Consumption (L/kg yield), recycling rate, source independence
- **Energy:** kWh per kg yield (lighting + pumps + HVAC), renewable fraction
- **Food:** Nutritional density per m², food safety (pathogen risk), food miles saved

**Benchmark values (urban hydroponics):**
- Water consumption: 0.5–2.0 L per kg leafy greens (vs. 40–200 L/kg in field agriculture)
- Energy: 1.5–4.0 kWh per kg lettuce (LED + DWC system)
- Yield: 30–60 kg/m²/year (lettuce, NFT)

---

## 2. Key Research Papers

| Title | Authors | Year | Venue | DOI/Link | Relevance |
|-------|---------|------|-------|----------|-----------|
| Hydroponic lettuce production in a controlled environment: effects of daily light integral | Albright et al. | 2000 | HortScience | 10.21273/HORTSCI.35.2.194 | DLI baseline data |
| Comparison of hydroponic systems for tomato production | Savvas et al. | 2013 | Scientia Horticulturae | 10.1016/j.scienta.2013.05.029 | System comparison |
| Urban food production on unused land in cities | Pölling et al. | 2016 | Agriculture | 10.3390/agriculture6030004 | Urban rooftop feasibility |
| Vapor pressure deficit controls transpiration and Ca distribution in lettuce | Bauerle & Toler | 2004 | J. Amer. Soc. Hort. Sci. | 10.21273/JASHS.129.3.394 | VPD effects on crop quality |
| The aeroponic system: history and future | Treftz & Omaye | 2016 | Functional Foods in Health and Disease | doi.org/10.31989/ffhd.v6i1.250 | Aeroponics overview |
| A review of the Kratky non-circulating hydroponics method | Various | 2018 | MDPI Horticulturae | 10.3390/horticulturae4030024 | Kratky system basis |
| Nutrient solutions for soilless growing systems | Resh | 2013 | CRC Press (book) | ISBN 9781439878675 | EC/pH reference standard |
| Vertical farming: smart urban agriculture | Benke & Tomkins | 2017 | Sustainability Science | 10.1007/s11625-016-0402-1 | Urban vertical systems |
| Water productivity and resources efficiency in urban hydroponics | Martin & van Klink | 2021 | Journal of Cleaner Production | 10.1016/j.jclepro.2021.127834 | WEF Nexus metrics |
| Energy use in controlled environment agriculture | Graamans et al. | 2018 | Biosystems Engineering | 10.1016/j.biosystemseng.2018.07.015 | Energy per kg yield |
| FAO: Growing Greener Cities | FAO | 2010 | FAO Reports | fao.org/3/i1730e/i1730e.pdf | FAO UA guidelines |
| Urban rooftop agriculture in Southeast Asia: barriers and opportunities | Yip & Chen | 2020 | Urban Agriculture & Regional Food Systems | 10.1002/uar2.20006 | Regional relevance |
| Optimal EC and pH for hydroponic crops: a meta-analysis | Kim et al. | 2022 | MDPI Horticulturae | 10.3390/horticulturae8030232 | EC/pH reference |

---

## 3. State-of-the-Art Methods & Tools

### 3.1 LED Grow Light Technology
- **Full-spectrum LED:** Modern LED panels deliver PAR-optimized spectra (400–700 nm with peaks at 430 nm blue and 660 nm red). Efficacy: 2.0–3.5 μmol/J.
- **DLI supplementation formula:** `Required supplement PPFD = (Target DLI - Natural DLI) × 1,000,000 / (photoperiod × 3600)`
- **Cost estimate (2025):** Quality LED panels: $20–60/fixture at 40–60W, covering ~0.25 m². Energy cost varies by region ($0.05–0.25/kWh).

### 3.2 Automated Dosing Systems
- EC and pH can be maintained automatically with two-part dosing pumps (Part A: Ca/Mg, Part B: NPK) controlled by Arduino/Raspberry Pi + EC/pH probes.
- Entry-level automated systems (BlueLab Guardian, Bluelab Combo Meter): $150–400.
- DIY solutions: Atlas Scientific EZO-EC + EZO-pH chips + peristaltic dosing pumps: $80–200.

### 3.3 Weather Data Integration
- **OpenWeatherMap API** (free tier: 1,000 calls/day): current temperature, humidity, UV index, cloud cover → feed into real-time VPD and DLI adjustment.
- **NASA POWER API** (free): historical daily solar irradiance at any lat/lon → reliable DLI baseline without real-time subscription.
- **USDA Plant Hardiness Zone map API** → frost date lookup → season planning.

### 3.4 Structural Assessment Tools
- Standard balcony/rooftop load capacity: 150–400 kg/m² (varies by building code / country).
- NFT system with full reservoirs: 25–60 kg/m².
- DWC system (20L reservoir + plants + structure): 15–40 kg/m².
- Rule of thumb: never exceed 50% of rated structural capacity without engineering sign-off.

### 3.5 Pest & Disease Management (IPM for Hydroponics)
- Primary threats: root rot (Pythium spp.), powdery mildew, aphids, whitefly, fungus gnats.
- IPM approach: biological controls (predatory insects, Bacillus subtilis), UV sterilization of nutrient solution, copper-mesh barriers.
- Monitoring: weekly visual inspection + EC/pH trending (unexplained EC drop = possible root rot).

---

## 4. Authoritative Data Sources

| Source | URL | Data Type | Update Frequency |
|--------|-----|-----------|-----------------|
| MDPI Horticulturae (open access) | https://www.mdpi.com/journal/horticulturae | Peer-reviewed research | Continuous |
| FAO Urban Agriculture | https://www.fao.org/urban-agriculture/en/ | Guidelines, reports | Periodic |
| RUAF Foundation | https://ruaf.org/ | Best practices, case studies | Monthly |
| ArXiv q-bio.QM | https://arxiv.org/list/q-bio.QM/recent | Preprints | Daily |
| USDA ARS Publications | https://www.ars.usda.gov/research/publications/ | Research reports | Continuous |
| NASA POWER API | https://power.larc.nasa.gov/ | Solar irradiance, meteorological | Daily |
| OpenWeatherMap API | https://openweathermap.org/api | Current weather, forecast | Real-time |
| Journal of Cleaner Production | https://www.journals.elsevier.com/journal-of-cleaner-production | Sustainability research | Continuous |
| HydroponicsResearch.com | https://www.hydroponicsresearch.com/ | Applied research summaries | Monthly |

---

## 5. Analytical Frameworks

| Framework | Description | Used In Sub-Skill |
|-----------|-------------|------------------|
| FAO Urban and Peri-urban Agriculture Guidelines (2010, 2012) | Policy framework for food safety, water use, spatial planning in urban farming | sub-scoring-engine (dimensions 1, 3) |
| Daily Light Integral (DLI) — ASABE Standard EP 506 | Quantitative standard for crop light requirements in controlled environments | sub-system-designer, sub-scoring-engine (dimension 2) |
| Vapor Pressure Deficit (VPD) — Buck equation | Thermodynamic measure of air dryness driving plant transpiration | sub-system-designer, sub-scoring-engine (dimension 3) |
| Hoagland Nutrient Solution Standard (Hoagland & Arnon, 1950; revised) | Reference standard for balanced hydroponic nutrient composition | sub-system-designer (nutrient schedule) |
| EC/pH Optimal Ranges — MDPI Horticulturae meta-analysis (Kim et al., 2022) | Evidence-based EC and pH targets per crop species and growth stage | sub-system-designer, sub-scoring-engine (dimension 4) |
| Water-Energy-Food Nexus Framework (WEF Nexus, Hoff 2011) | Multi-resource efficiency evaluation for food production systems | sub-scoring-engine (dimensions 5, 6) |
| USDA Plant Hardiness Zone System | Climate zone classification for crop season planning and frost risk | sub-profile-intake, sub-system-designer |

### 5.1 Scoring Dimension Framework (sub-scoring-engine)

| Dimension | Framework Anchor | Weight |
|-----------|-----------------|--------|
| 1. Food Safety Compliance | FAO UA Guidelines Chapter 4 | 15% |
| 2. Light Adequacy (DLI) | ASABE EP 506 / DLI tables | 20% |
| 3. Climate Suitability (VPD) | Buck equation VPD optimal ranges | 15% |
| 4. Nutrient Management | Hoagland / Kim et al. 2022 EC-pH | 20% |
| 5. Water Use Efficiency | WEF Nexus / Martin & van Klink 2021 | 15% |
| 6. Yield Potential | System benchmarks (Kratky/DWC/NFT/Aero) | 10% |
| 7. Structural & Electrical Safety | Local building code + residential electrical standards | 5% |

---

## 6. Self-Update Protocol

```yaml
crawl_config:
  knowledge_brain_path: "D:/Dungchan/skill_adv/232/SECOND-KNOWLEDGE-BRAIN.md"
  index_path: "D:/Dungchan/skill_adv/232/.knowledge_index.json"
  
  sources:
    - name: "MDPI Horticulturae RSS"
      url: "https://www.mdpi.com/journal/horticulturae/rss"
      type: "rss"
      keywords: ["hydroponics", "aeroponics", "DLI", "NFT", "urban agriculture", "soilless"]
      
    - name: "ArXiv q-bio.QM"
      url: "https://arxiv.org/search/?query=hydroponics+urban+agriculture&searchtype=all&start=0"
      type: "html_scrape"
      keywords: ["hydroponics", "aeroponics", "vertical farm", "controlled environment"]
      
    - name: "FAO Urban Agriculture"
      url: "https://www.fao.org/urban-agriculture/en/"
      type: "html_scrape"
      keywords: ["urban farming", "peri-urban", "food security", "hydroponic"]
      
    - name: "RUAF Foundation News"
      url: "https://ruaf.org/news/"
      type: "html_scrape"
      keywords: ["urban agriculture", "rooftop", "hydroponics", "food production"]

  relevance_threshold: 0.3
  min_score_to_include: 0.3
  deduplication: "sha256_of_url"
  
  schedule:
    cron: "0 6 * * 1"  # Every Monday at 06:00 UTC
    description: "Weekly knowledge update"
    
  append_format:
    papers_table: "| {title} | {authors} | {year} | {venue} | {url} | {relevance_note} |"
    log_entry: "| {date} | {source} | {count_added} | {notes} |"
```

---

## 7. Knowledge Update Log

| Date | Source | Entries Added | Notes |
|------|--------|--------------|-------|
| 2026-06-19 | Manual seed (CLAUDE author) | 13 papers, all sections | Initial knowledge base creation |
| — | — | — | Awaiting first automated crawl (2026-06-26) |
