from typing import List, Dict
from odds_system.models.data_structures import EuroCompanyOdds, OddsValue

class KellyAnalyzer:
    """
    凯利分析模块: 凯利指数分析庄家防范方向
    """
    @staticmethod
    def get_min_kelly(companies_odds: List[EuroCompanyOdds]) -> Dict[str, float]:
        """
        获取每个结果(胜/平/负)的最小凯利值
        用于判断庄家防范方向
        """
        if not companies_odds:
            return {"win": 0.0, "draw": 0.0, "lose": 0.0}
            
        min_win = min(co.kelly.win for co in companies_odds)
        min_draw = min(co.kelly.draw for co in companies_odds)
        min_lose = min(co.kelly.lose for co in companies_odds)
        
        return {"win": min_win, "draw": min_draw, "lose": min_lose}

    @staticmethod
    def get_risk_direction(kelly_values: Dict[str, float]) -> str:
        """
        识别凯利防范方向: 返回最小凯利值对应的结果
        """
        # 庄家通常防范凯利值最小的方向
        return min(kelly_values, key=kelly_values.get)

    @classmethod
    def identify_kelly_anomaly(cls, companies_odds: List[EuroCompanyOdds]) -> float:
        """
        识别凯利异常: 凯利分布的异常程度得分(0~1)
        异常情况: 某个结果的凯利值显著低于其他结果, 且普遍低于市场平均返还率
        """
        if not companies_odds:
            return 0.0
            
        min_kellies = cls.get_min_kelly(companies_odds)
        avg_return = sum(co.return_rate for co in companies_odds) / len(companies_odds)
        
        # 计算偏离平均返还率的异常分
        # 如果某个凯利值比平均返还率低很多, 说明防范严重
        anomalies = [max(0.0, (avg_return - val) * 10) for val in min_kellies.values()]
        
        # 归一化得分
        return min(1.0, max(anomalies))
