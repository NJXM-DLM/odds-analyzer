from typing import Dict, List
from odds_engine.models.euro_odds import EuroOdds

class ProbabilityCalculator:
    """
    概率计算模块: 欧赔转隐含概率（去水）
    """
    
    @staticmethod
    def calculate_implied_probability(win: float, draw: float, lose: float) -> Dict[str, float]:
        """
        计算单家公司的去水概率
        """
        if win <= 0 or draw <= 0 or lose <= 0:
            return {"win": 0.0, "draw": 0.0, "lose": 0.0}
            
        raw_prob_win = 1.0 / win
        raw_prob_draw = 1.0 / draw
        raw_prob_lose = 1.0 / lose
        
        total_sum = raw_prob_win + raw_prob_draw + raw_prob_lose
        
        return {
            "win": raw_prob_win / total_sum,
            "draw": raw_prob_draw / total_sum,
            "lose": raw_prob_lose / total_sum
        }

    @classmethod
    def get_market_average_probability(cls, euros: List[EuroOdds]) -> Dict[str, float]:
        """
        获取市场平均概率（共识概率）
        """
        if not euros:
            return {"win": 0.0, "draw": 0.0, "lose": 0.0}
            
        avg_win = sum(cls.calculate_implied_probability(e.win_now, e.draw_now, e.lose_now)["win"] for e in euros) / len(euros)
        avg_draw = sum(cls.calculate_implied_probability(e.win_now, e.draw_now, e.lose_now)["draw"] for e in euros) / len(euros)
        avg_lose = sum(cls.calculate_implied_probability(e.win_now, e.draw_now, e.lose_now)["lose"] for e in euros) / len(euros)
        
        return {"win": avg_win, "draw": avg_draw, "lose": avg_lose}
