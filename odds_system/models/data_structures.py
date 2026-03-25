from dataclasses import dataclass
from typing import Dict, List

@dataclass
class OddsValue:
    win: float
    draw: float
    lose: float

@dataclass
class EuroCompanyOdds:
    company: str
    initial: OddsValue
    current: OddsValue
    kelly: OddsValue
    return_rate: float

@dataclass
class AsianHandicapData:
    initial_handicap: float
    current_handicap: float
    initial_water_home: float
    current_water_home: float
    initial_water_away: float = 0.0  # Optional, default to 0
    current_water_away: float = 0.0  # Optional, default to 0

@dataclass
class MarketProbability:
    win: float
    draw: float
    lose: float
    margin: float
