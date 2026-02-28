"""
Generate pillar data using sxtwl for comparison with TypeScript alternatives.
Outputs JSON to stdout.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

import sxtwl
import json
from library.derived import Gan, Zhi, GAN_MAP, ZHI_MAP

# Test dates covering various edge cases
TEST_CASES = [
    # (year, month, day, hour, minute, description)
    # Normal dates across different years
    (1990, 1, 15, 10, 30, "Normal date 1990"),
    (2000, 6, 15, 14, 0, "Normal date 2000"),
    (2024, 3, 20, 8, 45, "Normal date 2024"),
    (1985, 12, 25, 6, 0, "Christmas 1985"),
    (1976, 7, 4, 12, 0, "Midday 1976"),

    # Li Chun (Beginning of Spring) boundary - year pillar changes here
    (2024, 2, 4, 3, 0, "Before Li Chun 2024 (Feb 4 ~16:27)"),
    (2024, 2, 4, 17, 0, "After Li Chun 2024"),
    (2025, 2, 3, 10, 0, "Before Li Chun 2025 (Feb 3 ~22:10)"),
    (2025, 2, 3, 23, 0, "After Li Chun 2025 + day crossover"),
    (2026, 2, 4, 3, 0, "Before Li Chun 2026 (Feb 4 ~04:02)"),
    (2026, 2, 4, 5, 0, "After Li Chun 2026"),

    # 23:00 day boundary (Zi hour = next day)
    (1995, 8, 10, 23, 30, "Late night - day changes at 23:00"),
    (2000, 1, 1, 23, 0, "New Year midnight boundary"),
    (2010, 6, 15, 22, 59, "Just before day change"),
    (2010, 6, 15, 23, 0, "Exactly at day change"),

    # Various solar term boundaries
    (2024, 3, 5, 10, 0, "Near Jingzhe 2024 (Awakening of Insects)"),
    (2024, 4, 4, 15, 0, "Near Qingming 2024 (Clear and Bright)"),
    (2024, 5, 5, 8, 0, "Near Lixia 2024 (Start of Summer)"),
    (2024, 6, 21, 4, 0, "Near Xiazhi 2024 (Summer Solstice)"),
    (2024, 12, 21, 18, 0, "Near Dongzhi 2024 (Winter Solstice)"),

    # Early and late years
    (1950, 3, 15, 9, 0, "1950 date"),
    (1960, 11, 8, 16, 30, "1960 date"),
    (2030, 7, 20, 11, 0, "Future date 2030"),

    # No hour provided (hour pillar should be absent)
    (1988, 9, 22, None, None, "No birth time"),
    (2024, 1, 1, None, None, "New Year 2024 no time"),

    # Month boundary solar terms
    (2024, 1, 6, 5, 0, "Near Xiaohan 2024 (Minor Cold)"),
    (2024, 8, 7, 8, 0, "Near Liqiu 2024 (Start of Autumn)"),
    (2024, 11, 7, 6, 0, "Near Lidong 2024 (Start of Winter)"),
]


def get_pillars(year, month, day, hour, minute):
    lunar_day = sxtwl.fromSolar(year, month, day)

    # Year pillar
    year_gz = lunar_day.getYearGZ()
    year_stem = GAN_MAP[Gan[year_gz.tg]]
    year_branch = ZHI_MAP[Zhi[year_gz.dz]]

    # Month pillar (with solar term adjustment)
    month_gz = lunar_day.getMonthGZ()
    if lunar_day.hasJieQi() and hour is not None and minute is not None:
        jieqi_index = lunar_day.getJieQi()
        if jieqi_index % 2 == 1:
            jieqi_jd = lunar_day.getJieQiJD()
            jd_fraction = jieqi_jd % 1
            transition_hour = (jd_fraction * 24 + 12) % 24
            birth_hour = hour + minute / 60
            if birth_hour < transition_hour:
                prev_day = lunar_day.before(1)
                month_gz = prev_day.getMonthGZ()

    month_stem = GAN_MAP[Gan[month_gz.tg]]
    month_branch = ZHI_MAP[Zhi[month_gz.dz]]

    # Day pillar (23:00 boundary)
    day_gz = lunar_day.getDayGZ()
    if hour is not None and hour >= 23:
        next_day = lunar_day.after(1)
        day_gz = next_day.getDayGZ()

    day_stem = GAN_MAP[Gan[day_gz.tg]]
    day_branch = ZHI_MAP[Zhi[day_gz.dz]]

    result = {
        "year": f"{year_stem} {year_branch}",
        "month": f"{month_stem} {month_branch}",
        "day": f"{day_stem} {day_branch}",
    }

    # Hour pillar
    if hour is not None:
        hour_gz = lunar_day.getHourGZ(hour)
        hour_stem = GAN_MAP[Gan[hour_gz.tg]]
        hour_branch = ZHI_MAP[Zhi[hour_gz.dz]]
        result["hour"] = f"{hour_stem} {hour_branch}"

    return result


results = []
for year, month, day, hour, minute, desc in TEST_CASES:
    pillars = get_pillars(year, month, day, hour, minute)
    results.append({
        "date": f"{year}-{month:02d}-{day:02d}",
        "time": f"{hour:02d}:{minute:02d}" if hour is not None else None,
        "desc": desc,
        "pillars": pillars,
    })

print(json.dumps(results, indent=2))
