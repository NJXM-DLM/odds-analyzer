from typing import List, Dict
from odds_system.models.data_structures import EuroCompanyOdds, OddsValue

class TrendAnalyzer:
    """
    时间趋势模块: 初始盘 vs 即时盘变化分析
    """
    
    @staticmethod
    def calculate_odds_trend(initial: OddsValue, current: OddsValue) -> Dict[str, str]:
        """
        计算赔率变化趋势 (升/降/平)
        """
        def get_trend(ini_v: float, cur_v: float) -> str:
            if cur_v > ini_v: return "升"
            elif cur_v < ini_v: return "降"
            return "平"
            
        return {
            "win": get_trend(initial.win, current.win),
            "draw": get_trend(initial.draw, current.draw),
            "lose": get_trend(initial.lose, current.lose)
        }

    @staticmethod
    def detect_conflict_signals(companies_odds: List[EuroCompanyOdds]) -> float:
        """
        检测时间趋势冲突信号: 赔率下降但凯利上升的冲突
        通常表示庄家诱盘或反常, 得分越高冲突越大 (0~1)
        """
        if not companies_odds:
            return 0.0
            
        conflict_count = 0
        total_signals = 0
        
        for co in companies_odds:
            # 胜平负三个结果检测
            # 初始到即时盘
            for result in ["win", "draw", "lose"]:
                ini_odds = getattr(co.initial, result)
                cur_odds = getattr(co.current, result)
                # 假设凯利初盘凯利也是由初盘赔率算出来的, 凯利随赔率下降而下降是正常的
                # 但如果凯利由于某种原因相对于市场返还率却反而升高了, 说明该结果风险大
                # 简化处理: 赔率下降, 且凯利高于其返还率(理论最大值), 则视为诱导
                if cur_odds < ini_odds:
                    cur_kelly = getattr(co.kelly, result)
                    if cur_kelly > co.return_rate:
                        conflict_count += 1
                total_signals += 1
        
        # 返回冲突强度
        return min(1.0, conflict_count / (len(companies_odds) * 1.5))
