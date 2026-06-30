# Micro Urban Agriculture Design & Management

[![Skill Phase](https://img.shields.io/badge/Phase-Production%20Ready-green)](https://github.com/dungnotnull/micro-urban-agriculture-design-agent-skill)
[![Status](https://img.shields.io/badge/Status-100%25%20Complete-brightgreen)](https://github.com/dungnotnull/micro-urban-agriculture-design-agent-skill)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-purple)](https://claude.com/claude-code)

A production-ready AI skill for designing, calculating, and continuously optimizing micro-scale urban farm systems on balconies, rooftops, and terraces. Powered by real weather data, DLI/VPD physics, and world-renowned soilless cultivation standards.

---

## Overview

Urban dwellers increasingly want to grow food at home but face steep learning curves around hydroponic systems, light availability, and nutrient management. This skill consolidates FAO guidelines, DLI/VPD physics, EC/pH standards, and real-time weather data into a single professional design system that produces complete, personalized micro-farm designs.

**What it delivers:**
- Complete hydroponic system design (NFT/DWC/Kratky/Aeroponics selection)
- Precise DLI (Daily Light Integral) and VPD (Vapor Pressure Deficit) calculations
- Customized nutrient schedules with EC/pH targets by growth stage
- Water and energy budget projections
- Multi-dimensional quality scoring across 7 frameworks
- Prioritized improvement roadmap with effort estimates and ROI analysis

**For whom:**
- Beginner-to-intermediate urban growers
- Balcony and rooftop gardeners
- Sustainability-focused households
- Urban agriculture NGOs and educators

---

## Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Climate Analysis** | Real-time weather data integration with DLI/VPD calculations for any location |
| **System Selection** | Algorithmic selection of optimal hydroponic system (NFT/DWC/Kratky/Aeroponics) based on 6 criteria |
| **Light Planning** | Precise supplemental LED requirements with wattage, photoperiod, and cost calculations |
| **Nutrient Management** | Stage-specific EC/pH schedules for 20+ crops with compatibility analysis |
| **Budget Projections** | Water usage (L/week), energy consumption (kWh/week), and monthly cost estimates |
| **Quality Scoring** | 7-dimension evaluation against FAO, ASABE, Buck equation, and WEF Nexus frameworks |
| **Improvement Roadmap** | Pareto-ranked recommendations with effort hours, costs, and yield-impact percentages |

### Supported Crop Categories

- **Leafy Greens:** Lettuce, Spinach, Kale, Arugula, Swiss Chard, Pak Choi, Watercress
- **Herbs:** Basil, Mint, Cilantro, Parsley, Chives, Oregano, Thyme
- **Fruiting Crops:** Cherry Tomato, Cucumber, Chili Pepper, Strawberry, Eggplant
- **Root Vegetables:** Carrot, Radish, Beet, Turnip

---

## Architecture

### Harness Flow

```
User Input → Profile Intake → System Design → Scoring → Devil's Advocate → Improvement Roadmap → Final Report
```

### Sub-Skills

| Sub-Skill | Purpose |
|-----------|---------|
| `sub-profile-intake` | Collects space, location, crops, budget with validation |
| `sub-system-designer` | Calculates DLI/VPD, selects system, designs layout, budgets |
| `sub-scoring-engine` | Scores across 7 dimensions using published frameworks |
| `sub-improvement-roadmap` | Generates ranked improvements with ROI analysis |

### Knowledge Pipeline

`tools/knowledge_updater.py` automatically fetches latest research from:
- MDPI Horticulturae RSS (peer-reviewed horticultural science)
- ArXiv q-bio.QM (quantitative biology preprints)
- FAO Urban Agriculture (policy guidelines)
- RUAF Foundation (urban farming best practices)

Runs weekly via cron to keep knowledge base current.

---

## Scoring Frameworks

The skill evaluates designs across 7 dimensions, each anchored to authoritative frameworks:

| Dimension | Framework | Weight |
|-----------|-----------|--------|
| D1: Food Safety | FAO UA Guidelines Chapter 4 | 15% |
| D2: Light Adequacy | ASABE EP506 Standard | 20% |
| D3: Climate Suitability | Buck Equation VPD | 15% |
| D4: Nutrient Management | Hoagland Solution, Kim et al. 2022 | 20% |
| D5: Water Efficiency | WEF Nexus, Martin & van Klink 2021 | 15% |
| D6: Yield Potential | System benchmarks | 10% |
| D7: Structural Safety | Building codes, IEC 60364 | 5% |

**Composite Score:** Weighted average (0-100 scale)
- 90-100: Excellent (production-ready)
- 75-89: Good (minor improvements)
- 60-74: Acceptable (several improvements needed)
- Below 60: Marginal/Poor (redesign required)

---

## Example Output

### Input Profile
```
Space: Balcony, 3m × 1.5m, South-facing
Location: Ho Chi Minh City, Vietnam
Crops: Lettuce, Basil
Budget: $80 USD
Experience: Beginner
```

### System Design Result
```
RECOMMENDED SYSTEM: Kratky Method (Passive Hydroponics)

Rationale:
- Budget fit: Optimal for $80 budget
- Experience fit: Perfect for beginners
- Maintenance: 0.5h/week required
- Crop compatibility: Ideal for leafy greens and herbs

LAYOUT:
4 × 5L Kratky tubs | 20 plant sites total
Growing area: 2.7 m² | Walkway: 1.8 m²

DLI ANALYSIS:
Natural DLI: 28-35 mol/m²/day (tropical latitude)
Effective DLI: 22-28 mol/m²/day (after orientation)
Both crops exceed optimal requirements year-round

NUTRIENT SCHEDULE:
Lettuce EC: 0.8-1.2 mS/cm (seedling) → 1.6-2.0 mS/cm (vegetative)
Basil EC: 1.0-1.6 mS/cm (seedling) → 1.8-2.2 mS/cm (vegetative)
pH target: 6.0-6.5 for both

BUDGETS:
Water: 8-12 L/week ($0.40/month)
Energy: $0 (passive system)
Yield: 600g/week (lettuce 400g + basil 200g)

EQUIPMENT LIST:
- 4× 5L food-grade containers: $12
- Net pots (20× 2"): $8
- Growing medium (perlite): $15
- Nutrient solution (1-month supply): $25
- pH test kit: $20
---
TOTAL INVESTMENT: $80 USD
```

### Quality Scorecard
```
DESIGN SCORECARD
Dimension                     Score   Weight   Weighted
D1 Food Safety                 88/100  15%      13.2
D2 Light Adequacy (DLI)        92/100  20%      18.4
D3 Climate Suitability (VPD)   81/100  15%      12.2
D4 Nutrient Management         90/100  20%      18.0
D5 Water Use Efficiency        85/100  15%      12.8
D6 Yield Potential            78/100  10%      7.8
D7 Structural & Electrical     95/100  5%       4.8
─────────────────────────────────────────────────────
COMPOSITE SCORE:               87.2 / 100  Rating: Good
```

### Improvement Roadmap (Top 5)
```
Priority  Action                                      Effort   Cost    Yield Impact  Timeline
1         Extend photoperiod 2h with timer           1h       $15     +12%         Week 1
2         Revise EC schedule (crop-stage-specific)   2h       $0      +10%         Week 1
3         Add shade netting for Apr-May VPD control   2h       $20     +8%          Week 1
4         Install carbon filter for water treatment   2h       $25     +5%          Month 1
5         Upgrade to NFT wall panels (future)         12h      $120    +20%         Month 3
```

---

## Installation

### For Claude Code Users

1. Clone this repository:
```bash
git clone https://github.com/dungnotnull/micro-urban-agriculture-design-agent-skill.git
cd micro-urban-agriculture-design-agent-skill
```

2. Copy to your Claude skills directory:
```bash
# Windows
Copy-Item -Path "skills\*" -Destination "$env:USERPROFILE\.claude\skills\micro-urban-agriculture-design\" -Recurse

# macOS/Linux
cp -r skills/* ~/.claude/skills/micro-urban-agriculture-design/
```

3. Restart Claude Code and invoke:
```
/micro-urban-agriculture-design
```

### For Knowledge Pipeline Setup

1. Install dependencies:
```bash
pip install crawl4ai feedparser requests beautifulsoup4 python-dateutil
```

2. Run weekly knowledge update:
```bash
python tools/knowledge_updater.py
```

3. Schedule automated updates (Linux/macOS):
```bash
# Add to crontab (crontab -e)
0 6 * * 1 /usr/bin/python3 /path/to/tools/knowledge_updater.py >> /var/log/knowledge_updater.log 2>&1
```

---

## Project Structure

```
micro-urban-agriculture-design/
├── README.md                          # This file
├── CLAUDE.md                          # Skill identity and usage
├── PROJECT-detail.md                  # Full technical specification
├── PROJECT-DEVELOPMENT-PHASE-TRACKING.md  # Development roadmap
├── SECOND-KNOWLEDGE-BRAIN.md          # Domain knowledge base
├── skills/
│   ├── main.md                        # Entry point harness
│   ├── sub-profile-intake.md          # User profile collection
│   ├── sub-system-designer.md         # System design calculations
│   ├── sub-scoring-engine.md          # Quality evaluation
│   └── sub-improvement-roadmap.md     # Improvement recommendations
├── tools/
│   └── knowledge_updater.py           # Knowledge pipeline (crawl4ai)
└── tests/
    └── test-scenarios.md              # 7 comprehensive test scenarios
```

---

## Testing

The skill includes 7 comprehensive test scenarios covering:

1. **Beginner Balcony (Tropical)** — Ho Chi Minh City, lettuce + basil
2. **Intermediate Rooftop (Temperate)** — Seoul, cherry tomatoes + lettuce
3. **Commercial Rooftop (Subtropical)** — Bangkok, large-scale leafy greens
4. **Zero-Budget (Equatorial)** — Singapore, passive spinach system
5. **North-Facing Edge Case** — Berlin, full LED dependency
6. **High TDS Water** — Dubai, RO filtration requirement
7. **Crop Incompatibility** — Hanoi, tomato + spinach conflict

Each scenario validates:
- DLI calculation accuracy (±10% of reference values)
- EC/pH compliance with MDPI Horticulturae standards
- Quality gate enforcement
- Graceful degradation behavior

---

## Scientific Foundations

### Key Concepts

**Daily Light Integral (DLI):** Cumulative photosynthetically active radiation over 24 hours. Measured in mol/m²/day. Critical for determining crop viability and supplemental LED requirements.

**Vapor Pressure Deficit (VPD):** Difference between saturation and actual vapor pressure. Drives transpiration, nutrient uptake, and disease susceptibility. Measured in kPa.

**Electrical Conductivity (EC):** Total dissolved nutrients in solution. Measured in mS/cm. Varies by crop and growth stage.

**pH:** Acidity/alkalinity of nutrient solution. Optimal range: 5.8-6.5 for most hydroponic crops.

### Primary References

| Framework | Source | Application |
|-----------|--------|-------------|
| FAO Urban Agriculture Guidelines | FAO 2010 | Food safety, spatial planning |
| ASABE EP506 | ASABE Standard | Plant growth lighting requirements |
| Buck Equation | Buck 1981 | VPD calculations |
| Hoagland Solution | Hoagland & Arnon 1950 | Nutrient formulation |
| WEF Nexus | Hoff 2011 | Water-energy-food efficiency |
| MDPI Horticulturae | Kim et al. 2022 | EC/pH optimal ranges |

---

## Development Status

**Current Phase:** Production Ready (Phase 5 of 5)

**Completion:** 100% — All phases complete

| Phase | Status | Deliverables |
|-------|--------|-------------|
| Phase 0: Research & Architecture | Complete | Frameworks, harness design, knowledge base |
| Phase 1: Core Sub-Skills | Complete | 4 production-ready sub-skill files |
| Phase 2: Main Harness | Complete | Orchestration, quality gates, graceful degradation |
| Phase 3: Knowledge Pipeline | Complete | crawl4ai integration, deduplication, automation |
| Phase 4: Testing | Complete | 7 validated scenarios |
| Phase 5: Integration | Complete | Cluster compatibility, documentation |

---

## Contributing

Contributions are welcome! Areas for enhancement:

1. **Additional Crops:** Expand CROP_DATABASE with more species
2. **Climate Data:** Integrate additional weather APIs
3. **System Types:** Add ebb-and-flow, drip irrigation
4. **Pest Management:** Expand IPM recommendations
5. **Localization:** Add region-specific equipment pricing

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make changes with clear commit messages
4. Update relevant tests
5. Submit a pull request

---

## Citation

If you use this skill in research or production, please cite:

```
Micro Urban Agriculture Design & Management AI Skill
Version 1.0
https://github.com/dungnotnull/micro-urban-agriculture-design-agent-skill
```

---

## License

MIT License - See LICENSE file for details

---

## Acknowledgments

- **FAO** for urban agriculture guidelines
- **ASABE** for plant growth lighting standards
- **MDPI Horticulturae** for open-access horticultural research
- **RUAF Foundation** for urban farming best practices
- **Claude Code community** for the skills framework

---

## Contact

- **GitHub:** https://github.com/dungnotnull/micro-urban-agriculture-design-agent-skill
- **Issues:** https://github.com/dungnotnull/micro-urban-agriculture-design-agent-skill/issues

---

## Star History

If you find this skill useful, please consider giving it a star!

Made with dedication for sustainable urban food systems.
