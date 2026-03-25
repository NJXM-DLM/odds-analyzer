from typing import Dict
from odds_engine.models.euro_odds import EuroOdds

class RecommendationModel:
    """
    推荐算法模块: 概率 × (1 / 凯利)
    """
    
    @staticmethod
    def calculate_recommendation(prob: Dict[str, float], min_kelly: Dict[str, float]) -> Dict:
        """
        生成推荐结果
        推荐指数 score = 概率 × (1 / 凯利)
        """
        # 胜
        win_idx = prob["win"] * (1.0 / (min_kelly["win"] + 0.001))
        # 平
        draw_idx = prob["draw"] * (1.0 / (min_kelly["draw"] + 0.001))
        # 负
        lose_idx = prob["lose"] * (1.0 / (min_kelly["lose"] + 0.001))
        
        indices = {"胜": win_idx, "平": draw_idx, "负": lose_idx}
        
        # 找出最大值作为结果
        recommendation = max(indices, key=indices.get)
        
        return {
            "recommendation": recommendation,
            "indices": {k: round(v, 4) for k, v in indices.items()}
        }
