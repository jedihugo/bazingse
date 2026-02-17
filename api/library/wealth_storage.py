# * =========================
# * WEALTH STORAGE (財庫) SYSTEM
# * =========================
#
# Based on the Twelve Growth Stages (十二长生) cycle:
# Each element has a tomb/storage (墓/库) at a specific Earthly Branch.
#
# The Yang stem growth cycle determines each element's tomb:
#   甲(Yang Wood):  长生 at 亥, 墓 at 未  →  Wood tomb = 未 (Wei)
#   丙(Yang Fire):  长生 at 寅, 墓 at 戌  →  Fire tomb = 戌 (Xu)
#   戊(Yang Earth): follows Fire's cycle   →  Earth tomb = 戌 (Xu)
#   庚(Yang Metal): 长生 at 巳, 墓 at 丑  →  Metal tomb = 丑 (Chou)
#   壬(Yang Water): 长生 at 申, 墓 at 辰  →  Water tomb = 辰 (Chen)
#
# WEALTH STORAGE = tomb of the Day Master's wealth element.
# A wealth vault requires TWO conditions for maximum activation:
#   1. FILLER (填庫): wealth element stems present elsewhere in chart
#   2. OPENER (冲開): storage branch's clash partner present in chart

from .derived import WUXING
from .core import STEMS


# * ==========================================
# * ELEMENT TO STORAGE BRANCH (十二长生 墓/库)
# * ==========================================

ELEMENT_STORAGE = {
    "Wood":  "Wei",   # 木墓于未
    "Fire":  "Xu",    # 火墓于戌
    "Earth": "Xu",    # 土墓于戌 (Earth follows Fire's growth cycle)
    "Metal": "Chou",  # 金墓于丑
    "Water": "Chen",  # 水墓于辰
}


# * ==========================================
# * DM TO WEALTH STORAGE BRANCH (財庫)
# * ==========================================
# DM controls wealth element → wealth element's tomb branch
#
# NOTE: Wood DM and Water DM share 戌 (Xu) as wealth storage,
#       because Earth tomb = Xu and Fire tomb = Xu.

DM_WEALTH_STORAGE = {
    "Wood":  "Xu",    # Wood → controls Earth (wealth) → Earth tomb at 戌
    "Fire":  "Chou",  # Fire → controls Metal (wealth) → Metal tomb at 丑
    "Earth": "Chen",  # Earth → controls Water (wealth) → Water tomb at 辰
    "Metal": "Wei",   # Metal → controls Wood (wealth) → Wood tomb at 未
    "Water": "Xu",    # Water → controls Fire (wealth) → Fire tomb at 戌
}


# * ==========================================
# * STORAGE BRANCH OPENERS (冲開)
# * ==========================================
# The four 库 branches open through their clash (冲) partner.

STORAGE_OPENER = {
    "Chou": "Wei",   # 丑未冲
    "Wei":  "Chou",  # 未丑冲
    "Chen": "Xu",    # 辰戌冲
    "Xu":   "Chen",  # 戌辰冲
}


# * ==========================================
# * LARGE WEALTH STORAGE PILLARS (大財庫)
# * ==========================================
# When DM stem sits DIRECTLY on its own wealth storage branch
# in the same pillar. Most powerful wealth storage configuration.
#
# Only valid sexagenary pairs (Yang+Yang or Yin+Yin):
#   甲(Yang Wood)  + 戌(Yang) = 甲戌  →  Wood DM on Earth storage
#   丁(Yin Fire)   + 丑(Yin)  = 丁丑  →  Fire DM on Metal storage
#   戊(Yang Earth)  + 辰(Yang) = 戊辰  →  Earth DM on Water storage
#   辛(Yin Metal)  + 未(Yin)  = 辛未  →  Metal DM on Wood storage
#   壬(Yang Water)  + 戌(Yang) = 壬戌  →  Water DM on Fire storage

LARGE_WEALTH_STORAGE = {
    "Jia-Xu": {
        "chinese": "甲戌",
        "dm_element": "Wood",
        "wealth_element": "Earth",
        "storage_branch": "Xu",
        "opener": "Chen",
    },
    "Ding-Chou": {
        "chinese": "丁丑",
        "dm_element": "Fire",
        "wealth_element": "Metal",
        "storage_branch": "Chou",
        "opener": "Wei",
    },
    "Wu-Chen": {
        "chinese": "戊辰",
        "dm_element": "Earth",
        "wealth_element": "Water",
        "storage_branch": "Chen",
        "opener": "Xu",
    },
    "Xin-Wei": {
        "chinese": "辛未",
        "dm_element": "Metal",
        "wealth_element": "Wood",
        "storage_branch": "Wei",
        "opener": "Chou",
    },
    "Ren-Xu": {
        "chinese": "壬戌",
        "dm_element": "Water",
        "wealth_element": "Fire",
        "storage_branch": "Xu",
        "opener": "Chen",
    },
}


# * ==========================================
# * WEALTH ELEMENT BY DM (controlling cycle)
# * ==========================================

DM_WEALTH_ELEMENT = WUXING["controlling"]


# * ==========================================
# * WEALTH ELEMENT STEMS (for filler detection)
# * ==========================================
# Map element → list of Heavenly Stems of that element

WEALTH_ELEMENT_STEMS = {}
for stem_id, stem in STEMS.items():
    elem = stem["element"]
    if elem not in WEALTH_ELEMENT_STEMS:
        WEALTH_ELEMENT_STEMS[elem] = []
    WEALTH_ELEMENT_STEMS[elem].append(stem_id)
