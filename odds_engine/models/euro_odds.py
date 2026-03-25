from dataclasses import dataclass

@dataclass
class EuroOdds:
    """
    欧赔数据结构
    """
    company: str

    win_init: float
    draw_init: float
    lose_init: float

    win_now: float
    draw_now: float
    lose_now: float

    kelly_win: float
    kelly_draw: float
    kelly_lose: float

    return_rate: float
