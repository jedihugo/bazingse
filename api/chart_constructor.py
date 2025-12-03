
import sxtwl
import math
from datetime import date, timedelta
from typing import Literal, List, Dict, Optional
from library import Gan, Zhi, GAN_MAP, ZHI_MAP

# * =================
# * CHART CONSTRUCTORS (calculator.py)
# * =================

def get_ten_god_value(ten_god_info):
    """Helper function to extract ten god value from either string or dictionary format"""
    if isinstance(ten_god_info, dict):
        return ten_god_info.get("abbreviation", ten_god_info.get("id", ""))
    return ten_god_info

def generate_luck_pillars(
    year_pillar: str,
    month_pillar: str,
    gender: Literal["male", "female"],
    dob: date,
) -> List[Dict]:
    """
    Generate 8 luck pillars for a BaZi chart.
    
    Args:
        year_pillar: Year pillar in format "HS EB" (e.g., "Jia Zi")
        month_pillar: Month pillar in format "HS EB" (e.g., "Bing Yin")
        gender: "male" or "female"
        dob: Date of birth
        
    Returns:
        List of 8 luck pillars with start ages
    """
    # Get the 60 pillars cycle (Jia Zi cycle)
    heavenly_stems = ["Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin", "Ren", "Gui"]
    earthly_branches = ["Zi", "Chou", "Yin", "Mao", "Chen", "Si", "Wu", "Wei", "Shen", "You", "Xu", "Hai"]
    
    sixty_pillars = []
    for i in range(60):
        hs_index = i % 10
        eb_index = i % 12
        sixty_pillars.append(f"{heavenly_stems[hs_index]} {earthly_branches[eb_index]}")
    
    # Find the index of the month pillar in the 60-pillar cycle
    month_index = sixty_pillars.index(month_pillar)
    
    # Determine if the year is Yang or Yin based on the Heavenly Stem
    year_hs = year_pillar.split(" ")[0]
    is_yang_year = year_hs in ["Jia", "Bing", "Wu", "Geng", "Ren"]
    
    # Determine direction (forward or reverse)
    forward = (gender == "male") == is_yang_year

    # Parse date of birth
    year, month, day = dob.year, dob.month, dob.day

    # Get sxtwl day object
    day_obj = sxtwl.fromSolar(year, month, day)

    def find_previous_and_next_major_jit(input_date: date):
        """
        Given a Gregorian date, finds the previous and next major "Jit" (Jieqi)
        and calculates the date difference to each.

        Args:
            input_date: A datetime.date object representing the Gregorian date.

        Returns:
            A dictionary containing the previous major Jit date, the next major Jit date,
            the number of days to the next Jit, and the number of days from the prior Jit.
        """
        # Initialize the sxtwl day object from the Gregorian date
        day_obj = sxtwl.fromSolar(input_date.year, input_date.month, input_date.day)

        # Find the next major Jit
        next_jit_day = day_obj
        while True:
            next_jit_day = next_jit_day.after(1)
            # A day has a Jieqi AND its index is odd (major Jit)
            if next_jit_day.hasJieQi() and next_jit_day.getJieQi() % 2 != 0:
                break
        
        next_jit_date = date(
            next_jit_day.getSolarYear(),
            next_jit_day.getSolarMonth(),
            next_jit_day.getSolarDay()
        )
        
        # Find the previous major Jit
        prev_jit_day = day_obj
        while True:
            prev_jit_day = prev_jit_day.before(1)
            # A day has a Jieqi AND its index is odd (major Jit)
            if prev_jit_day.hasJieQi() and prev_jit_day.getJieQi() % 2 != 0:
                break

        prev_jit_date = date(
            prev_jit_day.getSolarYear(),
            prev_jit_day.getSolarMonth(),
            prev_jit_day.getSolarDay()
        )

        # Calculate the date differences
        diff_to_next = (next_jit_date - input_date).days
        diff_from_prev = (input_date - prev_jit_date).days

        result = {
            "Previous Major Jit": prev_jit_date,
            "Next Major Jit": next_jit_date,
            "Days to Next Jit": diff_to_next,
            "Days from Prior Jit": diff_from_prev
        }

        return result

    if forward:
        days_diff = find_previous_and_next_major_jit(dob)["Days to Next Jit"] 
    else:
        days_diff = find_previous_and_next_major_jit(dob)["Days from Prior Jit"]

    start_age = math.ceil(days_diff / 3.0)


    # Generate the 8 luck pillars
    result = []
    for i in range(8):
        if forward:
            luck_index = (month_index + i + 1) % 60
        else:
            luck_index = (month_index - i - 1) % 60
        
        luck_pillar = sixty_pillars[luck_index]
        
        result.append({
            "pillar": luck_pillar,
            "start_age": start_age + (i * 10),
            "end_age": start_age + ((i + 1) * 10) - 1
        })
    
    return result


def generate_bazi_chart(year: int, month: int, day: int, hour: Optional[int] = None, minute: Optional[int] = None) -> Dict:
    """
    Generate a BaZi chart for a given date and time.
    
    Args:
        year: Year of birth
        month: Month of birth (1-12)
        day: Day of birth
        hour: Hour of birth (0-23), optional
        minute: Minute of birth (0-59), optional
        
    Returns:
        Dictionary containing the four pillars
    """
    
    # Get the lunar date using sxtwl
    lunar_day = sxtwl.fromSolar(year, month, day)
    
    # Year Pillar
    year_gz = lunar_day.getYearGZ()
    year_pillar = GAN_MAP[Gan[year_gz.tg]] + " " + ZHI_MAP[Zhi[year_gz.dz]]

    # Month Pillar - Need to check if we're before or after a solar term transition
    month_gz = lunar_day.getMonthGZ()
    
    # Check if today has a solar term transition and we have time information
    if lunar_day.hasJieQi() and hour is not None and minute is not None:
        # Get the solar term index (odd numbers are major terms that change the month)
        jieqi_index = lunar_day.getJieQi()
        
        # Only major solar terms (odd indices) change the month pillar
        if jieqi_index % 2 == 1:
            # Get the exact transition time in Julian Date
            jieqi_jd = lunar_day.getJieQiJD()
            jd_fraction = jieqi_jd % 1
            
            # The sxtwl library appears to return JD already localized for Beijing
            # Standard conversion: Beijing hour = (JD_fraction * 24 + 12) % 24
            # This gives us apparent solar time at Beijing meridian
            
            # Calculate apparent solar time
            apparent_solar_hour = (jd_fraction * 24 + 12) % 24
            
            # Based on empirical testing with authoritative sources,
            # a uniform correction of approximately 6.3 minutes works well
            # This likely accounts for the combined effect of:
            # - Ephemeris differences
            # - Coordinate system conversions
            # - Time standard differences
            
            UNIVERSAL_CORRECTION = 0.105  # 6.3 minutes in hours (best fit for known solar terms)
            
            transition_hour_beijing = (apparent_solar_hour - UNIVERSAL_CORRECTION) % 24
            
            # Get the birth time in hours
            birth_hour = hour + minute/60
            
            # If birth is before the transition, use previous month's pillar
            if birth_hour < transition_hour_beijing:
                # Get previous day's month pillar (which is the previous month)
                prev_day = lunar_day.before(1)
                month_gz = prev_day.getMonthGZ()
                print(f"Birth at {hour:02d}:{minute:02d} is before solar term at {int(transition_hour_beijing):02d}:{int((transition_hour_beijing % 1) * 60):02d}, using previous month pillar")
    
    month_pillar = GAN_MAP[Gan[month_gz.tg]] + " " + ZHI_MAP[Zhi[month_gz.dz]]

    # Day Pillar
    # In BaZi, the day changes at 23:00 (11 PM), not midnight
    day_gz = lunar_day.getDayGZ()
    
    # If birth time is 23:00 or later, use next day's pillar
    if hour is not None and hour >= 23:
        next_day = lunar_day.after(1)
        day_gz = next_day.getDayGZ()
        min_str = f"{minute:02d}" if minute is not None else "00"
        print(f"Birth at {hour:02d}:{min_str} uses next day's pillar (day changes at 23:00)")
    
    day_pillar = GAN_MAP[Gan[day_gz.tg]] + " " + ZHI_MAP[Zhi[day_gz.dz]]

    print("Year Pillar:", year_pillar)
    print("Month Pillar:", month_pillar)
    print("Day Pillar:", day_pillar)
    
    result = {
        "year_pillar": year_pillar,
        "month_pillar": month_pillar,
        "day_pillar": day_pillar,
    }
    
    # Hour Pillar (only if hour is provided)
    if hour is not None:
        hour_gz = lunar_day.getHourGZ(hour)
        hour_pillar = GAN_MAP[Gan[hour_gz.tg]] + " " + ZHI_MAP[Zhi[hour_gz.dz]]
        print("Hour Pillar:", hour_pillar)
        result["hour_pillar"] = hour_pillar

    return result
