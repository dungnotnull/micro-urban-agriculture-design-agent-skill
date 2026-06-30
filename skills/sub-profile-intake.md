---
name: sub-profile-intake
description: Gather user's space dimensions, location/climate, target crops, budget, and experience level to build a structured profile for urban farm system design.
---

## Purpose

Collect all structured inputs required to design a micro urban agriculture system. The output is a validated Profile JSON that drives all downstream sub-skills (sub-system-designer, sub-scoring-engine, sub-improvement-roadmap). This sub-skill transforms a user's natural-language description of their space and goals into a precise, quantified profile with climate data attached.

---

## Inputs

- User's natural-language description (conversational)
- Access to WebSearch (for climate/weather lookup)
- Access to SECOND-KNOWLEDGE-BRAIN.md (fallback for climate data)

---

## Workflow

### Step 1: Greet and frame the intake

Introduce the intake process clearly:
> "To design your ideal micro urban farm, I need to gather some details about your space, location, and goals. I'll ask you a series of short questions — most have simple answers. Let's start."

### Step 2: Collect space data

Ask (in one block to reduce back-and-forth):
1. **Space type:** Balcony / Rooftop / Terrace / Indoor room?
2. **Floor dimensions:** Length × width in meters (or square footage — convert to m²)
3. **Orientation:** Which compass direction does the primary open face look? (North / South / East / West / Southeast / etc.)
4. **Shade obstructions:** Are there walls, overhangs, neighboring buildings, or water tanks that cast shadow? If yes, describe approximate shadow coverage (e.g., "25% of space is shaded from 11am–2pm by adjacent wall")
5. **Floor type:** Concrete slab / wooden deck / tiled / other? (Structural context)
6. **Weight limit knowledge:** Do you know your balcony/rooftop's rated load capacity (kg/m²)? (Optional — if unknown, default to conservative 200 kg/m² assumption)

**Validation Rules:**
- `space_type`: Must be one of: balcony, rooftop, terrace, indoor
- `space_m2`: Numeric, must be > 0.5 m² and < 500 m² (reasonable bounds)
- `orientation`: Must be one of: north, south, east, west, northeast, northwest, southeast, southwest
- `floor_type`: Must be one of: concrete, wood, tile, metal, other
- `load_capacity_kg_m2`: Numeric, default 200 if unknown, range 50–1000 kg/m²

### Step 3: Collect location data

Ask:
1. **City or region name** (used for lat/lon lookup)
2. **Country** (for building code context)

Then:
- WebSearch: `"{city} latitude longitude"` → extract lat/lon
- WebSearch: `"{city} average monthly solar irradiance kWh/m2"` OR use NASA POWER API fallback
- WebSearch: `"{city} average monthly temperature humidity"` → extract monthly averages

If WebSearch unavailable:
- Use SECOND-KNOWLEDGE-BRAIN.md Section 1.1 latitude band table for approximate DLI estimate
- Flag: "Climate data from internal knowledge base — may vary from local micro-climate"

Record: `city`, `country`, `latitude`, `longitude`, `climate_zone` (tropical / subtropical / temperate / continental / arid), `avg_monthly_solar_irradiance[12]`, `avg_monthly_temp[12]`, `avg_monthly_humidity[12]`

**Climate Zone Classification Procedure:**

```python
# Climate zone determination based on latitude and temperature patterns
def classify_climate_zone(latitude: float, avg_temp_annual: float, avg_temp_coldest: float, avg_temp_hottest: float) -> str:
    """
    Classify climate zone based on Köppen-Geiger climate classification simplified.
    
    Returns: one of: tropical, subtropical, temperate, continental, arid
    """
    # Tropical: Within 23.5° of equator AND avg annual temp > 18°C
    if abs(latitude) <= 23.5 and avg_temp_annual > 18:
        return "tropical"
    
    # Subtropical: 23.5°–35° AND coldest month > 10°C
    if 23.5 < abs(latitude) <= 35 and avg_temp_coldest > 10:
        return "subtropical"
    
    # Temperate: 35°–50° OR distinct seasons with coldest > 0°C
    if 35 < abs(latitude) <= 50 or (avg_temp_coldest > 0 and avg_temp_hottest < 30):
        return "temperate"
    
    # Continental: 50°–70° OR large seasonal temperature variation (>25°C)
    if abs(latitude) > 50 or (avg_temp_hottest - avg_temp_coldest > 25):
        return "continental"
    
    # Arid: Low precipitation indicator (if humidity data < 40% annual average)
    # This is a simplified check; real arid classification needs precipitation data
    return "temperate"  # Default fallback

# Solar irradiance lookup by latitude band (kWh/m²/day, clear sky annual average)
SOLAR_IRRADIANCE_BY_LATITUDE = {
    "0-10": 5.5,      # Equatorial
    "10-20": 5.0,     # Tropical
    "20-30": 4.5,     # Subtropical
    "30-40": 4.0,     # Warm temperate
    "40-50": 3.5,     # Cool temperate
    "50-60": 3.0,     # Boreal
}

def get_baseline_solar_irradiance(latitude: float) -> float:
    """Get baseline solar irradiance for latitude (kWh/m²/day)."""
    abs_lat = abs(latitude)
    for band, value in SOLAR_IRRADIANCE_BY_LATITUDE.items():
        low, high = map(int, band.split("-"))
        if low <= abs_lat <= high:
            return value
    return 2.5  # Polar fallback
```

**Monthly Climate Data Estimation (when API unavailable):**

For locations without real-time weather data access, use these monthly patterns based on climate zone:

```python
# Monthly solar irradiance patterns (multiplier of annual average)
MONTHLY_SOLAR_MULTIPLIERS = {
    "tropical": [0.95, 0.97, 1.00, 1.02, 1.05, 1.07, 1.06, 1.04, 1.01, 0.99, 0.96, 0.94],
    "subtropical": [0.85, 0.90, 0.95, 1.05, 1.15, 1.20, 1.18, 1.10, 1.00, 0.92, 0.85, 0.82],
    "temperate": [0.60, 0.75, 0.95, 1.15, 1.30, 1.40, 1.35, 1.20, 0.95, 0.75, 0.55, 0.45],
    "continental": [0.45, 0.65, 0.90, 1.20, 1.45, 1.55, 1.50, 1.25, 0.90, 0.60, 0.40, 0.35],
}

def estimate_monthly_irradiance(climate_zone: str, annual_avg: float) -> list[float]:
    """Generate 12-month solar irradiance estimate from annual average."""
    multipliers = MONTHLY_SOLAR_MULTIPLIERS.get(climate_zone, MONTHLY_SOLAR_MULTIPLIERS["temperate"])
    return [round(annual_avg * m, 2) for m in multipliers]
```

### Step 4: Collect target crop list

Ask:
1. **Which crops do you want to grow?** (List all you have in mind — e.g., lettuce, basil, cherry tomatoes, strawberries)
2. **Primary goal:** Maximum yield? Variety? Specific crop for household consumption?
3. **Harvest frequency preference:** Continuous harvest (cut-and-come-again) vs. batch harvest?

For each crop named, look up in SECOND-KNOWLEDGE-BRAIN.md Section 1.1 (DLI requirements table):
- Record: crop name, DLI minimum, DLI optimal, EC range, pH range, crop cycle (days)
- Flag any crop whose DLI optimal exceeds local DLI estimate by >5 mol/m²/day as "requires supplemental lighting"

**Crop Taxonomy and Compatibility Rules:**

```python
# Crop categories for system compatibility
CROP_TAXONOMY = {
    "leafy_greens": {
        "crops": ["lettuce", "spinach", "kale", "arugula", "swiss_chard", "pak_choi", "bok_choy", "watercress"],
        "dli_range": (6, 17),  # mol/m²/day
        "ec_range": (0.8, 2.4),  # mS/cm
        "ph_range": (6.0, 6.5),
        "temp_optimal": (15, 22),  # °C
        "cycle_days": (21, 35),
        "compatible_systems": ["kratky", "dwc", "nft", "aeroponics"],
        "compatibility_score": {"leafy_greens": 1.0, "herbs": 0.9, "fruiting": 0.6, "root": 0.3}
    },
    "herbs": {
        "crops": ["basil", "mint", "cilantro", "parsley", "chive", "oregano", "thyme"],
        "dli_range": (8, 24),
        "ec_range": (0.8, 2.4),
        "ph_range": (5.8, 6.5),
        "temp_optimal": (18, 26),
        "cycle_days": (21, 42),
        "compatible_systems": ["kratky", "dwc", "nft", "aeroponics"],
        "compatibility_score": {"leafy_greens": 0.9, "herbs": 0.85, "fruiting": 0.5, "root": 0.2}
    },
    "fruiting": {
        "crops": ["tomato", "cherry_tomato", "cucumber", "chili_pepper", "pepper", "eggplant"],
        "dli_range": (18, 30),
        "ec_range": (2.0, 3.5),
        "ph_range": (5.8, 6.3),
        "temp_optimal": (22, 30),
        "cycle_days": (60, 90),
        "compatible_systems": ["nft", "aeroponics"],
        "compatibility_score": {"leafy_greens": 0.6, "herbs": 0.5, "fruiting": 0.9, "root": 0.4}
    },
    "root_vegetables": {
        "crops": ["carrot", "radish", "beet", "turnip"],
        "dli_range": (12, 20),
        "ec_range": (1.6, 2.8),
        "ph_range": (6.0, 6.8),
        "temp_optimal": (15, 22),
        "cycle_days": (35, 60),
        "compatible_systems": ["dwc", "aeroponics"],
        "compatibility_score": {"leafy_greens": 0.3, "herbs": 0.2, "fruiting": 0.4, "root": 0.95}
    }
}

def check_crop_compatibility(crop_list: list[str]) -> dict:
    """
    Check if crops in the list are compatible for shared-system cultivation.
    
    Returns:
        {
            "compatible": bool,
            "warnings": list[str],
            "recommendations": list[str],
            "ec_intersection": tuple or None,
            "ph_intersection": tuple or None
        }
    """
    result = {"compatible": True, "warnings": [], "recommendations": [], "ec_intersection": None, "ph_intersection": None}
    
    categories = set()
    crop_params = []
    
    for crop in crop_list:
        # Determine category
        for cat_name, cat_data in CROP_TAXONOMY.items():
            if crop.lower() in [c.lower() for c in cat_data["crops"]]:
                categories.add(cat_name)
                crop_params.append(cat_data)
                break
    
    # Check cross-compatibility
    if len(categories) > 1:
        for i, cat1 in enumerate(crop_params):
            for cat2 in crop_params[i+1:]:
                cat1_name = list(CROP_TAXONOMY.keys())[list(CROP_TAXONOMY.values()).index(cat1)]
                cat2_name = list(CROP_TAXONOMY.keys())[list(CROP_TAXONOMY.values()).index(cat2)]
                
                # Find compatibility key (handle different orderings)
                key1 = cat1_name.replace("_", " ")
                key2 = cat2_name.replace("_", " ")
                
                # Check for significant compatibility issues
                if cat1["dli_range"][1] < cat2["dli_range"][0] or cat2["dli_range"][1] < cat1["dli_range"][0]:
                    result["warnings"].append(
                        f"Significant DLI mismatch: {cat1_name} ({cat1['dli_range']}) vs {cat2_name} ({cat2['dli_range']}). "
                        "Consider seasonal separation or LED zoning."
                    )
                    result["compatible"] = False
                
                # Check EC intersection
                ec_intersect = (
                    max(cat1["ec_range"][0], cat2["ec_range"][0]),
                    min(cat1["ec_range"][1], cat2["ec_range"][1])
                )
                if ec_intersect[0] > ec_intersect[1]:  # No intersection
                    result["warnings"].append(
                        f"No safe EC overlap: {cat1_name} EC {cat1['ec_range']} vs {cat2_name} EC {cat2['ec_range']}. "
                        "Separate systems or crop rotation recommended."
                    )
                    result["compatible"] = False
                else:
                    if result["ec_intersection"] is None:
                        result["ec_intersection"] = ec_intersect
                    else:
                        # Use most restrictive intersection
                        result["ec_intersection"] = (
                            max(result["ec_intersection"][0], ec_intersect[0]),
                            min(result["ec_intersection"][1], ec_intersect[1])
                        )
    
    if result["compatible"]:
        result["recommendations"].append("All crops are compatible for shared-system cultivation.")
    else:
        result["recommendations"].append("Consider: (A) separate systems, (B) seasonal rotation, or (C) compromise with reduced yield.")
    
    return result
```

**Extended Crop Database (beyond SECOND-KNOWLEDGE-BRAIN.md Section 1.1):**

```python
CROP_DATABASE = {
    # Leafy Greens
    "lettuce": {"dli_min": 6, "dli_optimal": 14, "ec_min": 0.8, "ec_max": 2.4, "ph_min": 6.0, "ph_max": 6.5, "cycle_days": 30, "category": "leafy_greens"},
    "spinach": {"dli_min": 8, "dli_optimal": 16, "ec_min": 1.0, "ec_max": 2.2, "ph_min": 6.2, "ph_max": 6.8, "cycle_days": 35, "category": "leafy_greens"},
    "kale": {"dli_min": 10, "dli_optimal": 18, "ec_min": 1.6, "ec_max": 2.4, "ph_min": 6.0, "ph_max": 6.5, "cycle_days": 42, "category": "leafy_greens"},
    "arugula": {"dli_min": 6, "dli_optimal": 12, "ec_min": 0.8, "ec_max": 2.0, "ph_min": 6.0, "ph_max": 6.5, "cycle_days": 21, "category": "leafy_greens"},
    "swiss_chard": {"dli_min": 8, "dli_optimal": 16, "ec_min": 1.0, "ec_max": 2.2, "ph_min": 6.0, "ph_max": 6.5, "cycle_days": 35, "category": "leafy_greens"},
    "pak_choi": {"dli_min": 8, "dli_optimal": 14, "ec_min": 1.0, "ec_max": 2.0, "ph_min": 6.2, "ph_max": 6.5, "cycle_days": 28, "category": "leafy_greens"},
    "watercress": {"dli_min": 6, "dli_optimal": 10, "ec_min": 0.8, "ec_max": 1.8, "ph_min": 6.5, "ph_max": 7.0, "cycle_days": 21, "category": "leafy_greens"},
    
    # Herbs
    "basil": {"dli_min": 12, "dli_optimal": 20, "ec_min": 1.0, "ec_max": 2.4, "ph_min": 5.8, "ph_max": 6.4, "cycle_days": 28, "category": "herbs"},
    "mint": {"dli_min": 8, "dli_optimal": 14, "ec_min": 0.8, "ec_max": 2.0, "ph_min": 6.5, "ph_max": 7.0, "cycle_days": 28, "category": "herbs"},
    "cilantro": {"dli_min": 8, "dli_optimal": 14, "ec_min": 0.8, "ec_max": 2.0, "ph_min": 6.2, "ph_max": 6.5, "cycle_days": 28, "category": "herbs"},
    "parsley": {"dli_min": 8, "dli_optimal": 14, "ec_min": 1.0, "ec_max": 2.2, "ph_min": 6.0, "ph_max": 6.5, "cycle_days": 42, "category": "herbs"},
    "chive": {"dli_min": 6, "dli_optimal": 12, "ec_min": 0.8, "ec_max": 1.8, "ph_min": 6.0, "ph_max": 6.5, "cycle_days": 30, "category": "herbs"},
    
    # Fruiting
    "tomato": {"dli_min": 20, "dli_optimal": 28, "ec_min": 2.0, "ec_max": 3.5, "ph_min": 5.8, "ph_max": 6.3, "cycle_days": 85, "category": "fruiting"},
    "cherry_tomato": {"dli_min": 20, "dli_optimal": 28, "ec_min": 2.0, "ec_max": 3.5, "ph_min": 5.8, "ph_max": 6.3, "cycle_days": 70, "category": "fruiting"},
    "cucumber": {"dli_min": 20, "dli_optimal": 28, "ec_min": 2.0, "ec_max": 3.0, "ph_min": 5.8, "ph_max": 6.2, "cycle_days": 60, "category": "fruiting"},
    "chili_pepper": {"dli_min": 18, "dli_optimal": 25, "ec_min": 1.8, "ec_max": 3.0, "ph_min": 5.8, "ph_max": 6.3, "cycle_days": 75, "category": "fruiting"},
    "strawberry": {"dli_min": 12, "dli_optimal": 18, "ec_min": 1.0, "ec_max": 2.4, "ph_min": 5.5, "ph_max": 6.0, "cycle_days": 90, "category": "fruiting"},
    
    # Root Vegetables
    "carrot": {"dli_min": 12, "dli_optimal": 18, "ec_min": 1.6, "ec_max": 2.5, "ph_min": 6.0, "ph_max": 6.8, "cycle_days": 70, "category": "root_vegetables"},
    "radish": {"dli_min": 12, "dli_optimal": 18, "ec_min": 1.6, "ec_max": 2.4, "ph_min": 6.0, "ph_max": 6.5, "cycle_days": 28, "category": "root_vegetables"},
}
```

### Step 5: Collect budget and experience

Ask:
1. **Total budget (USD):** How much can you invest in equipment? (If zero, flag as Kratky/passive path)
   - Budget bands: Zero (<$20) / Starter ($20–100) / Moderate ($100–500) / Full ($500–2000) / Commercial (>$2000)
2. **Experience level:**
   - Beginner: Never grown hydroponically before
   - Intermediate: 1–2 successful hydroponic cycles
   - Advanced: Running an active system, comfortable with EC/pH adjustment
3. **Time availability for maintenance:** Hours per week available (used to filter system complexity)
4. **System preference (optional):** Any preference for Kratky / NFT / DWC / Aeroponics? (Default: skill recommends based on profile)

### Step 6: Collect utility data (optional but valuable)

Ask:
1. **Water source:** Municipal tap / well / rainwater harvesting?
2. **Known water TDS or EC (if measured):** Enter value in ppm or mS/cm (if unknown, default: assume 0.3–0.5 mS/cm for municipal water)
3. **Electricity access:** Is there a power outlet within 5 meters? (Required for active systems and lighting)
4. **Local electricity cost:** Cost per kWh in local currency (optional — for energy budget calculation)

### Step 7: Validate and confirm profile

Summarize collected data in a structured format and ask user to confirm or correct:

```
PROFILE SUMMARY
---------------
Space: [type], [dimensions] m², [orientation], [shade description]
Location: [city, country] — Lat [X]°, Lon [Y]°
Climate Zone: [type]
Est. Peak DLI (natural, summer): [X] mol/m²/day
Target Crops: [crop1 (DLI: X, EC: Y-Z), crop2 ...]
Budget: [band] (~$X)
Experience: [level]
Maintenance: [X h/week available]
Water: [source] (TDS ~[X] ppm)
Power: [available / unavailable]

Do you want to confirm this profile, or adjust any detail?
```

### Step 8: Resolve crop-climate incompatibilities (pre-flag)

Before passing to sub-system-designer:
- Compare each crop's DLI minimum to estimated natural DLI at user's location + season
- If DLI gap > 5 mol/m²/day for any crop: flag "Supplemental LED required for [crop]"
- If any two crops have incompatible temperature ranges (e.g., lettuce <20°C + basil >18°C OK; but spinach <15°C + tomato >18°C = incompatible in same system): flag for separate system recommendation
- If north-facing orientation at latitude >30°N in winter: flag "Low DLI warning — all crops may require supplemental lighting"

---

## Outputs

Structured Profile JSON passed to sub-system-designer:

```json
{
  "space_type": "balcony|rooftop|terrace|indoor",
  "space_m2": 4.5,
  "orientation": "south",
  "shade_description": "25% shaded by overhang 11am-2pm",
  "floor_type": "concrete",
  "load_capacity_kg_m2": 200,
  "city": "Ho Chi Minh City",
  "country": "Vietnam",
  "latitude": 10.8,
  "longitude": 106.7,
  "climate_zone": "tropical",
  "avg_monthly_solar_irradiance": [5.2, 5.5, 5.9, 5.6, 4.8, 4.2, 4.1, 4.3, 4.5, 4.7, 4.8, 5.0],
  "avg_monthly_temp_c": [27, 28, 29, 30, 30, 29, 28, 28, 27, 27, 27, 27],
  "avg_monthly_humidity_pct": [73, 70, 72, 78, 82, 85, 86, 85, 84, 83, 80, 75],
  "target_crops": [
    {"name": "lettuce", "dli_min": 6, "dli_optimal": 14, "ec_min": 0.8, "ec_max": 2.4, "ph_min": 6.0, "ph_max": 6.5, "cycle_days": 30},
    {"name": "basil", "dli_min": 12, "dli_optimal": 20, "ec_min": 1.0, "ec_max": 2.4, "ph_min": 5.8, "ph_max": 6.4, "cycle_days": 28}
  ],
  "budget_usd": 150,
  "budget_band": "moderate",
  "experience_level": "beginner",
  "maintenance_hours_per_week": 2,
  "preferred_system": null,
  "water_source": "municipal",
  "water_tds_ppm": 200,
  "power_available": true,
  "electricity_cost_per_kwh": 0.08,
  "dli_flags": ["basil requires supplemental LED in Dec-Feb"],
  "incompatibility_flags": []
}
```

---

## Quality Gate

The Profile JSON is valid and passes to sub-system-designer ONLY when ALL of the following are true:

- [ ] `space_m2` > 0 (numeric, positive)
- [ ] `orientation` is one of: north / south / east / west / northeast / northwest / southeast / southwest
- [ ] `latitude` and `longitude` are numeric (resolved from city name or user-provided)
- [ ] `target_crops` contains at least 1 crop with all fields: name, dli_min, dli_optimal, ec_min, ec_max, ph_min, ph_max
- [ ] `budget_usd` is numeric (0 is valid — routes to Kratky path)
- [ ] `experience_level` is one of: beginner / intermediate / advanced
- [ ] `power_available` is boolean (true/false)
- [ ] `dli_flags` and `incompatibility_flags` arrays are present (can be empty)
- [ ] If WebSearch was unavailable, `data_source` field = "internal_knowledge_base" with a limitation flag message included in output
