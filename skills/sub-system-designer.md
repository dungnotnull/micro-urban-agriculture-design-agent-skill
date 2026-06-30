---
name: sub-system-designer
description: Design a complete hydroponics/aeroponics system — layout, DLI/VPD calculations, nutrient schedule, water/energy budgets — tailored to the user's profile.
---

## Purpose

Transform the validated Profile JSON from sub-profile-intake into a complete, quantified system design. This sub-skill performs the core engineering work of the harness: selecting the optimal soilless system type, calculating precise light and climate requirements using DLI and VPD physics, building a week-by-week nutrient schedule with EC/pH targets, and projecting water and energy budgets. The output is a Design Specification document that sub-scoring-engine evaluates.

---

## Inputs

- Validated Profile JSON (from sub-profile-intake)
- Access to WebSearch (weather API, solar irradiance data)
- Access to WebFetch (DLI tables, VPD charts, system benchmarks)
- Access to SECOND-KNOWLEDGE-BRAIN.md (fallback + framework reference)

---

## Workflow

### Step 1: Calculate DLI for user's location and season

Using the Profile JSON's `latitude`, `avg_monthly_solar_irradiance`, and `orientation`:

**DLI Calculation Procedure:**
1. Retrieve monthly average solar irradiance (kWh/m²/day) for user's location
   - Primary: WebSearch `"NASA POWER API solar irradiance {latitude} {longitude}"` or `"{city} monthly solar irradiance kWh/m2"`
   - Fallback: Use SECOND-KNOWLEDGE-BRAIN.md latitude band table (Section 1.1)
2. Convert irradiance to PPFD: `PPFD (μmol/m²/s) ≈ solar_irradiance_kWh/m2/day × 1000 / 3.6 / daylight_hours × conversion_factor`
   - Simplified: `DLI (mol/m²/day) ≈ solar_irradiance_kWh/m2/day × 4.6` (standard conversion, clear sky)
3. Apply orientation factor:
   - South-facing (northern hemisphere) / North-facing (southern hemisphere): 100%
   - East/West-facing: 60–70% of peak DLI
   - North-facing (NH) / South-facing (SH): 25–40% of peak DLI
   - Diagonal orientations: interpolate
4. Apply shade reduction: `effective_DLI = DLI × (1 - shade_fraction)`
5. Compute worst-case month (winter solstice) and best-case month (summer solstice) DLI
6. Compare effective DLI to each crop's `dli_optimal` from Profile JSON:
   - Gap = dli_optimal - effective_DLI
   - If gap > 0: calculate required supplemental PPFD and LED wattage
   - `required_PPFD = gap × 1,000,000 / (photoperiod_hours × 3600)`
   - `LED_wattage = required_PPFD × growing_area_m2 / led_efficacy_umol_per_J` (use 2.5 μmol/J for quality LED)

Record for each month: `natural_DLI`, `effective_DLI`, `supplemental_required (true/false)`, `supplemental_PPFD`, `LED_wattage`

**Complete DLI Calculation Implementation:**

```python
import math
from typing import Tuple, List

class DLICalculator:
    """
    Daily Light Integral (DLI) calculator for urban agriculture.
    References: ASABE EP506, FAO Urban Agriculture Guidelines
    """
    
    # Orientation factors (fraction of peak DLI received)
    ORIENTATION_FACTORS = {
        "south": 1.0,      # Northern hemisphere optimum
        "southeast": 0.85,
        "southwest": 0.85,
        "east": 0.65,
        "west": 0.65,
        "northeast": 0.50,
        "northwest": 0.50,
        "north": 0.35,      # Northern hemisphere worst case
    }
    
    # Southern hemisphere adjustment (swap N/S)
    SOUTHERN_HEMISPHERE_ORIENTATIONS = {
        "north": 1.0,      # Southern hemisphere optimum
        "northeast": 0.85,
        "northwest": 0.85,
        "east": 0.65,
        "west": 0.65,
        "southeast": 0.50,
        "southwest": 0.50,
        "south": 0.35,      # Southern hemisphere worst case
    }
    
    # Standard LED efficacy values (μmol/J)
    LED_EFFICACY = {
        "standard": 2.0,
        "quality": 2.5,
        "premium": 3.2
    }
    
    def __init__(self, latitude: float, longitude: float, hemisphere: str = "northern"):
        """
        Initialize DLI calculator.
        
        Args:
            latitude: Degrees latitude (negative for southern hemisphere)
            longitude: Degrees longitude
            hemisphere: "northern" or "southern"
        """
        self.latitude = abs(latitude)
        self.longitude = longitude
        self.hemisphere = hemisphere if latitude >= 0 else "southern"
        
    def get_orientation_factor(self, orientation: str) -> float:
        """Get DLI reduction factor for orientation."""
        orientation = orientation.lower().replace("-", "").replace(" ", "")
        
        if self.hemisphere == "southern":
            mapping = self.SOUTHERN_HEMISPHERE_ORIENTATIONS
        else:
            mapping = self.ORIENTATION_FACTORS
            
        # Handle combined orientations (e.g., "southwest" → "southwest")
        for key, value in mapping.items():
            if key.replace(" ", "") in orientation:
                return value
        
        # Default to east/west if not found
        return 0.65
    
    def estimate_daylight_hours(self, month: int, latitude: float) -> float:
        """
        Estimate average daylight hours for a month at given latitude.
        Based on simplified astronomical calculation.
        """
        # Day of year for middle of month
        day_of_year = [15, 45, 74, 105, 135, 166, 196, 227, 258, 288, 319, 349][month - 1]
        
        # Solar declination
        declination = 23.45 * math.sin(math.radians(360 / 365 * (day_of_year - 81)))
        
        # Hour angle
        lat_rad = math.radians(latitude)
        dec_rad = math.radians(declination)
        
        # Daylight hours (simplified)
        try:
            hour_angle = math.degrees(math.acos(-math.tan(lat_rad) * math.tan(dec_rad)))
            daylight_hours = 2 * hour_angle / 15
        except (ValueError, ZeroDivisionError):
            # Polar region cases
            daylight_hours = 0 if latitude * declination < 0 else 24
        
        return max(0, min(24, daylight_hours))
    
    def calculate_monthly_dli(
        self,
        monthly_irradiance: List[float],  # kWh/m²/day
        orientation: str,
        shade_fraction: float = 0.0,
        photoperiod_hours: float = 16.0
    ) -> List[dict]:
        """
        Calculate effective DLI for all 12 months.
        
        Returns list of dicts with monthly DLI data:
        {
            "month": 1-12,
            "solar_irradiance_kwh": float,
            "daylight_hours": float,
            "natural_dli": float,
            "orientation_factor": float,
            "shade_factor": float,
            "effective_dli": float,
            "supplemental_required": bool,
            "supplemental_ppfd": float,
            "supplemental_wattage_m2": float
        }
        """
        orientation_factor = self.get_orientation_factor(orientation)
        shade_factor = 1.0 - shade_fraction
        
        monthly_data = []
        
        for month, irradiance in enumerate(monthly_irradiance, 1):
            daylight_hours = self.estimate_daylight_hours(month, self.latitude)
            
            # Convert solar irradiance to natural DLI
            # DLI (mol/m²/day) ≈ irradiance (kWh/m²/day) × 4.6
            natural_dli = irradiance * 4.6
            
            # Apply orientation and shade factors
            effective_dli = natural_dli * orientation_factor * shade_factor
            
            # Base PPFD from effective DLI
            # PPFD = DLI × 1,000,000 / (photoperiod × 3600)
            base_ppfd = effective_dli * 1_000_000 / (photoperiod_hours * 3600) if photoperiod_hours > 0 else 0
            
            monthly_data.append({
                "month": month,
                "solar_irradiance_kwh": irradiance,
                "daylight_hours": daylight_hours,
                "natural_dli": round(natural_dli, 2),
                "orientation_factor": orientation_factor,
                "shade_factor": shade_factor,
                "effective_dli": round(effective_dli, 2),
                "base_ppfd": round(base_ppfd, 1),
                "supplemental_required": False,
                "supplemental_ppfd": 0.0,
                "supplemental_wattage_m2": 0.0
            })
        
        return monthly_data
    
    def calculate_supplemental_lighting(
        self,
        monthly_data: List[dict],
        crop_dli_requirements: List[dict],  # [{"dli_min": X, "dli_optimal": Y}, ...]
        photoperiod_hours: float,
        led_efficacy: str = "quality"
    ) -> List[dict]:
        """
        Calculate supplemental lighting requirements for all months.
        
        Args:
            monthly_data: Output from calculate_monthly_dli()
            crop_dli_requirements: List of crop DLI requirements
            photoperiod_hours: Target photoperiod for supplemental lighting
            led_efficacy: LED quality tier
            
        Returns: Updated monthly_data with supplemental requirements
        """
        efficacy = self.LED_EFFICACY.get(led_efficacy, 2.5)
        
        # Find worst-case crop (highest DLI requirement)
        max_dli_optimal = max(crop.get("dli_optimal", 12) for crop in crop_dli_requirements)
        
        for month_data in monthly_data:
            effective_dli = month_data["effective_dli"]
            
            # Calculate DLI gap
            dli_gap = max(0, max_dli_optimal - effective_dli)
            
            if dli_gap > 0.5:  # Threshold for requiring supplementation
                month_data["supplemental_required"] = True
                
                # Required PPFD to fill gap
                supplemental_ppfd = dli_gap * 1_000_000 / (photoperiod_hours * 3600)
                
                # LED wattage per m²
                wattage_m2 = supplemental_ppfd / efficacy
                
                month_data["supplemental_ppfd"] = round(supplemental_ppfd, 1)
                month_data["supplemental_wattage_m2"] = round(wattage_m2, 1)
        
        return monthly_data
    
    def generate_dli_summary(self, monthly_data: List[dict]) -> dict:
        """Generate summary statistics for DLI analysis."""
        effective_dlis = [m["effective_dli"] for m in monthly_data]
        
        return {
            "annual_average_dli": round(sum(effective_dlis) / 12, 2),
            "peak_month_dli": max(effective_dlis),
            "minimum_month_dli": min(effective_dlis),
            "supplemental_months": sum(1 for m in monthly_data if m["supplemental_required"]),
            "max_supplemental_wattage": max((m["supplemental_wattage_m2"] for m in monthly_data), default=0)
        }
```

### Step 2: Calculate VPD for growing environment

Using `avg_monthly_temp_c` and `avg_monthly_humidity_pct`:

1. For each month, compute VPD:
   - `SVP (kPa) = 0.6108 × exp(17.27 × T / (T + 237.3))`
   - `VPD (kPa) = SVP × (1 - RH/100)`
2. Compare to optimal VPD ranges from SECOND-KNOWLEDGE-BRAIN.md Section 1.2
3. Classify each month:
   - VPD < 0.4: "High humidity risk — increase ventilation; risk of mold/root rot"
   - VPD 0.4–1.5: "Optimal range for most crops"
   - VPD > 1.5: "High VPD — increase misting frequency; reduce feeding EC during heat peaks"
4. Note: indoor balcony/enclosed terrace environments may differ significantly from outdoor weather station data — flag this uncertainty
5. Identify worst-case VPD month and recommend management strategy

**Complete VPD Calculation Implementation:**

```python
import math
from typing import List, Dict

class VPDCalculator:
    """
    Vapor Pressure Deficit (VPD) calculator for plant transpiration management.
    Reference: Buck equation (1981), ASABE EP536
    """
    
    # VPD optimal ranges by growth stage (kPa)
    VPD_RANGES = {
        "seedling": {"optimal": (0.4, 0.8), "min": 0.3, "max": 1.0},
        "vegetative": {"optimal": (0.8, 1.2), "min": 0.5, "max": 1.5},
        "flowering": {"optimal": (1.0, 1.5), "min": 0.8, "max": 1.8},
        "fruiting": {"optimal": (1.2, 1.6), "min": 0.8, "max": 2.0}
    }
    
    # Risk classifications
    RISK_LEVELS = {
        "too_low": (0, 0.4, "High humidity risk — mold, root rot, poor transpiration"),
        "optimal": (0.4, 1.5, "Optimal transpiration range for most crops"),
        "moderate_high": (1.5, 2.0, "Elevated VPD — increased misting needed"),
        "too_high": (2.0, 10.0, "Severe VPD stress — stomatal closure, wilt risk")
    }
    
    @staticmethod
    def saturation_vapor_pressure(temp_c: float) -> float:
        """
        Calculate saturation vapor pressure using Buck equation.
        
        Args:
            temp_c: Temperature in Celsius
            
        Returns:
            SVP in kPa
        """
        # Buck equation (1981) accurate to 0.1% over -40°C to +50°C
        return 0.6108 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
    
    @staticmethod
    def calculate_vpd(temp_c: float, relative_humidity_pct: float) -> float:
        """
        Calculate Vapor Pressure Deficit.
        
        Args:
            temp_c: Air temperature in Celsius
            relative_humidity_pct: Relative humidity (0-100%)
            
        Returns:
            VPD in kPa
        """
        svp = VPDCalculator.saturation_vapor_pressure(temp_c)
        vpd = svp * (1 - relative_humidity_pct / 100.0)
        return round(vpd, 3)
    
    @classmethod
    def classify_vpd(cls, vpd: float, growth_stage: str = "vegetative") -> Dict:
        """
        Classify VPD value and provide management recommendations.
        
        Returns:
            {
                "vpd": float,
                "classification": str,
                "risk": str,
                "recommendation": str,
                "in_optimal_range": bool
            }
        """
        # Determine risk level
        classification = "optimal"
        risk = "None"
        recommendation = "No intervention needed"
        in_optimal = True
        
        if vpd < 0.4:
            classification = "too_low"
            risk = "High"
            recommendation = "Increase air circulation, reduce humidity sources, avoid overwatering"
            in_optimal = False
        elif vpd > 2.0:
            classification = "too_high"
            risk = "High"
            recommendation = "Add misting system, shade cloth, increase humidity; reduce EC during peak heat"
            in_optimal = False
        elif vpd > 1.5:
            classification = "moderate_high"
            risk = "Moderate"
            recommendation = "Monitor plant water stress; consider midday misting in hot months"
        
        # Check against growth-stage-specific optimal range
        stage_range = cls.VPD_RANGES.get(growth_stage, cls.VPD_RANGES["vegetative"])
        stage_min, stage_max = stage_range["optimal"]
        
        stage_optimal = stage_min <= vpd <= stage_max
        
        return {
            "vpd": vpd,
            "classification": classification,
            "risk": risk,
            "recommendation": recommendation,
            "in_optimal_range": in_optimal,
            "in_stage_optimal_range": stage_optimal,
            "stage_min": stage_min,
            "stage_max": stage_max
        }
    
    @classmethod
    def calculate_monthly_vpd(
        cls,
        monthly_temp_c: List[float],
        monthly_humidity_pct: List[float],
        growth_stage: str = "vegetative"
    ) -> List[Dict]:
        """
        Calculate and classify VPD for all 12 months.
        
        Returns:
            List of dicts with monthly VPD data
        """
        monthly_vpd = []
        
        for month, (temp, humidity) in enumerate(zip(monthly_temp_c, monthly_humidity_pct), 1):
            vpd = cls.calculate_vpd(temp, humidity)
            classification = cls.classify_vpd(vpd, growth_stage)
            
            monthly_vpd.append({
                "month": month,
                "temperature_c": temp,
                "humidity_pct": humidity,
                "vpd": vpd,
                "classification": classification["classification"],
                "risk": classification["risk"],
                "recommendation": classification["recommendation"],
                "in_optimal_range": classification["in_optimal_range"]
            })
        
        return monthly_vpd
    
    @classmethod
    def generate_vpd_summary(cls, monthly_vpd: List[Dict]) -> Dict:
        """Generate VPD summary statistics."""
        optimal_months = sum(1 for m in monthly_vpd if m["in_optimal_range"])
        too_low_months = sum(1 for m in monthly_vpd if m["classification"] == "too_low")
        too_high_months = sum(1 for m in monthly_vpd if m["classification"] in ["moderate_high", "too_high"])
        
        vpd_values = [m["vpd"] for m in monthly_vpd]
        
        return {
            "min_vpd": min(vpd_values),
            "max_vpd": max(vpd_values),
            "avg_vpd": round(sum(vpd_values) / 12, 3),
            "optimal_months": optimal_months,
            "low_vpd_months": too_low_months,
            "high_vpd_months": too_high_months,
            "worst_month": monthly_vpd[vpd_values.index(max(vpd_values))]["month"],
            "recommendations": cls._generate_monthly_recommendations(monthly_vpd)
        }
    
    @staticmethod
    def _generate_monthly_recommendations(monthly_vpd: List[Dict]) -> List[str]:
        """Generate specific management recommendations for problematic months."""
        recommendations = []
        
        for month_data in monthly_vpd:
            if not month_data["in_optimal_range"]:
                month_name = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                            "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][month_data["month"] - 1]
                recommendations.append(
                    f"{month_name}: VPD {month_data['vpd']} kPa — {month_data['recommendation']}"
                )
        
        return recommendations
```

### Step 3: Select optimal system type

Using the system comparison matrix from SECOND-KNOWLEDGE-BRAIN.md Section 1.4, score each applicable system against the user's profile:

**Scoring dimensions (each 0–5 points):**
1. **Budget fit:** Does system cost align with `budget_band`?
   - Kratky: optimal for Zero/Starter; NFT/DWC: Starter–Moderate; Aeroponics: Full–Commercial
2. **Experience fit:** Does system complexity match `experience_level`?
   - Kratky: Beginner; DWC: Beginner–Intermediate; NFT: Intermediate; Aeroponics: Advanced
3. **Maintenance fit:** Does maintenance burden match `maintenance_hours_per_week`?
   - Kratky: 0.5h/week; DWC: 1h/week; NFT: 1.5h/week; Aeroponics: 2.5h/week
4. **Crop compatibility:** Does the system suit the target crops?
   - Kratky: Leafy greens, herbs only; DWC: Leafy greens, herbs; NFT: Leafy + fruiting; Aeroponics: All
5. **Space efficiency:** Given `space_m2` and `orientation`, which system maximizes growing area?
   - NFT wall panels: highest vertical efficiency; Kratky tubs: good for flat surfaces; DWC: floor-space dependent
6. **Power availability:** `power_available = false` → Kratky is the only viable option (score others 0)

Select system with highest total score. Present top 2 alternatives with scores for transparency.

If user specified `preferred_system`: cross-check score. If preferred system scores ≥ 80% of top system, honor preference. If <80%, flag the gap and explain.

**Complete System Selection Implementation:**

```python
from typing import Dict, List, Tuple
from enum import Enum

class SystemType(Enum):
    KRATKY = "kratky"
    DWC = "dwc"  # Deep Water Culture
    NFT = "nft"  # Nutrient Film Technique
    AEROPONICS = "aeroponics"

class BudgetBand(Enum):
    ZERO = (0, 20)
    STARTER = (20, 100)
    MODERATE = (100, 500)
    FULL = (500, 2000)
    COMMERCIAL = (2000, float('inf'))

class ExperienceLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class SystemSelector:
    """
    Select optimal hydroponic system based on user profile constraints.
    Uses multi-criteria decision analysis (MCDA) with weighted scoring.
    """
    
    # System specifications
    SYSTEM_SPECS = {
        SystemType.KRATKY: {
            "name": "Kratky (Passive)",
            "budget_compatibility": [BudgetBand.ZERO, BudgetBand.STARTER],
            "min_budget_usd": 0,
            "max_budget_usd": 100,
            "experience_required": ExperienceLevel.BEGINNER,
            "maintenance_hours_week": 0.5,
            "crop_categories": ["leafy_greens", "herbs"],
            "space_efficiency": 0.7,  # Fraction of floor area usable
            "power_required": False,
            "yield_multiplier": 0.7,  # Relative to NFT baseline
            "failure_risk": 0.05,
            "sites_per_m2": 15,
            "reservoir_liters_per_site": 2.5
        },
        SystemType.DWC: {
            "name": "Deep Water Culture",
            "budget_compatibility": [BudgetBand.STARTER, BudgetBand.MODERATE],
            "min_budget_usd": 50,
            "max_budget_usd": 300,
            "experience_required": ExperienceLevel.BEGINNER,
            "maintenance_hours_week": 1.0,
            "crop_categories": ["leafy_greens", "herbs"],
            "space_efficiency": 0.75,
            "power_required": True,
            "yield_multiplier": 0.85,
            "failure_risk": 0.10,
            "sites_per_m2": 18,
            "reservoir_liters_per_site": 3.0
        },
        SystemType.NFT: {
            "name": "Nutrient Film Technique",
            "budget_compatibility": [BudgetBand.STARTER, BudgetBand.MODERATE, BudgetBand.FULL],
            "min_budget_usd": 100,
            "max_budget_usd": 800,
            "experience_required": ExperienceLevel.INTERMEDIATE,
            "maintenance_hours_week": 1.5,
            "crop_categories": ["leafy_greens", "herbs", "fruiting"],
            "space_efficiency": 0.9,  # Highest with vertical mounting
            "power_required": True,
            "yield_multiplier": 1.0,  # Baseline
            "failure_risk": 0.20,
            "sites_per_m2": 25,
            "reservoir_liters_per_site": 1.5
        },
        SystemType.AEROPONICS: {
            "name": "Aeroponics",
            "budget_compatibility": [BudgetBand.FULL, BudgetBand.COMMERCIAL],
            "min_budget_usd": 500,
            "max_budget_usd": 5000,
            "experience_required": ExperienceLevel.ADVANCED,
            "maintenance_hours_week": 2.5,
            "crop_categories": ["leafy_greens", "herbs", "fruiting"],
            "space_efficiency": 0.95,
            "power_required": True,
            "yield_multiplier": 1.15,
            "failure_risk": 0.35,
            "sites_per_m2": 35,
            "reservoir_liters_per_site": 0.8
        }
    }
    
    # Scoring weights (sum = 1.0)
    SCORING_WEIGHTS = {
        "budget_fit": 0.20,
        "experience_fit": 0.15,
        "maintenance_fit": 0.15,
        "crop_compatibility": 0.25,
        "space_efficiency": 0.15,
        "power_availability": 0.10
    }
    
    def __init__(self, profile: Dict):
        """
        Initialize system selector with user profile.
        
        Args:
            profile: Validated profile JSON from sub-profile-intake
        """
        self.profile = profile
        self.budget_band = self._determine_budget_band(profile["budget_usd"])
        self.crop_categories = self._determine_crop_categories(profile["target_crops"])
    
    def _determine_budget_band(self, budget_usd: float) -> BudgetBand:
        """Determine budget band from USD amount."""
        for band in BudgetBand:
            min_usd, max_usd = band.value
            if min_usd <= budget_usd < max_usd:
                return band
        return BudgetBand.COMMERCIAL
    
    def _determine_crop_categories(self, target_crops: List[Dict]) -> List[str]:
        """Extract crop categories from target crop list."""
        categories = set()
        for crop in target_crops:
            crop_name = crop.get("name", "").lower()
            # Simple categorization
            if crop_name in ["lettuce", "spinach", "kale", "arugula", "swiss_chard", "pak_choi"]:
                categories.add("leafy_greens")
            elif crop_name in ["basil", "mint", "cilantro", "parsley"]:
                categories.add("herbs")
            elif crop_name in ["tomato", "cherry_tomato", "cucumber", "pepper", "strawberry"]:
                categories.add("fruiting")
        return list(categories)
    
    def score_budget_fit(self, system: SystemType) -> float:
        """Score budget compatibility (0-5 points)."""
        spec = self.SYSTEM_SPECS[system]
        min_budget = spec["min_budget_usd"]
        max_budget = spec["max_budget_usd"]
        user_budget = self.profile["budget_usd"]
        
        if self.budget_band in spec["budget_compatibility"]:
            if user_budget >= max_budget * 0.8:
                return 5.0  # Full compatibility with headroom
            elif user_budget >= (min_budget + max_budget) / 2:
                return 4.0  # Good fit
            else:
                return 3.0  # Adequate fit
        else:
            # Budget mismatch
            if user_budget >= max_budget:
                return 4.0  # User has budget but system is under-specified
            else:
                return 1.0  # Insufficient budget
    
    def score_experience_fit(self, system: SystemType) -> float:
        """Score experience compatibility (0-5 points)."""
        spec = self.SYSTEM_SPECS[system]
        required = spec["experience_required"]
        user_level = ExperienceLevel(self.profile["experience_level"])
        
        level_order = [ExperienceLevel.BEGINNER, ExperienceLevel.INTERMEDIATE, ExperienceLevel.ADVANCED]
        user_idx = level_order.index(user_level)
        required_idx = level_order.index(required)
        
        if user_idx >= required_idx:
            return 5.0  # User meets or exceeds requirement
        elif user_idx == required_idx - 1:
            return 3.0  # One level below — challenging but learnable
        else:
            return 1.0  # Significantly under-qualified
    
    def score_maintenance_fit(self, system: SystemType) -> float:
        """Score maintenance time compatibility (0-5 points)."""
        spec = self.SYSTEM_SPECS[system]
        required_hours = spec["maintenance_hours_week"]
        available_hours = self.profile.get("maintenance_hours_per_week", 2.0)
        
        if available_hours >= required_hours * 1.5:
            return 5.0  # Comfortable margin
        elif available_hours >= required_hours:
            return 4.0  # Meets minimum
        elif available_hours >= required_hours * 0.7:
            return 2.0  # Tight but possible
        else:
            return 1.0  # Insufficient time
    
    def score_crop_compatibility(self, system: SystemType) -> float:
        """Score crop compatibility (0-5 points)."""
        spec = self.SYSTEM_SPECS[system]
        system_crops = set(spec["crop_categories"])
        user_crops = set(self.crop_categories)
        
        # Intersection score
        compatible = system_crops & user_crops
        incompatible = user_crops - system_crops
        
        if not incompatible:
            return 5.0  # All crops compatible
        elif len(compatible) >= len(user_crops) * 0.7:
            return 3.0  # Most crops compatible
        else:
            return 1.0  # Significant incompatibility
    
    def score_space_efficiency(self, system: SystemType) -> float:
        """Score space efficiency for user's space (0-5 points)."""
        spec = self.SYSTEM_SPECS[system]
        efficiency = spec["space_efficiency"]
        space_m2 = self.profile["space_m2"]
        orientation = self.profile["orientation"]
        
        # Bonus for vertical systems (NFT, aeroponics) in small spaces
        if space_m2 < 5 and system in [SystemType.NFT, SystemType.AEROPONICS]:
            efficiency += 0.1
        
        # Penalty for north-facing in northern hemisphere (reduced DLI)
        if orientation.lower() in ["north", "northeast", "northwest"]:
            efficiency -= 0.15
        
        return min(5.0, max(1.0, efficiency * 5))
    
    def score_power_availability(self, system: SystemType) -> float:
        """Score power availability (0-5 points)."""
        spec = self.SYSTEM_SPECS[system]
        power_required = spec["power_required"]
        power_available = self.profile.get("power_available", True)
        
        if not power_required:
            return 5.0  # Passive system — always optimal
        elif power_available:
            return 5.0  # Power available and required
        else:
            return 0.0  # Power required but unavailable — disqualifying
    
    def score_system(self, system: SystemType) -> Dict:
        """Calculate complete score for a system type."""
        scores = {
            "budget_fit": self.score_budget_fit(system),
            "experience_fit": self.score_experience_fit(system),
            "maintenance_fit": self.score_maintenance_fit(system),
            "crop_compatibility": self.score_crop_compatibility(system),
            "space_efficiency": self.score_space_efficiency(system),
            "power_availability": self.score_power_availability(system)
        }
        
        # Calculate weighted total
        weighted_total = sum(
            scores[dim] * weight 
            for dim, weight in self.SCORING_WEIGHTS.items()
        )
        
        return {
            "system_type": system.value,
            "name": self.SYSTEM_SPECS[system]["name"],
            "scores": scores,
            "weighted_total": round(weighted_total, 2),
            "normalized_score": round(weighted_total / 5.0 * 100, 1)  # Convert to 0-100 scale
        }
    
    def select_optimal_system(self) -> Tuple[Dict, List[Dict]]:
        """
        Select and score all systems, return optimal and alternatives.
        
        Returns:
            (optimal_system, [alternative_systems])
        """
        # Score all systems
        all_scores = [self.score_system(sys) for sys in SystemType]
        
        # Sort by normalized score descending
        all_scores.sort(key=lambda x: x["normalized_score"], reverse=True)
        
        # Check if user has preferred system
        preferred = self.profile.get("preferred_system")
        if preferred:
            preferred_system = next((s for s in all_scores if s["system_type"] == preferred), None)
            if preferred_system:
                top_score = all_scores[0]["normalized_score"]
                preferred_score = preferred_system["normalized_score"]
                
                # If preferred is within 80% of top, honor it
                if preferred_score >= top_score * 0.8:
                    # Reorder with preferred first
                    all_scores.remove(preferred_system)
                    all_scores.insert(0, preferred_system)
                else:
                    # Flag the preference gap
                    preferred_system["preference_gap"] = top_score - preferred_score
        
        return all_scores[0], all_scores[1:]
```

### Step 4: Design system layout

Based on selected system type and `space_m2`:

**Layout design rules:**
- Leave 40% of floor area as walkway/access (unless wall-mounted NFT panels used)
- Calculate number of growing sites:
  - DWC: 1 site per ~0.03 m² (3.5" net pot spacing)
  - NFT: 1 site per 0.02 m² (2.5" hole spacing, 20cm channel pitch)
  - Kratky: 1 site per 0.04 m² (standard 5L tub / 6 plant sites)
  - Aeroponics tower: 1 site per 0.007 m² horizontal footprint (tower systems)
- Calculate reservoir size: 2L per plant site (Kratky passive), 5L per 4 sites (DWC), 10L sump (NFT)
- Produce ASCII/text layout diagram showing:
  - Growing zone vs. walkway
  - Reservoir placement
  - Light fixture positions
  - Electrical outlet proximity

**Example layout output (text-based):**
```
BALCONY LAYOUT (3m × 1.5m = 4.5 m², South-facing)
[Wall] [===NFT Channel 1=== ][===NFT Channel 2===] [Wall]
        12 sites                12 sites
[===NFT Channel 3=== ][===NFT Channel 4===]
        12 sites                12 sites
[Reservoir 40L] [Pump] [Walkway 0.6m] [Power strip]
TOTAL: 48 plants | Growing area: 2.7 m² | Walkway: 1.8 m²
```

### Step 5: Build nutrient schedule

For each target crop, build a stage-by-stage nutrient schedule using EC/pH standards from SECOND-KNOWLEDGE-BRAIN.md Section 1.3:

| Week | Stage | EC Target (mS/cm) | pH Target | Notes |
|------|-------|-------------------|-----------|-------|
| 1–2 | Seedling | [crop-specific min] | [crop-specific] | Start low; dilute solution |
| 3–4 | Early Vegetative | [mid range] | [range] | Increase N fraction |
| 5–6 | Vegetative | [optimal] | [range] | Full strength |
| 7+ | Harvest/Fruiting | [upper range] | [range] | Increase K for fruiting crops |

- For multiple crops in same system: use the intersection of their EC/pH ranges (most restrictive crop drives the schedule)
- If no safe intersection exists: recommend separate systems or phased growing
- Recommend nutrient brand or DIY two-part solution formula (reference Hoagland solution)
- Note solution change frequency: DWC/Kratky: top-up as needed, full change every 2–3 weeks; NFT: top-up daily, full reservoir change weekly

### Step 6: Calculate water budget

```
Water_evapotranspiration_L_per_week = crop_count × avg_transpiration_L_per_plant_per_day × 7
avg_transpiration: lettuce: 0.05–0.15 L/day; tomato: 0.3–0.5 L/day; basil: 0.08–0.12 L/day

Water_system_losses_L_per_week = evaporation from reservoir × 7 × 0.03 (3% daily evap rate)

Total_water_budget_L_per_week = Water_ET + Water_system_losses
Monthly water cost = Total_water_budget × 4 × local_water_rate_per_L (if known)
```

Note: Hydroponics water use is 90–95% less than soil growing per kg of yield. State this comparison explicitly for user context.

**Complete Water Budget Implementation:**

```python
from typing import Dict, List

class WaterBudgetCalculator:
    """
    Calculate water consumption and costs for hydroponic systems.
    References: WEF Nexus, Hoff 2011; Martin & van Klink 2021
    """
    
    # Crop-specific transpiration rates (L/day per plant)
    TRANSPIRATION_RATES = {
        "lettuce": 0.10,      # Range: 0.05–0.15
        "spinach": 0.08,
        "kale": 0.12,
        "arugula": 0.07,
        "basil": 0.10,        # Range: 0.08–0.12
        "mint": 0.12,
        "cilantro": 0.09,
        "tomato": 0.40,       # Range: 0.3–0.5
        "cherry_tomato": 0.35,
        "cucumber": 0.45,
        "chili_pepper": 0.38,
        "strawberry": 0.25,
    }
    
    # System-specific water loss factors
    SYSTEM_LOSS_FACTORS = {
        "kratky": 0.02,    # 2% daily evaporation (closed surface)
        "dwc": 0.03,       # 3% daily evaporation (aerated surface)
        "nft": 0.04,       # 4% daily evaporation (running film)
        "aeroponics": 0.05 # 5% losses (mist overspray + evaporation)
    }
    
    # Typical water costs by region (USD per 1000L)
    WATER_COSTS = {
        "north_america": 0.005,     # $5/1000L
        "europe": 0.004,
        "asia_developed": 0.003,
        "asia_developing": 0.002,
        "default": 0.004
    }
    
    def __init__(self, system_type: str, site_count: int, crop_list: List[Dict], 
                 reservoir_size_liters: float, region: str = "default"):
        """
        Initialize water budget calculator.
        
        Args:
            system_type: One of: kratky, dwc, nft, aeroponics
            site_count: Number of plant sites
            crop_list: List of crop dicts with "name" and "cycle_days"
            reservoir_size_liters: Total reservoir capacity
            region: Geographic region for water cost estimation
        """
        self.system_type = system_type.lower()
        self.site_count = site_count
        self.crop_list = crop_list
        self.reservoir_size = reservoir_size_liters
        self.loss_factor = self.SYSTEM_LOSS_FACTORS.get(system_type.lower(), 0.03)
        self.water_cost_per_1000L = self.WATER_COSTS.get(region, 0.004)
    
    def calculate_weekly_budget(self) -> Dict:
        """Calculate weekly water consumption and cost."""
        
        # Calculate total transpiration
        total_transpiration_l_day = 0.0
        for crop in self.crop_list:
            crop_name = crop.get("name", "").lower()
            transpiration = self.TRANSPIRATION_RATES.get(crop_name, 0.10)
            
            # Estimate fraction of sites dedicated to this crop
            # (Assume equal distribution if not specified)
            crop_sites = self.site_count / len(self.crop_list)
            total_transpiration_l_day += transpiration * crop_sites
        
        transpiration_l_week = total_transpiration_l_day * 7
        
        # Calculate system losses
        reservoir_evaporation_l_day = self.reservoir_size * self.loss_factor
        system_losses_l_week = reservoir_evaporation_l_day * 7
        
        # Total water budget
        total_l_week = transpiration_l_week + system_losses_l_week
        
        # Calculate cost
        cost_per_week = (total_l_week / 1000) * self.water_cost_per_1000L
        cost_per_month = cost_per_week * 4
        
        return {
            "transpiration_l_week": round(transpiration_l_week, 2),
            "system_losses_l_week": round(system_losses_l_week, 2),
            "total_l_week": round(total_l_week, 2),
            "total_l_month": round(total_l_week * 4, 1),
            "cost_usd_per_week": round(cost_per_week, 3),
            "cost_usd_per_month": round(cost_per_month, 2),
            "water_efficiency_l_per_kg_estimate": self._estimate_efficiency()
        }
    
    def _estimate_efficiency(self) -> float:
        """
        Estimate water use efficiency (L/kg yield).
        Typical hydroponics: 0.5–2.0 L/kg vs. 40–200 L/kg in field agriculture.
        """
        # Estimate yield based on system type and crops
        base_efficiency = {
            "kratky": 1.2,    # L/kg
            "dwc": 1.0,
            "nft": 0.8,
            "aeroponics": 0.6
        }.get(self.system_type, 1.0)
        
        return round(base_efficiency, 2)
```

### Step 7: Calculate energy budget

For active systems (DWC, NFT, Aeroponics):
```
Pump_energy_kWh_per_week = pump_wattage × hours_per_day × 7 / 1000
  NFT: 20–40W pump running 24/7 = 3.4–6.7 kWh/week
  DWC: 5–15W air pump running 24/7 = 0.84–2.52 kWh/week
  Aeroponics: 200–400W high-pressure pump, 5min on/30min off = 1.1–2.2 kWh/week

LED_energy_kWh_per_week = LED_wattage × photoperiod_hours × 7 / 1000

Total_energy_kWh_per_week = Pump_energy + LED_energy
Monthly energy cost = Total_energy × 4 × electricity_cost_per_kwh
```

**Complete Energy Budget Implementation:**

```python
from typing import Dict, Optional

class EnergyBudgetCalculator:
    """
    Calculate energy consumption and costs for hydroponic systems.
    References: Graamans et al. 2018, Biosystems Engineering
    """
    
    # System-specific pump requirements
    PUMP_SPECS = {
        "kratky": {
            "pump_wattage": 0,
            "hours_per_day": 0,
            "description": "Passive system — no pump required"
        },
        "dwc": {
            "pump_wattage": 10,      # Air pump (5–15W typical)
            "hours_per_day": 24,
            "description": "Air pump for oxygenation"
        },
        "nft": {
            "pump_wattage": 30,      # Water pump (20–40W typical)
            "hours_per_day": 24,
            "description": "Water pump for nutrient circulation"
        },
        "aeroponics": {
            "pump_wattage": 300,     # High-pressure pump (200–400W)
            "hours_per_day": 2.4,    # 5min on / 30min off = 8 cycles/day × 5min = 40min
            "description": "High-pressure misting pump (duty cycle)"
        }
    }
    
    # LED efficacy by quality tier (μmol/J)
    LED_EFFICACY = {
        "standard": 2.0,
        "quality": 2.5,
        "premium": 3.2
    }
    
    # Typical electricity costs by region (USD/kWh)
    ELECTRICITY_COSTS = {
        "north_america": 0.15,
        "europe": 0.25,
        "asia_developed": 0.20,
        "asia_developing": 0.10,
        "default": 0.15
    }
    
    def __init__(
        self,
        system_type: str,
        led_wattage: float,
        photoperiod_hours: float,
        region: str = "default",
        electricity_cost_usd_kwh: Optional[float] = None,
        led_quality: str = "quality"
    ):
        """
        Initialize energy budget calculator.
        
        Args:
            system_type: One of: kratky, dwc, nft, aeroponics
            led_wattage: Total LED wattage (if supplemental lighting used)
            photoperiod_hours: Hours per day LEDs run (if used)
            region: Geographic region for electricity cost estimation
            electricity_cost_usd_kwh: Override regional cost if known
            led_quality: LED quality tier for efficacy calculation
        """
        self.system_type = system_type.lower()
        self.led_wattage = led_wattage
        self.photoperiod_hours = photoperiod_hours
        self.pump_specs = self.PUMP_SPECS.get(system_type.lower(), self.PUMP_SPECS["dwc"])
        
        if electricity_cost_usd_kwh is not None:
            self.electricity_cost = electricity_cost_usd_kwh
        else:
            self.electricity_cost = self.ELECTRICITY_COSTS.get(region, 0.15)
        
        self.led_efficacy = self.LED_EFFICACY.get(led_quality, 2.5)
    
    def calculate_weekly_budget(self) -> Dict:
        """Calculate weekly energy consumption and cost."""
        
        # Pump energy
        pump_watts = self.pump_specs["pump_wattage"]
        pump_hours = self.pump_specs["hours_per_day"]
        pump_kwh_week = (pump_watts * pump_hours * 7) / 1000
        
        # LED energy (if applicable)
        led_kwh_week = 0.0
        if self.led_wattage > 0 and self.photoperiod_hours > 0:
            led_kwh_week = (self.led_wattage * self.photoperiod_hours * 7) / 1000
        
        # Total energy
        total_kwh_week = pump_kwh_week + led_kwh_week
        
        # Calculate costs
        cost_week = total_kwh_week * self.electricity_cost
        cost_month = cost_week * 4
        
        return {
            "pump_wattage": pump_watts,
            "pump_hours_per_day": pump_hours,
            "pump_kwh_per_week": round(pump_kwh_week, 2),
            "led_wattage": self.led_wattage,
            "led_photoperiod_hours": self.photoperiod_hours,
            "led_kwh_per_week": round(led_kwh_week, 2),
            "total_kwh_per_week": round(total_kwh_week, 2),
            "total_kwh_per_month": round(total_kwh_week * 4, 1),
            "cost_usd_per_week": round(cost_week, 2),
            "cost_usd_per_month": round(cost_month, 2),
            "energy_per_kg_yield_estimate": self._estimate_energy_per_kg()
        }
    
    def _estimate_energy_per_kg(self) -> float:
        """
        Estimate energy use per kg yield (kWh/kg).
        Reference: 1.5–4.0 kWh/kg lettuce for LED + DWC systems.
        """
        # Base energy per kg varies by system type
        base_energy = {
            "kratky": 0.0,    # Passive (may still have LED)
            "dwc": 2.0,       # kWh/kg
            "nft": 2.5,
            "aeroponics": 3.5
        }.get(self.system_type, 2.0)
        
        # Add LED contribution if significant
        if self.led_wattage > 0:
            led_contribution = (self.led_wattage * self.photoperiod_hours * 365) / 1000 / 50  # Assume 50kg/m²/year
            base_energy += led_contribution
        
        return round(base_energy, 2)
```

### Step 8: Estimate yield

```
Yield_g_per_week = site_count × avg_yield_per_plant_g / cycle_days × 7

Reference yield benchmarks (from SECOND-KNOWLEDGE-BRAIN.md Section 1.4):
- Lettuce (DWC): 150–200g per plant over 28–35 days → 30–50g/plant/week
- Basil (DWC): 100–150g per plant over 28 days → 25–37g/plant/week
- Cherry tomato (NFT): 300–500g per plant over 70 days → 30–50g/plant/week

Annual yield extrapolation = weekly_yield × 52 (assuming continuous production)
```

### Step 9: Compile Design Specification

Assemble all computed values into the Design Specification document with these sections:
1. System Selection Rationale (chosen system + scores of top 3 alternatives)
2. Layout Diagram (ASCII/text)
3. DLI Analysis (monthly table + supplemental LED plan if needed)
4. VPD Analysis (monthly table + management recommendations)
5. Nutrient Schedule (weekly table per crop)
6. Water Budget (L/week + monthly cost)
7. Energy Budget (kWh/week + monthly cost)
8. Yield Estimate (g/week per crop + annual projection)
9. Equipment List (with unit costs and total investment)

---

## Outputs

Design Specification document containing:

```json
{
  "system_type": "NFT|DWC|Kratky|Aeroponics",
  "system_selection_rationale": "...",
  "system_scores": {"NFT": 23, "DWC": 19, "Kratky": 15, "Aeroponics": 8},
  "layout": {
    "growing_area_m2": 2.7,
    "walkway_area_m2": 1.8,
    "total_plant_sites": 48,
    "layout_diagram": "...",
    "reservoir_size_L": 40
  },
  "dli_analysis": {
    "monthly_natural_dli": [14, 15, 16, ...],
    "monthly_effective_dli": [11.2, 12.0, 12.8, ...],
    "supplemental_led_required": true,
    "supplemental_wattage_per_m2": 35,
    "led_photoperiod_hours": 4
  },
  "vpd_analysis": {
    "monthly_vpd": [1.2, 1.3, 1.4, ...],
    "worst_month": "April",
    "worst_vpd": 1.8,
    "recommendations": ["Increase misting April–May", "Ensure air circulation"]
  },
  "nutrient_schedule": [...],
  "water_budget": {
    "L_per_week": 12.5,
    "monthly_cost_usd": 0.50
  },
  "energy_budget": {
    "kWh_per_week": 3.2,
    "monthly_cost_usd": 8.20
  },
  "yield_estimate": {
    "total_g_per_week": 1440,
    "annual_kg": 74.9,
    "by_crop": {"lettuce": "960g/week", "basil": "480g/week"}
  },
  "equipment_list": [
    {"item": "NFT channels (1m × 6)", "qty": 4, "unit_cost_usd": 15, "total_usd": 60},
    {"item": "Submersible pump 20W", "qty": 1, "unit_cost_usd": 18, "total_usd": 18},
    ...
  ],
  "total_equipment_cost_usd": 145
}
```

---

## Quality Gate

Design Specification passes to sub-scoring-engine ONLY when ALL of the following are true:

- [ ] DLI target is either met by natural light OR a supplemental LED plan is specified with wattage, photoperiod, and estimated energy cost
- [ ] VPD is calculated for at least the hottest and coolest months; management recommendations provided if VPD is outside 0.4–1.5 kPa range
- [ ] System type is selected with a scored justification against at least 2 alternatives
- [ ] Nutrient schedule covers all target crops across all growth stages (seedling / vegetative / fruiting or harvest)
- [ ] EC and pH targets fall within the crop-specific ranges from SECOND-KNOWLEDGE-BRAIN.md Section 1.3
- [ ] Water budget (L/week) is calculated with formula shown
- [ ] Energy budget (kWh/week) is calculated; zero for Kratky passive systems is acceptable
- [ ] Yield estimate is calculated and benchmarked against published reference values
- [ ] Equipment list is present with unit costs and total investment
- [ ] Total equipment cost does not exceed user's `budget_usd` by more than 15%; if it does, an alternative lower-cost system path is provided
