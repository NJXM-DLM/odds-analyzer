from dataclasses import dataclass

@dataclass
class AsianOdds:
    """
    亚盘数据结构
    """
    company: str

    initial_handicap: float
    current_handicap: float

    initial_water_home: float
    current_water_home: float
