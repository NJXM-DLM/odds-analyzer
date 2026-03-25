import numpy as np
from typing import List, Dict
from odds_system.models.data_structures import EuroCompanyOdds

class DivergenceAnalyzer:
    """
    分歧分析模块: 计算赔率标准差并识别市场分歧
    """
    
    @staticmethod
    def calculate_std_deviation(companies_odds: List[EuroCompanyOdds]) -> Dict[str, float]:
        """
        计算赔率标准差（胜/平/负）
        """
        if not companies_odds:
            return {"win": 0.0, "draw": 0.0, "lose": 0.0}
            
        wins = [co.current.win for co in companies_odds]
        draws = [co.current.draw for co in companies_odds]
        loses = [co.current.lose for co in companies_odds]
        
        return {
            "win": float(np.std(wins)),
            "draw": float(np.std(draws)),
            "lose": float(np.std(loses))
        }

    @classmethod
    def get_divergence_index(cls, companies_odds: List[EuroCompanyOdds]) -> float:
        """
        计算分歧指数（0~1）: 
        基于标准差对均值的比例(CV)计算市场共识的分歧程度
        """
        if not companies_odds:
            return 0.0
            
        wins = [co.current.win for co in companies_odds]
        draws = [co.current.draw for co in companies_odds]
        loses = [co.current.lose for co in companies_odds]
        
        avg_win = np.mean(wins)
        avg_draw = np.mean(draws)
        avg_lose = np.mean(loses)
        
        # 计算变异系数 (Coefficient of Variation)
        cv_win = np.std(wins) / avg_win
        cv_draw = np.std(draws) / avg_draw
        cv_lose = np.std(loses) / avg_lose
        
        # 平均分歧水平, 通常冷门伴随着高分歧
        avg_cv = (cv_win + cv_draw + cv_lose) / 3.0
        
        # 归一化指数: 经验值 CV=0.15 以上为极高分歧
        return min(1.0, avg_cv / 0.15)
