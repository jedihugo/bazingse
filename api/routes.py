
import sxtwl
import calendar as cal_module
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
    check_consult_promotion,
)

# Import DONG_GONG data dict for calendar endpoint
from library import DONG_GONG

# Import from chart_constructor
from chart_constructor import (
    generate_bazi_chart,
    generate_luck_pillars,
    generate_xiao_yun_pillars
)

# Import Comprehensive BaZi Engine
from library.comprehensive.engine import build_chart, analyze_for_api
from library.comprehensive.adapter import adapt_to_frontend

# sxtwl solar term indices for Four Extinction (四絕) and Four Separation (四離)
# Four Extinction: day before start-of-season terms (Li Chun, Li Xia, Li Qiu, Li Dong)
# Four Separation: day before mid-season terms (Chun Fen, Xia Zhi, Qiu Fen, Dong Zhi)
# sxtwl index mapping (verified empirically):
#   0=Dong Zhi, 1=Xiao Han, 2=Da Han, 3=Li Chun, 4=Yu Shui, 5=Jing Zhe,
#   6=Chun Fen, 7=Qing Ming, 8=Gu Yu, 9=Li Xia, 10=Xiao Man, 11=Mang Zhong,
#   12=Xia Zhi, 13=Xiao Shu, 14=Da Shu, 15=Li Qiu, 16=Chu Shu, 17=Bai Lu,
#   18=Qiu Fen, 19=Han Lu, 20=Shuang Jiang, 21=Li Dong, 22=Xiao Xue, 23=Da Xue
FOUR_EXTINCTION_INDICES = {3, 9, 15, 21}   # Li Chun, Li Xia, Li Qiu, Li Dong
FOUR_SEPARATION_INDICES = {0, 6, 12, 18}   # Dong Zhi, Chun Fen, Xia Zhi, Qiu Fen

JIEQI_NAMES = {
    3: ("li_chun", "立春", "Li Chun"),
    9: ("li_xia", "立夏", "Li Xia"),
    15: ("li_qiu", "立秋", "Li Qiu"),
    21: ("li_dong", "立冬", "Li Dong"),
    0: ("dong_zhi", "冬至", "Dong Zhi"),
    6: ("chun_fen", "春分", "Chun Fen"),
    12: ("xia_zhi", "夏至", "Xia Zhi"),
    18: ("qiu_fen", "秋分", "Qiu Fen"),
}

def check_four_extinction_separation(
    year: int, month: int, day: int,
    hour: Optional[float] = None,
) -> Optional[dict]:
    """Check if this calendar day (or a specific hour on it) overlaps with the
    24 hours before a Four Extinction (四絕) or Four Separation (四離) solar term.

    When ``hour`` is None (calendar view), returns the forbidden hour range for
    the entire day so the UI can display both the original rating and the
    forbidden overlay.  When ``hour`` is given (analyze_bazi), only returns a
    result if that specific hour falls inside the forbidden window.

    Returns dict with type/name info and forbidden_start_hour / forbidden_end_hour,
    or None if the day/hour is unaffected.
    """
    analysis_date = date(year, month, day)

    # Check the current day and the next day for relevant solar terms.
    # A term on day+1 creates a forbidden tail on the current day, and
    # a term on day+0 creates a forbidden head on the current day.
    for day_offset in range(2):
        check_date = analysis_date + timedelta(days=day_offset)
        lunar_day = sxtwl.fromSolar(check_date.year, check_date.month, check_date.day)

        if not lunar_day.hasJieQi():
            continue

        jq_idx = lunar_day.getJieQi()
        if jq_idx not in FOUR_EXTINCTION_INDICES and jq_idx not in FOUR_SEPARATION_INDICES:
            continue

        # Get exact solar term time (hours from midnight of check_date).
        # sxtwl returns JD already in CST (Beijing time, UTC+8).
        # Raw conversion is accurate to ~1 minute — no correction needed.
        jq_jd = lunar_day.getJieQiJD()
        jd_fraction = jq_jd % 1
        transition_hour = (jd_fraction * 24 + 12) % 24

        # Express everything in hours from analysis_date midnight
        term_total = day_offset * 24 + transition_hour
        forbidden_start_total = term_total - 24
        forbidden_end_total = term_total

        # Clamp to this calendar day [0, 24)
        overlap_start = max(forbidden_start_total, 0)
        overlap_end = min(forbidden_end_total, 24)

        if overlap_start >= overlap_end:
            continue

        # If a specific hour is given, only match if it falls inside
        if hour is not None and not (overlap_start <= hour < overlap_end):
            continue

        jq_id, jq_chinese, jq_english = JIEQI_NAMES[jq_idx]
        is_extinction = jq_idx in FOUR_EXTINCTION_INDICES
        return {
            "type": "four_extinction" if is_extinction else "four_separation",
            "chinese": "四絕" if is_extinction else "四離",
            "english": "Four Extinction" if is_extinction else "Four Separation",
            "solar_term_id": jq_id,
            "solar_term_chinese": jq_chinese,
            "solar_term_english": jq_english,
            "forbidden_start_hour": round(overlap_start, 2),
            "forbidden_end_hour": round(overlap_end, 2),
        }

    return None


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
    location: Optional[Literal["overseas", "birthplace"]] = Query(None, description="Location status: 'overseas' (Water boost from Ren-Zi + Gui-Hai) or 'birthplace' (Earth boost from 4 Earth pillars at 50%)"),
    school: Literal["classic", "physics"] = Query("classic", description="Analysis school: 'classic' (standard) or 'physics' (Yin/Yang polarity threshold)")
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
    
    # 4. Extract stems and branches from natal chart pillars
    day_pillar_str = natal_chart["day_pillar"]
    day_master_hs = day_pillar_str.split(" ")[0]

    # Extract all pillar components for comprehensive engine
    year_stem, year_branch = natal_chart["year_pillar"].split(" ")
    month_stem, month_branch = natal_chart["month_pillar"].split(" ")
    day_stem, day_branch = natal_chart["day_pillar"].split(" ")

    # Hour pillar (may not exist if birth time unknown)
    if "hour_pillar" in natal_chart:
        hour_stem, hour_branch = natal_chart["hour_pillar"].split(" ")
    else:
        hour_stem, hour_branch = day_stem, day_branch  # Fallback to day pillar

    # Luck pillar stems/branches for comprehensive engine
    lp_stem, lp_branch = "", ""
    if "luck_10_year" in chart_dict:
        lp_stem, lp_branch = chart_dict["luck_10_year"].split(" ")

    # Build luck pillars list for comprehensive engine
    luck_pillars_list = []
    if luck_pillars:
        for lp_data in luck_pillars:
            lp_pillar = lp_data["pillar"]
            lp_s, lp_b = lp_pillar.split(" ")
            start_age = lp_data.get("start_age", 0)
            luck_pillars_list.append({
                "stem": lp_s,
                "branch": lp_b,
                "start_age": start_age,
                "end_age": start_age + 10,
                "start_year": birth_date.year + start_age,
                "end_year": birth_date.year + start_age + 10,
            })

    # 5. Build comprehensive chart and run analysis
    comprehensive_chart = build_chart(
        gender=gender,
        birth_year=birth_date.year,
        year_stem=year_stem, year_branch=year_branch,
        month_stem=month_stem, month_branch=month_branch,
        day_stem=day_stem, day_branch=day_branch,
        hour_stem=hour_stem, hour_branch=hour_branch,
        luck_pillar_stem=lp_stem,
        luck_pillar_branch=lp_branch,
        luck_pillars=luck_pillars_list,
        current_year=analysis_year or datetime.now().year,
    )

    results = analyze_for_api(comprehensive_chart)

    # 6. Build response with adapter
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
            "annual_disabled": analysis_year is not None and not include_annual_luck,
            "is_xiao_yun": luck_10y_info.get("is_xiao_yun", False) if luck_10y_info else False,
            "da_yun_start_age": da_yun_start_age,
        }
    }

    # Apply adapter to get all frontend-expected fields
    adapted = adapt_to_frontend(comprehensive_chart, results)
    response.update(adapted)

    # Build time-period pillar nodes (annual, monthly, daily, hourly luck)
    # These are display-only nodes not part of the comprehensive engine's natal analysis
    time_period_map = {
        "yearly_luck": ("hs_yl", "eb_yl"),
        "monthly_luck": ("hs_ml", "eb_ml"),
        "daily_luck": ("hs_dl", "eb_dl"),
        "hourly_luck": ("hs_hl", "eb_hl"),
    }
    for chart_key, (hs_key, eb_key) in time_period_map.items():
        if chart_key in chart_dict:
            tp_stem, tp_branch = chart_dict[chart_key].split(" ")
            response[hs_key] = {
                "id": tp_stem,
                "base": {"id": tp_stem, "qi": {tp_stem: 100.0}},
                "post": {"id": tp_stem, "qi": {tp_stem: 100.0}},
                "badges": [],
                "interaction_ids": [],
            }
            tp_eb_qi = {qi[0]: float(qi[1]) for qi in EARTHLY_BRANCHES[tp_branch]["qi"]}
            response[eb_key] = {
                "id": tp_branch,
                "base": {"id": tp_branch, "qi": tp_eb_qi},
                "post": {"id": tp_branch, "qi": tp_eb_qi},
                "badges": [],
                "interaction_ids": [],
            }

    # If annual luck was disabled but year was provided, add display-only nodes
    if analysis_year and not include_annual_luck:
        annual_hs, annual_eb = annual_pillar_for_display.split(" ")
        response["hs_yl"] = {
            "id": annual_hs,
            "base": {"id": annual_hs, "qi": {annual_hs: 100.0}},
            "interaction_ids": [],
            "post": {"id": annual_hs, "qi": {annual_hs: 100.0}},
            "badges": [],
            "disabled": True
        }
        eb_qi = {qi_tuple[0]: float(qi_tuple[1]) for qi_tuple in EARTHLY_BRANCHES[annual_eb]["qi"]}
        response["eb_yl"] = {
            "id": annual_eb,
            "base": {"id": annual_eb, "qi": eb_qi},
            "interaction_ids": [],
            "post": {"id": annual_eb, "qi": eb_qi},
            "badges": [],
            "disabled": True
        }

    # Add misc field to 10-year luck nodes if they exist
    if luck_10y_info and "hs_10yl" in response and "eb_10yl" in response:
        response["hs_10yl"]["misc"] = luck_10y_info
        response["eb_10yl"]["misc"] = luck_10y_info

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

            dong_gong_data = {
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

            # Check Four Extinction (四絕) / Four Separation (四離)
            # analyze_bazi has a specific hour — check that exact moment
            analysis_hour_val = None
            if analysis_time:
                ah, am = extract_hour_minute(analysis_time)
                if ah is not None:
                    analysis_hour_val = ah + (am or 0) / 60

            forbidden = check_four_extinction_separation(
                analysis_year, analysis_month, analysis_day, analysis_hour_val
            )

            if forbidden:
                # Exact hour falls in forbidden window — override to dire
                dong_gong_data["forbidden"] = forbidden
                dong_gong_data["consult"] = None
                dong_gong_data["rating"] = {
                    "id": "dire",
                    "value": 1,
                    "symbol": "✗",
                    "chinese": forbidden["chinese"],  # 四絕 or 四離
                }
            else:
                dong_gong_data["forbidden"] = None
                # Consult promotion: inauspicious days with BOTH good_for AND positive description
                consult = check_consult_promotion(rating, day_info)
                if consult:
                    dong_gong_data["consult"] = {
                        "promoted": True,
                        "original_rating": dong_gong_data["rating"],
                        "reason": consult["reason"],
                    }
                    dong_gong_data["rating"] = {"id": "consult", "value": 2.5, "symbol": "?", "chinese": "議"}
                else:
                    dong_gong_data["consult"] = None

            response["dong_gong"] = dong_gong_data

    # Mappings are already set by adapt_to_frontend()

    response["school"] = school

    return response


# * =================
# * DONG GONG CALENDAR
# * =================

MOON_PHASES = [
    (1,  1,  "🌑", "New Moon",        "新月"),
    (2,  6,  "🌒", "Waxing Crescent", "蛾眉月"),
    (7,  8,  "🌓", "First Quarter",   "上弦月"),
    (9,  14, "🌔", "Waxing Gibbous",  "盈凸月"),
    (15, 15, "🌕", "Full Moon",        "满月"),
    (16, 21, "🌖", "Waning Gibbous",  "亏凸月"),
    (22, 23, "🌗", "Last Quarter",     "下弦月"),
    (24, 30, "🌘", "Waning Crescent", "残月"),
]

def get_moon_phase(lunar_day_num: int) -> dict:
    for start, end, emoji, english, chinese in MOON_PHASES:
        if start <= lunar_day_num <= end:
            return {"emoji": emoji, "english": english, "chinese": chinese, "lunar_day": lunar_day_num}
    return {"emoji": "🌑", "english": "New Moon", "chinese": "新月", "lunar_day": lunar_day_num}


@router.get("/dong_gong_calendar")
async def dong_gong_calendar(
    year: int = Query(..., description="Gregorian year"),
    month: int = Query(..., ge=1, le=12, description="Gregorian month (1-12)"),
) -> dict:
    """
    Return Dong Gong auspiciousness data for every day in a Gregorian month.
    Each day includes its day stem/branch, Chinese month, rating, officer,
    good_for/bad_for lists, and descriptions.
    """
    days_in_month = cal_module.monthrange(year, month)[1]
    first_day_weekday = cal_module.weekday(year, month, 1)  # 0=Mon, 6=Sun
    # Convert to Sunday=0 convention for calendar grid
    first_day_weekday_sun = (first_day_weekday + 1) % 7

    days = []
    chinese_months_seen = {}
    chinese_years_seen = {}

    for day in range(1, days_in_month + 1):
        lunar_day = sxtwl.fromSolar(year, month, day)

        # Year stem + branch (changes at Li Chun, not Jan 1)
        year_gz = lunar_day.getYearGZ()
        yr_stem = GAN_MAP[Gan[year_gz.tg]]
        yr_stem_chinese = Gan[year_gz.tg]
        yr_branch = ZHI_MAP[Zhi[year_gz.dz]]
        yr_branch_chinese = Zhi[year_gz.dz]

        # Track which Chinese years are spanned
        yr_key = f"{yr_stem}{yr_branch}"
        if yr_key not in chinese_years_seen:
            chinese_years_seen[yr_key] = {
                "stem": yr_stem,
                "stem_chinese": yr_stem_chinese,
                "branch": yr_branch,
                "branch_chinese": yr_branch_chinese,
            }

        # Day stem + branch
        day_gz = lunar_day.getDayGZ()
        day_stem = GAN_MAP[Gan[day_gz.tg]]
        day_branch = ZHI_MAP[Zhi[day_gz.dz]]

        # Day stem Chinese characters
        day_stem_chinese = Gan[day_gz.tg]
        day_branch_chinese = Zhi[day_gz.dz]

        # Month stem + branch (handles jieqi boundaries automatically)
        month_gz = lunar_day.getMonthGZ()
        month_stem = GAN_MAP[Gan[month_gz.tg]]
        month_stem_chinese = Gan[month_gz.tg]
        month_branch = ZHI_MAP[Zhi[month_gz.dz]]
        month_branch_chinese = Zhi[month_gz.dz]

        # Chinese month number from branch
        chinese_month = DONG_GONG_BRANCH_TO_MONTH.get(month_branch)

        # Track which Chinese months are spanned
        if chinese_month and chinese_month not in chinese_months_seen:
            month_info = DONG_GONG_MONTHS.get(chinese_month, {})
            chinese_months_seen[chinese_month] = {
                "month": chinese_month,
                "chinese": month_info.get("chinese", ""),
                "branch": month_info.get("branch", ""),
                "stem": month_stem,
                "stem_chinese": month_stem_chinese,
                "branch_id": month_branch,
                "branch_chinese": month_branch_chinese,
            }

        # Build day object
        day_obj = {
            "day": day,
            "weekday": (first_day_weekday_sun + day - 1) % 7,
            "day_stem": day_stem,
            "day_branch": day_branch,
            "day_stem_chinese": day_stem_chinese,
            "day_branch_chinese": day_branch_chinese,
            "pillar": f"{day_stem} {day_branch}",
            "year_stem": yr_stem,
            "year_branch": yr_branch,
            "year_stem_chinese": yr_stem_chinese,
            "year_branch_chinese": yr_branch_chinese,
            "chinese_month": chinese_month,
            "chinese_month_name": DONG_GONG_MONTHS.get(chinese_month, {}).get("chinese", "") if chinese_month else "",
            "moon_phase": get_moon_phase(lunar_day.getLunarDay()),
        }

        if chinese_month and month_branch:
            # Day officer
            day_officer = get_dong_gong_officer(month_branch, day_branch)
            officer_info = DONG_GONG_DAY_OFFICERS.get(day_officer, {})
            day_obj["officer"] = {
                "id": day_officer,
                "chinese": officer_info.get("chinese", ""),
                "english": officer_info.get("english", ""),
            }

            # Rating
            rating = get_dong_gong_rating(chinese_month, day_branch, day_stem)
            if rating:
                rating_info = DONG_GONG_RATINGS.get(rating, {})
                day_obj["rating"] = {
                    "id": rating,
                    "value": rating_info.get("value", 0),
                    "symbol": rating_info.get("symbol", ""),
                    "chinese": rating_info.get("chinese", ""),
                }
            else:
                day_obj["rating"] = None

            # Day info (good_for, bad_for, descriptions)
            day_info = get_dong_gong_day_info(chinese_month, day_branch)
            day_obj["good_for"] = day_info.get("good_for", []) if day_info else []
            day_obj["bad_for"] = day_info.get("bad_for", []) if day_info else []
            day_obj["description_chinese"] = day_info.get("description_chinese", "") if day_info else ""
            day_obj["description_english"] = day_info.get("description_english", "") if day_info else ""

            # Check Four Extinction (四絕) / Four Separation (四離)
            # No hour for calendar — returns the forbidden range for the whole day
            forbidden = check_four_extinction_separation(year, month, day)
            day_obj["forbidden"] = forbidden  # None if unaffected

            if forbidden:
                # Forbidden days never get promoted to consult
                day_obj["consult"] = None
            else:
                # Consult promotion: inauspicious days with BOTH good_for AND positive description
                consult = check_consult_promotion(rating, day_info)
                if consult:
                    day_obj["consult"] = {
                        "promoted": True,
                        "original_rating": day_obj["rating"],
                        "reason": consult["reason"],
                    }
                    day_obj["rating"] = {"id": "consult", "value": 2.5, "symbol": "?", "chinese": "議"}
                else:
                    day_obj["consult"] = None
        else:
            day_obj["officer"] = None
            day_obj["rating"] = None
            day_obj["good_for"] = []
            day_obj["bad_for"] = []
            day_obj["description_chinese"] = ""
            day_obj["description_english"] = ""
            day_obj["consult"] = None
            day_obj["forbidden"] = None

        days.append(day_obj)

    return {
        "year": year,
        "month": month,
        "first_day_weekday": first_day_weekday_sun,
        "days_in_month": days_in_month,
        "days": days,
        "chinese_months_spanned": list(chinese_months_seen.values()),
        "chinese_years_spanned": list(chinese_years_seen.values()),
    }


# * =================
# * PROFILE ENDPOINTS
# * =================

@router.on_event("startup")
async def startup():
    """Initialize database on startup."""
    init_db()


@router.post("/seed", status_code=201)
async def seed_database(db: Session = Depends(get_db)):
    """Seed the database with test profiles."""
    from models import Profile
    import uuid

    # Check if profiles already exist
    existing_count = db.query(Profile).count()
    if existing_count > 0:
        return {"message": f"Database already has {existing_count} profiles. Skipping seed."}

    # Test presets
    TEST_PRESETS = [
        {"date": "1969-07-04", "time": "18:20", "gender": "female", "name": "Test 1969-07-04"},
        {"date": "1992-07-06", "time": "09:30", "gender": "female", "name": "Test 1992-07-06"},
        {"date": "1995-04-19", "time": "17:30", "gender": "male", "name": "Test 1995-04-19"},
        {"date": "1985-06-23", "time": "13:30", "gender": "male", "name": "Test 1985-06-23"},
        {"date": "1988-02-02", "time": "13:30", "gender": "male", "name": "Test 1988-02-02"},
        {"date": "1986-11-29", "time": "13:30", "gender": "male", "name": "Test 1986-11-29"},
        {"date": "1995-08-14", "time": "11:30", "gender": "female", "name": "Test 1995-08-14"},
        {"date": "1995-07-18", "time": "16:30", "gender": "female", "name": "Test 1995-07-18"},
        {"date": "1992-09-18", "time": "09:30", "gender": "female", "name": "Test 1992-09-18"},
        {"date": "2002-04-17", "time": "08:20", "gender": "female", "name": "Test 2002-04-17"},
        {"date": "2019-09-18", "time": "05:00", "gender": "female", "name": "Test 2019-09-18"},
        {"date": "2021-08-09", "time": "21:00", "gender": "female", "name": "Test 2021-08-09"},
        {"date": "1985-03-20", "time": "23:00", "gender": "female", "name": "Test 1985-03-20"},
        {"date": "1995-02-10", "time": "10:10", "gender": "female", "name": "Test 1995-02-10"},
        {"date": "1946-08-12", "time": "07:00", "gender": "male", "name": "Suharsa"},
        {"date": "1962-11-03", "time": "11:45", "gender": "male", "name": "Malaysian - Mata Ikan"},
        {"date": "1954-02-09", "time": "09:30", "gender": "female", "name": "Test 1954-02-09"},
        {"date": "1949-12-19", "time": "08:00", "gender": "male", "name": "Test 1949-12-19"},
        {"date": "1955-10-18", "time": "20:00", "gender": "female", "name": "Test 1955-10-18"},
        {"date": "1992-12-25", "time": None, "gender": "female", "name": "Test 1992-12-25 (Unknown Hour)"},
        {"date": "1945-03-26", "time": "18:00", "gender": "male", "name": "Batubara (hutan, tanah, pulau)"},
        {"date": "1969-04-07", "time": "18:30", "gender": "female", "name": "Wu Chen Wealth Storage"},
    ]

    # Add test profiles
    for preset in TEST_PRESETS:
        profile = Profile(
            id=str(uuid.uuid4()),
            name=preset["name"],
            birth_date=preset["date"],
            birth_time=preset["time"],
            gender=preset["gender"],
        )
        db.add(profile)

    db.commit()
    return {"message": f"Successfully seeded {len(TEST_PRESETS)} profiles."}


@router.get("/profiles", response_model=List[ProfileResponse])
async def list_profiles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=10000),
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


# =============================================================================
# COMPREHENSIVE BAZI ANALYSIS (New Engine)
# =============================================================================

@router.get("/comprehensive_analysis")
async def comprehensive_analysis(
    gender: str = Query(..., description="male or female"),
    birth_year: int = Query(..., description="Gregorian birth year"),
    year_stem: str = Query(..., description="Year stem (Pinyin, e.g. Yi)"),
    year_branch: str = Query(..., description="Year branch (Pinyin, e.g. Chou)"),
    month_stem: str = Query(..., description="Month stem"),
    month_branch: str = Query(..., description="Month branch"),
    day_stem: str = Query(..., description="Day stem"),
    day_branch: str = Query(..., description="Day branch"),
    hour_stem: str = Query(..., description="Hour stem"),
    hour_branch: str = Query(..., description="Hour branch"),
    luck_pillar_stem: str = Query("", description="Current luck pillar stem (optional)"),
    luck_pillar_branch: str = Query("", description="Current luck pillar branch (optional)"),
):
    """
    Comprehensive BaZi analysis — pure Python, zero LLM, fully deterministic.
    Returns a complete markdown report covering all 11 sections.
    """
    from library.comprehensive import analyze

    try:
        report = analyze(
            gender=gender,
            birth_year=birth_year,
            year_stem=year_stem, year_branch=year_branch,
            month_stem=month_stem, month_branch=month_branch,
            day_stem=day_stem, day_branch=day_branch,
            hour_stem=hour_stem, hour_branch=hour_branch,
            luck_pillar_stem=luck_pillar_stem,
            luck_pillar_branch=luck_pillar_branch,
        )
        return {"status": "success", "report": report}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

