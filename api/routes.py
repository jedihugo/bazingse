
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
    ZHI_MAP
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
        - base_element_score: Elements before interactions
        - post_element_score: Elements after all interactions
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
        # Get qi scores from EARTHLY_BRANCHES
        eb_qi = {qi_item["stem"]: float(qi_item["score"]) for qi_item in EARTHLY_BRANCHES[annual_eb]["qi"]}
        
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
    
    # Add scores and interactions (2-tier: base=natal only, post=everything)
    response["base_element_score"] = interaction_results.get("base_element_score", {})
    response["post_element_score"] = interaction_results.get("post_element_score", {})
    response["interactions"] = interaction_results.get("interactions", {})
    response["daymaster_analysis"] = interaction_results["daymaster_analysis"]
    
    # Add mappings
    response["mappings"] = {
        "heavenly_stems": {
            stem_id: {
                "id": stem_data["id"],
                "pinyin": stem_data["pinyin"],
                "chinese": stem_data["chinese"],
                "english": stem_data["english"],
                "hex_color": stem_data["hex_color"]
            }
            for stem_id, stem_data in HEAVENLY_STEMS.items()
        },
        "earthly_branches": {
            branch_id: {
                "id": branch_data["id"],
                "chinese": branch_data["chinese"],
                "animal": branch_data["animal"],
                "hex_color": branch_data["hex_color"]
            }
            for branch_id, branch_data in EARTHLY_BRANCHES.items()
        },
        "ten_gods": TEN_GODS
    }
    
    return response

