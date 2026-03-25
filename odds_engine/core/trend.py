from typing import List, Dict
from odds_engine.models.euro_odds import EuroOdds

class TrendAnalyzer:
    """
    时间趋势模块: 初盘 vs 即时盘变化趋势
    """
    
    @staticmethod
    def analyze_win_trend(euros: List[EuroOdds]) -> str:
        """
        判断主胜趋势：增强 / 减弱 / 稳定
        基于市场平均欧赔的变化
        """
        if not euros:
            return "数据不足"
            
        avg_win_init = sum(e.win_init for e in euros) / len(euros)
        avg_win_now = sum(e.win_now for e in euros) / len(euros)
        
        # 赔率下降表示支持增强
        if avg_win_now < avg_win_init * 0.98: # 2% 变化阈值
            return "主胜增强"
        elif avg_win_now > avg_win_init * 1.02:
            return "主胜减弱"
        else:
            return "主胜稳定"

    @staticmethod
    def get_trend_conflict_score(euros: List[EuroOdds]) -> float:
        """
        计算趋势冲突评分 (0~1)
        检测：赔率下降但凯利上升的反向诱导信号
        """
        if not euros:
            return 0.0
            
        conflict_count = 0
        for e in euros:
            # 简化逻辑：仅检测主胜方向
            if e.win_now < e.win_init and e.kelly_win > e.return_rate:
                conflict_count += 1
                
        return min(1.0, conflict_count / len(euros))
