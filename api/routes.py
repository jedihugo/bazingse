
import sxtwl
from datetime import datetime, date, timedelta
from typing import Literal, Dict, List, Optional, Any
from fastapi import APIRouter, Query

# Import from library
from library import (
    HEAVENLY_STEMS,
    EARTHLY_BRANCHES,
    TEN_GODS,
    Gan,
    Zhi,
    GAN_MAP,
    ZHI_MAP,
    # Dong Gong Date Selection
    DONG_GONG_RATINGS,
    DONG_GONG_DAY_OFFICERS,
    DONG_GONG_MONTHS,
    DONG_GONG_BRANCH_TO_MONTH,
    get_dong_gong_officer,
    get_dong_gong_rating,
    get_dong_gong_day_info
)

# Import from chart_constructor
from chart_constructor import (
    generate_bazi_chart,
    generate_luck_pillars
)

# Import from bazingse
from bazingse import analyze_8_node_interactions

# * =================
# * API ENDPOINTS (endpoint.py)
# * =================

router = APIRouter()


def extract_hour_minute(birth_time: Optional[str]):
    """Extract hour and minute from birth_time string.
    Accepts both "HH:MM" format (e.g., "13:45") and old time slot format.
    Returns (None, None) if not provided or unknown.
    """
    if not birth_time or birth_time == "unknown":
        return None, None
    
    # Check if it's in HH:MM format
    if " - " not in birth_time and ":" in birth_time:
        parts = birth_time.split(":")
        hour = int(parts[0])
        minute = int(parts[1])
        return hour, minute
    
    # Old time slot format
    hour_range_start = birth_time.split(" - ")[0]
    hour = int(hour_range_start.split(":")[0])
    minute = int(hour_range_start.split(":")[1])
    return hour, minute


@router.get("/analyze_bazi")
async def analyze_bazi(
    birth_date: date = Query(..., description="Birth date in YYYY-MM-DD format"),
    birth_time: Optional[str] = Query(None, description="Birth time in HH:MM format (e.g., '13:45')"),
    gender: Literal["male", "female"] = Query(..., description="Gender"),
    analysis_year: Optional[int] = Query(None, description="Year to analyze (triggers 10-year luck pillar)"),
    include_annual_luck: bool = Query(True, description="Include annual luck in analysis (requires analysis_year)"),
    analysis_month: Optional[int] = Query(None, description="Month to analyze (1-12, requires analysis_year)"),
    analysis_day: Optional[int] = Query(None, description="Day to analyze (1-31, requires analysis_month)"),
    analysis_time: Optional[str] = Query(None, description="Time to analyze in HH:MM format (e.g., '14:30', requires analysis_day)"),
    talisman_year_hs: Optional[str] = Query(None, description="Talisman pillar 1 HS - any of 60 pillars (e.g., 'Jia', 'Yi', 'Bing')"),
    talisman_year_eb: Optional[str] = Query(None, description="Talisman pillar 1 EB - any of 60 pillars (e.g., 'Zi', 'Chou', 'Yin')"),
    talisman_month_hs: Optional[str] = Query(None, description="Talisman pillar 2 HS - any of 60 pillars"),
    talisman_month_eb: Optional[str] = Query(None, description="Talisman pillar 2 EB - any of 60 pillars"),
    talisman_day_hs: Optional[str] = Query(None, description="Talisman pillar 3 HS - any of 60 pillars"),
    talisman_day_eb: Optional[str] = Query(None, description="Talisman pillar 3 EB - any of 60 pillars"),
    talisman_hour_hs: Optional[str] = Query(None, description="Talisman pillar 4 HS - any of 60 pillars"),
    talisman_hour_eb: Optional[str] = Query(None, description="Talisman pillar 4 EB - any of 60 pillars"),
    location: Optional[Literal["overseas", "birthplace"]] = Query(None, description="Location status: 'overseas' (Water boost from Ren-Zi + Gui-Hai) or 'birthplace' (Earth boost from 4 Earth pillars at 50%)")
) -> dict:
    """
    Core BaZi analysis from first principles - analyzing natal chart with time periods.
    
    This is THE fundamental BaZi calculation: how one's natal destiny interacts with 
    life periods (past, present, or future). Not a "comparison" but the core analysis
    of destiny unfolding through time.
    
    Dynamic Pillar Generation:
    - Base: 4 natal pillars (year, month, day, hour) = 8 nodes - your natal destiny
    - +analysis_year: 10-year luck + annual pillar = +4 nodes - the time period
    - +analysis_month: Monthly pillar = +2 nodes - monthly influences
    - +analysis_day: Daily pillar = +2 nodes - daily influences  
    - +analysis_time: Hourly pillar = +2 nodes - hourly influences (HH:MM format)
    - Maximum: 9 pillars (4 natal + 1 luck + 4 time) = 18 nodes
    
    All WuXing interactions calculated between ALL nodes:
    - Combinations (transformations, harmonies)
    - Conflicts (clashes, harms, punishments)
    - Element flows (generation, control)
    
    Returns:
        - birth_info: Birth details (natal foundation)
        - analysis_info: Time period being analyzed
        - nodes: All HS and EB nodes with their qi states
        - base_element_score: Natal chart before interactions (raw qi)
        - natal_element_score: Natal chart after interactions (internal dynamics)
        - post_element_score: All nodes after interactions (full situation)
        - interactions: Complete interaction log
        - daymaster_analysis: Day master strength analysis
        - mappings: Reference data (stems, branches, ten gods)
    """
    
    # Extract natal birth time
    hour, minute = extract_hour_minute(birth_time)
    
    # 1. Generate natal chart (always)
    natal_chart = generate_bazi_chart(
        year=birth_date.year,
        month=birth_date.month,
        day=birth_date.day,
        hour=hour,
        minute=minute,
    )
    
    # 2. Start with natal chart
    chart_dict = dict(natal_chart)
    
    # 3. If analysis_year is provided, generate luck and time period pillars
    luck_10y_info = None  # Store 10-year luck period info for misc field
    if analysis_year:
        # Generate luck pillars to find the active one
        luck_pillars = generate_luck_pillars(
            year_pillar=natal_chart["year_pillar"],
            month_pillar=natal_chart["month_pillar"],
            gender=gender,
            dob=birth_date,
        )
        
        # Find 10-year luck pillar active at analysis_year
        age_at_analysis = analysis_year - birth_date.year
        for lp in luck_pillars:
            start_age = lp.get("start_age", 0)
            end_age = start_age + 10
            if start_age <= age_at_analysis < end_age:
                chart_dict["luck_10_year"] = lp["pillar"]
                # Calculate precise start and end dates
                start_date = birth_date + timedelta(days=int(start_age * 365.25))
                end_date = birth_date + timedelta(days=int(end_age * 365.25))
                luck_10y_info = {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat()
                }
                # Add time if birth_time provided
                if birth_time:
                    luck_10y_info["start_time"] = birth_time
                    luck_10y_info["end_time"] = birth_time
                break
        
        # If no luck pillar found, use first one
        if "luck_10_year" not in chart_dict and luck_pillars:
            first_lp = luck_pillars[0]
            chart_dict["luck_10_year"] = first_lp["pillar"]
            start_age = first_lp.get("start_age", 0)
            end_age = start_age + 10
            # Calculate precise dates
            start_date = birth_date + timedelta(days=int(start_age * 365.25))
            end_date = birth_date + timedelta(days=int(end_age * 365.25))
            luck_10y_info = {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
            if birth_time:
                luck_10y_info["start_time"] = birth_time
                luck_10y_info["end_time"] = birth_time
        
        # Generate time period pillars - use defaults for missing granularity
        analysis_month_val = analysis_month if analysis_month else 2  # Default Feb
        analysis_day_val = analysis_day if analysis_day else 15  # Default mid-month
        
        # Extract hour and minute from analysis_time if provided
        analysis_hour_val = None
        analysis_minute_val = None
        if analysis_time:
            analysis_hour_val, analysis_minute_val = extract_hour_minute(analysis_time)
        
        time_pillars = generate_bazi_chart(
            year=analysis_year,
            month=analysis_month_val,
            day=analysis_day_val,
            hour=analysis_hour_val,
            minute=analysis_minute_val,
        )
        
        # Store annual pillar for display (always, but only include in interactions if enabled)
        annual_pillar_for_display = time_pillars["year_pillar"]
        
        # Add annual pillar to chart_dict for interactions (only if include_annual_luck is True)
        if include_annual_luck:
            chart_dict["yearly_luck"] = time_pillars["year_pillar"]
        
        # Add monthly pillar (only if analysis_month is provided)
        if analysis_month:
            chart_dict["monthly_luck"] = time_pillars["month_pillar"]
        
        # Add daily pillar (only if analysis_day is provided)
        if analysis_day:
            chart_dict["daily_luck"] = time_pillars["day_pillar"]
        
        # Add hourly pillar (only if analysis_time is provided)
        if analysis_time:
            chart_dict["hourly_luck"] = time_pillars["hour_pillar"]
    
    # 4. Get month branch for interaction analysis
    day_pillar_str = natal_chart["day_pillar"]
    day_master_hs = day_pillar_str.split(" ")[0]
    
    month_pillar_str = natal_chart.get("month_pillar", "")
    month_branch = month_pillar_str.split(" ")[1] if " " in month_pillar_str else None
    
    # 5. Calculate ALL interactions across ALL nodes (including optional talismans)
    interaction_results = analyze_8_node_interactions(
        chart_dict,
        month_branch=month_branch,
        talisman_year_hs=talisman_year_hs,
        talisman_year_eb=talisman_year_eb,
        talisman_month_hs=talisman_month_hs,
        talisman_month_eb=talisman_month_eb,
        talisman_day_hs=talisman_day_hs,
        talisman_day_eb=talisman_day_eb,
        talisman_hour_hs=talisman_hour_hs,
        talisman_hour_eb=talisman_hour_eb,
        location=location
    )
    
    # 6. Build response
    response = {
        "birth_info": {
            "date": birth_date.isoformat(),
            "time": birth_time or "Unknown",
            "gender": gender
        },
        "analysis_info": {
            "year": analysis_year,
            "month": analysis_month,
            "day": analysis_day,
            "time": analysis_time,
            "has_luck_pillar": "luck_10_year" in chart_dict,
            "has_annual": "yearly_luck" in chart_dict,
            "has_monthly": "monthly_luck" in chart_dict,
            "has_daily": "daily_luck" in chart_dict,
            "has_hourly": "hourly_luck" in chart_dict,
            "annual_disabled": analysis_year is not None and not include_annual_luck,  # NEW: Flag for greyed-out display
        }
    }
    
    # Add all nodes from interaction results
    nodes_with_ten_gods = interaction_results.get("nodes", {})
    response.update(nodes_with_ten_gods)
    
    # If annual luck was disabled but year was provided, add display-only nodes
    # These nodes won't be in chart_dict (so not in interactions) but needed for UI
    if analysis_year and not include_annual_luck:
        # Generate temporary display nodes for annual pillar
        annual_hs, annual_eb = annual_pillar_for_display.split(" ")
        
        # Create minimal node structure for display (no interactions)
        response["hs_yl"] = {
            "base": {"id": annual_hs, "qi": {annual_hs: 100.0}},
            "interaction_ids": [],
            "post": {"id": annual_hs, "qi": {annual_hs: 100.0}},
            "badges": [],
            "disabled": True  # Mark as disabled for frontend
        }
        # Get qi scores from EARTHLY_BRANCHES (qi is list of (stem, score) tuples)
        eb_qi = {qi_tuple[0]: float(qi_tuple[1]) for qi_tuple in EARTHLY_BRANCHES[annual_eb]["qi"]}
        
        response["eb_yl"] = {
            "base": {"id": annual_eb, "qi": eb_qi},
            "interaction_ids": [],
            "post": {"id": annual_eb, "qi": eb_qi},
            "badges": [],
            "disabled": True  # Mark as disabled for frontend
        }
    
    # Add misc field to 10-year luck nodes if they exist
    if luck_10y_info and "hs_10yl" in response and "eb_10yl" in response:
        response["hs_10yl"]["misc"] = luck_10y_info
        response["eb_10yl"]["misc"] = luck_10y_info
    
    # Add scores and interactions (3-tier: base → natal → post)
    response["base_element_score"] = interaction_results.get("base_element_score", {})
    response["natal_element_score"] = interaction_results.get("natal_element_score", {})
    response["post_element_score"] = interaction_results.get("post_element_score", {})
    response["interactions"] = interaction_results.get("interactions", {})
    response["daymaster_analysis"] = interaction_results["daymaster_analysis"]
    response["wealth_storage_analysis"] = interaction_results.get("wealth_storage_analysis", {})
    response["unit_tracker"] = interaction_results.get("unit_tracker")  # Unit Story tracking

    # Add Dong Gong Date Selection info when daily luck is present
    if analysis_year and analysis_month and analysis_day and "daily_luck" in chart_dict and "monthly_luck" in chart_dict:
        daily_pillar = chart_dict["daily_luck"]  # e.g., "Geng Shen"
        daily_stem, daily_branch = daily_pillar.split(" ")

        # Extract the ACTUAL Chinese month branch from the monthly luck pillar
        monthly_pillar = chart_dict["monthly_luck"]  # e.g., "Geng Yin" for Yin month
        monthly_stem, monthly_branch = monthly_pillar.split(" ")

        # Get the Chinese month number from the branch (Yin=1, Mao=2, etc.)
        chinese_month = DONG_GONG_BRANCH_TO_MONTH.get(monthly_branch)

        if chinese_month and monthly_branch:
            # Calculate day officer using actual Chinese month branch
            day_officer = get_dong_gong_officer(monthly_branch, daily_branch)
            officer_info = DONG_GONG_DAY_OFFICERS.get(day_officer, {})

            # Get rating for this specific pillar using Chinese month number
            rating = get_dong_gong_rating(chinese_month, daily_branch, daily_stem)
            rating_info = DONG_GONG_RATINGS.get(rating, {}) if rating else {}

            # Get full day info (good_for, bad_for, descriptions)
            day_info = get_dong_gong_day_info(chinese_month, daily_branch)

            response["dong_gong"] = {
                "month": chinese_month,
                "month_branch": monthly_branch,
                "month_chinese": DONG_GONG_MONTHS.get(chinese_month, {}).get("chinese", ""),
                "day_stem": daily_stem,
                "day_branch": daily_branch,
                "pillar": daily_pillar,
                "officer": {
                    "id": day_officer,
                    "chinese": officer_info.get("chinese", ""),
                    "english": officer_info.get("english", ""),
                },
                "rating": {
                    "id": rating,
                    "value": rating_info.get("value", 0),
                    "symbol": rating_info.get("symbol", ""),
                    "chinese": rating_info.get("chinese", ""),
                } if rating else None,
                "good_for": day_info.get("good_for", []) if day_info else [],
                "bad_for": day_info.get("bad_for", []) if day_info else [],
                "description_chinese": day_info.get("description_chinese", "") if day_info else "",
                "description_english": day_info.get("description_english", "") if day_info else "",
            }

    # Add mappings (using new structure where key is the id)
    response["mappings"] = {
        "heavenly_stems": {
            stem_id: {
                "id": stem_id,
                "pinyin": stem_id,  # pinyin is the key
                "chinese": stem_data["chinese"],
                "english": stem_id,  # use pinyin as english equivalent
                "hex_color": stem_data["color"]
            }
            for stem_id, stem_data in HEAVENLY_STEMS.items()
        },
        "earthly_branches": {
            branch_id: {
                "id": branch_id,
                "chinese": branch_data["chinese"],
                "animal": branch_data["animal"],
                "hex_color": branch_data["color"],
                "qi": [
                    {
                        "stem": qi_tuple[0],
                        "score": qi_tuple[1],
                        "stem_chinese": HEAVENLY_STEMS.get(qi_tuple[0], {}).get("chinese", "?"),
                        "element": HEAVENLY_STEMS.get(qi_tuple[0], {}).get("element", "?"),
                        "polarity": HEAVENLY_STEMS.get(qi_tuple[0], {}).get("polarity", "?"),
                        "hex_color": HEAVENLY_STEMS.get(qi_tuple[0], {}).get("color", "#ccc")
                    }
                    for qi_tuple in branch_data.get("qi", [])
                ]
            }
            for branch_id, branch_data in EARTHLY_BRANCHES.items()
        },
        "ten_gods": TEN_GODS,
        # Event type styling for frontend rendering
        "event_types": {
            "registration": {"hex_color": "#60a5fa", "icon": "📝", "label": "Registration"},
            "seasonal": {"hex_color": "#fbbf24", "icon": "🍂", "label": "Seasonal"},
            "controlling": {"hex_color": "#f87171", "icon": "⚔️", "label": "Controlling"},
            "controlled": {"hex_color": "#f87171", "icon": "⚔️", "label": "Controlled"},
            "control": {"hex_color": "#f87171", "icon": "⚔️", "label": "Control"},
            "producing": {"hex_color": "#4ade80", "icon": "🌱", "label": "Producing"},
            "produced": {"hex_color": "#4ade80", "icon": "🌱", "label": "Produced"},
            "generation": {"hex_color": "#4ade80", "icon": "🌱", "label": "Generation"},
            "combination": {"hex_color": "#c084fc", "icon": "🤝", "label": "Combination"},
            "conflict": {"hex_color": "#fb923c", "icon": "💥", "label": "Conflict"},
            "conflict_aggressor": {"hex_color": "#fb923c", "icon": "💥", "label": "Conflict"},
            "conflict_victim": {"hex_color": "#fb923c", "icon": "💥", "label": "Conflict"},
            "same_element": {"hex_color": "#2dd4bf", "icon": "🔗", "label": "Same Element"},
        },
        # Ten gods styling for frontend rendering
        "ten_gods_styling": {
            "DM": {"hex_color": "#9333ea", "bg_hex": "#f3e8ff", "label": "Day Master"},
            "F": {"hex_color": "#2563eb", "bg_hex": "#dbeafe", "label": "Friend"},
            "RW": {"hex_color": "#3b82f6", "bg_hex": "#eff6ff", "label": "Rob Wealth"},
            "EG": {"hex_color": "#16a34a", "bg_hex": "#dcfce7", "label": "Eating God"},
            "HO": {"hex_color": "#22c55e", "bg_hex": "#f0fdf4", "label": "Hurting Officer"},
            "IW": {"hex_color": "#ca8a04", "bg_hex": "#fef9c3", "label": "Indirect Wealth"},
            "DW": {"hex_color": "#eab308", "bg_hex": "#fefce8", "label": "Direct Wealth"},
            "7K": {"hex_color": "#dc2626", "bg_hex": "#fee2e2", "label": "Seven Killings"},
            "DO": {"hex_color": "#ef4444", "bg_hex": "#fef2f2", "label": "Direct Officer"},
            "IR": {"hex_color": "#4b5563", "bg_hex": "#f3f4f6", "label": "Indirect Resource"},
            "DR": {"hex_color": "#6b7280", "bg_hex": "#f9fafb", "label": "Direct Resource"},
        },
        # Element colors for frontend rendering
        "elements": {
            "Wood": {"hex_color": "#22c55e", "hex_color_yang": "#16a34a", "hex_color_yin": "#4ade80"},
            "Fire": {"hex_color": "#ef4444", "hex_color_yang": "#dc2626", "hex_color_yin": "#f87171"},
            "Earth": {"hex_color": "#ca8a04", "hex_color_yang": "#a16207", "hex_color_yin": "#eab308"},
            "Metal": {"hex_color": "#6b7280", "hex_color_yang": "#4b5563", "hex_color_yin": "#9ca3af"},
            "Water": {"hex_color": "#3b82f6", "hex_color_yang": "#2563eb", "hex_color_yin": "#60a5fa"},
        }
    }

    return response

