from dataclasses import dataclass
from typing import List
from odds_engine.models.euro_odds import EuroOdds
from odds_engine.models.asian_odds import AsianOdds

@dataclass
class MatchData:
    """
    比赛数据集合，包含多家公司的欧赔和亚盘
    """
    euros: List[EuroOdds]
    asians: List[AsianOdds]
