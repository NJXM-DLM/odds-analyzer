import numpy as np
from typing import List
from odds_engine.models.euro_odds import EuroOdds
from odds_engine.models.asian_odds import AsianOdds

class DivergenceAnalyzer:
    """
    分歧分析模块: 计算欧赔和亚盘的标准差
    """
    
    @staticmethod
    def calculate_euro_divergence(euros: List[EuroOdds]) -> float:
        """
        计算欧赔分歧指数 (0~1)
        基于胜平负即时赔率的标准差均值
        """
        if not euros:
            return 0.0
            
        wins = [e.win_now for e in euros]
        draws = [e.draw_now for e in euros]
        loses = [e.lose_now for e in euros]
        
        # 计算变异系数 (CV = std / mean)
        cv_win = np.std(wins) / np.mean(wins)
        cv_draw = np.std(draws) / np.mean(draws)
        cv_lose = np.std(loses) / np.mean(loses)
        
        avg_cv = (cv_win + cv_draw + cv_lose) / 3.0
        
        # 归一化 (经验值: 0.1 以上为高分歧)
        return min(1.0, avg_cv / 0.1)

    @staticmethod
    def calculate_asian_divergence(asians: List[AsianOdds]) -> float:
        """
        计算亚盘盘口分歧
        """
        if not asians:
            return 0.0
            
        handicaps = [a.current_handicap for a in asians]
        # 盘口标准差，0.25 为一个盘口等级
        std_handicap = np.std(handicaps)
        
        return min(1.0, std_handicap / 0.25)
