---
name: sub-scoring-engine
description: Score a micro urban agriculture system design across 7 dimensions using FAO, DLI, VPD, EC/pH, WEF Nexus, and structural safety frameworks, producing a composite score and ranked strengths/weaknesses.
---

## Purpose

Produce a rigorous, multi-dimensional quality assessment of the system design from sub-system-designer. Every score is anchored to a named, citable framework — never ad hoc criteria. The output (7-dimension score matrix + composite score + strengths/weaknesses) feeds directly into sub-improvement-roadmap to generate evidence-based recommendations.

---

## Inputs

- Design Specification (from sub-system-designer)
- Validated Profile JSON (from sub-profile-intake)
- Access to SECOND-KNOWLEDGE-BRAIN.md (Sections 1–5 — frameworks, benchmarks, research papers)
- Access to WebFetch (live FAO/MDPI reference lookup; optional)

---

## Workflow

### Step 1: Load scoring framework definitions

From SECOND-KNOWLEDGE-BRAIN.md Section 5.1, the 7 scoring dimensions and their frameworks:

| Dim | Name | Framework | Weight |
|-----|------|-----------|--------|
| D1 | Food Safety Compliance | FAO UA Guidelines Ch. 4 | 15% |
| D2 | Light Adequacy (DLI) | ASABE EP 506 / DLI tables | 20% |
| D3 | Climate Suitability (VPD) | Buck equation VPD optimal ranges | 15% |
| D4 | Nutrient Management | Hoagland / Kim et al. 2022 EC-pH | 20% |
| D5 | Water Use Efficiency | WEF Nexus / Martin & van Klink 2021 | 15% |
| D6 | Yield Potential | System benchmarks (Kratky/DWC/NFT/Aero) | 10% |
| D7 | Structural & Electrical Safety | Local building code + residential electrical | 5% |

### Step 2: Score Dimension 1 — Food Safety Compliance

Framework: FAO Urban and Peri-Urban Agriculture Guidelines (2010), Chapter 4 (Food Safety Standards for Urban Farms)

**Rubric (0–100):**

| Score | Criterion |
|-------|-----------|
| 90–100 | Soilless system (no soil contamination risk); clean water source; no aerial pesticide exposure; nutrient-only inputs |
| 75–89 | Soilless system; minor risk identified (e.g., rooftop near industrial zone, high TDS water without treatment plan) |
| 60–74 | Soilless system but water source has elevated TDS/chlorine without mitigation specified; or structural contamination risk present |
| 40–59 | Water treatment plan missing despite high TDS indicator (>400 ppm); food handling protocol absent |
| Below 40 | System uses contaminated water source; soil-adjacent exposure risk; no mitigation |

**Assessment procedure:**
1. Check `water_source` and `water_tds_ppm` from Profile JSON
   - TDS < 200 ppm: full marks for water quality
   - TDS 200–400 ppm: minor deduction; recommend carbon filter
   - TDS > 400 ppm: significant deduction; require RO filter recommendation in design
2. Check `space_type`: rooftop systems have higher contamination risk from air pollution (consider in tropical/industrial cities)
3. Check whether nutrient schedule uses food-grade inputs (assumed yes for hydroponics; deduct if user mentioned synthetic soil fertilizers)
4. Record: `D1_score`, `D1_rationale`, `D1_citations: ["FAO UA Guidelines 2010, Ch.4"]`

**Complete D1 Scoring Implementation:**

```python
from typing import Dict

class FoodSafetyScorer:
    """
    Score Food Safety Compliance (D1) based on FAO Urban Agriculture Guidelines.
    Chapter 4: Food Safety Standards for Urban Farms
    """
    
    def __init__(self, profile: Dict, design_spec: Dict):
        """
        Initialize scorer with profile and design specification.
        
        Args:
            profile: Validated profile from sub-profile-intake
            design_spec: Design specification from sub-system-designer
        """
        self.profile = profile
        self.design = design_spec
        self.framework = "FAO Urban and Peri-Urban Agriculture Guidelines (2010), Chapter 4"
    
    def score(self) -> Dict:
        """
        Calculate D1 score (0-100) with rationale and citations.
        
        Returns:
            {
                "score": float,
                "rationale": str,
                "citations": list[str],
                "risk_factors": list[str],
                "recommendations": list[str]
            }
        """
        score = 100.0
        deductions = []
        risk_factors = []
        recommendations = []
        
        # Water quality assessment
        water_source = self.profile.get("water_source", "municipal")
        water_tds = self.profile.get("water_tds_ppm", 200)
        
        if water_source == "municipal":
            if water_tds < 100:
                # Excellent municipal water
                pass
            elif water_tds < 200:
                # Good municipal water
                pass
            elif water_tds < 400:
                # Elevated TDS — recommend carbon filter
                score -= 5
                deductions.append(f"Elevated TDS ({water_tds} ppm) — carbon filter recommended")
                recommendations.append("Install carbon filter to remove chlorine and reduce TDS")
            else:
                # High TDS — RO filtration required
                score -= 15
                deductions.append(f"High TDS ({water_tds} ppm) exceeds 400 ppm threshold")
                risk_factors.append("Water quality risk: high TDS may contain unknown contaminants")
                recommendations.append("Install reverse osmosis (RO) filtration system — mandatory for food safety")
        
        elif water_source == "well":
            score -= 5
            deductions.append("Well water source: requires quarterly testing for pathogens and heavy metals")
            risk_factors.append("Well water: contamination risk varies by location")
            recommendations.append("Test well water quarterly for E. coli, heavy metals, and nitrates")
        
        elif water_source == "rainwater":
            score -= 10
            deductions.append("Rainwater harvesting: requires filtration and storage safety")
            risk_factors.append("Rainwater: collection surface contamination risk")
            recommendations.append("Install first-flush diverter and UV sterilization for rainwater")
        
        # Space type assessment
        space_type = self.profile.get("space_type", "")
        if space_type == "rooftop":
            # Rooftop systems have air quality considerations
            city = self.profile.get("city", "")
            
            # High-risk cities for air pollution
            high_pollution_cities = [
                "delhi", "beijing", "lahore", "dhaka", "katowice", 
                "heping", " cairo", "tehran", "london"
            ]
            
            if any(city_name in city.lower() for city_name in high_pollution_cities):
                score -= 8
                deductions.append(f"Rooftop in high-air-pollution city ({city})")
                risk_factors.append("Airborne particulate deposition on foliage")
                recommendations.append("Rinse foliage before harvest; consider air filtration if enclosed")
            else:
                score -= 3
                deductions.append("Rooftop system: general air quality consideration")
                recommendations.append("Monitor local air quality index; rinse foliage before harvest")
        
        # Check for RO filter in design if TDS > 400
        if water_tds > 400:
            equipment_list = self.design.get("equipment_list", [])
            has_ro_filter = any("RO" in item.get("item", "").upper() or 
                              "reverse osmosis" in item.get("item", "").lower()
                              for item in equipment_list)
            
            if not has_ro_filter:
                score -= 20
                deductions.append("CRITICAL: No RO filter specified for high-TDS water source")
                risk_factors.append("Food safety violation: high-TDS water without treatment")
            else:
                # Recovery points for having RO filter
                score += 10
        
        # System type check (soilless = automatic points)
        system_type = self.design.get("system_type", "").lower()
        if system_type in ["kratky", "dwc", "nft", "aeroponics"]:
            # Soilless system — good
            pass
        else:
            score -= 30
            deductions.append("Non-soilless system: soil contamination risk")
        
        # Check for food safety protocol in design
        if "food_safety" not in str(self.design).lower():
            recommendations.append("Implement food safety protocol: worker hygiene, harvest sanitation")
        
        # Clamp score
        score = max(0, min(100, score))
        
        # Build rationale
        rationale = f"Food Safety Score: {score}/100. "
        if deductions:
            rationale += "Deductions: " + "; ".join(deductions) + ". "
        else:
            rationale += "No significant risks identified. "
        
        if recommendations:
            rationale += "Recommendations: " + "; ".join(recommendations[:3])
        
        return {
            "score": round(score, 1),
            "rationale": rationale,
            "citations": [self.framework],
            "risk_factors": risk_factors,
            "recommendations": recommendations
        }
```

### Step 3: Score Dimension 2 — Light Adequacy (DLI)

Framework: ASABE Standard EP 506 (Plant Growth Lighting); DLI tables (SECOND-KNOWLEDGE-BRAIN.md Section 1.1)

**Rubric (0–100):**

| Score | Criterion |
|-------|-----------|
| 90–100 | Effective DLI meets or exceeds `dli_optimal` for all target crops for all 12 months |
| 75–89 | Effective DLI meets `dli_min` for all crops all year; meets optimal for ≥8 months |
| 60–74 | DLI gap exists in winter months (<4 months below optimal); supplemental LED plan is specified and correct |
| 40–59 | DLI gap is persistent (>4 months below optimal); LED plan exists but undersized (calculated wattage insufficient) |
| Below 40 | Effective DLI below `dli_min` for any crop for any month without a supplemental plan |

**Assessment procedure:**
1. From Design Specification `dli_analysis`:
   - Count months where `effective_DLI >= dli_optimal` for worst-DLI crop
   - Count months where `effective_DLI >= dli_min` for worst-DLI crop
   - Check: if `supplemental_led_required = true`, verify `supplemental_wattage` calculation is correct
     - Recalculate: `required_PPFD = DLI_gap × 1,000,000 / (photoperiod_hours × 3600)`
     - Verify stated wattage = `required_PPFD × growing_area / 2.5 μmol/J`
2. Record: `D2_score`, `D2_rationale`, `D2_citations: ["ASABE EP 506", "DLI reference table, SECOND-KNOWLEDGE-BRAIN.md S1.1"]`

**Complete D2 Scoring Implementation:**

```python
from typing import Dict, List

class LightAdequacyScorer:
    """
    Score Light Adequacy / DLI (D2) based on ASABE EP506 and crop-specific DLI requirements.
    """
    
    def __init__(self, profile: Dict, design_spec: Dict):
        """
        Initialize scorer with profile and design specification.
        
        Args:
            profile: Validated profile from sub-profile-intake
            design_spec: Design specification from sub-system-designer
        """
        self.profile = profile
        self.design = design_spec
        self.frameworks = [
            "ASABE Standard EP506 (Plant Growth Lighting)",
            "DLI tables, SECOND-KNOWLEDGE-BRAIN.md Section 1.1"
        ]
    
    def score(self) -> Dict:
        """
        Calculate D2 score (0-100) with rationale and citations.
        
        Returns:
            {
                "score": float,
                "rationale": str,
                "citations": list[str],
                "monthly_analysis": list[dict],
                "recommendations": list[str]
            }
        """
        score = 100.0
        deductions = []
        recommendations = []
        monthly_analysis = []
        
        # Get DLI analysis from design
        dli_analysis = self.design.get("dli_analysis", {})
        monthly_data = dli_analysis.get("monthly_data", [])
        
        if not monthly_data:
            return {
                "score": 0,
                "rationale": "DLI analysis was not performed — cannot assess light adequacy",
                "citations": self.frameworks,
                "monthly_analysis": [],
                "recommendations": ["Run DLI calculation before scoring"]
            }
        
        # Get target crops and find worst-case DLI requirements
        target_crops = self.profile.get("target_crops", [])
        if not target_crops:
            return {
                "score": 0,
                "rationale": "No target crops specified — cannot assess light adequacy",
                "citations": self.frameworks,
                "monthly_analysis": [],
                "recommendations": ["Specify target crops before scoring"]
            }
        
        # Find crop with highest DLI requirement
        max_dli_min = max(crop.get("dli_min", 6) for crop in target_crops)
        max_dli_optimal = max(crop.get("dli_optimal", 14) for crop in target_crops)
        
        # Analyze each month
        months_at_optimal = 0
        months_at_minimum = 0
        months_below_minimum = 0
        months_requiring_supplement = 0
        
        for month_data in monthly_data:
            month = month_data.get("month", 1)
            effective_dli = month_data.get("effective_dli", 0)
            supplemental_required = month_data.get("supplemental_required", False)
            supplemental_wattage = month_data.get("supplemental_wattage_m2", 0)
            
            # Check against optimal
            at_optimal = effective_dli >= max_dli_optimal
            at_minimum = effective_dli >= max_dli_min
            below_minimum = effective_dli < max_dli_min
            
            if at_optimal:
                months_at_optimal += 1
            elif at_minimum:
                months_at_minimum += 1
            elif below_minimum and not supplemental_required:
                months_below_minimum += 1
                score -= 5
                deductions.append(f"Month {month}: DLI {effective_dli} below minimum {max_dli_min}")
            
            if supplemental_required:
                months_requiring_supplement += 1
                
                # Verify supplemental wattage is adequate
                if supplemental_wattage > 0:
                    # Recalculate required wattage
                    dli_gap = max_dli_optimal - effective_dli
                    photoperiod = self.design.get("led_photoperiod_hours", 16)
                    required_ppfd = dli_gap * 1_000_000 / (photoperiod * 3600)
                    required_wattage = required_ppfd / 2.5  # Quality LED efficacy
                    
                    if supplemental_wattage < required_wattage * 0.9:
                        score -= 3
                        deductions.append(
                            f"Month {month}: Supplemental LED undersized "
                            f"({supplemental_wattage}W/m² vs. {required_wattage:.1f}W/m² required)"
                        )
                        recommendations.append(
                            f"Increase LED wattage for month {month} to {required_wattage:.1f}W/m²"
                        )
                else:
                    score -= 10
                    deductions.append(f"Month {month}: Supplemental lighting required but not specified")
                    recommendations.append(f"Add supplemental LED plan for month {month}")
            
            monthly_analysis.append({
                "month": month,
                "effective_dli": effective_dli,
                "optimal_target": max_dli_optimal,
                "minimum_target": max_dli_min,
                "at_optimal": at_optimal,
                "at_minimum": at_minimum,
                "below_minimum": below_minimum,
                "supplemental_required": supplemental_required
            })
        
        # Score tier assessment
        if months_at_optimal == 12:
            # Perfect score
            pass
        elif months_at_minimum == 12 and months_at_optimal >= 8:
            # Good score
            score -= 5
        elif months_below_minimum == 0 and months_requiring_supplement <= 4:
            # Acceptable with supplements
            score -= 10
        elif months_below_minimum > 0:
            # Poor score
            score -= 20
        
        # Build rationale
        rationale = (
            f"DLI Adequacy Score: {score}/100. "
            f"{months_at_optimal}/12 months at optimal DLI, "
            f"{months_at_minimum}/12 months at minimum DLI, "
            f"{months_below_minimum} months below minimum, "
            f"{months_requiring_supplement} months requiring supplement."
        )
        
        if deductions:
            rationale += " Issues: " + "; ".join(deductions[:3])
        
        return {
            "score": max(0, min(100, round(score, 1))),
            "rationale": rationale,
            "citations": self.frameworks,
            "monthly_analysis": monthly_analysis,
            "recommendations": recommendations
        }
```

### Step 4: Score Dimension 3 — Climate Suitability (VPD)

Framework: Buck Equation VPD calculation; VPD optimal ranges table (SECOND-KNOWLEDGE-BRAIN.md Section 1.2)

**Rubric (0–100):**

| Score | Criterion |
|-------|-----------|
| 90–100 | VPD within 0.8–1.2 kPa (vegetative optimal) for ≥10 months; management plan for other 2 months |
| 75–89 | VPD within 0.4–1.5 kPa for all months; management recommendations for >1.5 kPa months included |
| 60–74 | VPD exceeds 1.5 kPa for 1–3 months; management recommendations provided but incomplete |
| 40–59 | VPD outside 0.4–1.5 range for >3 months; no management plan; or VPD analysis was not performed |
| Below 40 | VPD analysis absent; or VPD > 2.0 kPa in multiple months with no mitigation |

**Assessment procedure:**
1. From Design Specification `vpd_analysis`:
   - Count months within optimal range (0.4–1.5 kPa)
   - Check whether recommendations exist for out-of-range months
   - If enclosed space (balcony with enclosure / indoor): note that outdoor VPD values may overestimate actual growing environment VPD — apply +/- 15% uncertainty band
2. Record: `D3_score`, `D3_rationale`, `D3_citations: ["Buck equation", "VPD ranges, SECOND-KNOWLEDGE-BRAIN.md S1.2"]`

### Step 5: Score Dimension 4 — Nutrient Management

Framework: Hoagland & Arnon (1950, revised); Kim et al. (2022) MDPI Horticulturae meta-analysis

**Rubric (0–100):**

| Score | Criterion |
|-------|-----------|
| 90–100 | EC and pH targets match crop-specific optimal ranges for all growth stages; solution change schedule specified; multiple-crop EC/pH intersections verified |
| 75–89 | EC/pH correct for primary crop; secondary crops within acceptable (not optimal) range; solution change schedule present |
| 60–74 | EC/pH within general hydroponic acceptable range (1.0–2.5 mS/cm, pH 5.8–6.5) but not crop-stage-specific |
| 40–59 | EC/pH targets outside acceptable range for any crop at any stage; or nutrient schedule is absent |
| Below 40 | No nutrient management plan; or targets contradict published standards |

**Assessment procedure:**
1. For each crop in `target_crops`:
   - Check each stage's EC against `ec_min` and `ec_max` from Profile JSON
   - Check each stage's pH against `ph_min` and `ph_max` from Profile JSON
   - Check: if multiple crops share a system, verify EC/pH intersection is valid
2. Check nutrient schedule has entries for: seedling / vegetative / (fruiting if fruiting crop) / harvest
3. Record: `D4_score`, `D4_rationale`, `D4_citations: ["Hoagland & Arnon 1950", "Kim et al. 2022, MDPI Horticulturae"]`

### Step 6: Score Dimension 5 — Water Use Efficiency

Framework: WEF Nexus (Hoff 2011); Martin & van Klink (2021) Journal of Cleaner Production benchmarks

**Rubric (0–100):**

| Score | Criterion |
|-------|-----------|
| 90–100 | Water consumption < 1.0 L/kg yield (Kratky/NFT best case); recirculation system active; no discharge plan |
| 75–89 | Water consumption 1.0–2.0 L/kg yield (DWC/NFT standard); recirculation specified |
| 60–74 | Water consumption 2.0–5.0 L/kg yield; or non-recirculating system without justification |
| 40–59 | Water consumption > 5.0 L/kg yield; or water budget calculation absent |
| Below 40 | No water budget; or evidence of waste discharge without treatment |

**Assessment procedure:**
1. Compute: `water_efficiency = water_budget.L_per_week / (yield_estimate.total_g_per_week / 1000)`
   - Units: L/kg yield
2. Compare to benchmarks:
   - < 1.0 L/kg: excellent (leafy greens, NFT/Kratky)
   - 1.0–2.0 L/kg: good (fruiting crops, DWC)
   - > 2.0 L/kg: flag for improvement
3. Check: is system recirculating? (NFT, DWC: yes; Kratky: yes after drain-to-waste; Aeroponics: recirculating by design)
4. Record: `D5_score`, `D5_rationale`, `D5_citations: ["WEF Nexus, Hoff 2011", "Martin & van Klink 2021"]`

### Step 7: Score Dimension 6 — Yield Potential

Framework: System yield benchmarks from SECOND-KNOWLEDGE-BRAIN.md Section 1.4 and Section 3.1

**Rubric (0–100):**

| Score | Criterion |
|-------|-----------|
| 90–100 | Projected yield/m² is within top quartile for selected system type and crop |
| 75–89 | Projected yield/m² matches median published benchmark ± 20% |
| 60–74 | Projected yield/m² is 20–40% below median benchmark (DLI or space constraint) |
| 40–59 | Projected yield/m² is > 40% below median benchmark |
| Below 40 | Yield estimate absent or system fundamentally mismatched to target crops |

**Assessment procedure:**
1. Compute: `yield_per_m2_per_week = yield_estimate.total_g_per_week / layout.growing_area_m2`
2. Compare to published benchmarks per system type:
   - Kratky lettuce: 10–16 g/m²/week (slower cycle)
   - DWC lettuce: 16–22 g/m²/week
   - NFT lettuce: 18–25 g/m²/week
   - Aeroponics lettuce: 22–32 g/m²/week
3. Check: if effective DLI < dli_optimal, apply DLI yield reduction factor (linear: 10% reduction per 2 mol/m²/day below optimal)
4. Record: `D6_score`, `D6_rationale`, `D6_citations: ["SECOND-KNOWLEDGE-BRAIN.md S1.4 benchmarks"]`

### Step 8: Score Dimension 7 — Structural & Electrical Safety

Framework: Local residential building codes (general); IEC 60364 (electrical installations in buildings); OSHA residential standards

**Rubric (0–100):**

| Score | Criterion |
|-------|-----------|
| 90–100 | System weight ≤ 30% of rated structural load; all electrical loads within residential circuit breaker limits; safety checklist complete |
| 75–89 | System weight 30–50% of rated load; electrical load within limits; minor safety flag addressed |
| 60–74 | System weight 50–70% of rated load; or electrical load close to limit; professional assessment recommended |
| 40–59 | System weight > 70% of rated load; or electrical load exceeds residential standard circuit (15A/1800W) without dedicated circuit |
| Below 40 | No structural or electrical assessment performed; or calculated weight exceeds rated capacity |

**Assessment procedure:**
1. Calculate system weight:
   - `system_weight_kg = reservoir_size_L × 1.0 + structure_weight_kg + grow_medium_weight_kg + plant_weight_kg`
   - Estimate: NFT system 1.5–2.5 kg/plant site + full reservoir; DWC 3–5 kg/site; Kratky 1.0–2.0 kg/site
   - `weight_per_m2 = system_weight / layout.total_area_m2`
2. Compare to `load_capacity_kg_m2` from Profile JSON (default: 200 kg/m² if unknown)
   - Utilization = weight_per_m2 / load_capacity_kg_m2
3. Check electrical load:
   - Total watts = LED_wattage + pump_wattage
   - Standard residential circuit: 15A × 120V = 1800W or 15A × 220V = 3300W (depending on country)
   - Flag if total load > 80% of circuit capacity
4. Record: `D7_score`, `D7_rationale`, `D7_citations: ["IEC 60364", "Local building code assumption"]`

### Step 9: Calculate composite score and produce output

```
Composite_Score = D1×0.15 + D2×0.20 + D3×0.15 + D4×0.20 + D5×0.15 + D6×0.10 + D7×0.05
```

**Score interpretation:**
| Composite Score | Rating |
|-----------------|--------|
| 90–100 | Excellent — production-ready design |
| 75–89 | Good — minor improvements recommended |
| 60–74 | Acceptable — several important improvements needed |
| 40–59 | Marginal — significant redesign in key areas required |
| Below 40 | Poor — fundamental design flaws; major intervention required |

Identify:
- **Top 3 Strengths:** Dimensions with highest scores relative to their weight
- **Top 3 Weaknesses:** Dimensions with lowest scores relative to their weight (these drive the improvement roadmap)

**Complete Composite Scoring Implementation:**

```python
from typing import Dict, List, Tuple

class CompositeScorer:
    """
    Calculate composite score across 7 scoring dimensions.
    Weighted average formula with strength/weakness identification.
    """
    
    # Dimension weights (sum = 1.0)
    WEIGHTS = {
        "D1_food_safety": 0.15,
        "D2_light_dli": 0.20,
        "D3_climate_vpd": 0.15,
        "D4_nutrients": 0.20,
        "D5_water_efficiency": 0.15,
        "D6_yield_potential": 0.10,
        "D7_safety": 0.05
    }
    
    # Dimension display names
    DIMENSION_NAMES = {
        "D1_food_safety": "Food Safety Compliance",
        "D2_light_dli": "Light Adequacy (DLI)",
        "D3_climate_vpd": "Climate Suitability (VPD)",
        "D4_nutrients": "Nutrient Management",
        "D5_water_efficiency": "Water Use Efficiency",
        "D6_yield_potential": "Yield Potential",
        "D7_safety": "Structural & Electrical Safety"
    }
    
    # Rating thresholds
    RATING_THRESHOLDS = [
        (90, "Excellent — production-ready design"),
        (75, "Good — minor improvements recommended"),
        (60, "Acceptable — several important improvements needed"),
        (40, "Marginal — significant redesign required"),
        (0, "Poor — fundamental design flaws")
    ]
    
    def __init__(self, dimension_scores: Dict[str, Dict]):
        """
        Initialize composite scorer with individual dimension scores.
        
        Args:
            dimension_scores: Dict mapping dimension keys to score dicts
                {
                    "D1_food_safety": {"score": 88, "rationale": "...", "citations": [...]},
                    "D2_light_dli": {"score": 72, "rationale": "...", "citations": [...]},
                    ...
                }
        """
        self.dimension_scores = dimension_scores
    
    def calculate_composite(self) -> Dict:
        """
        Calculate composite score and identify strengths/weaknesses.
        
        Returns:
            {
                "scores": {
                    "D1_food_safety": {"score": 88, "weight": 0.15, "weighted": 13.2, ...},
                    ...
                },
                "composite_score": float,
                "rating": str,
                "strengths": list[str],
                "weaknesses": list[str]
            }
        """
        scores_output = {}
        weighted_sum = 0.0
        
        # Calculate weighted scores
        for dim_key, weight in self.WEIGHTS.items():
            dim_data = self.dimension_scores.get(dim_key, {})
            raw_score = dim_data.get("score", 0)
            weighted_score = raw_score * weight
            
            scores_output[dim_key] = {
                "score": raw_score,
                "weight": weight,
                "weighted": round(weighted_score, 2),
                "rationale": dim_data.get("rationale", ""),
                "citations": dim_data.get("citations", [])
            }
            
            weighted_sum += weighted_score
        
        composite_score = round(weighted_sum, 1)
        
        # Determine rating
        rating = "Unknown"
        for threshold, label in self.RATING_THRESHOLDS:
            if composite_score >= threshold:
                rating = label
                break
        
        # Identify strengths and weaknesses
        dimensions_by_performance = []
        for dim_key, weight in self.WEIGHTS.items():
            dim_data = self.dimension_scores.get(dim_key, {})
            score = dim_data.get("score", 0)
            # Sort by weighted performance (score relative to weight importance)
            performance_metric = score * weight
            dimensions_by_performance.append((dim_key, score, performance_metric))
        
        # Sort descending by performance
        dimensions_by_performance.sort(key=lambda x: x[2], reverse=True)
        
        # Top 3 strengths
        strengths = []
        for dim_key, score, _ in dimensions_by_performance[:3]:
            dim_name = self.DIMENSION_NAMES.get(dim_key, dim_key)
            strengths.append(f"{dim_name} (D{dim_key[1]}): {score}/100")
        
        # Bottom 3 weaknesses
        weaknesses = []
        for dim_key, score, _ in dimensions_by_performance[-3:]:
            dim_name = self.DIMENSION_NAMES.get(dim_key, dim_key)
            weaknesses.append(f"{dim_name} (D{dim_key[1]}): {score}/100")
        
        return {
            "scores": scores_output,
            "composite_score": composite_score,
            "rating": rating,
            "strengths": strengths,
            "weaknesses": weaknesses
        }
    
    def generate_scorecard(self) -> str:
        """
        Generate formatted scorecard for output.
        
        Returns:
            Formatted string scorecard
        """
        composite = self.calculate_composite()
        
        lines = [
            "DESIGN SCORECARD",
            "-" * 70,
            f"{'Dimension':<35} {'Score':>8} {'Weight':>8} {'Weighted':>10}",
            "-" * 70
        ]
        
        for dim_key in ["D1_food_safety", "D2_light_dli", "D3_climate_vpd", 
                       "D4_nutrients", "D5_water_efficiency", "D6_yield_potential", "D7_safety"]:
            dim_name = self.DIMENSION_NAMES.get(dim_key, dim_key)
            dim_data = composite["scores"][dim_key]
            score = dim_data["score"]
            weight_pct = dim_data["weight"] * 100
            weighted = dim_data["weighted"]
            
            lines.append(f"{dim_name:<35} {score:>7.1f} {weight_pct:>7.0f}% {weighted:>10.2f}")
        
        lines.append("-" * 70)
        lines.append(f"{'COMPOSITE SCORE:':<35} {composite['composite_score']:>24.1f}")
        lines.append(f"{'Rating:':<35} {composite['rating']:>24}")
        
        return "\n".join(lines)
```

---

## Outputs

Scored Report:

```json
{
  "scores": {
    "D1_food_safety": {"score": 88, "weight": 0.15, "weighted": 13.2, "rationale": "...", "citations": [...]},
    "D2_light_dli": {"score": 72, "weight": 0.20, "weighted": 14.4, "rationale": "...", "citations": [...]},
    "D3_climate_vpd": {"score": 81, "weight": 0.15, "weighted": 12.2, "rationale": "...", "citations": [...]},
    "D4_nutrients": {"score": 90, "weight": 0.20, "weighted": 18.0, "rationale": "...", "citations": [...]},
    "D5_water_efficiency": {"score": 85, "weight": 0.15, "weighted": 12.8, "rationale": "...", "citations": [...]},
    "D6_yield_potential": {"score": 68, "weight": 0.10, "weighted": 6.8, "rationale": "...", "citations": [...]},
    "D7_safety": {"score": 92, "weight": 0.05, "weighted": 4.6, "rationale": "...", "citations": [...]}
  },
  "composite_score": 82.0,
  "rating": "Good — minor improvements recommended",
  "strengths": [
    "Strong nutrient management plan with crop-stage-specific EC/pH (D4: 90)",
    "Food safety well-addressed with soilless system and clean water source (D1: 88)",
    "Structural load within safe parameters (D7: 92)"
  ],
  "weaknesses": [
    "DLI deficit in November–February without full LED supplemental plan (D2: 72)",
    "Yield potential below NFT benchmark due to partial shade (D6: 68)",
    "VPD exceeds 1.5 kPa in dry season months without misting plan (D3: 81)"
  ]
}
```

---

## Quality Gate

Scored Report passes to sub-improvement-roadmap ONLY when ALL of the following are true:

- [ ] All 7 dimensions have numeric scores (0–100)
- [ ] Each score has a written rationale (minimum 1 sentence)
- [ ] Each score cites at least one named framework or paper
- [ ] Composite score is computed using the weighted formula
- [ ] Rating label is assigned from the interpretation table
- [ ] Exactly 3 strengths and 3 weaknesses are identified
- [ ] Weaknesses correspond to the lowest-weighted-score dimensions (consistent with data)
