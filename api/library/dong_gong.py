# * =========================
# * DONG GONG DATE SELECTION (董公择日)
# * =========================
# Traditional Chinese date selection reference
# Structure: DONG_GONG[month][day_branch] -> day info with pillar ratings
#
# NOTE: Day Officers (十二建除) are derived from STEMS/BRANCHES in derived.py
# BRANCHES is the single source of truth in core.py

from .core import BRANCHES
from .derived import (
    DAY_OFFICERS,
    DAY_OFFICER_ORDER,
    get_day_officer,
)

# Rating scale for day auspiciousness
DONG_GONG_RATINGS = {
    "excellent": {"value": 5, "symbol": "★", "chinese": "大吉"},
    "auspicious": {"value": 4, "symbol": "✓", "chinese": "吉"},
    "fair": {"value": 3, "symbol": "●", "chinese": "平"},
    "inauspicious": {"value": 2, "symbol": "▲", "chinese": "凶"},
    "dire": {"value": 1, "symbol": "✗", "chinese": "大凶"}
}

# =============================================================================
# BACKWARD COMPATIBILITY ALIASES (now derived from core.py)
# =============================================================================
# These are kept for backward compatibility but now reference core.py

# Day Officers - reference from core
DONG_GONG_DAY_OFFICERS = {
    DAY_OFFICERS[i]["id"]: {"order": i, "chinese": DAY_OFFICERS[i]["chinese"], "english": DAY_OFFICERS[i]["english"]}
    for i in range(12)
}

# Officer order - reference from core
DONG_GONG_OFFICER_ORDER = DAY_OFFICER_ORDER

# Branch order for Dong Gong (starting from Yin = month 1)
DONG_GONG_BRANCH_ORDER = sorted(BRANCHES.keys(), key=lambda b: BRANCHES[b]["dong_gong_index"])

# Month mappings - derived from branches
DONG_GONG_MONTHS = {
    BRANCHES[b]["month"]: {"branch": b, "chinese": f"{'正' if BRANCHES[b]['month'] == 1 else ['一','二','三','四','五','六','七','八','九','十','十一','十二'][BRANCHES[b]['month']-1]}月", "english": f"Month {BRANCHES[b]['month']}"}
    for b in BRANCHES
}

DONG_GONG_BRANCH_TO_MONTH = {b: BRANCHES[b]["month"] for b in BRANCHES}


def get_dong_gong_officer(month_branch: str, day_branch: str) -> str:
    """
    Calculate the Day Officer for a given month and day branch.
    Now uses core.py's get_day_officer function.
    """
    officer = get_day_officer(month_branch, day_branch)
    return officer["id"] if officer else None

# Main Dong Gong reference dictionary
# Key: month number (1-12)
# Value: dict of day branches with their ratings and descriptions
DONG_GONG = {
    # ========================================
    # MONTH 1 - Tiger Month (正月 / 寅月)
    # ========================================
    1: {
        "Yin": {
            "officer": "Jian",
            "pillars": {
                "Jia-Yin": "inauspicious",
                "Bing-Yin": "inauspicious",
                "Wu-Yin": "inauspicious",
                "Geng-Yin": "inauspicious",
                "Ren-Yin": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["construction", "marriage", "contracts", "important_activities"],
            "description_chinese": "往亡日。不利起造、結婚姻、納采，主家長病、招官司犯之主六十日、一百二十日內損小口，一年內見重喪，百事不宜。",
            "description_english": "Emptiness Day (往亡日). Not ideal for construction, marriage, or contracts. Those who use this day will face illness in elders, lawsuits. Within 60-120 days children may be harmed. Within a year, there may be double mourning. All activities should be avoided.",
        },
        "Mao": {
            "officer": "Chu",
            "pillars": {
                "Yi-Mao": "inauspicious",
                "Ding-Mao": "inauspicious",
                "Ji-Mao": "inauspicious",
                "Xin-Mao": "inauspicious",
                "Gui-Mao": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["renovation", "marriage", "construction"],
            "description_chinese": "不宜起造、婚姻，犯之主六十日內損家長、招官司。三五年內見凶冷退，主兄弟不義、各業分散、惡人相逢、生離死別。",
            "description_english": "Not suitable for renovation or marriage. Those who use it will see harm to elders and lawsuits within 60 days. Within 3-5 years there will be misfortune and decline, brothers will be disloyal, businesses scatter, meeting with evil people, and separation in life or death.",
        },
        "Chen": {
            "officer": "Man",
            "pillars": {
                "Jia-Chen": "dire",
                "Bing-Chen": "inauspicious",
                "Wu-Chen": "dire",
                "Geng-Chen": "inauspicious",
                "Ren-Chen": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["most_activities", "construction", "marriage", "business"],
            "description_chinese": "天富、天賊、天羅星臨。甲辰雖有氣，與戊辰同，熬集中宮，百事皆忌，犯之主殺人、退財，大凶。餘辰日亦不吉。",
            "description_english": "Heavenly Fortune, Heavenly Thief, and Heavenly Spiral stars arrive. Jia Chen and Wu Chen have negative Qi concentrated in Central Palace - all activities forbidden. Those who violate this may face killing, loss of wealth - greatly inauspicious. Other Chen days are also unfavorable.",
        },
        "Si": {
            "officer": "Ping",
            "pillars": {
                "Yi-Si": "inauspicious",
                "Ding-Si": "inauspicious",
                "Ji-Si": "inauspicious",
                "Xin-Si": "inauspicious",
                "Gui-Si": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["marriage", "business", "legal_matters"],
            "description_chinese": "小紅砂，朱雀、勾絞、到州星臨，犯之主招官司、損家長、宅女媳婦。三、五年內重重不利、破財，大凶。田蠶不收、産死、自縊、被惡人處刑。",
            "description_english": "Lesser Red Embrace, Red Phoenix, Grappling Hook, and Arriving States stars. Those who use this day face lawsuits, harm to elders, damage to women of the household. Within 3-5 years there will be repeated misfortune, loss of wealth - greatly inauspicious. Farms will not produce, stillbirths, suicides, and punishment by evil people.",
        },
        "Wu": {
            "officer": "Ding",
            "pillars": {
                "Jia-Wu": "auspicious",
                "Bing-Wu": "excellent",
                "Wu-Wu": "auspicious",
                "Geng-Wu": "auspicious",
                "Ren-Wu": "auspicious",
            },
            "good_for": ["renovation", "burial", "moving", "business", "travel", "marriage"],
            "bad_for": [],
            "description_chinese": "黃砂日，有黃羅、紫檀、天皇、地皇、金銀庫樓、田塘、月財庫、貯星，諸吉星蓋照，宜起造、安葬、移徙、開張、出行、婚姻，主六十日、一百二十日內進橫財、田產，或因附寄成家，大作大發、小作小發，主田蠶大收穫，金銀滿庫。",
            "description_english": "Yellow Embrace Day with Yellow Spiral, Purple Sandalwood, Heavenly Emperor, Earthly Emperor, Gold & Silver Treasury, Field Pond, Monthly Fortune Treasury, Storage stars - all auspicious stars shine upon it. Suitable for construction, burial, moving, opening business, travel, marriage. Within 60-120 days will gain unexpected wealth and property. Great undertakings bring great prosperity, small undertakings bring small prosperity. Fields and silkworms yield great harvest, gold and silver fill the treasury.",
        },
        "Wei": {
            "officer": "Zhi",
            "pillars": {
                "Yi-Wei": "dire",
                "Ding-Wei": "inauspicious",
                "Ji-Wei": "inauspicious",
                "Xin-Wei": "inauspicious",
                "Gui-Wei": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["moving", "marriage", "business", "construction"],
            "description_chinese": "天賊、朱雀、勾絞星臨。六十日、一百二十日內損六畜、傷騾馬、成惡疾。乙未熬入中宮，更忌起造、婚姻、開張、築策亭事。",
            "description_english": "Heavenly Thief, Red Phoenix, and Grappling Hook stars arrive. Within 60-120 days will harm livestock, injure mules and horses, contract terrible illness. Yi Wei has negative Qi in Central Palace - especially avoid construction, marriage, opening business, building pavilions.",
        },
        "Shen": {
            "officer": "Po",
            "pillars": {
                "Jia-Shen": "inauspicious",
                "Bing-Shen": "inauspicious",
                "Wu-Shen": "inauspicious",
                "Geng-Shen": "dire",
                "Ren-Shen": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["legal_matters", "business", "marriage", "important_activities"],
            "description_chinese": "遇朱雀、勾絞星，主招官司、口舌、退牲財，三、五年內見寡婦、醜事。庚申正四廢，更凶。",
            "description_english": "Encounters Red Phoenix and Grappling Hook stars, causing lawsuits, disputes, loss of livestock and wealth. Within 3-5 years will see widows and scandals. Geng Shen is Four Abandonment Day - even more inauspicious.",
        },
        "You": {
            "officer": "Wei",
            "pillars": {
                "Yi-You": "inauspicious",
                "Ding-You": "auspicious",
                "Ji-You": "inauspicious",
                "Xin-You": "dire",
                "Gui-You": "inauspicious",
            },
            "good_for": ["burial", "travel", "debt_collection", "meeting_officials"],
            "bad_for": ["construction", "marriage"],
            "description_chinese": "辛酉正四廢，不宜用事。惟丁酉有天德福星蓋照，宜安葬、出行、開張、星蓋吉。只不宜起造、婚姻、嫁娶等事，乃比和之日也。餘酉日均不可用。",
            "description_english": "Xin You is Four Abandonment Day - unsuitable for activities. Only Ding You has Heavenly Virtue and Prosperity stars shining upon it, suitable for burial, travel, opening business - the stars are auspicious. Just not suitable for construction, marriage, or wedding matters - this is a Harmonizing Day. Other You days cannot be used.",
        },
        "Xu": {
            "officer": "Cheng",
            "pillars": {
                "Jia-Xu": "dire",
                "Bing-Xu": "inauspicious",
                "Wu-Xu": "dire",
                "Geng-Xu": "inauspicious",
                "Ren-Xu": "dire",
            },
            "good_for": [],
            "bad_for": ["construction", "marriage", "moving", "important_activities"],
            "description_chinese": "天喜、地網星同臨，不宜犯之。主家長病、人口不義、冷退。丙戌、戊戌、庚戌、壬戌，熬集中宮，犯之主首殺人、兄弟不義、死別生離，尤忌起造、婚姻、入宅、修作。",
            "description_english": "Sky Happiness and Earthly Net stars arrive together - should not be violated. Causes elders' illness, disloyal people, decline and withdrawal. Bing Xu, Wu Xu, Geng Xu, Ren Xu have negative Qi concentrated in Central Palace - those who violate face leading to killing, disloyal brothers, separation in death or life. Especially avoid construction, marriage, moving in, renovation.",
        },
        "Hai": {
            "officer": "Shou",
            "pillars": {
                "Yi-Hai": "inauspicious",
                "Ding-Hai": "inauspicious",
                "Ji-Hai": "inauspicious",
                "Xin-Hai": "inauspicious",
                "Gui-Hai": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["important_activities", "construction", "marriage"],
            "description_chinese": "有勾絞不宜用事。犯之損家長、害子孫。六十日、一百二十日內主南方白衣刑剋、男女多災，大凶。惟平日地支與月建陰陽合德者次吉。",
            "description_english": "Has Grappling Hook star - not suitable for activities. Those who violate will harm elders and grandchildren. Within 60-120 days there will be punishment from white-clothed people from the south, many disasters for men and women - greatly inauspicious. Only days where earthly branch has Yin-Yang harmonious virtue with monthly establishment are secondarily auspicious.",
        },
        "Zi": {
            "officer": "Kai",
            "pillars": {
                "Jia-Zi": "inauspicious",
                "Bing-Zi": "auspicious",
                "Wu-Zi": "auspicious",
                "Geng-Zi": "auspicious",
                "Ren-Zi": "inauspicious",
            },
            "good_for": ["burial", "travel", "business"],
            "bad_for": ["construction", "marriage", "moving"],
            "description_chinese": "甲子自死之金，五行陰忌之日。壬子木打寶瓶，終是北方沐浴之地，不宜起造、婚姻、入宅、開張等事。戊子、丙子、庚子三日，水土生人用之大吉。內有黃羅、紫檀、天皇、地皇、金銀寶藏、財庫貯、聯珠眾星蓋照，主六十日、一百二十日內得大財、貴人接引、職祿、謀事大吉，旺六畜、益財產、亦宜安葬。",
            "description_english": "Jia Zi is Self-Death Metal, Five Element Yin Avoidance Day. Ren Zi wood strikes treasure vase, ultimately is northern bathing place - not suitable for construction, marriage, moving in, opening business. Wu Zi, Bing Zi, Geng Zi - these three days are greatly auspicious for Water and Earth element people. Contains Yellow Spiral, Purple Sandalwood, Heavenly Emperor, Earthly Emperor, Gold & Silver Treasure, Fortune Treasury Storage, Pearl Chain stars all shining. Within 60-120 days will gain great wealth, noble people will guide, official positions, great fortune in planning. Thriving livestock, increasing property, also suitable for burial.",
        },
        "Chou": {
            "officer": "Bi",
            "pillars": {
                "Yi-Chou": "inauspicious",
                "Ding-Chou": "inauspicious",
                "Ji-Chou": "inauspicious",
                "Xin-Chou": "inauspicious",
                "Gui-Chou": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["marriage", "construction", "buying_livestock"],
            "description_chinese": "不利婚姻、起造，防虎蛇傷、騾馬踢、戒惡疾貧病，大凶。",
            "description_english": "Not favorable for marriage or construction. Beware of injury from tigers and snakes, kicks from mules and horses, avoid terrible illness and poverty - greatly inauspicious.",
        },
    },

    # ========================================
    # MONTH 2 - Rabbit Month (二月 / 卯月)
    # ========================================
    2: {},  # TODO: Waiting for correct reference data

    # ========================================
    # MONTH 3 - Dragon Month (三月 / 辰月)
    # ========================================
    3: {},  # TODO: Waiting for correct reference data

    # ========================================
    # MONTH 4 - Snake Month (四月 / 巳月)
    # ========================================
    4: {
        "Si": {
            "officer": "Jian",
            "pillars": {
                "Yi-Si": "inauspicious",
                "Ding-Si": "inauspicious",
                "Ji-Si": "inauspicious",
                "Xin-Si": "inauspicious",
                "Gui-Si": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["travel", "marriage", "burial", "renovation", "moving", "business"],
            "description_chinese": "小紅砂日。不利出行、嫁娶、安葬、造作、入宅、開張等事。犯之主冷退、疾病、田蠶不收、客死不歸、財產破散，受死之日也。",
            "description_english": "Lesser Red Embrace Star Day. Unsuitable for travel, marriage, burial, renovation, moving or business. Violating causes illness, property loss, fatal accidents overseas, or bankruptcy.",
        },
        "Wu": {
            "officer": "Chu",
            "pillars": {
                "Jia-Wu": "excellent",
                "Bing-Wu": "inauspicious",
                "Wu-Wu": "inauspicious",
                "Geng-Wu": "excellent",
                "Ren-Wu": "excellent",
            },
            "good_for": ["renovation", "marriage", "business", "travel", "moving", "education"],
            "bad_for": [],
            "description_chinese": "黃砂。庚午月德，惟甲午、壬午，有黃羅、紫檀、天皇、地皇星蓋照，宜修造、婚姻、開張、出行、入宅等事。六十日、一百二十日內增田地、進人口、生貴子，大旺。丙午、戊午，天地轉煞，用之凶。",
            "description_english": "Yellow Embrace Star. Jia Wu, Geng Wu (Monthly Virtue), Ren Wu excellent with auspicious stars. Good for renovation, marriage, business, travel, moving. Benefits within 60-120 days. Bing Wu and Wu Wu have Heaven/Earth Drilling Sha - avoid.",
        },
        "Wei": {
            "officer": "Man",
            "pillars": {
                "Yi-Wei": "inauspicious",
                "Ding-Wei": "inauspicious",
                "Ji-Wei": "auspicious",
                "Xin-Wei": "auspicious",
                "Gui-Wei": "inauspicious",
            },
            "good_for": ["fixing_structures", "burial"],
            "bad_for": ["marriage", "construction"],
            "description_chinese": "天富、天賊。辛未有天、月二德，己未有火星，均次吉，宜定礎、造架、埋葬，但婚姻、起造二事不載又修造，曆云是日白虎入中宮，用之非不利，須查是年月日，如有吉星與命宮相合方可。",
            "description_english": "Sky Pledge and Sky Thief stars. Xin Wei has Heavenly/Monthly Virtue. Ji Wei has Fire Star - both secondarily auspicious. Good for fixing structures or burial. Unsuitable for marriage and construction. Other Wei days have White Tiger.",
        },
        "Shen": {
            "officer": "Ping",
            "pillars": {
                "Jia-Shen": "dire",
                "Bing-Shen": "inauspicious",
                "Wu-Shen": "inauspicious",
                "Geng-Shen": "dire",
                "Ren-Shen": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["renovation", "travel", "burial", "marriage", "moving"],
            "description_chinese": "朱雀、勾絞星臨，不利起造、出行、安葬、婚姻、入宅，主招官司、口舌、小口生災。甲申、庚申，熬入中宮，更凶，必主小人牽連、禍事、破財、生子醜怪、有水火災厄。",
            "description_english": "Red Phoenix and Grappling Hook stars. Unsuitable for renovation, travel, burial, marriage, moving. Causes legal issues, disputes, harm to children. Jia Shen and Geng Shen worst - petty people, accidents, wealth loss, birth defects, fire/water hazards.",
        },
        "You": {
            "officer": "Ding",
            "pillars": {
                "Yi-You": "inauspicious",
                "Ding-You": "inauspicious",
                "Ji-You": "inauspicious",
                "Xin-You": "inauspicious",
                "Gui-You": "inauspicious",
            },
            "good_for": ["minor_activities"],
            "bad_for": ["groundbreaking", "burial", "marriage", "moving", "renovation"],
            "description_chinese": "雖有九土鬼，不宜動土、安葬，若小小營為在四月，酉為次吉之日。如婚姻、入宅、修造，斷不可用，主凶。",
            "description_english": "Nine Earth Ghost Star dominates. Unsuitable for groundbreaking or burial. Minor activities may reap minor gains. Not for major activities like marriage, moving, or renovation.",
        },
        "Xu": {
            "officer": "Zhi",
            "pillars": {
                "Jia-Xu": "fair",
                "Bing-Xu": "dire",
                "Wu-Xu": "inauspicious",
                "Geng-Xu": "inauspicious",
                "Ren-Xu": "dire",
            },
            "good_for": ["minor_activities"],
            "bad_for": ["renovation", "marriage", "burial", "moving", "business"],
            "description_chinese": "有勾絞，丙戌、壬戌，熬入中宮，百事大凶。甲戌，小小營為次吉。二十四向諸煞朝天，偷修則可，婚姻、安葬、入宅、開張，非所宜，用之主損宅長、傷手足、耗錢財，大凶。",
            "description_english": "Grappling Hook present. Bing Xu and Ren Xu worst with Sha Qi. Jia Xu fair for minor activities. Sha Qi in all 24 directions. Avoid renovation, marriage, burial, moving, business. Causes injury to elders/limbs, wealth loss.",
        },
        "Hai": {
            "officer": "Po",
            "pillars": {
                "Yi-Hai": "inauspicious",
                "Ding-Hai": "inauspicious",
                "Ji-Hai": "inauspicious",
                "Xin-Hai": "inauspicious",
                "Gui-Hai": "dire",
            },
            "good_for": [],
            "bad_for": ["all_activities"],
            "description_chinese": "往亡，朱雀、勾絞，招官司、小人啾唧之災，主損錢財、染疾病。癸亥正四廢，更凶，是月亥日諸事忌之。",
            "description_english": "Emptiness Day with Red Phoenix and Grappling Hook. Attracts petty people and legal problems. Causes wealth loss and illness. Gui Hai is Direct Abandonment Day - worst. Avoid all activities on Hai days this month.",
        },
        "Zi": {
            "officer": "Wei",
            "pillars": {
                "Jia-Zi": "inauspicious",
                "Bing-Zi": "auspicious",
                "Wu-Zi": "auspicious",
                "Geng-Zi": "excellent",
                "Ren-Zi": "inauspicious",
            },
            "good_for": ["renovation", "marriage", "groundbreaking", "travel", "business", "moving"],
            "bad_for": [],
            "description_chinese": "庚子月德，丙子、戊子，起造、婚姻、興工、動土、出行、開張、移徙，進人口、益子孫、旺田土、增財產、大作小發。甲子是自死之金，五行無氣，又是四正廢，用之損人口，主冷退。壬子木打寶瓶，北方沐浴之地，福力甚薄。",
            "description_english": "Geng Zi has Monthly Virtue - excellent. Bing Zi and Wu Zi good for renovation, marriage, groundbreaking, travel, business, moving - brings family expansion, wealth increase. Jia Zi and Ren Zi are Four Direct Abandonment Days - weak Qi, causes injuries and deteriorating fortunes.",
        },
        "Chou": {
            "officer": "Cheng",
            "pillars": {
                "Yi-Chou": "inauspicious",
                "Ding-Chou": "dire",
                "Ji-Chou": "inauspicious",
                "Xin-Chou": "inauspicious",
                "Gui-Chou": "dire",
            },
            "good_for": [],
            "bad_for": ["all_activities"],
            "description_chinese": "天喜、天成，欲犯朱雀、勾絞，用之招官司、口舌、小人、肆誕妄毀。丁丑、癸丑，熬入宮，更凶，此數日犯空亡、破財、小人陷害。",
            "description_english": "Despite Sky Happiness and Heavenly Success, Red Phoenix and Grappling Hook negate benefits. Causes legal issues, disputes, petty people interference. Ding Chou and Gui Chou worst - Death and Emptiness rule, wealth loss, sabotage.",
        },
        "Yin": {
            "officer": "Shou",
            "pillars": {
                "Jia-Yin": "inauspicious",
                "Bing-Yin": "inauspicious",
                "Wu-Yin": "inauspicious",
                "Geng-Yin": "inauspicious",
                "Ren-Yin": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["all_activities"],
            "description_chinese": "與戊丑日同，亦不吉。",
            "description_english": "Effects identical to Chou days - inauspicious for all activities.",
        },
        "Mao": {
            "officer": "Kai",
            "pillars": {
                "Yi-Mao": "auspicious",
                "Ding-Mao": "auspicious",
                "Ji-Mao": "excellent",
                "Xin-Mao": "excellent",
                "Gui-Mao": "excellent",
            },
            "good_for": ["travel", "marriage", "renovation", "business", "moving"],
            "bad_for": [],
            "description_chinese": "辛卯天德，癸卯、己卯，有黃羅、紫檀、天皇、地皇星蓋照，出行、婚葬、造作、開張、入宅等事，大吉。主謀事亨通、貴人接引、進財祿。餘卯次吉。",
            "description_english": "Xin Mao has Heavenly Virtue. Gui Mao and Ji Mao have Yellow Spiral, Purple Sandalwood, Heavenly/Earthly Emperor stars - excellent. Good for travel, marriage, renovation, business, moving. Brings success, noble people help, wealth increase. Other Mao days also favorable.",
        },
        "Chen": {
            "officer": "Bi",
            "pillars": {
                "Jia-Chen": "dire",
                "Bing-Chen": "fair",
                "Wu-Chen": "dire",
                "Geng-Chen": "fair",
                "Ren-Chen": "fair",
            },
            "good_for": ["minor_activities"],
            "bad_for": ["marriage", "renovation", "business", "moving", "burial"],
            "description_chinese": "戊辰、甲辰，熬入中宮，不利婚姻、修造、開張、入宅、安葬，犯之財產有失、損人口、六畜不旺。庚辰雖值月德，卻有天地轉煞之疑。丙辰、壬辰火星，小小營為則可，不宜婚姻、起造、移徙、開張大用也。",
            "description_english": "Jia Chen and Wu Chen have negative stars - unsuitable for marriage, renovation, business, moving, burial. Causes property loss, harm to children, sick animals. Geng Chen has Monthly Virtue but Heaven/Earth Turning Sha. Bing Chen and Ren Chen have Fire Star - fair for minor activities only.",
        },
    },

    # ========================================
    # MONTH 5 - Horse Month (五月 / 午月)
    # ========================================
    5: {
        "Wu": {
            "officer": "Jian",
            "pillars": {
                "Jia-Wu": "auspicious",
                "Bing-Wu": "inauspicious",
                "Wu-Wu": "inauspicious",
                "Geng-Wu": "inauspicious",
                "Ren-Wu": "inauspicious",
            },
            "good_for": ["burial"],
            "bad_for": ["most_activities"],
            "description_chinese": "甲午天赦，雖是轉煞，埋葬用之次吉。餘午日埋葬亦不利。若別事用，主招官司、口舌、孤寡、窮病，蓋五月逢午，皆係天地轉煞也。",
            "description_english": "All Wu (Horse) days affected by Heaven and Earth Drilling Sha. Only Jia Wu has Heavenly Pardon - slightly favorable for burial. Other Wu days cause legal problems, gossip, loneliness, sickness.",
        },
        "Wei": {
            "officer": "Chu",
            "pillars": {
                "Yi-Wei": "dire",
                "Ding-Wei": "fair",
                "Ji-Wei": "fair",
                "Xin-Wei": "fair",
                "Gui-Wei": "fair",
            },
            "good_for": ["minor_activities"],
            "bad_for": ["marriage", "business", "moving", "renovation"],
            "description_chinese": "惟乙未最為不利，如嫁親、開張、入宅、修造，主迸人口、生疾病、損財。其餘未日，小作可用，乃次吉之日也。",
            "description_english": "Yi Wei is dire - unsuitable for marriage, business, moving, renovation. Causes illness and wealth loss. Other Wei days are fair and moderately usable.",
        },
        "Shen": {
            "officer": "Man",
            "pillars": {
                "Jia-Shen": "auspicious",
                "Bing-Shen": "auspicious",
                "Wu-Shen": "auspicious",
                "Geng-Shen": "fair",
                "Ren-Shen": "inauspicious",
            },
            "good_for": ["burial", "marriage", "moving", "business", "travel"],
            "bad_for": ["groundbreaking"],
            "description_chinese": "天富、天喜，甲申、丙申、戊申，宜安葬、起造、婚姻、入宅、開張、出行次吉。不宜動土。庚申只宜安葬，不宜修造、入宅。壬申西沉之日，五行無氣，不可用。",
            "description_english": "Heavenly Fortune and Sky Happiness present. Jia/Bing/Wu Shen good for burial, marriage, moving, business, travel - not groundbreaking. Geng Shen only for burial. Ren Shen has weak Qi - avoid.",
        },
        "You": {
            "officer": "Ping",
            "pillars": {
                "Yi-You": "inauspicious",
                "Ding-You": "inauspicious",
                "Ji-You": "inauspicious",
                "Xin-You": "inauspicious",
                "Gui-You": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["all_activities"],
            "description_chinese": "小紅砂，有朱雀、勾絞、到州星，招官司、損長幼、家下伶仃、百事不宜，犯之大凶。",
            "description_english": "Lesser Red Embrace with Red Phoenix and Grappling Hook stars. Causes legal issues, harms eldest and youngest in household. Highly inauspicious - families will not grow or expand.",
        },
        "Xu": {
            "officer": "Ding",
            "pillars": {
                "Jia-Xu": "excellent",
                "Bing-Xu": "inauspicious",
                "Wu-Xu": "excellent",
                "Geng-Xu": "excellent",
                "Ren-Xu": "inauspicious",
            },
            "good_for": ["renovation", "groundbreaking", "moving", "business", "marriage", "burial"],
            "bad_for": [],
            "description_chinese": "甲戌、戊戌、庚戌，有黃羅、紫檀、天皇、地皇、金銀、寶藏、田塘、庫珠、聚祿、駕馬、御聖遊頑星蓋照，大吉。如起造、興工、動土、入宅、開張、婚姻、埋葬諸事，加官進爵、生貴子、益棟財。惟丙戌、壬戌二日，熬入中宮，雖有吉星相解，終難受益。",
            "description_english": "Jia/Wu/Geng Xu excellent with many auspicious stars. Good for renovation, groundbreaking, moving, business, marriage, burial. Brings promotions, noble children, wealth. Bing Xu and Ren Xu have Sha Qi - benefits reduced.",
        },
        "Hai": {
            "officer": "Zhi",
            "pillars": {
                "Yi-Hai": "auspicious",
                "Ding-Hai": "fair",
                "Ji-Hai": "fair",
                "Xin-Hai": "inauspicious",
                "Gui-Hai": "dire",
            },
            "good_for": ["simple_renovation"],
            "bad_for": [],
            "description_chinese": "乙亥可小修，為次吉。丁亥、己亥又次吉。辛亥，陰府決遣之日。癸亥，六甲窮日，又正四廢，大凶。",
            "description_english": "Yi Hai auspicious for simple renovation. Ding Hai and Ji Hai are fair. Xin Hai is Yin Qi Day. Gui Hai is Six Jia Weakness Day and Four Direct Day - dire, avoid all activities.",
        },
        "Zi": {
            "officer": "Po",
            "pillars": {
                "Jia-Zi": "inauspicious",
                "Bing-Zi": "inauspicious",
                "Wu-Zi": "inauspicious",
                "Geng-Zi": "inauspicious",
                "Ren-Zi": "dire",
            },
            "good_for": [],
            "bad_for": ["marriage", "renovation", "burial", "moving"],
            "description_chinese": "天賊，不宜嫁親、造作、安葬、入宅等事，犯之招官司、損六畜、田產不收，大凶。壬子，正四廢，更凶，此日百事不利，犯之受死。",
            "description_english": "Heavenly Thief star. Unsuitable for marriage, renovation, burial, moving. Causes legal issues, livestock harm, property loss. Ren Zi is Four Direct Day - worst, avoid all activities.",
        },
        "Chou": {
            "officer": "Wei",
            "pillars": {
                "Yi-Chou": "inauspicious",
                "Ding-Chou": "dire",
                "Ji-Chou": "inauspicious",
                "Xin-Chou": "inauspicious",
                "Gui-Chou": "dire",
            },
            "good_for": [],
            "bad_for": ["marriage", "renovation", "moving"],
            "description_chinese": "丁丑、癸丑不宜嫁親、造作、安葬、入宅，犯之田產不收、財物失脫、虎咬蛇傷，多凶。餘丑亦不吉，損六畜、招官司，諸事不宜。",
            "description_english": "Ding Chou and Gui Chou are dire - unsuitable for marriage, renovation, moving. Causes property loss, tiger/snake attacks. Other Chou days also inauspicious - damage to livestock, legal issues.",
        },
        "Yin": {
            "officer": "Cheng",
            "pillars": {
                "Jia-Yin": "excellent",
                "Bing-Yin": "excellent",
                "Wu-Yin": "excellent",
                "Geng-Yin": "excellent",
                "Ren-Yin": "auspicious",
            },
            "good_for": ["groundbreaking", "construction", "moving", "business", "conception"],
            "bad_for": [],
            "description_chinese": "黃砂、天喜，丙寅天、月二德，庚寅、戊寅、甲寅，有黃羅、紫檀、天皇、地皇、金銀庫樓、玉堂、寶藏、吉星相照，興工動土、定礎搪架、入宅、開張，六十日一百二十日內益財增喜，家門從此富盛，世道愈見安康，大吉也。是月壬寅雖有吉星相照，內中稍有煞星相處，次吉。",
            "description_english": "Yellow Embrace and Sky Happiness. Bing Yin has Heavenly/Monthly Virtue. Jia/Wu/Geng Yin have many auspicious stars - excellent for groundbreaking, construction, moving, business, conception. Benefits within 60-120 days. Ren Yin has some Sha Qi - secondarily auspicious.",
        },
        "Mao": {
            "officer": "Shou",
            "pillars": {
                "Yi-Mao": "inauspicious",
                "Ding-Mao": "inauspicious",
                "Ji-Mao": "inauspicious",
                "Xin-Mao": "inauspicious",
                "Gui-Mao": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["all_activities"],
            "description_chinese": "往亡，有朱雀、勾絞，小人刑害、禍患纏綿、官司、口舌、損六畜，百事不宜，大凶。",
            "description_english": "Emptiness Day with Red Phoenix and Grappling Hook. Causes petty people interference, legal problems, disputes, harm to pets. Avoid all activities.",
        },
        "Chen": {
            "officer": "Kai",
            "pillars": {
                "Jia-Chen": "inauspicious",
                "Bing-Chen": "excellent",
                "Wu-Chen": "inauspicious",
                "Geng-Chen": "excellent",
                "Ren-Chen": "excellent",
            },
            "good_for": ["all_activities"],
            "bad_for": [],
            "description_chinese": "天成、丙辰，有月德；庚辰、壬辰，有黃羅、紫檀吉星蓋照，用之增田產、六畜興旺、生貴子，百事大吉。惟戊辰、甲辰，熬入中宮，大凶。",
            "description_english": "Heavenly Success star. Bing Chen has Monthly Virtue. Geng Chen and Ren Chen have Yellow Spiral and Purple Sandalwood - excellent for all activities, brings property, livestock prosperity, noble children. Jia Chen and Wu Chen have Sha Qi - avoid.",
        },
        "Si": {
            "officer": "Bi",
            "pillars": {
                "Yi-Si": "auspicious",
                "Ding-Si": "inauspicious",
                "Ji-Si": "inauspicious",
                "Xin-Si": "auspicious",
                "Gui-Si": "inauspicious",
            },
            "good_for": ["renovation", "groundbreaking", "moving", "marriage", "business", "travel"],
            "bad_for": [],
            "description_chinese": "乙巳、辛巳，有黃羅、紫檀星蓋照，興工作、動土、修造、池塘、倉庫、牛羊欄圈、入宅、婚姻、開張、出行、大益家門，子孫昌盛、田產倍收、人口安康，大吉。餘巳不言。",
            "description_english": "Yi Si and Xin Si have Yellow Spiral and Purple Sandalwood - auspicious for renovation, groundbreaking, pond excavation, moving, marriage, business, travel. Brings offspring prosperity, wealth increase, health. Other Si days unsuitable.",
        },
    },

    # ========================================
    # MONTH 6 - Goat Month (六月 / 未月)
    # ========================================
    6: {
        "Wei": {
            "officer": "Jian",
            "pillars": {
                "Yi-Wei": "dire",
                "Ding-Wei": "inauspicious",
                "Ji-Wei": "inauspicious",
                "Xin-Wei": "inauspicious",
                "Gui-Wei": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["renovation", "marriage", "moving", "business", "important_activities"],
            "description_chinese": "乙未,煞入中宮,不利修造、婚姻、入宅、開張、上官、諸事犯之不吉,犯之招時氣瘟疫、損人口、失財物,大凶。",
            "description_english": "On a Yi Wei Day, Sha (Killing) Qi enters the Central Palace of a residence or workplace, making this day unsuitable to undertake renovation works, get married, move into a new house, open a business or assume a new post. Violating this rule of caution will result in chaos and all facets of life being adversely affected; from family members being hurt to wealth being lost. It is therefore best to avoid this day insofar as all important activities or endeavors are concerned.",
        },
        "Shen": {
            "officer": "Chu",
            "pillars": {
                "Jia-Shen": "excellent",
                "Bing-Shen": "inauspicious",
                "Wu-Shen": "auspicious",
                "Geng-Shen": "fair",
                "Ren-Shen": "auspicious",
            },
            "good_for": ["construction", "renovation", "burial", "groundbreaking", "landscaping", "travel", "business"],
            "bad_for": [],
            "description_chinese": "甲申,有天、月二德、黃羅、紫檀星蓋照,利竪造、起造、安葬、動土、開山、斬草、出行、開張,百事皆吉。餘申日亦大吉。惟丙申一日,五行無氣,不可用。庚申日慎用。",
            "description_english": "The presence of the auspicious Heavenly and Monthly Virtue, as well as Yellow Spiral and Purple Sandalwood Stars lend positive support to this Jia Shen Day. It is hence a suitable and auspicious day for constructing vertical beams, renovation, burial, ground-digging, excavating mountains for development purposes, landscaping, travel and launching a business. The other Shen (Monkey) days are also considered auspicious, except for the Bing Shen Day when Qi of the Five Elements is either trapped or dead, and therefore cannot be used. In addition, one needs to be cautious if using the Geng Shen Day for significant activities or endeavors.",
        },
        "You": {
            "officer": "Man",
            "pillars": {
                "Yi-You": "auspicious",
                "Ding-You": "inauspicious",
                "Ji-You": "inauspicious",
                "Xin-You": "auspicious",
                "Gui-You": "inauspicious",
            },
            "good_for": ["lumbering", "fastening_frames", "fixing_column", "constructing_house"],
            "bad_for": ["important_activities"],
            "description_chinese": "天喜、天富。乙酉、辛酉,伐木、捻架、定碓、起造,乃次吉日。己酉九土鬼日;癸酉小葬日。又犯黑煞所臨,僅可備於急用。丁酉逢滿日,亦不利,此數日恐吉中有凶,終不美,用宜慎之。",
            "description_english": "The positive Sky Happiness and Heavenly Fortune Stars are present on Yi You and Xin You Days. Even so, these days are only moderately suitable to be used for particular activities such as lumbering, fastening frames, fixing a new column or pedestal, or constructing a new house. The Ji You Day is also known as a Nine Earth Ghost Day, while the Gui You Day is identified as a Lesser Cremate Day. Both these days harbor inauspiciously Black Sha (Killing) Qi and are therefore unsuitable for important activities. A Ding You Day appears to be initially auspicious due to the presence of positive stars but since it is also the harbinger of hidden problems, it should be avoided insofar as activities or endeavors are concerned.",
        },
        "Xu": {
            "officer": "Ping",
            "pillars": {
                "Jia-Xu": "auspicious",
                "Bing-Xu": "inauspicious",
                "Wu-Xu": "inauspicious",
                "Geng-Xu": "inauspicious",
                "Ren-Xu": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["moving", "marriage", "important_activities"],
            "description_chinese": "有朱雀、勾絞,又犯到州星,不利入宅、婚姻、招官非、損人口、退血財,大凶。等事,犯之主招官非,為玄女倫修之日,為俱白,二十四日向諸神朝天之日,有氣可用。惟甲戌一日,陰府修之日。",
            "description_english": "The presence of the negative Red Phoenix and Grappling Hook Stars make this day unsuitable for moving into a new house or getting married. Its detrimental effects include legal entanglements, family members being more prone to injuries and poor health. Only the Jia Xu Day contains some auspicious stars, making it usable for activities or endeavors of importance.",
        },
        "Hai": {
            "officer": "Ding",
            "pillars": {
                "Yi-Hai": "excellent",
                "Ding-Hai": "excellent",
                "Ji-Hai": "auspicious",
                "Xin-Hai": "inauspicious",
                "Gui-Hai": "inauspicious",
            },
            "good_for": ["travel", "moving", "marriage", "education", "renovation", "groundbreaking", "meeting_important_people"],
            "bad_for": [],
            "description_chinese": "己亥火星,丁亥有黃羅、紫檀、天皇、地皇星蓋照,乙亥文昌值日,宜出行、入宅、婚姻、入學、修造、動土、冬官見貴,招財祿、生貴子、大作大發、小作小發。文昌乙亥在午,文昌是太陽,午宮乃太陽之位,故有文昌星值日,是以大吉。辛亥是婦人之金,陰氣全盛,癸亥六甲窮日,五行無氣,此二日不宜用。",
            "description_english": "The Ji Hai Day is marked by the presence of the Fire Star, while the Ding Hai Day contains the Yellow Spiral, Purple Sandalwood, Heavenly Emperor and Earthly Emperor Stars. Meanwhile, the Yi Hai Day is accompanied by the Literary Star; making it a good day to embark on a journey, move into a new house, get married, commence studies at a new school, or engage in renovation or groundbreaking works or see somebody of importance. Using such a day will bring about wealth opportunities and the birth of a noble son. The more significant the activity, the more prominent the outcome. The Literary Star present on a Yi Hai Day can be found in the Wu (Horse) Palace. The literary star is akin to the Sun, which in turn is strongest when it is found in Wu Palace - thereby augmenting the Literary Arts Star positive effects even further. However, the Qi on a Xin Hai Day is overly Yin in polarity, while the Gui Hai Day is also known as a Six Jia Exhaustion Day. Neither of these two days possesses any Qi, so avoid using them for any activities or endeavors.",
        },
        "Zi": {
            "officer": "Zhi",
            "pillars": {
                "Jia-Zi": "fair",
                "Bing-Zi": "excellent",
                "Wu-Zi": "auspicious",
                "Geng-Zi": "excellent",
                "Ren-Zi": "inauspicious",
            },
            "good_for": ["renovation", "groundbreaking", "moving", "business", "travel"],
            "bad_for": [],
            "description_chinese": "黃砂。丙子、庚子,利起造、興工、動土、及倉庫、入宅、移徙、開張、出行。戊子次吉。在正月六月值天德、月德,甲子雖是六甲之首,不可用,然自死之金,五行無氣,平常之人,不能當此黑煞,北方將軍之氣,壬子木打寶瓶,北方沐浴之地,又是正四廢,更忌用。",
            "description_english": "The presence of the Yellow Embrace Star makes Bing Zi and Geng Zi Days suitable for renovation, ground-digging, opening something previously stored or contained, moving into a new house, launching a business and travel. In addition, Wu Zi Days are considered secondary-choice days. However, although a Jia Zi Day may appear to be the best of the 60 Jia Zi (Day Pillar) combinations, since it enjoys the presence of Heavenly and Monthly Virtue Stars this month, it cannot be used because Metal Qi is dead and the Five Elements are totally devoid of strength. Meanwhile, a Ren Zi Day assumes the Bath Position in the North sector, thereby making defining it as one of the Direct Pure Days; which should not be used for activities or endeavors of any sort.",
        },
        "Chou": {
            "officer": "Po",
            "pillars": {
                "Yi-Chou": "inauspicious",
                "Ding-Chou": "dire",
                "Ji-Chou": "inauspicious",
                "Xin-Chou": "dire",
                "Gui-Chou": "dire",
            },
            "good_for": [],
            "bad_for": ["business", "travel", "marriage", "important_activities"],
            "description_chinese": "小紅砂。此日無吉星,不可營為,萬不得已須擇時,僅作小小急用。若起造、開張、出行、婚姻等事,主損六畜、招官司。丁丑、癸丑,煞入中宮,犯之殺人,凶不可言。",
            "description_english": "The Lesser Red Embrace Star presides over this day, which otherwise lacks the presence of auspicious stars. Hence, employ caution if you wish to select this date for a certain purpose. It is certainly unsuitable for opening a business, travel and marriage, as it spells harm for animals and livestock, as well as the advent of legal issues. The Ding Chou and Gui Chou Days are the worst, as Sha (Killing) Qi enters the Central Palace on these days. Using them will only bring about catastrophe for occupants and unwitting victims.",
        },
        "Yin": {
            "officer": "Wei",
            "pillars": {
                "Jia-Yin": "excellent",
                "Bing-Yin": "auspicious",
                "Wu-Yin": "auspicious",
                "Geng-Yin": "auspicious",
                "Ren-Yin": "auspicious",
            },
            "good_for": ["business", "renovation", "moving", "marriage"],
            "bad_for": ["travel", "opening_land", "burial"],
            "description_chinese": "夏為鬼神空亡。甲寅有天月二德、黃羅、紫檀、金銀庫樓、祿馬、寶蓋、帝駕蓋照,但不利遠行、起造、入宅、婚姻,緣有為鬼神凶宅之疑耳。如開山、埋葬、營謀百事,六十日、一百二十日內生貴子、家業興旺、貴人接引、進產業,大吉。餘寅日次吉。",
            "description_english": "This day, also known as the Ghost and Deities Emptiness Day, Jia Yin Day, is ironically accompanied by the presence of the auspicious Heavenly and Monthly Virtue, Yellow Spiral, Purple Sandalwood, Golden Ingot, Storage and Prosperous Treasure Stars. Hence, it may indeed be considered auspicious, but should still not be utilized for travel, renovation, moving into a new residence and marriage. This day is however totally unusable for Opening (Exploring) New Land or Burial. Nevertheless, used well or carefully, one will be blessed with the birth of a noble child, and an increase in material assets within 60 to 120 days. In addition, there will be no shortage of help in times of need from noble people. Do note though that the other Yin (Tiger) Days are considered secondary in terms of usefulness.",
        },
        "Mao": {
            "officer": "Cheng",
            "pillars": {
                "Yi-Mao": "excellent",
                "Ding-Mao": "auspicious",
                "Ji-Mao": "auspicious",
                "Xin-Mao": "excellent",
                "Gui-Mao": "auspicious",
            },
            "good_for": ["renovation", "moving", "business", "travel", "marriage"],
            "bad_for": [],
            "description_chinese": "天喜。乙卯、辛卯有黃羅、紫檀、鑒與寶蓋、緣蔭、馬泣星蓋照,瓊玉、金寶、天帝、聚寶、諸吉星照臨,利造作、入宅、開行、出行、婚姻等事,主益子孫、旺田產、進橫財、增房屋、生貴子,大吉。餘卯次吉。",
            "description_english": "In addition to the presence of the auspicious Sky Happiness Star, Yi Mao and Xin Mao Days are also accompanied by the presence of the following positive Stars: The Yellow Spiral, Purple Sandalwood, Precious Cover, Prosperous Inheritance, Sky Horse, Precious Jade, Golden Treasure, Heavenly King and Converging Treasure. This situation makes such days suitable for renovation, moving into a new house, opening a new business, travel and marriage. Used well, one will witness ones material wealth and assets increasing, as well as ones offspring prospering. Do note that the other Mao (Rabbit) Days are considered second-best options.",
        },
        "Chen": {
            "officer": "Shou",
            "pillars": {
                "Jia-Chen": "excellent",
                "Bing-Chen": "auspicious",
                "Wu-Chen": "inauspicious",
                "Geng-Chen": "inauspicious",
                "Ren-Chen": "auspicious",
            },
            "good_for": ["renovation", "burial", "business"],
            "bad_for": [],
            "description_chinese": "甲辰天德。丙辰、壬辰三日次吉,利偷方修理,主益田產、旺六畜、宜安葬、營為。庚辰為騰蛇、朱雀,不宜用。戊辰亦不吉。",
            "description_english": "The Jia Chen Day is accompanied by the Heavenly Virtue Star, while Bing Chen and Ren Chen Days are considered secondary auspicious days. Activities or endeavors undertaken on these days will bring about an improvement in material fortunes and an amassment of wealth and other worldly assets. Burials may also be undertaken on these days. However, the Geng Chen Day is rendered unusable by the presence of the Surging Snake and Red Phoenix Stars and similarly, the Wu Chen Day is also unsuitable for use.",
        },
        "Si": {
            "officer": "Kai",
            "pillars": {
                "Yi-Si": "auspicious",
                "Ding-Si": "inauspicious",
                "Ji-Si": "inauspicious",
                "Xin-Si": "inauspicious",
                "Gui-Si": "auspicious",
            },
            "good_for": ["construction", "groundbreaking", "moving", "business"],
            "bad_for": [],
            "description_chinese": "天成、天賊。福生宜結福,乙巳、癸巳,興工、動土、入宅、開張次吉。餘巳不利,犯月厭,凶。",
            "description_english": "The Heavenly Success and Heavenly Ripper Stars govern this day, thereby facilitating the accumulation of prosperous Qi. Yi Si and Gui Si Days are the next best choice of days to commence construction, move into a new house, or launch or officiate an event. These days may hence be used if there is no other suitable substitute of days, although they should only be utilized very carefully for specific purposes.",
        },
        "Wu": {
            "officer": "Bi",
            "pillars": {
                "Jia-Wu": "auspicious",
                "Bing-Wu": "fair",
                "Wu-Wu": "inauspicious",
                "Geng-Wu": "fair",
                "Ren-Wu": "fair",
            },
            "good_for": ["minor_activities"],
            "bad_for": ["major_activities"],
            "description_chinese": "往亡。甲午天赦,不係轉煞,又值月德,然亦只可小用,因有受死不全之氣。丙午葬日,如小小營為,庚午小葬次吉。壬午、庚午,餘事不宜。戊午重喪,不可用。",
            "description_english": "This day is also known as an Emptiness Day. However, the Jia Wu Day is accompanied by the positive Heavenly Pardon and Monthly Virtue Stars, which act to negate or neutralize the ill-effects of the Drilling Sha that is also present. The Bing Wu Day can be used for affairs of lesser significance, while Ren Wu and Geng Wu Days can be utilized for even more insignificant matters. Avoid using a Wu Wu Day, though.",
        },
    },

    # ========================================
    # MONTH 7 - Monkey Month (七月 / 申月)
    # ========================================
    7: {},  # TODO: Waiting for correct reference data
    # ========================================
    # MONTH 8 - Rooster Month (八月 / 酉月)
    # ========================================
    8: {
        "You": {
            "officer": "Jian",
            "pillars": {
                "Yi-You": "inauspicious",
                "Ding-You": "inauspicious",
                "Ji-You": "inauspicious",
                "Xin-You": "inauspicious",
                "Gui-You": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["all_activities"],
            "description_chinese": "小紅砂、天成。乃五行自敗之時,百事招凶。兼犯天地轉然,用之大凶,招官司、產厄、水火災厄、子孫迸散、敗家。",
            "description_english": "The presence of inauspicious stars supercedes the influence of the Lesser Red Embrace and Heavenly Success Stars; resulting in the Qi of the Five Elements being weak. Avoid undertaking any important activities or endeavors on this day, more so when it also carries the Heaven and Earth Drilling Sha. Such a combination only heightens the risk of lawsuits, miscarriage, as well as water and fire hazards. Worse still, one's descendents will have no affinity amongst themselves, resulting in a broken family and poor familial fortunes.",
        },
        "Xu": {
            "officer": "Chu",
            "pillars": {
                "Jia-Xu": "auspicious",
                "Bing-Xu": "inauspicious",
                "Wu-Xu": "auspicious",
                "Geng-Xu": "excellent",
                "Ren-Xu": "inauspicious",
            },
            "good_for": ["construction", "groundbreaking", "moving", "business", "marriage"],
            "bad_for": [],
            "description_chinese": "庚戌天、月二德,戊戌、甲戌,宜興工、動土、入宅、開張、婚姻等事,用之次吉。丙戌、壬戌,然入中宮,諸事不宜,犯之主失財、冷退,大凶。",
            "description_english": "On Geng Xu Days, the auspicious Heavenly and Monthly Virtue Stars exert their positive influence. Furthermore, Wu Xu and Jia Xu Days are also good for commencing construction or groundbreaking works, moving into a new house, opening a new business and getting married. However, Sha (Killing) Qi renders Bing Xu and Ren Xu Days unsuitable for activities or endeavors of importance. Accordingly, loss of wealth will follow those who use such days for their endeavors.",
        },
        "Hai": {
            "officer": "Man",
            "pillars": {
                "Yi-Hai": "excellent",
                "Ding-Hai": "excellent",
                "Ji-Hai": "excellent",
                "Xin-Hai": "inauspicious",
                "Gui-Hai": "dire",
            },
            "good_for": ["renovation", "construction", "groundbreaking", "moving", "marriage", "business", "travel"],
            "bad_for": [],
            "description_chinese": "天富。乙亥、文昌、貴顯之星。丁亥、己亥有黃羅、紫檀、天皇、地皇、華彩操持、祿馬諸星蓋照,利起造、興工、動土、挺架、入宅、嫁娶、開張、出行、營為諸事,大作大發,小作小發,六十日、一百二十日內,遲至週年便見覆財,成家生貴子、旺田產、興六畜。辛亥陰府決遣之日,非陽間所用。癸亥六甲窮日,五行無氣,不可用。",
            "description_english": "The Heavenly Fortune Star is present throughout the month, while Yi Hai Days are also blessed with the presence of the Literary Arts Star. Likewise, Ding Hai and Ji Hai Days are accompanied by good stars such as the Yellow Spiral, Purple Sandalwood, Heavenly Emperor, Magnificent Colors and Prosperous Horse Stars. As such, these days are ideal for renovations, commencing construction, groundbreaking, building or moving into a new house, marriage, opening a business and travel. Activities or endeavors that are done on a large-scale will reap huge gains, while smaller-scale endeavors will enjoy gains on a corresponding scale. The positive results of using these days will be seen within 60 to 120 days, with a notable increase of wealth and assets as well as the birth of noble children. However, Xin Hai Days are overly Yin while a Gui Hai Day is also known as a Six Jia Weakness Day and is therefore devoid of Qi. Avoid using these days if possible.",
        },
        "Zi": {
            "officer": "Ping",
            "pillars": {
                "Jia-Zi": "inauspicious",
                "Bing-Zi": "auspicious",
                "Wu-Zi": "auspicious",
                "Geng-Zi": "auspicious",
                "Ren-Zi": "inauspicious",
            },
            "good_for": ["renovation", "marriage", "moving", "travel", "groundbreaking"],
            "bad_for": [],
            "description_chinese": "往亡。朱雀、勾絞,招官司,損宅長。丙子乃水潔淨之時,庚子火星傍天、月二德,戊子等三日,利起造、嫁娶、入宅、出行、動土,用之卻吉。甲子亦有火星,但是北方黑然之氣,玉子草木凋零之時,五行無氣,不可用。",
            "description_english": "This is known as an Emptiness Day, due to the presence of the negative Red Phoenix and Grappling Hook Stars. As such, it is the harbinger of legal issues and also causes the eldest family member to be more prone to injury. From a more positive angle, a Bing Zi Day contains pure and serene Water Qi, while a Geng Zi Day is marked by the presence of the auspicious Fire and Monthly Virtue Stars. Such circumstances make these two days, including a Wu Zi Day suitable for renovations, marriage, moving into a new house, travel or groundbreaking. However, while a Jia Zi Day harbors the positive Fire Star, it is also adversely affected by the presence of Black Sha (Killing) Qi from the North, which renders it unsuitable for use. Lastly, the Qi of the Five Elements on a Ren Zi Day is weak and therefore useless as well.",
        },
        "Chou": {
            "officer": "Ding",
            "pillars": {
                "Yi-Chou": "fair",
                "Ding-Chou": "fair",
                "Ji-Chou": "inauspicious",
                "Xin-Chou": "fair",
                "Gui-Chou": "fair",
            },
            "good_for": ["minor_activities"],
            "bad_for": [],
            "description_chinese": "辛丑、癸丑、乙丑、丁丑亦次吉,惟己丑不利,諸事不宜,犯之主疾病、生災,凶。",
            "description_english": "Xin Chou, Gui Chou, Yi Chou and Ding Chou Days are fairly useable, although Ji Chou Days are inauspicious. As such, do not use Ji Chou Days for any important activities or endeavors, for this will result in one being especially susceptible to ailments and miscarriage.",
        },
        "Yin": {
            "officer": "Zhi",
            "pillars": {
                "Jia-Yin": "dire",
                "Bing-Yin": "auspicious",
                "Wu-Yin": "auspicious",
                "Geng-Yin": "excellent",
                "Ren-Yin": "auspicious",
            },
            "good_for": ["renovation", "marriage", "groundbreaking", "moving", "business", "travel"],
            "bad_for": [],
            "description_chinese": "黃砂。庚寅、天月二德,有黃羅、紫檀、天皇、地皇、金銀寶藏、田塘、庫珠聚、祿帶馬鑾、與官曜眾吉星照臨。宜起造、嫁娶、動土、移居、開張、出行、旺田產、進橫財、增六畜、添人口、與子孫改門庭、家道隆昌。餘寅亦次吉可用,惟甲寅乃正四廢,凶。",
            "description_english": "The positive Yellow Embrace Star presides over this day. In addition, Geng Yin Day are also supported by the positive energies of the Heavenly and Earthly Virtue Stars. The combined presence of other auspicious stars including the Yellow Emperor, Purple Sandalwood, Heavenly Emperor, Earthly Emperor, Golden Ingot, Precious Treasure, Field Pond, Storage Pearl, Converging Wealth and Sky Horse Stars makes such days most ideal for renovation, marriage, groundbreaking, moving house, launching a business and travel. Their useful energies will contribute to an increase in one wealth, as well as the expansion and growth of one family. In addition, success will be forthcoming in business dealings and all other facets of life. Avoid using a Jia Yin Day, though, as it is one of the inauspicious Four Direct Days.",
        },
        "Mao": {
            "officer": "Po",
            "pillars": {
                "Yi-Mao": "dire",
                "Ding-Mao": "inauspicious",
                "Ji-Mao": "fair",
                "Xin-Mao": "inauspicious",
                "Gui-Mao": "fair",
            },
            "good_for": [],
            "bad_for": ["important_activities"],
            "description_chinese": "天賊。癸卯、己卯用事次吉,餘卯不利,有朱雀、勾絞,招官司、口舌,兼犯月厭之凶。乙卯正四廢,亦凶。",
            "description_english": "The Heavenly Thief Star governs this day, thereby rendering only Gui Mao and Ji Mao Days fairly useable. The remaining Mao (Rabbit) Days are, however, inauspicious due to the presence of the negative Red Phoenix and Grappling Hook Stars. These inauspicious stars are the harbingers of lawsuits and malicious gossip. Avoid using a Yi Mao Day in particular, as it is one of the Four Direct Days and hence an extremely inauspicious one.",
        },
        "Chen": {
            "officer": "Wei",
            "pillars": {
                "Jia-Chen": "inauspicious",
                "Bing-Chen": "auspicious",
                "Wu-Chen": "inauspicious",
                "Geng-Chen": "inauspicious",
                "Ren-Chen": "excellent",
            },
            "good_for": ["renovation", "business", "travel", "moving", "marriage"],
            "bad_for": [],
            "description_chinese": "壬辰水潔淨之時,丙辰,宜破土、興工、開張、出行、入宅、婚姻,百事順利,大吉。戊辰、草木凋零,庚辰天地相疑,不吉。甲辰然入中宮,大凶。",
            "description_english": "Water Qi on a Ren Chen Day is purely, serene and well-balanced. As such, this day is ideal for renovations, opening a business, travel, moving into a new house or getting married. Bing Chen Days are moderately suitable for groundbreaking, starting a fresh endeavor, opening a business, traveling, enter a new house and marriage. The outcomes of all activities undertaken on these days will be auspicious. Note, however, that Wu Chen Geng Chen and Jia Chen are not useable – particularly Jia Chen Days, when Sha (Killing) Qi can be found in the Central Palace.",
        },
        "Si": {
            "officer": "Cheng",
            "pillars": {
                "Yi-Si": "excellent",
                "Ding-Si": "inauspicious",
                "Ji-Si": "excellent",
                "Xin-Si": "inauspicious",
                "Gui-Si": "inauspicious",
            },
            "good_for": ["marriage", "moving", "construction", "groundbreaking", "business", "travel"],
            "bad_for": [],
            "description_chinese": "天喜。乙巳、己巳,有紫檀、帶祿驛馬、集聚曲堂諸星蓋照,宜婚姻、入宅、興工、動工、開張、出行、起造、豬牛羊棧均大吉,百事順利,餘巳日次吉。",
            "description_english": "The presence of the Sky Happiness Star further enhances the positive energies on Yi Si and Ji Si Days, which already enjoy the auspicious energies of the Purple Sandalwood and Prosperous Sky Horse Stars. Accordingly, such days are suitable for marriage, moving into a new house, commencing construction work, groundbreaking, launching a business and travel. The remaining Si (Snake) Days, however, should only be regarded as second-best options.",
        },
        "Wu": {
            "officer": "Shou",
            "pillars": {
                "Jia-Wu": "inauspicious",
                "Bing-Wu": "auspicious",
                "Wu-Wu": "auspicious",
                "Geng-Wu": "inauspicious",
                "Ren-Wu": "excellent",
            },
            "good_for": ["groundbreaking", "burial"],
            "bad_for": [],
            "description_chinese": "福生,可惜建破來沖刑,壬午火星用事次吉。丙午動土、安葬、一切營為亦次吉。惟戊午有火星,不利。庚午亦不利。犯之損子孫、招官非、冷退,凶。甲午日未詳。",
            "description_english": "Although the Prosperous Growth Star is present, the unfortunate occurrence of a Destruction, Clash and Punishment relationship – all simultaneously – tarnish whatever positive energies this day might otherwise have. However, a Ren Wu Day is supported by the positive energies of the Fire Star and is therefore considered above-average in terms of usability. Likewise, Bing Wu Days may be used for groundbreaking and burial, while Wu Wu Days are also accompanied by the presence of the Fire Star. However, Geng Wu Days are inauspicious, and only spell harm for one's descendents as well as the threat of legal problems. Similarly, the Qi on a Jia Wu Day is fickle, at best.",
        },
        "Wei": {
            "officer": "Kai",
            "pillars": {
                "Yi-Wei": "inauspicious",
                "Ding-Wei": "auspicious",
                "Ji-Wei": "auspicious",
                "Xin-Wei": "auspicious",
                "Gui-Wei": "auspicious",
            },
            "good_for": ["burial", "cutting_trees", "excavating"],
            "bad_for": [],
            "description_chinese": "丁未、己未、辛未、癸未,均是次吉之日,只宜斬草、開山、掘樹、安葬等事。惟乙未百事不利,凶,內犯棄敗死絕之鄉。",
            "description_english": "Ding Wei, Ji Wei, Xin Wei and Gui Wei Days are fairly usable, but care should be taken to confine their usage to only activities such as burial, cutting trees or excavating mountains. Do not use Yi Wei especially for activities of significance, for their resultant outcomes will be disastrous.",
        },
        "Shen": {
            "officer": "Bi",
            "pillars": {
                "Jia-Shen": "auspicious",
                "Bing-Shen": "excellent",
                "Wu-Shen": "excellent",
                "Geng-Shen": "excellent",
                "Ren-Shen": "auspicious",
            },
            "good_for": ["travel", "groundbreaking", "moving", "marriage", "burial", "business"],
            "bad_for": [],
            "description_chinese": "戊申天赦,庚申、丙申,天、月二德,宜出行、修方、動土、興工、定碓、挺架、婚姻、入宅、安葬、開張、作倉庫、牛羊豬欄,利子孫、旺田產、進橫財、家門發達,上吉。甲申、壬申次吉。",
            "description_english": "The Wu Shen Day is also known as the Heavenly Pardon Day. Other auspicious days include Geng Shen and Bing Shen Days, which enjoy the positive energies exerted by the Heavenly and Monthly Virtue Stars. As such, these days are ideal for travel, groundbreaking, building or moving into a new house, marriage, burial or launching a business. Their positive consequences include an increase in wealth and good descendant luck. Use these days where possible, due to their extremely auspicious energies. Jia Shen and Ren Shen Days remain second-tier options.",
        },
    },
    # ========================================
    # MONTH 9 - Dog Month (九月 / 戌月)
    # ========================================
    9: {
        "Xu": {
            "officer": "Jian",
            "pillars": {
                "Jia-Xu": "inauspicious",
                "Bing-Xu": "excellent",
                "Wu-Xu": "inauspicious",
                "Geng-Xu": "inauspicious",
                "Ren-Xu": "inauspicious",
            },
            "good_for": ["renovation", "marriage", "business", "travel"],
            "bad_for": ["important_activities"],
            "description_chinese": "丙戌，天、月二德卻吉。餘戌不利，若用之主損財，資窮大凶。",
            "description_english": "Bing Xu Days are supported by the positive energies of the Heavenly Virtue and Monthly Virtue Stars. The other Xu (Dog) days are inauspicious, and embarking on significant endeavors on such days will result in wealth being lost and catastrophes.",
        },
        "Hai": {
            "officer": "Chu",
            "pillars": {
                "Yi-Hai": "excellent",
                "Ding-Hai": "excellent",
                "Ji-Hai": "auspicious",
                "Xin-Hai": "dire",
                "Gui-Hai": "dire",
            },
            "good_for": ["renovation", "business", "marriage", "moving", "travel", "groundbreaking"],
            "bad_for": [],
            "description_chinese": "天成。乙亥、丁亥，宜起造、開張、嫁娶、入宅、出行、動土，諸事大吉，主子孫興旺、速富貴。癸亥六甲窮日，不可用。辛亥純陰之氣，非陽間所用。己亥火星，惟起造嫁娶吉。",
            "description_english": "The Heavenly Success Star renders Yi Hai and Ding Hai Days suitable for renovations, opening a business, marriage, moving, travel and groundbreaking. Ji Hai has Fire Star, usable for marriage. Gui Hai is Six Jia Weakness Day. Xin Hai is overly Yin - avoid both.",
        },
        "Zi": {
            "officer": "Man",
            "pillars": {
                "Jia-Zi": "auspicious",
                "Bing-Zi": "excellent",
                "Wu-Zi": "inauspicious",
                "Geng-Zi": "inauspicious",
                "Ren-Zi": "inauspicious",
            },
            "good_for": ["marriage", "business", "travel", "moving", "groundbreaking", "burial"],
            "bad_for": [],
            "description_chinese": "黃砂、天富。丙子，水潔淨之時，兼有天、月二德、黃羅、紫檀、天皇、地皇、層霄連珠、祿馬，諸吉星蓋照，宜嫁娶、開張、出行、入宅、興工、動土、定礎、挺架、安葬。壬子木打寶瓶，草木凋零，大凶。餘子日不宜用事。甲子有黃羅、紫檀星蓋照，可用。",
            "description_english": "Yellow Embrace and Heavenly Fortune Stars present. Bing Zi has pure Water Qi with Heavenly/Monthly Virtue, Yellow Spiral, Purple Sandalwood stars - excellent for marriage, business, travel, moving, groundbreaking, burial. Jia Zi also usable with Yellow Spiral stars. Ren Zi and other Zi days are inauspicious.",
        },
        "Chou": {
            "officer": "Ping",
            "pillars": {
                "Yi-Chou": "inauspicious",
                "Ding-Chou": "excellent",
                "Ji-Chou": "inauspicious",
                "Xin-Chou": "inauspicious",
                "Gui-Chou": "dire",
            },
            "good_for": ["minor_activities"],
            "bad_for": ["major_activities"],
            "description_chinese": "小紅砂。有福生，惜被月建沖破，朱雀、勾絞，招官司、掛據，諸事不利。若小小營為，內有福生，亦僅可用。丁丑、癸丑，然入中宮，更凶。",
            "description_english": "Lesser Red Embrace with Prosperous Growth Star, but clashed by Monthly Star. Red Phoenix and Grappling Hook cause lawsuits. Ding Chou has offsetting positive stars. Avoid Gui Chou at all costs. Only minor activities on most days.",
        },
        "Yin": {
            "officer": "Ding",
            "pillars": {
                "Jia-Yin": "inauspicious",
                "Bing-Yin": "excellent",
                "Wu-Yin": "excellent",
                "Geng-Yin": "excellent",
                "Ren-Yin": "inauspicious",
            },
            "good_for": ["renovation", "marriage", "travel", "moving", "business"],
            "bad_for": [],
            "description_chinese": "丙寅，天、月二德，庚寅、戊寅，有黃羅、紫檀、天皇、地皇，諸星蓋照，宜起造、嫁娶、出行、入宅、開張，一切諸事，主進財，生貴子、興家道、旺六畜，大吉。壬寅犯月厭，受死無解。惟甲寅正四廢，凶。",
            "description_english": "Bing Yin has Heavenly and Monthly Virtue. Geng Yin and Wu Yin have Yellow Spiral, Purple Sandalwood, Heavenly/Earthly Emperor stars - suitable for renovation, marriage, travel, moving, business. Brings wealth and noble offspring. Ren Yin violates Month Detest Star. Jia Yin is Four Abandonment Day - avoid.",
        },
        "Mao": {
            "officer": "Zhi",
            "pillars": {
                "Yi-Mao": "dire",
                "Ding-Mao": "auspicious",
                "Ji-Mao": "excellent",
                "Xin-Mao": "excellent",
                "Gui-Mao": "auspicious",
            },
            "good_for": ["business", "travel", "moving", "groundbreaking", "renovation", "marriage"],
            "bad_for": [],
            "description_chinese": "辛卯、己卯有黃羅紫檀、天皇地皇諸吉星蓋照。宜開張、出行、入宅、動土、修方、嫁娶，起造倉庫，主進財產、增人口、興家進旺六畜大吉。惟乙卯正四廢凶。",
            "description_english": "Xin Mao and Ji Mao have Yellow Spiral, Purple Sandalwood, Heavenly/Earthly Emperor stars - ideal for business, travel, moving, groundbreaking, renovation. Brings wealth increase and family expansion. Ding Mao also auspicious. Yi Mao is Four Abandonment Day - avoid. Other Mao days are secondary.",
        },
        "Chen": {
            "officer": "Po",
            "pillars": {
                "Jia-Chen": "dire",
                "Bing-Chen": "fair",
                "Wu-Chen": "dire",
                "Geng-Chen": "fair",
                "Ren-Chen": "inauspicious",
            },
            "good_for": ["minor_repairs"],
            "bad_for": ["marriage", "business", "moving", "major_activities"],
            "description_chinese": "往亡。丙辰天月二德，修造小吉，但不宜嫁娶、開張、入宅、移居，主損六畜、耗血財、招口舌。餘辰日更不吉。甲辰、戊辰然入中宮，大凶。",
            "description_english": "Death and Emptiness Star present. Bing Chen has Heavenly/Monthly Virtue - suitable only for minor repairs. Major activities like marriage, business, moving are unsuitable. Jia Chen and Wu Chen have Sha Qi in Central Palace - worst of all. Remaining Chen days also inauspicious.",
        },
        "Si": {
            "officer": "Wei",
            "pillars": {
                "Yi-Si": "excellent",
                "Ding-Si": "fair",
                "Ji-Si": "fair",
                "Xin-Si": "fair",
                "Gui-Si": "fair",
            },
            "good_for": ["landscaping", "construction", "renovation", "marriage", "burial", "moving", "business", "travel"],
            "bad_for": [],
            "description_chinese": "乙巳，宜斬草、安葬、興工、造作、嫁娶、開張、納采、移居、出行、入宅，主益子孫、家道興隆、發財，大吉。餘巳次吉，只宜小作可用，不利婚姻、遷居、開張、出行，犯之凶敗。",
            "description_english": "Yi Si Day is excellent for landscaping, construction, renovation, marriage, burial, moving, business, travel - brings descendant luck, family prosperity, wealth. Other Si days are only fair - usable for small endeavors only, not for marriage, moving or business.",
        },
        "Wu": {
            "officer": "Cheng",
            "pillars": {
                "Jia-Wu": "auspicious",
                "Bing-Wu": "excellent",
                "Wu-Wu": "auspicious",
                "Geng-Wu": "auspicious",
                "Ren-Wu": "auspicious",
            },
            "good_for": ["marriage", "renovation", "moving", "travel", "business", "trade", "groundbreaking", "landscaping", "burial"],
            "bad_for": [],
            "description_chinese": "天喜。丙午天月二德，黃羅、紫檀、天皇、地皇、金銀、庫樓、祿馬諸星拱照，宜婚姻、起造、入宅、出行、開張、倉庫、經商、買賣、動土、斬草、安葬，全吉，大作大發，小作小發，富貴添丁、奴婢自來、謀望勝常。餘午日次吉，可用。",
            "description_english": "Sky Happiness Star present. Bing Wu has Heavenly/Monthly Virtue with Yellow Spiral, Purple Sandalwood, Heavenly/Earthly Emperor, Golden Ingot, Storage, Prosperous Horse stars - suitable for all activities. Large endeavors bring large gains. All Horse days are auspicious.",
        },
        "Wei": {
            "officer": "Shou",
            "pillars": {
                "Yi-Wei": "inauspicious",
                "Ding-Wei": "inauspicious",
                "Ji-Wei": "excellent",
                "Xin-Wei": "auspicious",
                "Gui-Wei": "auspicious",
            },
            "good_for": ["burial", "beams_columns"],
            "bad_for": ["renovation", "marriage", "travel", "moving", "business"],
            "description_chinese": "己未，是葬日。辛未、癸未，定碓、挺架、次吉，但不利起造、婚姻、出行、入宅、安葬、開張、倉庫等事，主損血財、遭瘟疫。乙未、朱雀、勾絞、白虎，入中宮，丁未亦凶。",
            "description_english": "Ji Wei is Burial Day - excellent. Xin Wei and Gui Wei are second-best for installing beams and columns. Not suitable for renovation, marriage, travel, moving or business - causes wealth loss and illness. Yi Wei and Ding Wei have Red Phoenix, Grappling Hook, White Tiger - avoid.",
        },
        "Shen": {
            "officer": "Kai",
            "pillars": {
                "Jia-Shen": "excellent",
                "Bing-Shen": "auspicious",
                "Wu-Shen": "excellent",
                "Geng-Shen": "inauspicious",
                "Ren-Shen": "auspicious",
            },
            "good_for": ["burial", "yin_house"],
            "bad_for": ["renovation", "marriage", "moving", "business"],
            "description_chinese": "天賊。戊申天赦，甲申水潔淨之時，有黃羅、紫檀、聚祿帶馬星蓋照，宜安葬、作生基。但西沉之日，五行無氣，沉當秋暮之候，不宜起造、婚姻、入宅、開張，惟安葬獲吉，益子孫、家門發達。餘申次吉。庚申，乃白虎入中宮，犯之殺人，更凶。",
            "description_english": "Heavenly Thief Star present. Wu Shen is Heavenly Pardon Day. Jia Shen has pure Water Qi with Yellow Spiral, Purple Sandalwood, Converging Prosperity, Belted Horse stars - ideal for burial or Yin House. Towards end of Autumn, Five Elements lack Qi - not for renovation, marriage, moving, business. Geng Shen has White Tiger in Central Palace - extremely dangerous.",
        },
        "You": {
            "officer": "Bi",
            "pillars": {
                "Yi-You": "inauspicious",
                "Ding-You": "fair",
                "Ji-You": "inauspicious",
                "Xin-You": "inauspicious",
                "Gui-You": "inauspicious",
            },
            "good_for": ["minor_activities", "burial"],
            "bad_for": ["renovation", "marriage", "moving", "business"],
            "description_chinese": "此時秋冬交界，俱為殺傷。己酉九土鬼，乙酉是安葬日。餘酉亦宜小用，但是五行無氣，名為暴敗，熬重之日，不宜起造、婚姻、入宅、開張，用之冷退，凶。",
            "description_english": "Autumn-Winter transition period when Yang Qi diminishes. Ji You harbors Nine Earth Ghost Star. Yi You is Burial Day. Remaining You days only suitable for minor endeavors - Five Elements lack Qi. Unsuitable for renovation, marriage, moving, business - will cause luck to deteriorate.",
        },
    },
    # ========================================
    # MONTH 10 - Pig Month (十月 / 亥月)
    # ========================================
    10: {
        "Hai": {
            "officer": "Jian",
            "pillars": {
                "Yi-Hai": "fair",
                "Ding-Hai": "inauspicious",
                "Ji-Hai": "fair",
                "Xin-Hai": "inauspicious",
                "Gui-Hai": "inauspicious",
            },
            "good_for": ["minor_activities"],
            "bad_for": ["renovation", "business", "marriage", "moving", "travel", "burial"],
            "description_chinese": "不利起造、開張、嫁娶、入宅、出行、安葬,用之招官司、損家長。即乙亥、己亥,亦只宜小作營為,緣十月建亥不利。",
            "description_english": "Not auspicious for renovation, launching a business, marriage, moving into a new house, travel or burial. These activities will result in legal entanglements and the eldest member of the family being prone to injury. However, Yi Hai and Ji Hai Days may be used for activities of low significance.",
        },
        "Zi": {
            "officer": "Chu",
            "pillars": {
                "Jia-Zi": "auspicious",
                "Bing-Zi": "inauspicious",
                "Wu-Zi": "inauspicious",
                "Geng-Zi": "inauspicious",
                "Ren-Zi": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["most_activities"],
            "description_chinese": "雖是五行旺相,但秋冬交界之初,有轉煞之凶。古云轉煞而傷,未可輕用。甲子天赦不是轉煞。可用。",
            "description_english": "Even though the Qi of the Five Elements is prosperous, the transition from Autumn to Winter carries Heaven and Earth Drilling Sha 轉煞 - rendering this day unusable. However, Jia Zi Days are Heavenly Pardon 天赦 Days without this interference, and can be utilized.",
        },
        "Chou": {
            "officer": "Man",
            "pillars": {
                "Yi-Chou": "inauspicious",
                "Ding-Chou": "dire",
                "Ji-Chou": "inauspicious",
                "Xin-Chou": "inauspicious",
                "Gui-Chou": "dire",
            },
            "good_for": [],
            "bad_for": ["renovation", "marriage", "celebrations", "doorframes", "most_activities"],
            "description_chinese": "天富、天成、天賊,丁丑、癸丑,煞入中宮,不利起造、嫁娶,鼓樂宴啖等事,以及釘門,務驚動神煞損人丁,傷六畜。餘丑日亦不宜用,只可請魂入墓,凡金入丑宮,五行無氣,並犯月厭天賊之凶。",
            "description_english": "Heavenly Fortune 天富, Heavenly Success 天成, Heavenly Thief 天賊 Stars preside. On Ding Chou and Gui Chou Days, Sha (Killing) Qi enters the Central Palace - unsuitable for renovation, marriage, celebrations or installing doorframes. Violating this rule brings harm to people and livestock. Other Chou days are equally unusable.",
        },
        "Yin": {
            "officer": "Ping",
            "pillars": {
                "Jia-Yin": "excellent",
                "Bing-Yin": "inauspicious",
                "Wu-Yin": "inauspicious",
                "Geng-Yin": "auspicious",
                "Ren-Yin": "auspicious",
            },
            "good_for": ["minor_repairs"],
            "bad_for": ["major_activities"],
            "description_chinese": "天富、天成。有到州星,事到官府而後散。惟甲寅乃上吉,壬寅、庚寅次吉,小小修則可,大作不宜。餘寅日凶。不可用。",
            "description_english": "With the presence of Heavenly Fortune 天富 and Heavenly Success 天成 Stars, Jia Yin days are good, with Ren Yin and Geng Yin also reasonably usable. These days should not be used for activities of great significance. Other Tiger days are inauspicious and should be avoided.",
        },
        "Mao": {
            "officer": "Ding",
            "pillars": {
                "Yi-Mao": "auspicious",
                "Ding-Mao": "auspicious",
                "Ji-Mao": "excellent",
                "Xin-Mao": "excellent",
                "Gui-Mao": "auspicious",
            },
            "good_for": ["groundbreaking", "construction", "moving", "marriage", "travel", "business"],
            "bad_for": [],
            "description_chinese": "乙卯天德、辛卯、己卯,宜動土、興工、定礎、上樑、嫁娶、入宅、出行、開張等用之,吉曜照臨,餘卯次吉。",
            "description_english": "Yi Mao Days are supported by the Heavenly Virtue 天德 Star. Xin Mao and Ji Mao Days are ideal for groundbreaking, commencing construction, building or moving into a new house, marriage, travel or launching a business. Remaining Mao Days are secondary in auspiciousness.",
        },
        "Chen": {
            "officer": "Zhi",
            "pillars": {
                "Jia-Chen": "excellent",
                "Bing-Chen": "auspicious",
                "Wu-Chen": "dire",
                "Geng-Chen": "inauspicious",
                "Ren-Chen": "inauspicious",
            },
            "good_for": ["minor_repairs"],
            "bad_for": ["renovation", "construction", "marriage", "moving"],
            "description_chinese": "甲辰雖有天月二德,只可偷修,若起造、興工、嫁娶、入宅則不利。十月雖不是敗日,然終有凶。餘辰亦不利,惟丙辰日可以開山、斬草、安葬次吉。戊辰煞入中宮,大凶。不可用。",
            "description_english": "Even with Heavenly 天德 and Monthly Virtue 月德 Stars, use Jia Chen Days only for minor repairs - unsuitable for renovation, construction, marriage or moving. Bing Chen Days are suitable for excavating, landscaping and burial. Wu Chen Days have Sha in Central Palace - extremely inauspicious.",
        },
        "Si": {
            "officer": "Po",
            "pillars": {
                "Yi-Si": "auspicious",
                "Ding-Si": "dire",
                "Ji-Si": "inauspicious",
                "Xin-Si": "inauspicious",
                "Gui-Si": "inauspicious",
            },
            "good_for": ["minor_activities"],
            "bad_for": ["important_activities"],
            "description_chinese": "小紅砂日。亦犯朱雀、勾絞,膝蛇,諸事不宜。惟乙巳有天德,只可小小營為,用之次吉。丁巳正四廢,凶。犯之雷霆散敗、橫事、失財。",
            "description_english": "Lesser Red Embrace Day 小紅砂日, accompanied by Red Phoenix 朱雀 and Grappling Hook 勾絞 Stars. Avoid for important activities. Yi Si Day with Heavenly Virtue 天德 may be used for minor matters. Ding Si Day is Direct Abandonment Day 正四廢 - could result in accidents or loss of wealth.",
        },
        "Wu": {
            "officer": "Wei",
            "pillars": {
                "Jia-Wu": "excellent",
                "Bing-Wu": "dire",
                "Wu-Wu": "auspicious",
                "Geng-Wu": "auspicious",
                "Ren-Wu": "auspicious",
            },
            "good_for": ["marriage", "business", "renovation", "groundbreaking", "travel", "moving", "burial"],
            "bad_for": [],
            "description_chinese": "黃砂。甲午月德,有黃羅、紫檀、金銀,庫樓。諸吉星蓋照,嫁娶、開張、起造、動土、出行、入宅、安葬,大吉。餘午日次吉,丙午正四廢,凶。",
            "description_english": "Yellow Embrace 黃砂 Star exerts influence. Jia Wu Days have Monthly Virtue 月德 with Yellow Spiral 黃羅, Purple Sandalwood 紫檀, Golden Ingot 金銀 and Storage 庫樓 Stars - excellent for marriage, business, renovation, groundbreaking, travel, moving and burial. Other Horse days are second-best. Bing Wu is Direct Abandonment Day 正四廢 - extremely inauspicious.",
        },
        "Wei": {
            "officer": "Cheng",
            "pillars": {
                "Yi-Wei": "inauspicious",
                "Ding-Wei": "auspicious",
                "Ji-Wei": "auspicious",
                "Xin-Wei": "auspicious",
                "Gui-Wei": "excellent",
            },
            "good_for": ["repairs", "marriage", "debt_collection", "travel", "moving"],
            "bad_for": [],
            "description_chinese": "月建三合,惜乙未煞入中宮,忌出行、安葬、嫁娶、入宅、開張、修造等事。惟癸未火星,木入秦州,是貴人之星,值黃羅、紫檀、金銀,聯珠星蓋照,宜起造、嫁娶、納財、問名、出行、遇貴,入家宅永安寧,主週年百日,得貴人接引、進田產、生貴子、發福,上吉。餘未次吉。",
            "description_english": "Forms Three Harmony 三合 with month, but Sha Qi enters Central Palace on Yi Wei Days - unsuitable for travel, burial, marriage, moving, business or repairs. Gui Wei Days have Fire Star with Nobleman Star and Yellow Spiral, Purple Sandalwood, Golden Ingot, Shining Pearl stars - ideal for repairs, marriage, debt-collection, travel and moving. Other Wei days are second-tier.",
        },
        "Shen": {
            "officer": "Shou",
            "pillars": {
                "Jia-Shen": "excellent",
                "Bing-Shen": "fair",
                "Wu-Shen": "fair",
                "Geng-Shen": "dire",
                "Ren-Shen": "fair",
            },
            "good_for": ["burial", "marriage", "travel", "moving", "groundbreaking", "business"],
            "bad_for": [],
            "description_chinese": "卻犯到州星,用之招官司、損人口。惟甲申水潔淨之時,水土長生居申,利安葬、嫁娶、出行、入宅、動土、開張、起造、營為。主週年百日貴人自來提拔、諸事得意。庚申受死無氣。又煞入中宮,犯之主殺人,大凶。",
            "description_english": "Generally inauspicious - heralds legal entanglements and risk of harm to family. However, Water Qi on Jia Shen Days is pure with growth potential - ideal for burial, marriage, travel, moving, groundbreaking or business. Brings noble assistance throughout the year. Avoid Geng Shen Days as Qi is dead - extremely inauspicious.",
        },
        "You": {
            "officer": "Kai",
            "pillars": {
                "Yi-You": "excellent",
                "Ding-You": "auspicious",
                "Ji-You": "inauspicious",
                "Xin-You": "auspicious",
                "Gui-You": "auspicious",
            },
            "good_for": ["marriage", "moving", "renovation", "business", "burial"],
            "bad_for": [],
            "description_chinese": "乙酉天德,是葬日,宜嫁親、入宅、起造、開張,用之上吉,主增田宅、受職祿、光門户、奴婢義、僕自來投倚、諸事順遂。己酉九土鬼,安葬則可,不宜大用。餘酉日次吉。",
            "description_english": "Yi You Day has Heavenly Virtue 天德 and is a Burial Day 葬日 - ideal for marriage, moving, renovation or opening a business. Brings increase in wealth/assets and prospect of promotion. Remaining Rooster Days are reasonably useable. Ji You harbors Nine Earth Ghost Star - only for burial, avoid otherwise.",
        },
        "Xu": {
            "officer": "Bi",
            "pillars": {
                "Jia-Xu": "excellent",
                "Bing-Xu": "dire",
                "Wu-Xu": "dire",
                "Geng-Xu": "inauspicious",
                "Ren-Xu": "inauspicious",
            },
            "good_for": ["marriage", "business", "travel", "moving"],
            "bad_for": ["groundbreaking", "renovation", "burial"],
            "description_chinese": "火星。甲戌月德,宜嫁娶、開張、出行、入宅,但不利動土、起造、埋葬。丙戌、戊戌,百事凶敗。",
            "description_english": "Fire Star 火星 present throughout the month. Jia Xu Days have Monthly Virtue 月德 - ideal for marriage, opening a business, travel or moving. Unsuitable for groundbreaking, renovation and burial. Avoid major activities on Bing Xu and Wu Xu Days.",
        },
    },
    11: {},  # Zi month
    12: {},  # Chou month
}


def get_dong_gong_rating(month: int, day_branch: str, stem: str) -> str:
    """
    Get the auspiciousness rating for a specific pillar on a specific day.
    Returns: "excellent", "auspicious", "fair", "inauspicious", "dire", or None
    """
    if month not in DONG_GONG or not DONG_GONG[month]:
        return None
    if day_branch not in DONG_GONG[month]:
        return None
    pillar_key = f"{stem}-{day_branch}"
    pillars = DONG_GONG[month][day_branch].get("pillars", {})
    return pillars.get(pillar_key)


def get_dong_gong_day_info(month: int, day_branch: str) -> dict:
    """
    Get complete day information including officer, ratings, and descriptions.
    """
    if month not in DONG_GONG or not DONG_GONG[month]:
        return None
    return DONG_GONG[month].get(day_branch)
