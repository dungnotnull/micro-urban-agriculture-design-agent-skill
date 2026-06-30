---
name: sub-improvement-roadmap
description: Translate scoring gaps into a prioritized, quantified improvement roadmap with effort estimates, yield-impact percentages, cost estimates, and milestone timelines.
---

## Purpose

Convert the weaknesses identified by sub-scoring-engine into a concrete, Pareto-ranked action plan. Every improvement item is quantified with effort (person-hours + USD cost), expected yield-impact (percentage increase above current design baseline), and a milestone timeline. The roadmap is the practical deliverable that makes the entire skill actionable — not just advisory.

---

## Inputs

- Scored Report (from sub-scoring-engine)
- Validated Profile JSON (from sub-profile-intake)
- Design Specification (from sub-system-designer)
- Access to WebSearch (supplemental LED pricing, nutrient solution costs, equipment prices)
- Access to SECOND-KNOWLEDGE-BRAIN.md (benchmarks, frameworks)

---

## Workflow

### Step 1: Map scoring gaps to improvement categories

For each dimension where `score < 80`:
1. Calculate the gap: `gap = 80 - score` (80 is the target threshold for a "Good" design)
2. Map to improvement category:

| Dimension | Score Gap → Improvement Category |
|-----------|----------------------------------|
| D1 (Food Safety) | Water treatment, pathogen controls, food handling protocol |
| D2 (DLI / Light) | Supplemental LED plan, light schedule optimization, crop selection revision |
| D3 (VPD / Climate) | Misting system, ventilation, timing of watering to cooler hours, seasonal crop rotation |
| D4 (Nutrients) | EC/pH schedule revision, dosing automation, multi-crop compatibility |
| D5 (Water Use) | System recirculation upgrade, rainwater harvesting, leak reduction |
| D6 (Yield) | Plant spacing optimization, DLI increase, crop cycle acceleration, higher-yield variety selection |
| D7 (Safety) | Weight reduction (lightweight media), electrical circuit assessment, engineering sign-off |

### Step 2: Generate improvement items

For each improvement category with a gap:
1. Generate at least 2 specific improvement items per gap dimension
2. For each item, fill in:

**Item Template:**
```
Priority: [rank by impact/effort ratio]
Title: [specific action, not generic advice]
Dimension: [D1–D7]
Score Gap Addressed: [current score → target score]
Effort Hours: [person-hours to implement]
Effort USD: [one-time cost in USD]
Recurring Cost USD/Month: [if applicable]
Expected Yield-Impact: [% increase in yield above current baseline]
Expected Score Improvement: [estimated D-score points gained]
Timeline: [Week 1 / Month 1 / Month 3 / Year 1]
Implementation Steps: [numbered, 3–5 concrete steps]
Evidence Source: [paper, framework, or benchmark from SECOND-KNOWLEDGE-BRAIN.md]
```

### Step 3: Quantify yield-impact

Use the following reference data from SECOND-KNOWLEDGE-BRAIN.md to estimate yield-impact:

| Improvement Type | Typical Yield-Impact |
|-----------------|---------------------|
| Supplemental LED (meet DLI optimal) | +20–40% yield vs. DLI deficit baseline |
| EC/pH optimization (crop-stage-specific vs. flat) | +10–20% yield |
| Upgrade from Kratky to NFT (same DLI) | +15–25% yield |
| Upgrade from DWC to Aeroponics (same DLI) | +15–30% yield |
| VPD management (misting in high-VPD months) | +5–15% yield quality (reduced tipburn, bitterness) |
| Water recirculation upgrade (from drain-to-waste) | 0% yield impact; 40–60% water saving |
| Plant spacing optimization | +10–20% canopy coverage |
| Lightweight grow media upgrade (from perlite to rock wool) | +5% yield from faster root development |

**Yield-impact calculation:**
```
yield_impact_pct = reference_impact_range × (score_gap / 40) × adjustment_factor
adjustment_factor: 1.0 for primary crop; 0.7 for secondary crop
```

### Step 4: Estimate effort and cost

**Effort estimation rubric:**

| Task Type | Effort Hours |
|-----------|-------------|
| Research & purchase (single item) | 1–3h |
| Install LED fixtures (per 1m²) | 2–4h |
| Upgrade system type (DWC→NFT) | 8–16h |
| Set up misting system (per zone) | 4–8h |
| Install EC/pH auto-dosing | 4–8h |
| Install water filtration | 2–4h |
| Redesign plant spacing | 1–2h |
| Consult structural engineer | 2–4h (professional cost: $150–400) |

**Cost estimation procedure:**
- WebSearch: `"LED grow light {wattage}W price"` or `"NFT hydroponics channel price"`
- If WebSearch unavailable: use SECOND-KNOWLEDGE-BRAIN.md Section 3.1 price ranges
- Present costs as ranges (low/mid/high) to account for regional variation

**Complete Effort & Cost Estimation Implementation:**

```python
from typing import Dict, List, Tuple
from enum import Enum

class TaskCategory(Enum):
    RESEARCH = "research_purchase"
    LED_INSTALL = "led_installation"
    SYSTEM_UPGRADE = "system_upgrade"
    MISTING_SETUP = "misting_setup"
    AUTOMATION_INSTALL = "automation_install"
    FILTRATION_INSTALL = "filtration_install"
    LAYOUT_REDESIGN = "layout_redesign"
    PROFESSIONAL_CONSULT = "professional_consult"
    SCHEDULE_ADJUST = "schedule_adjust"
    MAINTENANCE_ROUTINE = "maintenance_routine"

class EffortEstimator:
    """
    Estimate effort hours and USD costs for improvement tasks.
    Uses reference data from SECOND-KNOWLEDGE-BRAIN.md Section 3.1
    """
    
    # Base effort hours by task category
    EFFORT_HOURS = {
        TaskCategory.RESEARCH: (1, 3),
        TaskCategory.LED_INSTALL: (2, 4),
        TaskCategory.SYSTEM_UPGRADE: (8, 16),
        TaskCategory.MISTING_SETUP: (4, 8),
        TaskCategory.AUTOMATION_INSTALL: (4, 8),
        TaskCategory.FILTRATION_INSTALL: (2, 4),
        TaskCategory.LAYOUT_REDESIGN: (1, 2),
        TaskCategory.PROFESSIONAL_CONSULT: (2, 4),
        TaskCategory.SCHEDULE_ADJUST: (0.5, 1),
        TaskCategory.MAINTENANCE_ROUTINE: (0.5, 1)
    }
    
    # Cost ranges by equipment type (USD)
    EQUIPMENT_COSTS = {
        "led_panel_40w": (30, 60),
        "led_panel_80w": (50, 100),
        "led_controller": (15, 40),
        "carbon_filter": (20, 50),
        "ro_filter_50gpd": (80, 150),
        "ec_ph_monitor": (80, 200),
        "peristaltic_dosing_pump": (150, 300),
        "mist_nozzle_set": (30, 80),
        "shade_netting_50": (15, 40),
        "nft_channel_1m": (10, 25),
        "submersible_pump_20w": (15, 30),
        "air_pump_10w": (10, 25),
        "reservoir_40l": (15, 30),
        "net_pot_2inch": (0.5, 1.5),
        "grow_media_rockwool": (10, 25),
        "grow_media_perlite": (5, 15)
    }
    
    # Professional service costs (USD)
    PROFESSIONAL_COSTS = {
        "structural_engineer_consult": (150, 400),
        "electrician_install": (50, 150),
        "plumber_install": (50, 150)
    }
    
    # Labor cost assumption for user's own time (USD/hour)
    LABOR_COST_PER_HOUR = 50.0
    
    def estimate_task(
        self,
        category: TaskCategory,
        equipment_items: List[str] = None,
        professional_services: List[str] = None,
        complexity_multiplier: float = 1.0,
        area_m2: float = 1.0
    ) -> Dict:
        """
        Estimate effort and cost for a single improvement task.
        
        Args:
            category: Task category enum
            equipment_items: List of equipment keys from EQUIPMENT_COSTS
            professional_services: List of service keys from PROFESSIONAL_COSTS
            complexity_multiplier: Multiplier for effort hours (0.5–2.0)
            area_m2: Area in m² for scaling per-unit costs
            
        Returns:
            {
                "effort_hours_min": float,
                "effort_hours_max": float,
                "effort_hours_avg": float,
                "equipment_cost_min": float,
                "equipment_cost_max": float,
                "equipment_cost_avg": float,
                "professional_cost_min": float,
                "professional_cost_max": float,
                "professional_cost_avg": float,
                "total_cost_min": float,
                "total_cost_max": float,
                "total_cost_avg": float
            }
        """
        # Base effort hours
        base_hours_min, base_hours_max = self.EFFORT_HOURS.get(
            category, (1, 3)
        )
        
        # Apply complexity multiplier
        effort_hours_min = base_hours_min * complexity_multiplier
        effort_hours_max = base_hours_max * complexity_multiplier
        
        # Scale by area for applicable tasks
        if category in [TaskCategory.LED_INSTALL, TaskCategory.SYSTEM_UPGRADE]:
            effort_hours_min *= area_m2
            effort_hours_max *= area_m2
        
        effort_hours_avg = (effort_hours_min + effort_hours_max) / 2
        
        # Equipment costs
        equipment_cost_total = (0, 0)
        if equipment_items:
            equipment_min = sum(
                self.EQUIPMENT_COSTS.get(item, (0, 0))[0] 
                for item in equipment_items
            )
            equipment_max = sum(
                self.EQUIPMENT_COSTS.get(item, (0, 0))[1] 
                for item in equipment_items
            )
            equipment_cost_total = (equipment_min, equipment_max)
        
        equipment_cost_min, equipment_cost_max = equipment_cost_total
        equipment_cost_avg = (equipment_cost_min + equipment_cost_max) / 2
        
        # Professional service costs
        professional_cost_total = (0, 0)
        if professional_services:
            prof_min = sum(
                self.PROFESSIONAL_COSTS.get(service, (0, 0))[0]
                for service in professional_services
            )
            prof_max = sum(
                self.PROFESSIONAL_COSTS.get(service, (0, 0))[1]
                for service in professional_services
            )
            professional_cost_total = (prof_min, prof_max)
        
        professional_cost_min, professional_cost_max = professional_cost_total
        professional_cost_avg = (professional_cost_min + professional_cost_max) / 2
        
        # Total costs
        total_cost_min = equipment_cost_min + professional_cost_min
        total_cost_max = equipment_cost_max + professional_cost_max
        total_cost_avg = (total_cost_min + total_cost_max) / 2
        
        return {
            "category": category.value,
            "effort_hours_min": round(effort_hours_min, 1),
            "effort_hours_max": round(effort_hours_max, 1),
            "effort_hours_avg": round(effort_hours_avg, 1),
            "equipment_cost_min": round(equipment_cost_min, 2),
            "equipment_cost_max": round(equipment_cost_max, 2),
            "equipment_cost_avg": round(equipment_cost_avg, 2),
            "professional_cost_min": round(professional_cost_min, 2),
            "professional_cost_max": round(professional_cost_max, 2),
            "professional_cost_avg": round(professional_cost_avg, 2),
            "total_cost_min": round(total_cost_min, 2),
            "total_cost_max": round(total_cost_max, 2),
            "total_cost_avg": round(total_cost_avg, 2)
        }
```

### Step 5: Rank improvements by Pareto impact/effort ratio

```
impact_effort_ratio = (expected_yield_impact_pct × D_score_gain_weight) / (effort_hours + cost_usd / 50)
```
Where `cost_usd / 50` converts cost into equivalent "effort hours" at $50/hour for standardized ranking.

Sort all improvements descending by `impact_effort_ratio`. The top item is Priority 1.

**Constraint:** Improvements ranked higher than their dependency must come first:
- Example: "Install LED fixtures" must precede "Extend photoperiod" in the timeline
- Example: "Upgrade to recirculating system" must precede "Install auto-dosing"

**Complete Pareto Ranking Implementation:**

```python
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class ImprovementItem:
    """Represents a single improvement recommendation."""
    priority: int
    title: str
    dimension: str  # D1–D7
    score_gap: Tuple[float, float]  # (current_score, target_score)
    effort_hours_avg: float
    cost_usd_avg: float
    yield_impact_pct: float
    expected_score_gain: float
    timeline: str  # Week 1 / Month 1 / Month 3 / Year 1
    implementation_steps: List[str]
    evidence_source: str
    dependencies: List[str] = None  # Items this depends on

class ParetoRanker:
    """
    Rank improvements by Pareto impact/effort ratio.
    Uses multi-criteria decision analysis for prioritization.
    """
    
    # D-score gain weights by dimension
    DIMENSION_WEIGHTS = {
        "D1": 0.15,
        "D2": 0.20,
        "D3": 0.15,
        "D4": 0.20,
        "D5": 0.15,
        "D6": 0.10,
        "D7": 0.05
    }
    
    # Labor cost assumption for effort/cost normalization
    LABOR_COST_PER_HOUR = 50.0
    
    def __init__(self, scored_report: Dict):
        """
        Initialize Pareto ranker with scored report.
        
        Args:
            scored_report: Output from sub-scoring-engine with composite score
        """
        self.scored_report = scored_report
        self.current_scores = {
            dim: data.get("score", 70)
            for dim, data in scored_report.get("scores", {}).items()
        }
    
    def calculate_impact_effort_ratio(
        self,
        yield_impact_pct: float,
        dimension: str,
        score_gain: float,
        effort_hours: float,
        cost_usd: float
    ) -> float:
        """
        Calculate Pareto impact/effort ratio.
        
        Args:
            yield_impact_pct: Expected yield increase (% above baseline)
            dimension: D1–D7 dimension identifier
            score_gain: Expected D-score improvement
            effort_hours: Person-hours required
            cost_usd: One-time USD cost
            
        Returns:
            Impact/effort ratio (higher = better ROI)
        """
        # Get dimension weight
        dim_weight = self.DIMENSION_WEIGHTS.get(dimension, 0.15)
        
        # Convert cost to effort-equivalent hours
        effort_equivalent_hours = effort_hours + (cost_usd / self.LABOR_COST_PER_HOUR)
        
        # Calculate ratio
        if effort_equivalent_hours > 0:
            ratio = (yield_impact_pct * dim_weight) / effort_equivalent_hours
        else:
            ratio = 0.0
        
        return round(ratio, 4)
    
    def rank_improvements(
        self,
        improvements: List[ImprovementItem]
    ) -> List[ImprovementItem]:
        """
        Sort improvements by Pareto impact/effort ratio.
        
        Args:
            improvements: List of improvement items with all fields populated
            
        Returns:
            Improvements list sorted by priority (highest ratio first)
        """
        # Calculate impact/effort ratio for each item
        for item in improvements:
            score_gain = item.score_gap[1] - item.score_gap[0]
            item.pareto_ratio = self.calculate_impact_effort_ratio(
                item.yield_impact_pct,
                item.dimension,
                score_gain,
                item.effort_hours_avg,
                item.cost_usd_avg
            )
        
        # Sort by ratio descending
        improvements.sort(key=lambda x: x.pareto_ratio, reverse=True)
        
        # Resolve dependencies — ensure dependencies come first
        ranked = []
        processed = set()
        
        max_iterations = len(improvements) * 2  # Prevent infinite loops
        iteration = 0
        
        while len(ranked) < len(improvements) and iteration < max_iterations:
            iteration += 1
            for item in improvements:
                if item in processed:
                    continue
                
                # Check dependencies
                deps_satisfied = True
                if item.dependencies:
                    for dep_title in item.dependencies:
                        dep_item = next(
                            (i for i in improvements if i.title == dep_title),
                            None
                        )
                        if dep_item and dep_item not in processed:
                            deps_satisfied = False
                            break
                
                if deps_satisfied:
                    ranked.append(item)
                    processed.add(item)
        
        # Assign priority numbers
        for priority, item in enumerate(ranked, 1):
            item.priority = priority
        
        return ranked
    
    def generate_ranked_table(
        self,
        improvements: List[ImprovementItem]
    ) -> str:
        """
        Generate formatted ranking table for output.
        
        Returns:
            Formatted markdown table
        """
        lines = [
            "| Priority | Title | Dim | Score Gap | Effort (h) | Cost (USD) | Yield Impact | Timeline |",
            "|----------|-------|-----|-----------|-----------|-----------|--------------|---------|"
        ]
        
        for item in improvements:
            score_gap_str = f"{item.score_gap[0]}→{item.score_gap[1]}"
            lines.append(
                f"| {item.priority} | {item.title} | {item.dimension} | "
                f"{score_gap_str} | {item.effort_hours_avg} | ${item.cost_usd_avg} | "
                f"+{item.yield_impact_pct}% | {item.timeline} |"
            )
        
        return "\n".join(lines)
```

### Step 6: Assign milestone timeline

Assign each improvement to one of four milestone buckets:
- **Week 1 (Immediate / Quick Win):** Low effort (<4 hours), low cost (<$30), high impact
  - Example: Adjust EC schedule, reposition plants for better DLI, add shade cloth on overheating days
- **Month 1 (Near-Term):** Moderate effort (4–16 hours), moderate cost ($30–200)
  - Example: Install supplemental LED fixtures, add carbon filter to water inlet
- **Month 3 (Medium-Term):** Higher effort (16–40 hours), higher cost ($200–1000)
  - Example: Upgrade from Kratky to NFT system, install automated EC/pH dosing
- **Year 1 (Strategic):** Major investment (>40 hours or >$1000), long-term structural changes
  - Example: Full rooftop system expansion, rainwater harvesting installation, structural engineering assessment

### Step 7: Compile the roadmap document

Structure the output as a professional improvement roadmap document with:

1. **Executive Summary** (3 bullets: current state, primary gap, biggest ROI improvement)
2. **Ranked Improvement Table** (all items sorted by priority)
3. **Milestone Plan** (4-column Gantt-style: Week 1 / Month 1 / Month 3 / Year 1)
4. **Expected Outcomes** (composite score projection after implementing top 5 improvements)
5. **Budget Summary** (total investment for all improvements; minimum viable budget for top-3 improvements)
6. **Evidence Appendix** (citations for every improvement claim)

---

## Outputs

Improvement Roadmap document:

**Ranked Improvement Table (example):**

| Priority | Title | Dim | Score Gap | Effort (h) | Cost (USD) | Yield Impact | Timeline |
|----------|-------|-----|-----------|-----------|-----------|--------------|---------|
| 1 | Extend photoperiod by 2h using timer-controlled LED | D2 | 72→86 | 1h | $15 | +12% | Week 1 |
| 2 | Add 40W LED panel for Dec–Feb DLI supplementation | D2 | 72→86 | 3h | $45 | +25% | Month 1 |
| 3 | Revise EC schedule: crop-stage-specific targets | D4 | 85→93 | 2h | $0 | +10% | Week 1 |
| 4 | Install 0.5m² shade netting for April–May VPD control | D3 | 81→89 | 2h | $20 | +8% quality | Week 1 |
| 5 | Add carbon filter inline to water inlet | D1 | 88→94 | 2h | $25 | +5% (safety) | Month 1 |
| 6 | Upgrade from DWC to NFT wall panel layout | D6 | 68→82 | 12h | $120 | +20% | Month 3 |
| 7 | Install auto-dosing peristaltic pump | D4 | 93→97 | 6h | $180 | +5% | Month 3 |

**Expected Composite Score Progression:**
- Current score: 82.0 (Good)
- After Week 1 improvements (#1, #3, #4): ~85.5 (Good → approaching Excellent)
- After Month 1 improvements (#2, #5): ~88.3 (Good)
- After Month 3 improvements (#6, #7): ~91.7 (Excellent)

**Milestone Plan:**
```
Week 1:   [Extend photoperiod] [Revise EC schedule] [Install shade netting]
Month 1:  [Add LED panel] [Install carbon filter]
Month 3:  [Upgrade to NFT] [Install auto-dosing]
Year 1:   [Optional: rooftop expansion / rainwater harvesting]
```

---

## Quality Gate

Improvement Roadmap passes to main harness synthesis ONLY when ALL of the following are true:

- [ ] At least 5 improvement items are listed
- [ ] Every item has: title, dimension addressed, effort (hours), cost (USD), expected yield-impact (%), and timeline
- [ ] All items are ranked by `impact_effort_ratio` (highest first)
- [ ] Milestone plan assigns every item to exactly one of: Week 1 / Month 1 / Month 3 / Year 1
- [ ] No improvement is placed in an earlier milestone than its dependency
- [ ] Composite score progression is computed for at least 3 milestone stages
- [ ] Every yield-impact claim is cited to a framework, paper, or benchmark in SECOND-KNOWLEDGE-BRAIN.md
- [ ] Total investment budget is summarized separately for "top 3 improvements" and "all improvements"
- [ ] The roadmap focuses on specific, actionable items — not generic advice (e.g., "install 40W LED panel" not "consider more lighting")
