
import sxtwl
from datetime import datetime, date, timedelta
from typing import Literal, Dict, List, Optional, Any
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db, init_db
from schemas import ProfileCreate, ProfileUpdate, ProfileResponse, LifeEventCreate, LifeEventUpdate, LifeEvent
import crud

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
    get_dong_gong_day_info,
    # Life Aspects Analysis
    generate_health_analysis,
    generate_wealth_analysis,
    generate_learning_analysis,
    generate_ten_gods_detail,
)

# Import from chart_constructor
from chart_constructor import (
    generate_bazi_chart,
    generate_luck_pillars,
    generate_xiao_yun_pillars
)

# Import from bazingse
from bazingse import analyze_8_node_interactions

# Import Pattern Engine integration
from library.pattern_engine.integration import analyze_with_pattern_engine

# Import Narrative Interpretation System
from library.narrative import generate_narrative, generate_pillar_stories

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
    luck_pillars = None   # Store Da Yun pillars for analysis_info
    da_yun_start_age = None  # Age when Da Yun begins
    if analysis_year:
        # Generate Da Yun (10-year luck) pillars to find the active one
        luck_pillars = generate_luck_pillars(
            year_pillar=natal_chart["year_pillar"],
            month_pillar=natal_chart["month_pillar"],
            gender=gender,
            dob=birth_date,
        )

        # Get Da Yun start age (when first 10-year luck pillar begins)
        da_yun_start_age = luck_pillars[0].get("start_age", 0) if luck_pillars else 0

        # Calculate age at analysis (Western age)
        age_at_analysis = analysis_year - birth_date.year

        # Check if we're in Xiao Yun period (before Da Yun starts)
        # Xiao Yun requires hour pillar (birth time)
        if age_at_analysis < da_yun_start_age and "hour_pillar" in natal_chart:
            # Generate Xiao Yun pillars for pre-Da Yun years
            xiao_yun_pillars = generate_xiao_yun_pillars(
                hour_pillar=natal_chart["hour_pillar"],
                year_pillar=natal_chart["year_pillar"],
                gender=gender,
                da_yun_start_age=da_yun_start_age,
            )

            # Find Xiao Yun pillar for this age
            # Chinese age = Western age + 1, so we need to match start_age (which is Western)
            for xp in xiao_yun_pillars:
                if xp["start_age"] == age_at_analysis:
                    chart_dict["luck_10_year"] = xp["pillar"]
                    # Calculate precise dates for this single year
                    start_date = birth_date + timedelta(days=int(age_at_analysis * 365.25))
                    end_date = birth_date + timedelta(days=int((age_at_analysis + 1) * 365.25))
                    luck_10y_info = {
                        "start_date": start_date.isoformat(),
                        "end_date": end_date.isoformat(),
                        "is_xiao_yun": True,
                        "chinese_age": xp["chinese_age"],  # 虛歲
                    }
                    if birth_time:
                        luck_10y_info["start_time"] = birth_time
                        luck_10y_info["end_time"] = birth_time
                    break

            # If no exact match found but we're in Xiao Yun range, use first pillar
            if "luck_10_year" not in chart_dict and xiao_yun_pillars:
                first_xp = xiao_yun_pillars[0]
                chart_dict["luck_10_year"] = first_xp["pillar"]
                start_date = birth_date
                end_date = birth_date + timedelta(days=365)
                luck_10y_info = {
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "is_xiao_yun": True,
                    "chinese_age": first_xp["chinese_age"],
                }
                if birth_time:
                    luck_10y_info["start_time"] = birth_time
                    luck_10y_info["end_time"] = birth_time
        else:
            # Da Yun period - find 10-year luck pillar active at analysis_year
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
                        "end_date": end_date.isoformat(),
                        "is_xiao_yun": False,
                    }
                    # Add time if birth_time provided
                    if birth_time:
                        luck_10y_info["start_time"] = birth_time
                        luck_10y_info["end_time"] = birth_time
                    break

            # If no luck pillar found (e.g., age before Xiao Yun with no hour pillar), use first Da Yun
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
                    "end_date": end_date.isoformat(),
                    "is_xiao_yun": False,
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
            "is_xiao_yun": luck_10y_info.get("is_xiao_yun", False) if luck_10y_info else False,  # True if in Xiao Yun (小運) period
            "da_yun_start_age": da_yun_start_age,  # Age when Da Yun (大運) begins
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

    # Generate Life Aspects Analysis (Health, Wealth, Learning)
    daymaster_element = HEAVENLY_STEMS.get(day_master_hs, {}).get("element", "")
    daymaster_strength = interaction_results.get("daymaster_analysis", {}).get("strength", "Balanced")
    daymaster_support_pct = interaction_results.get("daymaster_analysis", {}).get("support_percentage", 50.0)

    # Get seasonal states for month
    seasonal_states = {}
    if month_branch and month_branch in EARTHLY_BRANCHES:
        seasonal_states = EARTHLY_BRANCHES[month_branch].get("element_states", {})

    # Health Analysis (TCM organ-element correlations + control cycle imbalances)
    health_analysis = generate_health_analysis(
        interactions=interaction_results.get("interactions", {}),
        post_element_score=interaction_results.get("post_element_score", {}),
        natal_element_score=interaction_results.get("natal_element_score", {}),
        month_branch=month_branch,
        daymaster_element=daymaster_element
    )
    response["health_analysis"] = health_analysis

    # Wealth Analysis (Financial opportunities and risks)
    wealth_analysis = generate_wealth_analysis(
        interactions=interaction_results.get("interactions", {}),
        post_element_score=interaction_results.get("post_element_score", {}),
        natal_element_score=interaction_results.get("natal_element_score", {}),
        seasonal_states=seasonal_states,
        daymaster_element=daymaster_element,
        daymaster_strength=daymaster_strength,
        wealth_storage_analysis=interaction_results.get("wealth_storage_analysis")
    )
    response["wealth_analysis"] = wealth_analysis

    # Learning Analysis (Education and skill development)
    learning_analysis = generate_learning_analysis(
        interactions=interaction_results.get("interactions", {}),
        post_element_score=interaction_results.get("post_element_score", {}),
        natal_element_score=interaction_results.get("natal_element_score", {}),
        seasonal_states=seasonal_states,
        daymaster_element=daymaster_element,
        daymaster_strength=daymaster_strength,
        support_percentage=daymaster_support_pct
    )
    response["learning_analysis"] = learning_analysis

    # Ten Gods Detail Analysis (per-node breakdown)
    ten_gods_detail = generate_ten_gods_detail(
        nodes=nodes_with_ten_gods,
        day_master_stem=day_master_hs,
        interactions=interaction_results.get("interactions", {})
    )
    response["ten_gods_detail"] = ten_gods_detail

    # Extract Year Branch for context-dependent Shen Sha (Gu Chen, Gua Su, etc.)
    year_pillar = natal_chart.get("year_pillar", "")
    year_branch = year_pillar.split(" ")[1] if " " in year_pillar else ""

    # Pattern Engine Analysis (enhanced pattern detection + severity + predictions)
    pattern_engine_analysis = analyze_with_pattern_engine(
        interactions=interaction_results.get("interactions", {}),
        seasonal_states=seasonal_states,
        daymaster_stem=day_master_hs,
        daymaster_element=daymaster_element,
        post_element_score=interaction_results.get("post_element_score", {}),
        year_branch=year_branch,
    )
    response["pattern_engine_analysis"] = pattern_engine_analysis

    # Enhance existing analysis with Pattern Engine insights
    domain_analysis = pattern_engine_analysis.get("domain_analysis", {})
    enhanced_patterns = pattern_engine_analysis.get("enhanced_patterns", [])
    recommendations = pattern_engine_analysis.get("recommendations", [])

    # Enhance health_analysis with Pattern Engine data
    if "health" in domain_analysis:
        health_domain = domain_analysis["health"]
        health_patterns = [p for p in enhanced_patterns if "health" in p.get("affected_domains", [])]
        health_recs = [r for r in recommendations if r.get("domain") == "health"]

        response["health_analysis"]["pattern_engine"] = {
            "pattern_count": health_domain.get("pattern_count", 0),
            "compound_severity": health_domain.get("compound_severity", 0),
            "severity_level": health_domain.get("severity_level", "unknown"),
            "top_patterns": [
                {
                    "chinese_name": p.get("chinese_name"),
                    "severity": p.get("severity", {}).get("normalized_score", 0),
                    "level": p.get("severity", {}).get("level", "unknown"),
                }
                for p in sorted(health_patterns, key=lambda x: x.get("severity", {}).get("normalized_score", 0), reverse=True)[:5]
            ],
            "recommendations": health_recs,
        }

    # Enhance wealth_analysis with Pattern Engine data
    if "wealth" in domain_analysis:
        wealth_domain = domain_analysis["wealth"]
        wealth_patterns = [p for p in enhanced_patterns if "wealth" in p.get("affected_domains", [])]
        wealth_recs = [r for r in recommendations if r.get("domain") == "wealth"]

        response["wealth_analysis"]["pattern_engine"] = {
            "pattern_count": wealth_domain.get("pattern_count", 0),
            "compound_severity": wealth_domain.get("compound_severity", 0),
            "severity_level": wealth_domain.get("severity_level", "unknown"),
            "top_patterns": [
                {
                    "chinese_name": p.get("chinese_name"),
                    "severity": p.get("severity", {}).get("normalized_score", 0),
                    "level": p.get("severity", {}).get("level", "unknown"),
                }
                for p in sorted(wealth_patterns, key=lambda x: x.get("severity", {}).get("normalized_score", 0), reverse=True)[:5]
            ],
            "recommendations": wealth_recs,
        }

    # Enhance learning_analysis with Pattern Engine data (uses education domain)
    if "education" in domain_analysis:
        edu_domain = domain_analysis["education"]
        edu_patterns = [p for p in enhanced_patterns if "education" in p.get("affected_domains", [])]

        response["learning_analysis"]["pattern_engine"] = {
            "pattern_count": edu_domain.get("pattern_count", 0),
            "compound_severity": edu_domain.get("compound_severity", 0),
            "severity_level": edu_domain.get("severity_level", "unknown"),
            "top_patterns": [
                {
                    "chinese_name": p.get("chinese_name"),
                    "severity": p.get("severity", {}).get("normalized_score", 0),
                    "level": p.get("severity", {}).get("level", "unknown"),
                }
                for p in sorted(edu_patterns, key=lambda x: x.get("severity", {}).get("normalized_score", 0), reverse=True)[:5]
            ],
        }

    # Add special stars to response (from Pattern Engine)
    response["special_stars"] = pattern_engine_analysis.get("special_stars", [])

    # Add unified recommendations (from Pattern Engine)
    response["recommendations"] = recommendations

    # Generate Narrative Interpretation
    narrative_analysis = generate_narrative(
        interactions=interaction_results.get("interactions", {}),
        post_element_score=interaction_results.get("post_element_score", {}),
        natal_element_score=interaction_results.get("natal_element_score", {}),
        daymaster_analysis=interaction_results.get("daymaster_analysis", {}),
        wealth_storage_analysis=interaction_results.get("wealth_storage_analysis"),
        special_stars=pattern_engine_analysis.get("special_stars", []),
        ten_gods_detail=response.get("ten_gods_detail", {}),  # Add Ten Gods for richer narratives
        nodes=response,  # Pass full response for pillar analysis
        locale="en",  # Default to English, can be parameterized later
        max_narratives=15,  # Increase limit for more comprehensive analysis
    )
    response["narrative_analysis"] = narrative_analysis

    # Generate Pillar-Based Stories (node-by-node narrative with minimap)
    pillar_stories = generate_pillar_stories(
        nodes_data=response,  # Contains all node data (hs_d, eb_d, etc.)
        daymaster_analysis=interaction_results.get("daymaster_analysis", {}),
        element_context=narrative_analysis.get("element_context", {}),
        special_stars=pattern_engine_analysis.get("special_stars", []),
        interactions=interaction_results.get("interactions", {}),
        locale="en",
    )
    response["pillar_stories"] = pillar_stories

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


# * =================
# * PROFILE ENDPOINTS
# * =================

@router.on_event("startup")
async def startup():
    """Initialize database on startup."""
    init_db()


@router.get("/profiles", response_model=List[ProfileResponse])
async def list_profiles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List all profiles."""
    profiles = crud.get_profiles(db, skip=skip, limit=limit)
    return profiles


@router.post("/profiles", response_model=ProfileResponse, status_code=201)
async def create_profile(
    profile_data: ProfileCreate,
    db: Session = Depends(get_db)
):
    """Create a new profile."""
    profile = crud.create_profile(db, profile_data)
    return profile


@router.get("/profiles/{profile_id}", response_model=ProfileResponse)
async def get_profile(
    profile_id: str,
    db: Session = Depends(get_db)
):
    """Get a single profile by ID."""
    profile = crud.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/profiles/{profile_id}", response_model=ProfileResponse)
async def update_profile(
    profile_id: str,
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing profile."""
    profile = crud.update_profile(db, profile_id, profile_data)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.delete("/profiles/{profile_id}", status_code=204)
async def delete_profile(
    profile_id: str,
    db: Session = Depends(get_db)
):
    """Delete a profile."""
    success = crud.delete_profile(db, profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return None


# * =================
# * LIFE EVENT ENDPOINTS
# * =================

@router.post("/profiles/{profile_id}/life_events", response_model=LifeEvent, status_code=201)
async def create_life_event(
    profile_id: str,
    event_data: LifeEventCreate,
    db: Session = Depends(get_db)
):
    """Create a new life event for a profile."""
    event = crud.add_life_event(db, profile_id, event_data)
    if not event:
        raise HTTPException(status_code=404, detail="Profile not found")
    return event


@router.get("/profiles/{profile_id}/life_events/{event_id}", response_model=LifeEvent)
async def get_life_event(
    profile_id: str,
    event_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific life event."""
    event = crud.get_life_event(db, profile_id, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Life event not found")
    return event


@router.put("/profiles/{profile_id}/life_events/{event_id}", response_model=LifeEvent)
async def update_life_event(
    profile_id: str,
    event_id: str,
    event_data: LifeEventUpdate,
    db: Session = Depends(get_db)
):
    """Update a life event."""
    event = crud.update_life_event(db, profile_id, event_id, event_data)
    if not event:
        raise HTTPException(status_code=404, detail="Life event not found")
    return event


@router.delete("/profiles/{profile_id}/life_events/{event_id}", status_code=204)
async def delete_life_event(
    profile_id: str,
    event_id: str,
    db: Session = Depends(get_db)
):
    """Delete a life event."""
    success = crud.delete_life_event(db, profile_id, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Life event not found")
    return None

