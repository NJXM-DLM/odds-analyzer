from typing import Dict, List
from odds_engine.models.euro_odds import EuroOdds

class KellyAnalyzer:
    """
    凯利分析模块: 获取最小凯利并检测异常
    """
    
    @staticmethod
    def get_min_kelly(euros: List[EuroOdds]) -> Dict[str, float]:
        """
        获取每个结果的最小凯利值
        """
        if not euros:
            return {"win": 0.0, "draw": 0.0, "lose": 0.0}
            
        return {
            "win": min(e.kelly_win for e in euros),
            "draw": min(e.kelly_draw for e in euros),
            "lose": min(e.kelly_lose for e in euros)
        }

    @classmethod
    def calculate_kelly_anomaly(cls, euros: List[EuroOdds]) -> float:
        """
        计算凯利异常得分 (0~1)
        逻辑：如果某项结果的最小凯利显著低于平均返还率，则视为庄家严防，得分高
        """
        if not euros:
            return 0.0
            
        min_kellies = cls.get_min_kelly(euros)
        avg_return = sum(e.return_rate for e in euros) / len(euros)
        
        # 计算偏离度
        deviations = [(avg_return - val) for val in min_kellies.values() if val < avg_return]
        
        if not deviations:
            return 0.0
            
        # 归一化得分 (假设偏离 0.1 为极高风险)
        max_dev = max(deviations)
        return min(1.0, max_dev / 0.1)
