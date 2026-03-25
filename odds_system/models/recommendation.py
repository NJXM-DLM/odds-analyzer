from typing import Dict, List
from odds_system.models.data_structures import MarketProbability, EuroCompanyOdds

class RecommendationModel:
    """
    推荐算法模块: 综合概率与凯利指数生成推荐结果
    """
    
    @staticmethod
    def calculate_recommendation_index(prob: MarketProbability, min_kelly: Dict[str, float]) -> Dict[str, float]:
        """
        推荐指数 = 概率 × (1 / 凯利)
        算法逻辑: 概率高且凯利低的方向(庄家防范方向)推荐度最高
        """
        # 避免除以0
        win_idx = prob.win * (1.0 / (min_kelly["win"] + 0.001))
        draw_idx = prob.draw * (1.0 / (min_kelly["draw"] + 0.001))
        lose_idx = prob.lose * (1.0 / (min_kelly["lose"] + 0.001))
        
        # 归一化得分
        total = win_idx + draw_idx + lose_idx
        
        return {
            "win": win_idx / total,
            "draw": draw_idx / total,
            "lose": lose_idx / total
        }

    @staticmethod
    def get_recommendation_result(rec_index: Dict[str, float]) -> str:
        """
        获取推荐结果: 返回推荐指数最大的结果
        """
        mapping = {"win": "胜", "draw": "平", "lose": "负"}
        max_key = max(rec_index, key=rec_index.get)
        return mapping[max_key]
