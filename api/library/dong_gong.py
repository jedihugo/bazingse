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
        "overview": {
            "chinese": "月德丙、月恩丙、母倉亥子、天德合壬。",
            "monthly_virtue": "Bing",  # 月德
            "monthly_benevolence": "Bing",  # 月恩
            "motherly_storage": ["Hai", "Zi"],  # 母倉
            "heavenly_virtue": "Ren",  # 天德合
            "four_extinction": "li_chun",  # 四絕: 1 day before Li Chun 立春
            "three_killings": {
                "direction": "North",
                "starts_after": "yu_shui",  # 雨水 (Rain Water)
                "sectors": ["Hai", "Zi", "Chou"],  # 亥(NW3), 子(N2), 丑(NE1)
            },
            "notes": "For the Tiger 寅 (Yin) Month, the positive Monthly Virtue 月德 and Monthly Benevolence 月恩 Stars can be found on Bing 丙 Days. Pig 亥 (Hai) and Rat 子 (Zi) Days are accompanied by the auspicious Motherly Storage 母倉 Star. The Heavenly Virtue 天德 Star supports Ren 壬 Days. One day before Li Chun (Coming of Spring) is called the Four Extinction 四絕 Day. After Yu Shui (Rain Water), the Three Killings 三煞 occupies the North - avoid renovation or groundbreaking in Hai (NW3), Zi (N2), Chou (NE1) sectors.",
        },
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
    2: {
        "overview": {
            "chinese": "月德甲、月恩丁、母倉亥子、天德合己。",
            "monthly_virtue": "Jia",  # 月德
            "monthly_benevolence": "Ding",  # 月恩
            "motherly_storage": ["Hai", "Zi"],  # 母倉
            "heavenly_virtue": "Ji",  # 天德合
            "four_separation": "chun_fen",  # 四離: 1 day before Chun Fen 春分
            "three_killings": {
                "direction": "West",
                "starts_after": "jing_zhi",  # 驚蟄 (Awakening of Worms)
                "sectors": ["Shen", "You", "Xu"],  # 申(SW3), 酉(W2), 戌(NW1)
            },
            "notes": "During the Rabbit 卯 (Mao) Month, the Monthly Virtue 月德 Star presides over Jia 甲 Days, the Monthly Benevolence 月恩 Star is present on Ding 丁 Days. The Motherly Storage 母倉 Star accompanies Pig 亥 (Hai) and Rat 子 (Zi) Days. The Heavenly Virtue 天德 Star supports Ji 己 Days. One day before Spring Equinox (Chun Fen) is the Four Separation 四離 Day. After Jing Zhi (Awakening of Worms), the Three Killings 三煞 is in the West - avoid renovation or groundbreaking in Shen (SW3), You (W2), Xu (NW1) sectors.",
        },
        "Mao": {
            "officer": "Jian",
            "pillars": {
                "Yi-Mao": "inauspicious",
                "Ding-Mao": "inauspicious",
                "Ji-Mao": "inauspicious",
                "Xin-Mao": "inauspicious",
                "Gui-Mao": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["all_activities"],
            "description_chinese": "不宜用事,犯之損家長,及少房子孫,遭瘟疫,貧苦、哭泣重重。三、五年或遲至九年,橫禍敗亡。二月建卯日,為天地轉煞之日也。",
            "description_english": "This day is unsuitable for activities of any sort, for if violated, its harmful energies will wreak havoc on your loved ones at home – both young and old. They will be particularly susceptible to poor health and financial losses, with many other unfortunate events following suit. Worse still, the malevolent effects can last to a minimum of 3 years and a maximum of 9 years; with the possibility of even fatal accidents threatening domestic happiness. The Establish 建 (Jian) Day of the 2nd Month is an especially inauspicious day; also known as the 'Heaven & Earth Rotating Sha' 天地轉煞.",
        },
        "Chen": {
            "officer": "Chu",
            "pillars": {
                "Jia-Chen": "dire",
                "Bing-Chen": "inauspicious",
                "Wu-Chen": "dire",
                "Geng-Chen": "inauspicious",
                "Ren-Chen": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["moving", "marriage", "business"],
            "description_chinese": "不利移居、入宅、婚姻、開張、一切營為等事。犯之六十日至一百二十日內主招官司,損財敗田蠶,失產業。甲辰戊辰殺集中宮更凶。主三年內亡宅長、舊物作怪、火盜侵欺。",
            "description_english": "Avoid moving house (or moving into a new residence), tying the marital knot or launching a new commercial venture on this day. Violating this rule will result in lawsuits arising, as well as leakage of wealth and other material assets (including property) within a timeframe of 60 to 120 days. Avoid the Jia Chen 甲辰 and Wu Chen 戊辰 days in particular, as their effects are the worst. After all, you certainly do not wish to see a death of a beloved elderly member in your household, or a fire or armed robbery threatening the tranquility of your loved ones.",
        },
        "Si": {
            "officer": "Man",
            "pillars": {
                "Yi-Si": "fair",
                "Ding-Si": "fair",
                "Ji-Si": "fair",
                "Xin-Si": "fair",
                "Gui-Si": "fair",
            },
            "good_for": ["renovation", "travel", "business", "marriage", "moving"],
            "bad_for": ["groundbreaking"],
            "description_chinese": "天空、往亡日,不宜動土。如修造,百事俱吉,若在乾巽二宮起造皆吉,出行、開張、婚姻、入宅,內有黃羅、紫檀、田塘、庫貯,星蓋照,主年內家生貴子,田蠶興旺,永代吉昌。",
            "description_english": "This is a Sky Emptiness 天空 and therefore, Void Day. It is unsuitable to be used for groundbreaking ceremonies, although simple renovation works or adjustments will bear auspicious results. Similarly, any endeavors undertaken on the Qian 乾 and Xun 巽 palaces will yield positive outcomes. Certainly, by all means, go ahead and travel, launch a business, get married or move into your new residence, as these activities will enjoy the positive energies of the Yellow Spiral 黃羅, Purple Sandalwood 紫檀, Field 田塘 and Wealth Storage 庫貯 Stars. In addition, couples that are trying to conceive will find the ladies producing noble offspring within a year, and there will also be an increment in material assets such as property.",
        },
        "Wu": {
            "officer": "Ping",
            "pillars": {
                "Jia-Wu": "inauspicious",
                "Bing-Wu": "inauspicious",
                "Wu-Wu": "inauspicious",
                "Geng-Wu": "inauspicious",
                "Ren-Wu": "inauspicious",
            },
            "good_for": ["yang_tomb"],
            "bad_for": ["marriage", "renovation"],
            "description_chinese": "只宜作生基、如婚姻、修造。用之六十日、一百二十日內招官司、損人口、三、六、九年冷退。生基即壽木及生基也。",
            "description_english": "Such a date is only suitable to be applied to Yang Tombs 生基. It is unsuitable for marriages or renovation works. Activating the energies of this day will only result in lawsuits and legal entanglements arising within 60 to 120 days. More tragically, there might also be a decrease amongst your family members within the space of 3 to 6 years.",
        },
        "Wei": {
            "officer": "Ding",
            "pillars": {
                "Yi-Wei": "dire",
                "Ding-Wei": "inauspicious",
                "Ji-Wei": "inauspicious",
                "Xin-Wei": "inauspicious",
                "Gui-Wei": "auspicious",
            },
            "good_for": ["external_renovation"],
            "bad_for": ["marriage", "construction", "internal_renovation"],
            "description_chinese": "不利婚姻、起造,是陰宮主事,不宜向家內動作,一切屋外修為不妨。乙未乃白虎入中宮,更凶,犯之損人口。是月惟癸未一日乃水入秦州,因癸水當長生,相旺之際,內有黃羅、紫檀、天皇、地皇星蓋照,利人畜、添子孫、進田地、大吉。餘未日俱不利。",
            "description_english": "Marriages, construction works or internal renovations should be avoided at all costs when it comes to using this day. You may, however, engage in external renovations to your property. This date is also not suitable to undertake any significant private domestic affairs. Of all the inauspicious days, the Yi Wei 乙未 Day is the most detrimental, as it harbors the ominous White Tiger Star. The wellbeing of property occupants will be adversely affected if this particular day is violated. However, the Gui Wei Day is actually an auspicious day as it enjoys the protection of the Yellow Spiral 黃羅, Purple Sandalwood 紫檀, Heavenly Emperor 天皇 and Earthly Emperor 地皇 stars. Put simply, such a day augurs well for the residents of a household, descendant luck as well as asset and property gains. Do note however that the other Wei 未 (Goat) days are not auspicious.",
        },
        "Shen": {
            "officer": "Zhi",
            "pillars": {
                "Jia-Shen": "auspicious",
                "Bing-Shen": "auspicious",
                "Wu-Shen": "auspicious",
                "Geng-Shen": "inauspicious",
                "Ren-Shen": "auspicious",
            },
            "good_for": ["renovation", "groundbreaking", "burial", "marriage", "business", "moving", "travel"],
            "bad_for": [],
            "description_chinese": "有天、月二德,宜修造、動土、埋葬、婚姻、開張、入宅、出行等事。並有黃羅、紫檀、金銀庫樓、寶藏星蓋照,三、六、九年內大旺,添人口、生貴子、置田產,大吉。庚申日乃春正四廢,百事皆忌。",
            "description_english": "The Heavenly 天德 and Monthly Virtue 月德 Stars guard over this day, therefore making it a positive one to commence renovation or groundbreaking works, undertake burials, get married, launch a new business, move into a new residence or even travel. The auspicious bevy of stars governing this day include the Yellow Spiral 黃羅, Purple Sandalwood 紫檀, Gold & Silver Storage 金銀庫樓 and Precious Treasure 寶藏 stars, which bring about fantastic prosperity, an increase in the population, the birth of a noble child and tremendous material gains. In short, the recipient will enjoy affluence (in whatever perceived form) within 3, 6 or 9 years. However, the Geng Shen 庚申 Day is not a useable one since it is a Four Direct Day 正四廢.",
        },
        "You": {
            "officer": "Po",
            "pillars": {
                "Yi-You": "inauspicious",
                "Ding-You": "inauspicious",
                "Ji-You": "inauspicious",
                "Xin-You": "dire",
                "Gui-You": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["marriage", "renovation"],
            "description_chinese": "小紅砂、天賊星臨，不利婚姻、修造等事,犯之六十日、一百二十日內招官司、口舌、陰人劫、耗小口、疾病。辛酉正四廢,更凶,此日乃月破大凶之日。",
            "description_english": "The inauspicious Lesser Red Embrace 小紅砂 and Heavenly Thief Stars 天賊 are present on this day, rendering it unsuitable to tie the knot or renovate the house. Do not violate the harmful energies of these stars, as they are the harbingers of legal entanglements, disputes, robberies, people falling ill, children being endangered or even evil spirits and phantoms. In particular, look out for the Xin You 辛酉 Day, which is one of the Four Direct Days at its worst.",
        },
        "Xu": {
            "officer": "Wei",
            "pillars": {
                "Jia-Xu": "inauspicious",
                "Bing-Xu": "dire",
                "Wu-Xu": "inauspicious",
                "Geng-Xu": "inauspicious",
                "Ren-Xu": "dire",
            },
            "good_for": ["yang_tomb"],
            "bad_for": ["renovation", "marriage"],
            "description_chinese": "宜合板作生基。如修造、會親、婚姻,不利長房,先退田地、火盜侵欺。又云丙戌、壬戌,熬入中宮,更凶。",
            "description_english": "By all means, go ahead and make a Yang Tomb 生基 on this day. Refrain from renovating your property, proposing marriage or tying the knot on this day, though. If you happen to inadvertently activate its negative energies and also happen to be the 'eldest' in seniority of any kind within a household, be warned that a fire risk threatens your property. The worst days are the Bing Xu 丙戌 and Ren Xu 壬戌.",
        },
        "Hai": {
            "officer": "Cheng",
            "pillars": {
                "Yi-Hai": "auspicious",
                "Ding-Hai": "auspicious",
                "Ji-Hai": "auspicious",
                "Xin-Hai": "excellent",
                "Gui-Hai": "excellent",
            },
            "good_for": ["marriage", "business", "moving", "travel", "construction", "burial"],
            "bad_for": [],
            "description_chinese": "天喜,有天皇、地皇、黃羅、紫檀、玉堂、聚寶星蓋照,宜婚姻、開張、入宅、出行、起造、安葬、定控架,六十日、一百二十日內進財、貴人接引、謀事大吉。是月之辛亥、癸亥上吉。",
            "description_english": "The Sky Happiness 天喜, Heavenly Emperor 天皇, Earthly Emperor 地皇, Yellow Spiral 黃羅, Purple Sandalwood 紫檀, Jade Hall 玉堂 and Precious Convergence 聚寶 stars rule over this day, and their combined positive energies augur well for any endeavor. Hence, such days are good for marriages, launching a new business, moving house, travel, building a new residence and even burial services. With plenty of hard work, recipients will reap substantial returns-on-investment within 60 to 120 days, as well as assistance in times of need from noble people. Furthermore, nothing will remain bad or undesirable for a long time. Make the most of the Xin Hai 辛亥 and Gui Hai 癸亥 Days, as they are the best ones to have.",
        },
        "Zi": {
            "officer": "Shou",
            "pillars": {
                "Jia-Zi": "inauspicious",
                "Bing-Zi": "inauspicious",
                "Wu-Zi": "inauspicious",
                "Geng-Zi": "inauspicious",
                "Ren-Zi": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["marriage", "construction", "moving", "business"],
            "description_chinese": "忌婚姻、起造、入宅、開張,犯之三年內必退財、無進益,主是非、官訟、產業虛耗。",
            "description_english": "Do not get married, commence construction on a development, move into a new house or start a business on this day. Violating its harmful energies will only result in your wealth deteriorating and your loved ones pursuits proving to be futile over the next 3 years. Worse still, you will tend to attract gossip and legal problems as well as lose your material assets (such as properties) wherever you go and whatever you do.",
        },
        "Chou": {
            "officer": "Kai",
            "pillars": {
                "Yi-Chou": "inauspicious",
                "Ding-Chou": "dire",
                "Ji-Chou": "inauspicious",
                "Xin-Chou": "inauspicious",
                "Gui-Chou": "dire",
            },
            "good_for": [],
            "bad_for": ["renovation", "construction", "marriage", "meeting_relatives"],
            "description_chinese": "不利造作、裝修、婚姻、會親,犯之主田蠶不收、室有產厄、湯火之災。丁丑、癸丑,熬入中宮更凶,主官非、損人口、小人侵害。",
            "description_english": "A most unsuitable day for renovation or construction works, marriages or even meeting your future in-laws, as well as relatives. In addition, you also risk losing your house, investments, loved ones, wealth or even literally suffer fire-caused burns. Pay particular attention to the Ding Chou 丁丑 and Gui Chou 癸丑 days, as they herald the entry of negative stars into the Central Palace and hence Qi at its worst. In real-life situations, these pertain to lawsuits, physical injuries to residents and the interference of malicious, petty-minded people.",
        },
        "Yin": {
            "officer": "Bi",
            "pillars": {
                "Jia-Yin": "inauspicious",
                "Bing-Yin": "inauspicious",
                "Wu-Yin": "inauspicious",
                "Geng-Yin": "inauspicious",
                "Ren-Yin": "inauspicious",
            },
            "good_for": ["yang_tomb"],
            "bad_for": ["renovation", "groundbreaking", "marriage", "moving", "business"],
            "description_chinese": "黃砂,活曜星臨。宜合板、作生基。但不利修造、動土、婚姻、入宅、開張等事。是日乃五行無氣,平常之用則可,雖無大害,不用為妙。",
            "description_english": "With the presence of the Yellow Embrace 黃砂 Star, this is a suitable day for preparing a Yang Tomb. It is however unsuitable to carry out renovation or groundbreaking work, tie the matrimonial knot, enter a new house or launch a business. As this day does not have any Qi present within the Five Elements, use it for only unimportant events, and you will find any potential negative effects reduced to a minimum. In plain terms, this is neither a harmful nor beneficial day.",
        },
    },

    # ========================================
    # MONTH 3 - Dragon Month (三月 / 辰月)
    # ========================================
    3: {
        "overview": {
            "chinese": "月德壬、月恩庚、母倉亥子、天德合丁。",
            "monthly_virtue": "Ren",  # 月德
            "monthly_benevolence": "Geng",  # 月恩
            "motherly_storage": ["Hai", "Zi"],  # 母倉
            "heavenly_virtue": "Ding",  # 天德合
            "three_killings": {
                "direction": "South",
                "starts_after": "qing_ming",  # 清明 (Clear & Bright)
                "sectors": ["Si", "Wu", "Wei"],  # 巳(SE3), 午(S2), 未(SW1)
            },
            "notes": "For the Dragon 辰 (Chen) Month, the Monthly Virtue 月德 Star is present on Ren 壬 Days, the Monthly Benevolence 月恩 Star presides over Geng 庚 Days. The Motherly Storage 母倉 Star accompanies Pig 亥 (Hai) and Rat 子 (Zi) Days. The Heavenly Virtue 天德 Star supports Ding 丁 Days. After Qing Ming (Clear & Bright), the Three Killings 三煞 is in the South. At Gu Yu (Grain Rain), avoid renovation or groundbreaking in Si (SE3), Wu (S2), Wei (SW1) sectors.",
        },
        "Chen": {
            "officer": "Jian",
            "pillars": {
                "Jia-Chen": "dire",
                "Bing-Chen": "inauspicious",
                "Wu-Chen": "dire",
                "Geng-Chen": "inauspicious",
                "Ren-Chen": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["renovation", "burial", "marriage", "business"],
            "description_chinese": "有地網、勾絞,不利修造、安葬、婚姻、開張等事犯之主湯火驚傷,縱生男生女皆醜拙,惡陋無益。甲辰、戊辰,然入中宮,更凶,主三年內家破人亡。",
            "description_english": "The negative Earth Net 地網 and Grappling Hook 勾絞 Stars lord over the day – making it unsuitable for renovation, a marriage, burial or even launching a business. Once violated, these Stars spell disaster in the form of fire hazards, strained relationships and plain bad fortune. Avoid the particularly inauspicious Jia Chen 甲辰 and Wu Chen 戊辰 days, lest they cause domestic discord or a death in the family within 3 years.",
        },
        "Si": {
            "officer": "Chu",
            "pillars": {
                "Yi-Si": "inauspicious",
                "Ding-Si": "excellent",
                "Ji-Si": "auspicious",
                "Xin-Si": "inauspicious",
                "Gui-Si": "dire",
            },
            "good_for": ["renovation", "moving", "groundbreaking", "marriage"],
            "bad_for": ["burial"],
            "description_chinese": "丁巳宜修造、入宅、移居、動土、作用、婚姻等事,大吉。己巳進作、入宅等事亦吉,如犯,犯遠長不利用。辛巳忌日不宜用。癸巳大凶,又是十惡忌,亦不宜用。此皆必應之事也。",
            "description_english": "Use the Ding Si 丁巳 Day for renovation, moving house, groundbreaking ceremonies, marriages or other important events. The Ji Si 己巳 Day is particularly good to move into a new residence, but unsuitable for burials or groundbreaking ceremonies. The Yi Si 乙巳 or Gui Si 癸巳 Day contains the Ten Ferocious 十惡 Stars and is therefore unusable for any sort of activity.",
        },
        "Wu": {
            "officer": "Man",
            "pillars": {
                "Jia-Wu": "inauspicious",
                "Bing-Wu": "fair",
                "Wu-Wu": "inauspicious",
                "Geng-Wu": "dire",
                "Ren-Wu": "auspicious",
            },
            "good_for": ["general_activities"],
            "bad_for": ["burial"],
            "description_chinese": "天窮,甲午有土鬼。丙午干率,不能見吉。戊午有福鬼,敗亡。並犯重喪,即安葬不可用。庚午十惡日,不可宜。壬午天、月二德,用之次吉。",
            "description_english": "The Heavenly Fortune 天窮 Star is present but since it coincides with a Jia Wu 甲午 Day, the negative Earth Ghost 土鬼 Star is present as well. Luck on a Bing Wu 丙午 Day is average, as it is not supported by any auspicious stars. Its Wu Wu 戊午 counterpart is ruled by the inauspicious Mad Ghost 福鬼 and Void Loss 敗亡 Stars – both premonitions of death within the family and also unsuitable for burial days. Similarly, a Geng Wu 庚午 Day is considered one of the Ten Ferocious Days 十惡日, thereby making it unusable. Only the Ren Wu 壬午 Day enjoys the positive energies of the Heaven & Monthly Virtue Stars 天月二德, which make it an auspicious day.",
        },
        "Wei": {
            "officer": "Ping",
            "pillars": {
                "Yi-Wei": "dire",
                "Ding-Wei": "inauspicious",
                "Ji-Wei": "inauspicious",
                "Xin-Wei": "inauspicious",
                "Gui-Wei": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["all_activities"],
            "description_chinese": "與正五月相似,不宜用事,即小小修偕亦不利。若乙未更加凶煞,蓋煞值天,犯之損傷、疾病。",
            "description_english": "This day is unsuitable for all major or important activities. The Yi Wei 乙未 Day is the worst of all such days, since it is accompanied by negative stars.",
        },
        "Shen": {
            "officer": "Ding",
            "pillars": {
                "Jia-Shen": "auspicious",
                "Bing-Shen": "auspicious",
                "Wu-Shen": "inauspicious",
                "Geng-Shen": "inauspicious",
                "Ren-Shen": "excellent",
            },
            "good_for": ["gardening", "construction", "groundbreaking", "burial"],
            "bad_for": ["travel", "official_duties"],
            "description_chinese": "甲申、丙申、言斷等、豎土、空破、按柱等、安葬、大吉。宅中有天、月二德,天喜、地喜、金輿、龍輿、當照。是中十全大吉利。戊申天大利,亦凶。庚申正四廢,亦凶。壬申有天皇、空亡、敗亡,不宜出行、出軍。",
            "description_english": "The Jia Shen 甲申 and Bing Shen 丙申 Days are particularly suitable for gardening, construction (piling), groundbreaking or burial activities. In fact, the positive effects from undertaking such activities on these days will be seen in 2 to 3 years' time, where either your offspring will benefit or your personal wealth will increase. A Ren Shen 壬申 Day that is already blessed with the Heaven and Monthly Virtue Stars – coupled with the auspicious Yellow Spiral 黃螭, Purple Sandalwood 紫檀, Heavenly Emperor 天皇, Earthly Emperor 地皇 and Gold & Silver Storage 金銀庫 Stars – will see all endeavors producing highly positive outcomes! However, a Wu Shen 戊申 Day harbors the inauspicious Sky Chief 天皇, Void & Emptiness 空亡 and Void Loss 敗亡 Stars and should not be used for any sort of activity. The same principle applies to a Geng Shen 庚申 Day, which is one of the Four Direct Days 四直. Such a day is generally unsuitable for traveling, dispatching troops or assuming official duties.",
        },
        "You": {
            "officer": "Zhi",
            "pillars": {
                "Yi-You": "excellent",
                "Ding-You": "excellent",
                "Ji-You": "inauspicious",
                "Xin-You": "inauspicious",
                "Gui-You": "auspicious",
            },
            "good_for": ["renovation", "moving", "marriage", "business", "travel", "burial"],
            "bad_for": [],
            "description_chinese": "乙酉宜修造、入宅、婚姻、開張、出行等事,癸酉安葬大吉,丁酉安葬次吉。己酉有九土鬼,辛酉正四廢不宜用。",
            "description_english": "A Yi You 乙酉 Day is recommended to commence renovation works, enter a new house, get married, start a business or travel. Similarly, a Gui You 癸酉 Day is highly befitting for a burial service. If the burial cannot be done on a Gui You 癸酉 Day, then select a Ding You 丁酉 Day, which is the next-best option in the list of good burial days. Do note, however, that a Ji You 己酉 Day harbors the Nine Earth Ghost 九土鬼 Star while the Xin You 辛酉 Day is considered a Four Direct Day 正四廢 and therefore unusable.",
        },
        "Xu": {
            "officer": "Po",
            "pillars": {
                "Jia-Xu": "inauspicious",
                "Bing-Xu": "dire",
                "Wu-Xu": "inauspicious",
                "Geng-Xu": "inauspicious",
                "Ren-Xu": "dire",
            },
            "good_for": [],
            "bad_for": ["important_activities"],
            "description_chinese": "值月建冲煞,諸事不宜。丙戌、壬戌,然入中宮,惡凶。",
            "description_english": "This day clashes with the Month Branch. As such, avoid undertaking any important activities on such a day, especially Bing Xu 丙戌 and Ren Xu 壬戌 Days; which are the worst of such days.",
        },
        "Hai": {
            "officer": "Wei",
            "pillars": {
                "Yi-Hai": "auspicious",
                "Ding-Hai": "inauspicious",
                "Ji-Hai": "excellent",
                "Xin-Hai": "inauspicious",
                "Gui-Hai": "dire",
            },
            "good_for": ["education", "starting_school"],
            "bad_for": ["health_related"],
            "description_chinese": "天成,有凶煞。己亥,火星有文昌盖照,上學大吉,俸事次吉。乙亥僵府流建之期,除氣全盛,辛亥間所宜。丁亥乂鸞黑然,癸亥六甲弱日。據之,主絕人,又受死累,不可用。",
            "description_english": "The Heavenly Success 天成 and Violent Danger 凶煞 Stars govern this day, simultaneously. In addition, a Ji Hai 己亥 Day is influenced by both the auspicious Fire Star 火星 and Literary Arts 文昌 Stars. Accordingly, such circumstances make this Ji Hai Day a good day to start a pupil's studies at a new school. Other endeavors will also reap positive rewards. If it is not possible to begin such an endeavor on a Ji Hai 己亥 Day, then select the next best choice a Yi Hai 乙亥 Day. Do note, however, that the Qi of a Xin Hai 辛亥 Day is overly Yin in nature. Likewise, a Ding Hai 丁亥 Day contains the ominous Black Sha 黑煞 while a Gui Hai 癸亥 Day is a Six Jia Weakness Day 六甲弱日. Accordingly, the Qi of the Elements present during these days are weak and insufficient. Worse still, such Qi denote death and failing health. Avoid using these days at all costs.",
        },
        "Zi": {
            "officer": "Cheng",
            "pillars": {
                "Jia-Zi": "auspicious",
                "Bing-Zi": "auspicious",
                "Wu-Zi": "auspicious",
                "Geng-Zi": "auspicious",
                "Ren-Zi": "fair",
            },
            "good_for": ["minor_activities"],
            "bad_for": ["major_activities", "business", "marriage", "moving"],
            "description_chinese": "黃砂、天喜,壬子端有天、月二德,乃一白主事、木打寶瓶,緣是北方冰浴之地,福力威減,但小小修備為則可。若開張、修置及婚姻等吉,用之就見日。",
            "description_english": "The Yellow Embrace 黃砂 and Sky Happiness 天喜 stars preside over this day. But before celebrating, you might want to know that the Ren Zi 壬子 Day has the Northern Mu Yu Bath location – where Elemental Qi is very weak and prosperous Qi minimal – alongside the Heavenly and Monthly Virtue 天月二德 Noble Stars! This is by no means anything ominous or inauspicious; it merely means that the Ren Zi Day can still be used for activities of less importance. Just don't use this day for significant activities, due to its inadequate Qi. If you choose to ignore this advice, then be prepared for water-related hazards threatening your family. Likewise, launching of a major new business, travel, moving into a new house and getting married will result in the day (and possibly, the event) ending on a very sour note!",
        },
        "Chou": {
            "officer": "Shou",
            "pillars": {
                "Yi-Chou": "inauspicious",
                "Ding-Chou": "dire",
                "Ji-Chou": "inauspicious",
                "Xin-Chou": "inauspicious",
                "Gui-Chou": "dire",
            },
            "good_for": [],
            "bad_for": ["renovation", "marriage", "moving"],
            "description_chinese": "小紅砂、天賊、丁丑、癸丑、然入中宮,不利修造、婚姻、入宅等事,犯之主損財、瘧痰、爭論、是非,凶,餘丑亦不吉,防小人刑害。",
            "description_english": "The Lesser Red Embrace 小紅砂 and Heavenly Thief 天賊 stars going this day. Avoid Ding Chou 丁丑 and Gui Chou 癸丑 Days when it comes to renovation, tying the knot or entering a house for the first time. Breaking this rule will lead to a loss in wealth, ailments and legal entanglements. The other Chou 丑 (Ox) days are not that inauspicious, but they are still powerful enough to attract malicious, petty-minded people.",
        },
        "Yin": {
            "officer": "Kai",
            "pillars": {
                "Jia-Yin": "fair",
                "Bing-Yin": "fair",
                "Wu-Yin": "excellent",
                "Geng-Yin": "fair",
                "Ren-Yin": "excellent",
            },
            "good_for": ["significant_events", "yang_tomb", "property", "promotion"],
            "bad_for": [],
            "description_chinese": "天赦。戊寅,天救用之吉。是救用及合板作生基,用之遷四地、生貴子、聰宮發,上吉。但有六不成六之終,用之終難不利,甚逢之。",
            "description_english": "Heavenly Thief 天赦 star present. The Wu Yin 戊寅 Heavenly Pardon 天救 star, and can therefore be used for significant events and activities. Similarly, a Ren Yin 壬寅 Day contains the Heavenly and Monthly Virtue 天月二德 stars is a good one, which promises material and property gains, the birth of a noble son and even a promotion. However, the other Tiger 寅 (Yin) days do not share the same potential as the Ren Yin 壬寅 Day.",
        },
        "Mao": {
            "officer": "Bi",
            "pillars": {
                "Yi-Mao": "inauspicious",
                "Ding-Mao": "inauspicious",
                "Ji-Mao": "inauspicious",
                "Xin-Mao": "inauspicious",
                "Gui-Mao": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["renovation", "marriage", "burial", "moving"],
            "description_chinese": "不宜造作、婚姻、堅墓、入宅等事。犯之損傷疾凶、不宜造作、婚姻、埋葬、入宅等事,犯之損傷、疾病、冷退,凶,百事不宜。",
            "description_english": "This day is unsuitable for renovations, marriages, burials or moving into a new residence. Violating this protocol will only result in family members and loved ones getting injured or falling ill.",
        },
    },

    # ========================================
    # MONTH 4 - Snake Month (四月 / 巳月)
    # ========================================
    4: {
        "overview": {
            "chinese": "月德庚、月恩巳、天德合丙。",
            "monthly_virtue": "Geng",  # 月德
            "monthly_benevolence": "Si",  # 月恩
            "heavenly_virtue": "Bing",  # 天德合
            "four_extinction": "li_xia",  # 四絕: 1 day before Li Xia 立夏
            "three_killings": {
                "direction": "East",
                "starts_after": "xiao_man",  # 小滿 (Small Sprout)
                "sectors": ["Yin", "Mao", "Chen"],  # 寅(NE3), 卯(E2), 辰(SE1)
            },
            "notes": "During the Snake 巳 (Si) Month, Geng 庚 Days are accompanied by the Monthly Virtue 月德 Star, and Snake 巳 (Si) Days are accompanied by the Monthly Benevolence 月恩 Star. The Heavenly Virtue 天德 Star supports Bing 丙 Days. One day before Li Xia (Coming of Summer) is the Four Extinction 四絕 Day. After Xiao Man (Small Sprout), the Three Killings 三煞 occupies the East - avoid renovation or groundbreaking in Yin (NE3), Mao (E2), Chen (SE1) sectors.",
        },
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
        "overview": {
            "chinese": "月德丙、月恩戊、母倉寅卯、天德合寅。",
            "monthly_virtue": "Bing",  # 月德
            "monthly_benevolence": "Wu",  # 月恩
            "motherly_storage": ["Yin", "Mao"],  # 母倉
            "heavenly_virtue": "Yin",  # 天德合
            "four_separation": "xia_zhi",  # 四離: 1 day before Xia Zhi 夏至
            "three_killings": {
                "direction": "North",
                "starts_after": "mang_zhong",  # 芒種 (Planting of Thorny Crops)
                "sectors": ["Hai", "Zi", "Chou"],  # 亥(NW3), 子(N2), 丑(NE1)
            },
            "notes": "In the Horse 午 (Wu) Month, Bing 丙 Days are supported by the Monthly Virtue 月德 Star, Wu 戊 Days are accompanied by the Monthly Benevolence 月恩 Star. The Motherly Storage 母倉 Star exerts positive influence on Tiger 寅 (Yin) and Rabbit 卯 (Mao) Days. The Heavenly Virtue 天德 Star combines with Tiger 寅 (Yin) Days. One day before Summer Solstice (Xia Zhi) is the Four Separation 四離 Day. After Mang Zhong (Planting of Thorny Crops), the Three Killings 三煞 is in the North - avoid groundbreaking in Hai (NW3), Zi (N2), Chou (NE1) sectors.",
        },
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
        "overview": {
            "chinese": "月德甲、月恩辛、母倉寅卯。天德合己。",
            "monthly_virtue": "Jia",  # 月德
            "monthly_benevolence": "Xin",  # 月恩
            "motherly_storage": ["Yin", "Mao"],  # 母倉
            "heavenly_virtue": "Ji",  # 天德合
            "three_killings": {
                "direction": "West",
                "starts_after": "xiao_shu",  # 小暑 (Lesser Heat)
                "sectors": ["Shen", "You", "Xu"],  # 申(SW3), 酉(W2), 戌(NW1)
            },
            "notes": "During the Goat 未 (Wei) Month, the Monthly Virtue 月德 Star is present on Jia 甲 Days, the Monthly Benevolence 月恩 Star is present on Xin 辛 Days. The Motherly Storage 母倉 Star exerts auspicious influence on Tiger 寅 (Yin) and Rabbit 卯 (Mao) Days. The Heavenly Virtue 天德 Star combines with Ji 己 Days. After Xiao Shu (Lesser Heat), the Three Killings 三煞 is in the West. At Da Shu (Greater Heat), avoid renovation or groundbreaking in Shen (SW3), You (W2), Xu (NW1) sectors.",
        },
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
    7: {
        "overview": {
            "chinese": "月德壬、月恩壬、母倉辰戌丑未。天德合戊。",
            "monthly_virtue": "Ren",  # 月德
            "monthly_benevolence": "Ren",  # 月恩
            "motherly_storage": ["Chen", "Xu", "Chou", "Wei"],  # 母倉
            "heavenly_virtue": "Wu",  # 天德合
            "four_extinction": "li_qiu",  # 四絕: 1 day before Li Qiu 立秋
            "three_killings": {
                "direction": "South",
                "starts_after": "chu_shu",  # 處暑 (Heat Ends)
                "sectors": ["Si", "Wu", "Wei"],  # 巳(SE3), 午(S2), 未(SW1)
            },
            "notes": "In the Monkey 申 (Shen) Month, the Monthly Virtue 月德 and Monthly Benevolence 月恩 Stars both preside over Ren 壬 Days. The Motherly Storage 母倉 Star lords over Dragon 辰 (Chen), Dog 戌 (Xu), Ox 丑 (Chou) and Goat 未 (Wei) Days. The Heavenly Virtue 天德 Star supports Wu 戊 Days. One day before Li Qiu (Coming of Autumn) is the Four Extinction 四絕 Day. After Chu Shu (Heat Ends), the Three Killings 三煞 is in the South - avoid groundbreaking in Si (SE3), Wu (S2), Wei (SW1) sectors.",
        },
        "Shen": {
            "officer": "Jian",
            "pillars": {
                "Jia-Shen": "auspicious",
                "Bing-Shen": "inauspicious",
                "Wu-Shen": "excellent",
                "Geng-Shen": "inauspicious",
                "Ren-Shen": "auspicious",
            },
            "good_for": ["burial"],
            "bad_for": ["most_activities"],
            "description_chinese": "戊申為天赦,甲申、壬申為比和之日,只宜埋葬。然月建上凶,不可用。庚申然入中宮,丙申五行無氣,更主凶。",
            "description_english": "The Wu Shen 戊申 Day contains the auspicious Heavenly Pardon 天赦 Star, while Jia Shen 甲申 and Ren Shen 壬申 Days are equally suitable for burials. Note, however, that Sha (Killing) Qi enters the Central Palace on a Geng Shen 庚申 Day and on a Bing Shen 丙申 Day, the Five Elements are devoid of any Qi. As such, using any of these days will only result in disappointment and catastrophe.",
        },
        "You": {
            "officer": "Chu",
            "pillars": {
                "Yi-You": "auspicious",
                "Ding-You": "inauspicious",
                "Ji-You": "inauspicious",
                "Xin-You": "dire",
                "Gui-You": "inauspicious",
            },
            "good_for": ["land_clearing", "burial", "construction", "repairs", "travel", "business", "moving"],
            "bad_for": [],
            "description_chinese": "往亡。乙酉無凶星,開山、斬草、安葬、興工、定礎、搭架、修方、造作、出行、開張、入宅、移居,次吉。己酉九土鬼,丁酉凶敗,癸酉伏劍之金,北方黑煞將軍之氣,損傷、凶惡。辛酉天地轉煞,正四廢,凶。",
            "description_english": "This is considered an Emptiness 往亡 Day. However, there are no negative stars affecting Yi You 乙酉 Days and hence, they may be used for opening or exploring new land, quarrying works, landscaping projects, burial, starting construction work, building a new house, repairs, travel, opening a business, entering a new house or migrating. The Ji You 己酉 Day is marked by the presence of the Nine Earth Ghost 九土鬼 Star, while Ding You 丁酉 and Gui You 癸酉 Days should be avoided, especially as the latter harbors 'dulled' Metal Sword Qi. Such a combination only spells harm and disastrous outcomes. In addition, a Xin You 辛酉 Day is also known as a Pure Direct Day 正四廢, containing Heaven and Earth Drilling Sha 天地轉煞 – making it an inauspicious day for activities or endeavors.",
        },
        "Xu": {
            "officer": "Man",
            "pillars": {
                "Jia-Xu": "inauspicious",
                "Bing-Xu": "inauspicious",
                "Wu-Xu": "inauspicious",
                "Geng-Xu": "inauspicious",
                "Ren-Xu": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["all_activities", "legal_matters", "health"],
            "description_chinese": "天富、天賊。丙戌、壬戌,朱雀、勾絞、白虎入中宮,用之主招官司、是非、家門衰敗、損人口、疾病纏綿,一起一倒,不離床席,大凶,忌之。",
            "description_english": "While the Heavenly Fortune 天富 and Heavenly Thief 天賊 Stars are simultaneously present, Bing Xu 丙戌 and Ren Xu 壬戌 Days also harbor the negative Red Phoenix 朱雀, Grappling Hook 勾絞 and White Tiger 白虎 Stars. The presence of such stars forewarn of legal entanglements, hassles and malicious gossip, as well as worsening health amongst family members. As such, do not use these days at all costs.",
        },
        "Hai": {
            "officer": "Ping",
            "pillars": {
                "Yi-Hai": "inauspicious",
                "Ding-Hai": "inauspicious",
                "Ji-Hai": "inauspicious",
                "Xin-Hai": "inauspicious",
                "Gui-Hai": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["all_activities", "legal_matters", "accidents"],
            "description_chinese": "腾蛇缠绕,损人口、遭官司、口舌、横祸,凶。",
            "description_english": "The inauspicious Surging Snake 腾蛇 Star bedevils this day, resulting in family members being easily injured, legal problems arising, accidents and mishaps occurring and the interference of petty-minded people. This is a very inauspicious day and should therefore be avoided.",
        },
        "Zi": {
            "officer": "Ding",
            "pillars": {
                "Jia-Zi": "inauspicious",
                "Bing-Zi": "excellent",
                "Wu-Zi": "auspicious",
                "Geng-Zi": "auspicious",
                "Ren-Zi": "inauspicious",
            },
            "good_for": ["renovation", "burial", "marriage", "business", "travel", "moving", "ground_digging"],
            "bad_for": [],
            "description_chinese": "丙子潔净之水,又遇旺地,值黃羅、紫檀星蓋照,宜修造、安葬、娶親、開張、出行、入宅、興工、動土,主子孫繁昌富盛,大吉。庚子、戊子次吉。壬子木打寶瓶水,不逢時,乃葉落之木。甲子自死之金,此值秋金,殺氣方盛,不宜用也。",
            "description_english": "Water Qi is pure and serene on Bing Zi 丙子 Days, therefore resulting in prosperous Qi being produced. The presence of the auspicious Yellow Spiral 黃羅 and Purple Sandalwood 紫檀 Stars enhance the positive energies of these days, making them suitable for renovation, burial, proposing marriage, opening a business, travel, moving into a new house, and ground-digging works. Used well, one's children and descendants will prosper accordingly, due to the extremely auspicious energies present. Meanwhile, Geng Zi 庚子 and Wu Zi 戊子 Days may also be considered as second-best options. However, the Qi is neither conducive nor good on Ren Zi 壬子 Days. In fact, the Qi on Jia Zi 甲子 Days is extremely weak and totally unusable.",
        },
        "Chou": {
            "officer": "Zhi",
            "pillars": {
                "Yi-Chou": "inauspicious",
                "Ding-Chou": "dire",
                "Ji-Chou": "inauspicious",
                "Xin-Chou": "inauspicious",
                "Gui-Chou": "dire",
            },
            "good_for": [],
            "bad_for": ["all_activities", "wealth", "family"],
            "description_chinese": "有朱雀,勾絞腾蛇,白虎之然不宜用事。犯之主退財、傷人口。丁丑癸丑然入中宮,不可用。乃受命之日也。",
            "description_english": "The presence of the negative Red Phoenix 朱雀 and Grappling Hook 勾絞 Stars only serve to worsen the adversity of the Snake 腾蛇 and White Tiger 白虎 Sha Qi. Inadvertently tapping into such an inauspicious combination will only result in loss of wealth or worse still, a death in the family. In particular, avoid Ding Chou 丁丑 and Gui Chou 癸丑 Days for all important activities or endeavors, for their harmful energies will only cause people to be hurt or wealth to be lost.",
        },
        "Yin": {
            "officer": "Po",
            "pillars": {
                "Jia-Yin": "dire",
                "Bing-Yin": "inauspicious",
                "Wu-Yin": "inauspicious",
                "Geng-Yin": "inauspicious",
                "Ren-Yin": "auspicious",
            },
            "good_for": ["burial"],
            "bad_for": ["important_activities", "legal_matters", "wealth"],
            "description_chinese": "甲寅正四廢,凶。庚寅、戊寅、丙寅皆不吉,諸事不宜,主官司、退財、人口啾唧。惟壬寅一日有月德,只利安葬也。",
            "description_english": "The Jia Yin 甲寅 Day is also one of the Four Direct 正四廢 Days. It is an inauspicious day, on which any important endeavors or activities should not be conducted. Furthermore, Geng Yin 庚寅, Wu Yin 戊寅 and Bing Yin 丙寅 Days are only unsuitable, as they display a tendency to attract legal issues and leakage of wealth. Only the Ren Yin 壬寅 Day, accompanied by the presence of the Monthly Virtue 月德 Star, is suitable for burials.",
        },
        "Mao": {
            "officer": "Wei",
            "pillars": {
                "Yi-Mao": "dire",
                "Ding-Mao": "excellent",
                "Ji-Mao": "auspicious",
                "Xin-Mao": "auspicious",
                "Gui-Mao": "excellent",
            },
            "good_for": ["renovation", "marriage", "ground_digging", "construction", "business", "travel", "appointments"],
            "bad_for": [],
            "description_chinese": "乙卯正四廢,凶。癸卯、丁卯有天德、黃羅、紫檀、金銀庫樓、玉堂聚寶星蓋照,宜造、婚姻、嫁娶、興工、動土、定礎、搭架、開張、出行、作倉庫、牛羊欄圈、主家業昌盛,人口興旺、生貴子、進横財、主家富貴雍穆。餘卯日次吉。",
            "description_english": "The Yi Mao 乙卯 Day is also known as one of the Four Direct 正四廢 Days, and therefore a negative day. However, Gui Mao 癸卯 and Ding Mao 丁卯 Days enjoy the support of the auspicious Heavenly Virtue 天德, Yellow Spiral 黃羅, Purple Sandalwood 紫檀, Golden Ingot 金銀, Storage 庫樓, Jade Hall 玉堂 and Converging Treasure 聚寶 Stars. The presence of these stars makes such days suitable for renovation, marriage, ground-digging, building or moving into a new house, launching a business, travel, or appointing a new officer or supervisor. Used properly, one will see one's family expanding in numbers, with the birth of noble children as well as an increase in wealth. All the other Mao 卯 (Rabbit) days are considered to be 'secondarily' useful for important endeavors or activities.",
        },
        "Chen": {
            "officer": "Cheng",
            "pillars": {
                "Jia-Chen": "inauspicious",
                "Bing-Chen": "auspicious",
                "Wu-Chen": "inauspicious",
                "Geng-Chen": "auspicious",
                "Ren-Chen": "excellent",
            },
            "good_for": ["burial", "minor_activities"],
            "bad_for": ["large_scale_activities"],
            "description_chinese": "天喜。壬辰月德,庚辰、丙辰三日皆是葬日,次吉,俱不宜大用。戊辰、甲辰白虎入中宮,犯之三、六、九年萧索遭凶。",
            "description_english": "With the presence of the Sky Happiness 天喜 Star, accompanied by the Monthly Virtue Noble 月德 Star, the Ren Chen 壬辰 Day is a fairly auspicious one. In fact, Geng Chen 庚辰 and Bing Chen 丙辰 Days are also reasonably auspicious days, and can be used for endeavors or activities of lesser significance. They should not, however, be used for large-scale, important activities. Wu Chen 戊辰 and Jia Chen 甲辰 Days are unfortunately accompanied by the presence of the White Tiger 白虎 Star, which renders them inauspicious if used. Ill-fortune and poor luck will befall anyone who uses these days within a period of 3, 6 or 9 years.",
        },
        "Si": {
            "officer": "Shou",
            "pillars": {
                "Yi-Si": "inauspicious",
                "Ding-Si": "inauspicious",
                "Ji-Si": "inauspicious",
                "Xin-Si": "inauspicious",
                "Gui-Si": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["all_activities", "legal_matters", "family"],
            "description_chinese": "小紅砂。有朱雀、勾絞、腾蛇,諸事不利,犯之招官司、損人口,大凶。",
            "description_english": "While the Lesser Red Embrace 小紅砂 Star presides over the day, the Red Phoenix 朱雀, Grappling Hook 勾絞 and Surging Snake 腾蛇 Stars are also present; therefore making it unsuitable for all activities or endeavors of importance. Do not utilize these days for any activity or endeavor of importance, lest legal problems arise and family members are more susceptible or prone to injury.",
        },
        "Wu": {
            "officer": "Kai",
            "pillars": {
                "Jia-Wu": "auspicious",
                "Bing-Wu": "excellent",
                "Wu-Wu": "excellent",
                "Geng-Wu": "inauspicious",
                "Ren-Wu": "excellent",
            },
            "good_for": ["visiting_relatives", "marriage", "renovation", "burial", "business", "travel", "moving", "ground_digging"],
            "bad_for": [],
            "description_chinese": "黃砂。壬午月德,丙午、戊午三日,利會親、嫁娶、修造、埋葬、開張、出行、入宅、動土諸事,六十日、一百二十日內招財、獲福、田產興旺、貴人接引、人畜安康。餘午次吉,惟庚午大凶。",
            "description_english": "While the Yellow Embrace 黃砂 Star is present, Ren Wu 壬午 Days also enjoy the positive energies of the Monthly Virtue 月德 Star, with Bing Wu 丙午 and Wu Wu 戊午 Days equally useable. Accordingly, such days are ideal for visiting relatives (customarily for proposing marriage), tying the knot, renovation, burial, business openings, travel, moving into a new house and ground-digging. The useful energies present on these days will bring about an increase in material wealth within 60 to 120 days, and there will also be no shortage of help from noble people in times of need. Jia Wu 甲午 Days may also be used, but Geng Wu 庚午 Days contain extremely inauspicious stars and should be avoided at all costs.",
        },
        "Wei": {
            "officer": "Bi",
            "pillars": {
                "Yi-Wei": "inauspicious",
                "Ding-Wei": "auspicious",
                "Ji-Wei": "excellent",
                "Xin-Wei": "auspicious",
                "Gui-Wei": "excellent",
            },
            "good_for": ["renovation", "moving", "construction", "business", "travel"],
            "bad_for": [],
            "description_chinese": "天成、天賊,癸未火星天德,己未火星,宜修造、入宅、定礎、搭架、出行、開張次吉。辛未、丁未小用亦次吉。惟乙未然入中宮,若在庭中釘丁、打物、喧嘩、吵叫等類,驚動神然,刑於家長,損傷頭目手足,大凶,主血光湯火之厄、飛來禍事、小人侵害、官司、口舌纏綿。凡然入中宮之日俱宜仿此選忌。",
            "description_english": "The Heavenly Success 天成 and Heavenly Thief 天賊 Stars exert their influence, and on Gui Wei 癸未 Days, the Fire Star 火星 and Heavenly Virtue 天德 Stars add their own effects. Accordingly, Ji Wei 己未 Day is ideal for renovation or moving into a new house. However, Xin Wei 辛未 and Ding Wei 丁未 Days can only be used for smaller-scale activities. Take note that on Yi Wei 乙未 Days, Sha (Killing) Qi pierces the very heart of the day, and hence such days should be avoided. Those who ignore this warning will encounter a blood-shedding disaster or worsening health, or find that elderly family members get hurt easily. From a materialistic perspective, they will also tend to lose their personal belongings more easily.",
        },
    },
    # ========================================
    # MONTH 8 - Rooster Month (八月 / 酉月)
    # ========================================
    8: {
        "overview": {
            "chinese": "月德庚、月恩癸、母倉辰戌丑未。天德合亥。",
            "monthly_virtue": "Geng",  # 月德
            "monthly_benevolence": "Gui",  # 月恩
            "motherly_storage": ["Chen", "Xu", "Chou", "Wei"],  # 母倉
            "heavenly_virtue": "Hai",  # 天德合
            "four_separation": "qiu_fen",  # 四離: 1 day before Qiu Fen 秋分
            "three_killings": {
                "direction": "East",
                "starts_after": "bai_lu",  # 白露 (White Dew)
                "sectors": ["Yin", "Mao", "Chen"],  # 寅(NE3), 卯(E2), 辰(SE1)
            },
            "notes": "In the Rooster 酉 (You) Month, the Monthly Virtue 月德 Star is present on Geng 庚 Days, the Monthly Benevolence 月恩 Star presides over Gui 癸 Days. The Motherly Storage 母倉 Star exerts positive influence on Dragon 辰 (Chen), Dog 戌 (Xu), Ox 丑 (Chou) and Goat 未 (Wei) Days. The Heavenly Virtue 天德 Star combines with Pig 亥 (Hai) Days. One day before Qiu Fen (Autumn Equinox) is the Four Separation 四離 Day. After Bai Lu (White Dew), the Three Killings 三煞 is in the East - avoid groundbreaking in Yin (NE3), Mao (E2), Chen (SE1) sectors.",
        },
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
        "overview": {
            "chinese": "月德丙、月恩庚、母倉辰戌丑未。天德合辛。",
            "monthly_virtue": "Bing",  # 月德
            "monthly_benevolence": "Geng",  # 月恩
            "motherly_storage": ["Chen", "Xu", "Chou", "Wei"],  # 母倉
            "heavenly_virtue": "Xin",  # 天德合
            "three_killings": {
                "direction": "North",
                "starts_after": "han_lu",  # 寒露 (Cold Dew)
                "sectors": ["Hai", "Zi", "Chou"],  # 亥(NW3), 子(N2), 丑(NE1)
            },
            "notes": "In the Dog 戌 (Xu) Month, Bing 丙 Days are accompanied by the Monthly Virtue 月德 Star, Geng 庚 Days are accompanied by the Monthly Benevolence 月恩 Star. The Motherly Storage 母倉 Star supports Dragon 辰 (Chen), Dog 戌 (Xu), Ox 丑 (Chou) and Goat 未 (Wei) Days. The Heavenly Virtue 天德 Star combines with Xin 辛 Days. After Han Lu (Cold Dew), the Three Killings 三煞 is in the North. At Shuang Jiang (Frosting), avoid renovation or groundbreaking in Hai (NW3), Zi (N2), Chou (NE1) sectors.",
        },
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
        "overview": {
            "chinese": "月德甲、月恩乙、母倉申酉。天德合庚。",
            "monthly_virtue": "Jia",  # 月德
            "monthly_benevolence": "Yi",  # 月恩
            "motherly_storage": ["Shen", "You"],  # 母倉
            "heavenly_virtue": "Geng",  # 天德合
            "four_extinction": "li_dong",  # 四絕: 1 day before Li Dong 立冬
            "three_killings": {
                "direction": "West",
                "starts_after": "xiao_xue",  # 小雪 (Lesser Snow)
                "sectors": ["Shen", "You", "Xu"],  # 申(SW3), 酉(W2), 戌(NW1)
            },
            "notes": "In the Pig 亥 (Hai) Month, the Monthly Virtue 月德 Star presides over Jia 甲 Days, the Monthly Benevolence 月恩 Star exerts auspicious influence on Yi 乙 Days. The Motherly Storage 母倉 Star supports Monkey 申 (Shen) and Rooster 酉 (You) Days. The Heavenly Virtue 天德 Star combines with Geng 庚 Days. One day before Li Dong (Coming of Winter) is the Four Extinction 四絕 Day. After Xiao Xue (Lesser Snow), the Three Killings 三煞 is in the West - avoid renovation or groundbreaking in Shen (SW3), You (W2), Xu (NW1) sectors.",
        },
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
    # ========================================
    # MONTH 11 - Rat Month (十一月 / 子月)
    # ========================================
    11: {
        "overview": {
            "chinese": "月德壬、月恩甲、母倉申酉。天德合申。",
            "monthly_virtue": "Ren",  # 月德
            "monthly_benevolence": "Jia",  # 月恩
            "motherly_storage": ["Shen", "You"],  # 母倉
            "heavenly_virtue": "Shen",  # 天德合
            "four_separation": "dong_zhi",  # 四離: 1 day before Dong Zhi 冬至
            "three_killings": {
                "direction": "South",
                "starts_after": "da_xue",  # 大雪 (Greater Snow)
                "sectors": ["Si", "Wu", "Wei"],  # 巳(SE3), 午(S2), 未(SW1)
            },
            "notes": "In the Rat 子 (Zi) Month, Ren 壬 Days are accompanied by the Monthly Virtue 月德 Star, Jia 甲 Days are presided over by the Monthly Benevolence 月恩 Star. The Motherly Storage 母倉 Star exerts positive influence on Monkey 申 (Shen) and Rooster 酉 (You) Days. Monkey Days also enjoy the support of the Heavenly Virtue 天德 Star. One day before Dong Zhi (Winter Solstice) is the Four Abandonment 四離 Day. After Da Xue (Greater Snow), the Three Killings 三煞 is in the South - avoid groundbreaking in Si (SE3), Wu (S2), Wei (SW1) sectors.",
        },
        "Zi": {
            "officer": "Jian",
            "pillars": {
                "Jia-Zi": "inauspicious",
                "Bing-Zi": "inauspicious",
                "Wu-Zi": "inauspicious",
                "Geng-Zi": "inauspicious",
                "Ren-Zi": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["all_activities", "marriage", "business", "construction"],
            "description_chinese": "火星。甲子天赦日進神，惜被月建沖破，用之主官司、破敗，諸天赦不合之日也。丙子雖值水旺之時，退神為地煞，亦與月建相沖，其時水斷溪澗力，亦甚減，終是吉中凶兆，主先進益後禍害，正冰消瓦裂之時也。",
            "description_english": "The Fire Star 火星 present throughout the Day. While Jia Zi 甲子 Days are also marked by the presence of the Heavenly Pardon 天赦 Star, any positive effects are unfortunately negated by the inauspicious Month Establish Star 月建. Hence, using a Jia Zi Day will result in legal issues and other hassles. Similarly, while Water Qi is prosperous on Bing Zi 丙子 Days, the presence of negative stars causes all positive energies to be neutralized - particularly by the Month Establish 月建 Star. As these positive Qi are significantly stifled, using such days will produce problematic or disastrous outcomes, even though things may appear positive initially.",
        },
        "Chou": {
            "officer": "Chu",
            "pillars": {
                "Yi-Chou": "excellent",
                "Ding-Chou": "auspicious",
                "Ji-Chou": "auspicious",
                "Xin-Chou": "auspicious",
                "Gui-Chou": "auspicious",
            },
            "good_for": ["marriage", "renovation", "travel", "business", "groundbreaking", "cutting_trees", "quarrying"],
            "bad_for": [],
            "description_chinese": "天瘟。乙丑金墓之鄉，宜嫁娶、起造、出行、開張、動土、伐樹、開山，有吉星蓋照，主貴人接引、謀望遂意。餘丑次吉。",
            "description_english": "The presence of the Heavenly Delicate 天瘟 Star makes Yi Chou 乙丑 Days especially ideal for marriage, renovation, travel, opening a business, groundbreaking, cutting trees, or quarrying or excavating mountains. Such a combination also indicates the availability of assistance from noble people. The remaining Chou 丑 (Ox) Days are only secondary in terms of usability and auspiciousness.",
        },
        "Yin": {
            "officer": "Man",
            "pillars": {
                "Jia-Yin": "fair",
                "Bing-Yin": "auspicious",
                "Wu-Yin": "excellent",
                "Geng-Yin": "auspicious",
                "Ren-Yin": "excellent",
            },
            "good_for": ["marriage", "moving", "renovation", "burial", "travel", "business"],
            "bad_for": ["groundbreaking"],
            "description_chinese": "黃砂、天富。是土瘟，但不宜動土。然有福生並黃羅、紫檀、天皇、地皇星蓋照，宜嫁娶、入宅、起造、安葬、出行、開張，百事順遂。壬寅、戊寅上吉，丙寅、庚寅次吉，甲寅又次吉。",
            "description_english": "The presence of the Yellow Sand 黃砂 and Heavenly Fortune 天富 Stars on this day render it unsuitable for groundbreaking. Nevertheless, it is still considered a Prosperous Growth 福生 Day, due to the presence of the auspicious Yellow Spiral 黃羅, Purple Sandalwood 紫檀, Heavenly Emperor 天皇 and Earthly Emperor 地皇 Stars. As such, use this day for marriage, moving into a new house, renovation, burial, travel and opening a business – it augurs well for all significant or large-scale activities. Where possible, use the Ren Yin 壬寅 and Wu Yin 戊寅 Days, as they are the best of the lot. Bing Yin 丙寅 and Geng Yin 庚寅 Days are considered second-grade, with Jia Yin 甲寅 Days being third-grade, in descending order.",
        },
        "Mao": {
            "officer": "Ping",
            "pillars": {
                "Yi-Mao": "auspicious",
                "Ding-Mao": "inauspicious",
                "Ji-Mao": "inauspicious",
                "Xin-Mao": "inauspicious",
                "Gui-Mao": "inauspicious",
            },
            "good_for": [],
            "bad_for": ["most_activities", "legal_matters", "wealth_matters"],
            "description_chinese": "天賊。辛卯火星，卻犯朱雀、勾絞，用之招官司、損財物、好爭鬥、傷情義、多惡疾招官。惟乙卯一日次吉，餘卯主父子、兄弟不義、爭鬥、自縊，惡人劫害、破敗，大凶。",
            "description_english": "The Heavenly Thief 天賊 is present throughout the day. A Xin Mao 辛卯 Day is also marked by the presence of the Fire Star 火星, although it also harbors negative stars such as the Red Phoenix 朱雀 and Grappling Hook 勾絞, which make it unsuitable for use. The overall outcomes include legal issues, a decrease in wealth, disputes and quarrels, strained relationships, and serious ailments. A Yi Mao 乙卯 Day, however, is considered an above-average day and may be used with care. The remaining Mao 卯 (Rabbit) Days should be avoided, for they cause discord and misunderstanding between fathers and their sons, arguments and failure, as well as give rise to selfishness and provide means for malicious people to harm oneself.",
        },
        "Chen": {
            "officer": "Ding",
            "pillars": {
                "Jia-Chen": "inauspicious",
                "Bing-Chen": "inauspicious",
                "Wu-Chen": "inauspicious",
                "Geng-Chen": "inauspicious",
                "Ren-Chen": "auspicious",
            },
            "good_for": ["burial", "fixing_doorframes", "marriage", "moving"],
            "bad_for": ["most_activities"],
            "description_chinese": "雖云吉。卻有天羅地網之咎，貴人不臨，營為不利，熬占中宮，犯之殺人，凶。惟壬辰雖犯官符，內有天德、黃羅、紫檀、天皇、地皇星蓋照，宜安葬、安門、嫁親、出行、入宅，主家門興旺。生貴子賢孫。甲辰、戊辰似為吉，然熬入中宮，嫁親、入宅等是所宜用。壬辰大宜安葬、安門，上吉。餘事慎之。乃死氣之日，百事不利。犯官符與劫然，飛宮官符同到此方。",
            "description_english": "Even though this day is typically regarded as an auspicious day, it nevertheless contains the Heavenly Net 天羅 and Earthly Web 地網 Stars, which 'prevent' the arrival and therefore positive outcomes brought about by Nobleman Stars. The Ren Chen 壬辰 Day also paradoxically violates the Officer Charm 官符 Star while harboring the Heavenly Virtue 天德, Yellow Spiral 黃羅, Purple Sandalwood 紫檀, Heavenly Emperor 天皇 and Earthly Emperor 地皇 Stars. This makes it only suitable for burial, fixing doorframes, marriage or entering a new house. It however also heralds the birth of offspring who will prosper in life. Use the other Chen 辰 (Dragon) Days with care, as the Qi on these days is dead. Adding to their inauspiciousness is the presence of the Officer Charm 官符, Robbery Sha 劫煞 and Flying Palace 飛宮 Stars.",
        },
        "Si": {
            "officer": "Zhi",
            "pillars": {
                "Yi-Si": "excellent",
                "Ding-Si": "dire",
                "Ji-Si": "excellent",
                "Xin-Si": "auspicious",
                "Gui-Si": "excellent",
            },
            "good_for": ["burial", "positioning_door", "groundbreaking", "marriage", "moving", "business", "travel"],
            "bad_for": [],
            "description_chinese": "乙巳、癸巳、己巳有黃羅、紫檀、天皇、地皇諸星蓋照，宜安葬、安門、興土、動土、嫁、入宅、出行、開張、營為，諸事用之，添人口、旺家門、生貴子、增田地，大吉。辛巳次吉。丁巳正四廢，凶。",
            "description_english": "Yi Si 乙巳, Gui Si 癸巳 and Ji Si 己巳 Days are accompanied by the presence of the auspicious Yellow Spiral 黃羅, Purple Sandalwood 紫檀, Heavenly Emperor 天皇 and Earthly Emperor 地皇 Stars. This makes these particular days ideal for burial, positioning a door, groundbreaking, marriage, moving into a new house, travel or opening a business. Utilized well, they will bring about an increase in the number of one family members through the birth of noble children, as well as an increase in wealth and possessions. Likewise, a Xin Si 辛巳 Day may 'only' be second-grade, but it is still auspicious enough to be utilized. Avoid using a Ding Si 丁巳 Day, though, as it is a Direct Abandonment 正四廢 Day.",
        },
        "Wu": {
            "officer": "Po",
            "pillars": {
                "Jia-Wu": "inauspicious",
                "Bing-Wu": "inauspicious",
                "Wu-Wu": "inauspicious",
                "Geng-Wu": "inauspicious",
                "Ren-Wu": "fair",
            },
            "good_for": [],
            "bad_for": ["important_activities", "health_matters"],
            "description_chinese": "天賊。壬午火星傍月德，僅可小小急用。餘午日招瘟疫、害六畜，乃月建沖破之日，凶。丙午正四廢凶。",
            "description_english": "The Heavenly Thief 天賊 Star is present throughout the month. On Ren Wu 壬午 Days, the Fire Star 火星 along with the Monthly Virtue 月德 Star exert their influence, making such days only suitable for activities of minor importance. The remaining Wu 午 (Horse) Days unsuitable for all important activities or endeavors and if used, will make one more susceptible to sickness and animals and livestock more exposed to harm.",
        },
        "Wei": {
            "officer": "Wei",
            "pillars": {
                "Yi-Wei": "dire",
                "Ding-Wei": "excellent",
                "Ji-Wei": "auspicious",
                "Xin-Wei": "inauspicious",
                "Gui-Wei": "inauspicious",
            },
            "good_for": ["burial", "all_matters"],
            "bad_for": [],
            "description_chinese": "丁未天河水潔淨之時，用之百事全吉。己未日利埋葬最吉。餘事亦吉。此二日用事，進人口、增田産、得橫財。辛未、癸未諸事主不利。乙未熬入中宮，更凶。",
            "description_english": "On a Ding Wei 丁未 Day, the Heavenly Stream 天河 produces pure and serene Water Qi, making it a very auspicious day that may be suitably used for all matters. Ji Wei 己未 Days are also very good and best suited for burial. Used properly, these two days could lead to one's family expanding and prospering. However, Xin Wei 辛未 and Gui Wei 癸未 Days are unsuitable insofar as important activities are concerned. A Yi Wei 乙未 Day, in particular, is the worst of the 5 types of days, what with the presence of Sha (Killing) Qi in the Central Palace.",
        },
        "Shen": {
            "officer": "Cheng",
            "pillars": {
                "Jia-Shen": "excellent",
                "Bing-Shen": "inauspicious",
                "Wu-Shen": "excellent",
                "Geng-Shen": "fair",
                "Ren-Shen": "excellent",
            },
            "good_for": ["all_activities", "business", "wealth_matters", "childbirth"],
            "bad_for": [],
            "description_chinese": "天喜。壬申天喜、月二德之時，值黃羅、紫檀、甲中、戊申，五行有氣照，一切作為、百福駢臻，諸事順遂，諸吉星蓋起造若起適大宜安葬，及屋外小修造則可。若起造主擔家長、傷陰人、入宅、開張、立見凶神聚入中宮，善人不能除福，謂之五行無氣，然採用此日，不避齒煩前去攔阻，無如上切中，上年見有人立見災禍。可知此書擇日，實有應驗不可輕視。丙申日用事，驚犯鬼哭神號，更宜慎之。",
            "description_english": "The Sky Happiness 天喜 Star is present throughout the day. In addition, Ren Shen 壬申 Days are also accompanied by the Heavenly Virtue 天德 and Monthly Virtue 月德 Stars. Meanwhile, on Jia Shen 甲申 and Wu Shen 戊申 Days, the Qi of the Five Elements are strong and enhanced by the presence of the Yellow Spiral 黃羅, Purple Sandalwood 紫檀, Precious Treasure 寶藏, Golden Ingot 金銀 and Storage 庫樓 Stars. This makes such days perfect for all important activities or endeavors, for if used, they will produce outcomes that increase wealth or result in the birth of a noble child. However, Geng Shen 庚申 Days are only suitable for burial or minor renovation works to the interior of a house. Using a Geng Shen Day for important endeavors or activities such as marriage, entering a new house or opening a business will immediately bring about disastrous outcomes; where elderly family members may be susceptible to poor health, children will tend to get hurt more easily, and one's fortune and sense of harmony will deteriorate. Bing Shen 丙申 Days are the worst of the lot, and should definitely be avoided for all important activities.",
        },
        "You": {
            "officer": "Shou",
            "pillars": {
                "Yi-You": "inauspicious",
                "Ding-You": "inauspicious",
                "Ji-You": "inauspicious",
                "Xin-You": "inauspicious",
                "Gui-You": "inauspicious",
            },
            "good_for": ["burial"],
            "bad_for": ["renovation", "business", "travel", "moving", "marriage"],
            "description_chinese": "小紅砂。有到州星，事到官司而後散，只宜埋葬、次吉。忌起造、開張、出行、入宅、嫁娶等事。犯之官非、冷退、損傷財物，凶。餘酉不利。",
            "description_english": "With the Lesser Red Embrace 小紅砂 Star governing the day, the only suitable activity that may be done is burial. Do not use this day for renovation, launching a business, travel, moving into a new house or get married. Ignoring this warning will result in lawsuits surfacing, as well as a decrease in wealth and other material assets. Similarly, the other You 酉 (Rooster) Days are not favorable either.",
        },
        "Xu": {
            "officer": "Kai",
            "pillars": {
                "Jia-Xu": "auspicious",
                "Bing-Xu": "dire",
                "Wu-Xu": "inauspicious",
                "Geng-Xu": "inauspicious",
                "Ren-Xu": "dire",
            },
            "good_for": ["burial", "minor_activities"],
            "bad_for": ["most_activities"],
            "description_chinese": "往亡。小葬亦僅備於急用，乃次吉之日。如丙戌、壬戌熬入中宮，諸事忌用。甲戌八方俱白，二十四向諸神朝天，玄女倫修之日，可用。",
            "description_english": "As this is an Emptiness Day 往亡, it should only be used for insignificant or minor activities, although burials may be undertaken on this day. Avoid Bing Xu 丙戌 and Ren Xu 壬戌 Days, though, as they are the worst days with Sha (Killing) Qi entering the Central Palace. Jia Xu 甲戌 Days may however be used, as they are supported by the presence of positive day stars.",
        },
        "Hai": {
            "officer": "Bi",
            "pillars": {
                "Yi-Hai": "excellent",
                "Ding-Hai": "auspicious",
                "Ji-Hai": "excellent",
                "Xin-Hai": "dire",
                "Gui-Hai": "dire",
            },
            "good_for": ["renovation", "trading", "wealth_matters", "childbirth"],
            "bad_for": [],
            "description_chinese": "乙亥、己亥。文昌貴顯之星，黃羅、紫檀、天皇、地皇、聯珠、天垣、聚祿、帶馬、金銀庫樓、寶藏星蓋照，宜起造、營為，百事皆吉，方二十四向皆利，用之家道豐盈、生貴子、進財祿、旺六畜。丁亥次吉之日，癸亥六甲窮日。辛亥婦人之金、陰府決遣之期，一年四季皆不可用。惟二月之辛亥吉，餘亥皆不可用也。",
            "description_english": "The Yi Hai 乙亥 and Ji Hai 己亥 Days enjoy the support of the Literary Arts 文昌 as well as the Yellow Spiral 黃羅, Purple Sandalwood 紫檀, Heavenly Emperor 天皇, Earthly Emperor 地皇, Stringed Pearl 聯珠, Heavenly Provincial 天垣, Converging Prosperity 聚祿, Sky Horse 帶馬, Golden Ingot 金銀, Storage Wealth 庫樓, Precious Treasure 寶藏 Stars. Such days accordingly produce auspicious outcomes, and are suitable for renovation and trading, in particular. Used well, they will bring about an increase in wealth and assets, and the birth of noble offspring. Meanwhile, a Ding Hai 丁亥 Day is regarded as a 'secondarily' auspicious day. However, a Gui Hai 癸亥 Day is one of the Six Jia Weakness Days 六甲窮日, while a Xin Hai 辛亥 Day is overly Yin in Qi and therefore cannot be used.",
        },
    },
    # ========================================
    # MONTH 12 - Ox Month (十二月 / 丑月)
    # ========================================
    12: {
        "overview": {
            "chinese": "月德庚、月恩辛、母倉申酉。天德合乙。",
            "monthly_virtue": "Geng",  # 月德
            "monthly_benevolence": "Xin",  # 月恩
            "motherly_storage": ["Shen", "You"],  # 母倉
            "heavenly_virtue": "Yi",  # 天德合
            "three_killings": {
                "direction": "East",
                "starts_after": "xiao_han",  # 小寒 (Lesser Cold)
                "sectors": ["Yin", "Mao", "Chen"],  # 寅(NE3), 卯(E2), 辰(SE1)
            },
            "notes": "In the Ox 丑 (Chou) Month, the Monthly Virtue 月德 Star accompanies Geng 庚 Days, the Monthly Benevolence 月恩 Star presides over Xin 辛 Days. The Motherly Storage 母倉 Star exerts auspicious influence on Monkey 申 (Shen) and Rooster 酉 (You) Days. The Heavenly Virtue 天德 Star lends its positive energies to Yi 乙 Days. After Xiao Han (Lesser Cold), the Three Killings 三煞 is in the East. At Da Han (Greater Cold), avoid renovation or groundbreaking in Yin (NE3), Mao (E2), Chen (SE1) sectors.",
        },
        "Chou": {
            "officer": "Jian",
            "pillars": {
                "Yi-Chou": "excellent",
                "Ding-Chou": "dire",
                "Ji-Chou": "excellent",
                "Xin-Chou": "fair",
                "Gui-Chou": "inauspicious",
            },
            "good_for": ["quarrying", "excavation", "landscaping", "construction", "groundbreaking", "marriage", "business", "travel", "moving"],
            "bad_for": ["celebrations"],
            "description_chinese": "紅砂、往亡日。乙丑、己丑,宜開山、斬草、興工、動土、嫁娶、開張、出行、入宅,次吉之日也。丁丑熬入中宮,不宜鼓樂、喧嘩、婚姻之事,犯之主刑家長、宅母。癸丑雖旺,乃六熬入中宮,損傷人口,凶。",
            "description_english": "The presence of the Red Embrace 紅砂 Star makes this an Emptiness Day 往亡日. Yi Chou 乙丑 and Ji Chou 己丑 Days are however suitable for quarrying, excavation, landscaping, construction and groundbreaking works, as well as marriage, opening a business, travel or moving into a new house. On Ding Chou 丁丑 Days, Sha Qi enters the Central Palace, rendering such days unsuitable for celebrations or marriage. Ignoring this warning will only result in elderly family members being more susceptible to illness or injury. Similarly, even though Gui Chou 癸丑 Days are considered prosperous, there is still Sha Qi in the Central Palace, which puts the health and safety of family members at risk. As such, these days should be regarded as inauspicious and hence avoided.",
        },
        "Yin": {
            "officer": "Chu",
            "pillars": {
                "Jia-Yin": "excellent",
                "Bing-Yin": "excellent",
                "Wu-Yin": "auspicious",
                "Geng-Yin": "excellent",
                "Ren-Yin": "excellent",
            },
            "good_for": ["renovation", "marriage", "burial", "moving", "business", "travel"],
            "bad_for": [],
            "description_chinese": "庚寅火星、天月二德,甲寅、丙寅、壬寅有火星及黃羅、紫檀、天皇、地皇、寶藏、庫珠、金銀、福祿、文昌、祿馬,官蓋眾吉星照臨,宜起造、婚姻、安葬、入宅、開張、出行,百事順利,用之家門發達、動土雙進財產、名登虎榜。戊寅,亦有火星,乃次吉之日,可用。",
            "description_english": "Geng Yin 庚寅 Days enjoy the supportive energies of the Fire 火星, Heavenly Virtue 天德 and Monthly Virtue 月德 Stars. Similarly, Jia Yin 甲寅, Bing Yin 丙寅, and Ren Yin 壬寅 Days are accompanied by the presence of the Fire 火星, Yellow Spiral 黃羅, Purple Sandalwood 紫檀, Heavenly Emperor 天皇, Earthly Emperor 地皇, Precious Carriage 寶蓋, Pearl Storage 庫珠, Golden Ingot 金銀, Fortune Prosperity 福祿, Literary Arts 文昌 and Prosperous Horse 祿馬 Stars. This makes all these days ideal for renovations, marriage, burial, moving into a new house, opening a business and travel, with positive outcomes guaranteed for all endeavors. Those who tap into the useful energies of these days will prosper and enjoy an increase in wealth, and the reputation carried by a good name. A Wu Yin 戊寅 Day is also accompanied by the Fire Star 火星, making it a secondary good day to be used.",
        },
        "Mao": {
            "officer": "Man",
            "pillars": {
                "Yi-Mao": "inauspicious",
                "Ding-Mao": "inauspicious",
                "Ji-Mao": "inauspicious",
                "Xin-Mao": "auspicious",
                "Gui-Mao": "inauspicious",
            },
            "good_for": ["marriage", "construction"],
            "bad_for": ["groundbreaking"],
            "description_chinese": "天富。土瘟,不宜動土。犯之天瘟一年,若用卯日娶親、問名等事小吉,但有六成六不合之疑。惟辛卯造作、興工,乃是次吉之日也。",
            "description_english": "Despite the presence of the Heavenly Fortune 天富 Star, the threat of an earth-bound disease looms over one's head. Using this day for groundbreaking will only result in one being plagued by health problems throughout the year. It is moderately suitable for marriage, however, with a Xin Mao 辛卯 Day usable for construction purposes.",
        },
        "Chen": {
            "officer": "Ping",
            "pillars": {
                "Jia-Chen": "inauspicious",
                "Bing-Chen": "inauspicious",
                "Wu-Chen": "inauspicious",
                "Geng-Chen": "excellent",
                "Ren-Chen": "auspicious",
            },
            "good_for": ["marriage", "burial", "work", "travel", "moving"],
            "bad_for": [],
            "description_chinese": "有到州星,事到官而後散。惟壬辰宜娶親、埋葬、娶親、興工、出行、入宅,次吉。庚辰天、月二德,宜小作,次吉。戊辰草木凋零之時,五行無氣,乃是退星,又熬入中宮,諸事不利,凶。",
            "description_english": "What begins well will end less-than-desirably. As such, while Ren Chen 壬辰 Days harbor good stars, they are only moderately suitable for marriage, burial, commencing work, travel or moving into new premises. One would do better to utilize Geng Chen 庚辰 Days, which are supported by the Heavenly and Earthly Virtue stars and therefore slightly more auspicious. On a Wu Chen 戊辰 Day, however, there is no Qi in the Five Elements, and this scenario, coupled with Sha Qi entering the Central Palace, only makes for an extremely inauspicious day.",
        },
        "Si": {
            "officer": "Ding",
            "pillars": {
                "Yi-Si": "inauspicious",
                "Ding-Si": "dire",
                "Ji-Si": "inauspicious",
                "Xin-Si": "inauspicious",
                "Gui-Si": "auspicious",
            },
            "good_for": ["quarrying", "landscaping"],
            "bad_for": ["marriage", "business", "travel", "moving", "building"],
            "description_chinese": "天成。一云官符星。非但云是死氣之日,如待方合吉神累,值山、新草之事,乃次吉之日,水潔淨之時,或可用開入宅、定碓、挺架,卻是天上大空亡納音自絕不宜吉,雖有喜神化解,亦屬難免。如旺巳日,主口明年命、向山不犯沖煞,可用。丁巳正四廢,凶。一年四季皆用巳日,亦屬難免。",
            "description_english": "Although the Heavenly Success Star is present, it is also accompanied by the Officer Charm Star 官符星, which denotes legal matters. As such, this day can only be used if there are other positive stars present to tip the scales towards the more positive side. A Gui Si 癸巳 Day is suitable to excavate mountains or for quarrying and landscaping works, although it remains a less-than-ideal date that should not be used for marriage, opening a business, business-related travel, or moving into or building a new house. On this day, the self Na Yin element is in extinction. Meanwhile, a Ding Si 丁巳 Day is also one of the Direct Abandonment 正四廢 Days, and therefore an inauspicious one that should be avoided. Likewise, those who use the remaining Si 巳(Snake) days subject themselves to the possibility of gossip and slander, even with the presence of favorable stars. To err on the side of caution, only use such days if there are other prosperous stars present, and in tandem with one's birth details (BaZi) and the Facing/Sitting Direction of one's property.",
        },
        "Wu": {
            "officer": "Zhi",
            "pillars": {
                "Jia-Wu": "auspicious",
                "Bing-Wu": "dire",
                "Wu-Wu": "auspicious",
                "Geng-Wu": "excellent",
                "Ren-Wu": "excellent",
            },
            "good_for": ["renovation", "marriage", "moving", "business", "travel", "groundbreaking", "burial"],
            "bad_for": [],
            "description_chinese": "庚午,天月二德。如庚午年作庚山甲向,宜可收納音也。況其日有用庚辰時者,時遇三合照甲庚,而庚祿居中,辰馬又值壬中,此之謂生成祿馬日,龍馬遇祿星,聖人面面星有黃羅、紫檀、天皇、地皇、金銀寶樓,眾吉星蓋照,主益子孫、旺家門、進田產、遷祿位,壬午並吉,餘午次吉,丙午正四廢,凶。",
            "description_english": "Geng Wu 庚午 Days have the Heavenly 天德 and Monthly Virtue 月德 Stars present. Hence, during a Geng Wu Year 庚午年, use the Geng Sitting 庚山, Jia Facing 甲向 setup to receive Na Yin Qi. One can also utilize the Geng Chen 庚辰 Hour, to produce a Three Harmony Shining on Jia and Geng 三合照甲庚 formation, where the Geng Prosperous 祿 Branch resides in the Shen 申 (Monkey) Stem. Such a day is also known as a Prosperous Sky Horse Day 生成祿馬日, which is further supported by a host of auspicious stars including the Yellow Spiral 黃羅, Purple Sandalwood 紫檀, Heavenly Emperor 天皇, Earthly Emperor 地皇, Golden Ingot 金銀 and Precious Building 寶樓. This combination brings about an increase in wealth and good advancement opportunities in life. Do note however that while Ren Wu 壬午 Days are also very auspicious days, the other Wu 午 (Horse) days are only considered second-tier options. Only the Bing Wu 丙午 day is completely unusable, as it is one of the Direct Abandonment 正四廢 Days.",
        },
        "Wei": {
            "officer": "Po",
            "pillars": {
                "Yi-Wei": "inauspicious",
                "Ding-Wei": "excellent",
                "Ji-Wei": "inauspicious",
                "Xin-Wei": "inauspicious",
                "Gui-Wei": "excellent",
            },
            "good_for": ["groundbreaking", "marriage", "travel", "moving", "business"],
            "bad_for": [],
            "description_chinese": "丁未水居巨鰲,癸未水入秦州,內有文昌貴顯之星,宜動土、興工、出行、入宅、娶親、開張,百事大吉。己未、辛未,熬入中宮,凶,乙未亦不利。",
            "description_english": "Qi is prosperous and thriving on Ding Wei 丁未 and Gui Wei 癸未 Days, which also enjoy the positive energies of the Literary Arts 文昌 Star. As such, these days are suitable groundbreaking, marriage, travel, moving into a new house or opening a business, as all endeavors undertaken will bear fruit. Ji Wei 己未, Xin Wei 辛未 and Yi Wei 乙未 Days, however, harbor Sha Qi, and should hence be avoided.",
        },
        "Shen": {
            "officer": "Wei",
            "pillars": {
                "Jia-Shen": "fair",
                "Bing-Shen": "fair",
                "Wu-Shen": "inauspicious",
                "Geng-Shen": "fair",
                "Ren-Shen": "fair",
            },
            "good_for": ["minor_repairs", "burial"],
            "bad_for": ["major_renovations", "business", "moving", "marriage"],
            "description_chinese": "庚申天月二德,宜修造、安葬、小小營為,次吉。如大家千百工以上起造、開張、入宅、婚等事,卻不宜。其日熬入中宮,不利家長人者,雖有天、月二德,亦無如之何作,用事損傷手足、匠夫。破失損壞器血。大作遭見損、小作緩慾,若作牛羊豬圈,六十日、一百二十日內便見虎狼傷害,更生瘟疫。甲申起造、安葬吉。丙申、壬申只宜埋葬吉。戊申日未詳。",
            "description_english": "Although a Geng Shen 庚申 Day is marked by the presence of the Heavenly and Earthly Virtue 天月二德 Stars, it is only suitable for minor repairs and burial. This day should not be used for major renovations, opening a business, moving into a new house or marriage, as this would result in Sha Qi entering the Central Palace, and harming the eldest member in a family. Worse still, anyone who taps into the energies of this day will be likely attacked by a tiger or wolf, and/or fall ill easily, within 60 to 120 days. A Jia Shen 甲申 Day may also be used for minor repairs and burial, while Bing Shen 丙申 and Ren Shen 壬申 Days are especially auspicious days for burial.",
        },
        "You": {
            "officer": "Cheng",
            "pillars": {
                "Yi-You": "excellent",
                "Ding-You": "fair",
                "Ji-You": "excellent",
                "Xin-You": "auspicious",
                "Gui-You": "excellent",
            },
            "good_for": ["marriage", "renovation", "business", "moving", "burial"],
            "bad_for": [],
            "description_chinese": "天喜。己酉、癸酉,為金旺之時,有黃羅、紫檀、金玖、庫樓、五堂、庫珠、聚祿、眾祿帶馬,吉星蓋照,利婚姻、起造、開張、入宅、安葬,全吉日也,主子孫興旺、百事稱心。丁酉亦為金旺惟,惟埋葬大吉,餘事次之,辛酉金鸃次吉。",
            "description_english": "With the presence of the Sky Happiness Star, Ji You 己酉 and Gui You 癸酉 Days are further boosted by prosperous Metal Qi. Similarly, Water Qi on a Yi You 乙酉 Day is pure and in perfect balance, with the presence of auspicious stars such as the Yellow Spiral 黃羅, Purple Sandalwood 紫檀, Golden Ingot 金銀, Storage Building 庫樓, Converging Prosperous 聚祿 and Armored Horse 帶馬. Use these days for marriage, renovations, business openings, moving into a new house and burial; their positive energies will produce powerful and prosperous descendents. However, while a Ding You 丁酉 Day, which also harbors prosperous Metal Qi, can be used for burial, the outcome of using such a day for other matters will only bring about moderate results. Similarly, a Xin You 辛酉 Day is only considered a second-grade date, in terms of usability.",
        },
        "Xu": {
            "officer": "Shou",
            "pillars": {
                "Jia-Xu": "auspicious",
                "Bing-Xu": "inauspicious",
                "Wu-Xu": "inauspicious",
                "Geng-Xu": "auspicious",
                "Ren-Xu": "inauspicious",
            },
            "good_for": ["minor_activities"],
            "bad_for": ["most_activities"],
            "description_chinese": "有到州星,事到公堂而後散。庚戌有天、月二德、八位魁星有男子之權,先招口舌,而後大吉。甲戌,八方俱白,二十四向諸神朝天,天玄女倫修之日可用。丙戌、壬戌,熬入中宮,壬戌百事皆忌。戊戌日,亦不可用。",
            "description_english": "One will experience a good start that will unfortunately end in a poor finish. However, Geng Xu 庚戌 Days are accompanied by the Heavenly and Monthly Virtue Stars, which augur well for the authority of males; although they may well have to overcome obstacles first, before reaping the rewards of their labor. Similarly, Jia Xu 甲戌 Days may also be used. Avoid Bing Xu 丙戌 and Ren Xu 壬戌 Days though, as they harbor negative Qi. Wu Xu 戊戌 Day also should not be used.",
        },
        "Hai": {
            "officer": "Kai",
            "pillars": {
                "Yi-Hai": "excellent",
                "Ding-Hai": "auspicious",
                "Ji-Hai": "excellent",
                "Xin-Hai": "inauspicious",
                "Gui-Hai": "dire",
            },
            "good_for": ["building", "moving", "marriage", "business", "travel"],
            "bad_for": [],
            "description_chinese": "天賊、月厭。乙亥有文昌星,己亥火星,有文昌顯貴星,宜定碓、挺架、婚姻、開張、入宅、出行、營為,諸事全吉營為諸事全吉,宜用戊辰時,是日雖犯天賊,卻有天狗護之宜不妨,故上吉。如過此日生人,大壞之命。宜用。丁亥亦宜用事。辛亥陰氣太甚,非陽間所宜用。癸亥六甲窮日,不可用。己亥因有火星,諸事可用,無不順利,而稱心如意耳。",
            "description_english": "The Heavenly Thief 天賊 and Month Detest 月厭 Stars are simultaneously present throughout the day. Nevertheless, Yi Hai 乙亥 Days are accompanied by the Literary Arts 文昌 Star, while Ji Hai 己亥 Days harbor the 火星 Fire Star and also the Literary Arts 文昌 Star. Such days are hence ideal for building or moving into a new house, marriage, opening a business, travel etc. Try to use a Ding Hai 丁亥 if possible, as it is suitable for most activities. Yin Qi is overly strong on Xin Hai 辛亥 Days, while a Gui Hai 癸亥 Day is one of the 60 Jia Zi 陰氣太甚 Days. One would be better off using a Ji Hai 己亥 Day, because the presence of the Fire Star 火星 makes it ideal for any type of activity or endeavor.",
        },
        "Zi": {
            "officer": "Bi",
            "pillars": {
                "Jia-Zi": "fair",
                "Bing-Zi": "inauspicious",
                "Wu-Zi": "fair",
                "Geng-Zi": "auspicious",
                "Ren-Zi": "inauspicious",
            },
            "good_for": ["minor_activities"],
            "bad_for": ["groundbreaking", "major_activities"],
            "description_chinese": "黃砂。庚子雖有天、月二德,卻是天地轉熬之時,壬子、丙子,天轉地熬,不宜興工、動土,犯之大凶。甲子天赦,是進神日,並戊子,宜小可修為,吉,若大用之則凶禍,縱縱不詳甚莫大馬,納音凶熬,乃北方造之神,純陰不黑熬之氣,用事司曹廟令,非大貴不敢用,當用者慎之。",
            "description_english": "The Yellow Spiral 黃砂 Star is present throughout the day. Geng Zi 庚子 Days are however accompanied by the Heavenly and Earthly Virtues 天月二德 Stars, which clash simultaneously with the negative Heaven and Earth Drilling Sha 天轉地熬 Star. This makes a Geng Zi Day unsuitable for groundbreaking or commencing a new task; for violating this rule would only bring about disaster and catastrophe. Ren Zi 壬子 and Bing Zi 丙子 day also has the Heaven and Earth Drilling Sha 天轉地熬 should not be used. A Jia Zi 甲子 Day is also known as a Heavenly Pardon 天赦 Day, while a Wu Zi 戊子 Day is ideal for activities of minor importance. Do not use such days for major or important events, though.",
        },
    }
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


# Keywords that indicate positive/conditional use in an inauspicious day's description
CONSULT_POSITIVE_KEYWORDS = [
    "suitable", "auspicious", "good for", "recommended", "benefit",
    "prosper", "wealth", "noble", "gain", "positive outcome",
    "secondarily", "moderately suitable", "fairly useable",
]


def check_consult_promotion(rating: str, day_info: dict) -> dict | None:
    """If an inauspicious rating has positive tone, return consult promotion info."""
    if rating != "inauspicious" or not day_info:
        return None

    good_for = day_info.get("good_for", [])
    desc = (day_info.get("description_english", "") or "").lower()

    if good_for:
        activities = ", ".join(a.replace("_", " ") for a in good_for)
        return {"promoted": True, "reason": f"Good for: {activities}"}

    if any(kw in desc for kw in CONSULT_POSITIVE_KEYWORDS):
        return {"promoted": True, "reason": "Description indicates conditional positive use"}

    return None
