from typing import Dict, List
from odds_system.models.data_structures import AsianHandicapData, EuroCompanyOdds

class AsianHandicapAnalyzer:
    """
    亚盘分析模块: 盘口水位变化分析
    """
    
    @staticmethod
    def analyze_handicap_change(data: AsianHandicapData) -> str:
        """
        计算盘口变化（升盘/降盘/平）
        """
        # 正数为主让, 负数为受让
        if data.current_handicap > data.initial_handicap:
            return "升盘"
        elif data.current_handicap < data.initial_handicap:
            return "降盘"
        return "平盘"

    @staticmethod
    def analyze_water_change(data: AsianHandicapData) -> str:
        """
        计算水位变化 (升水/降水/平水)
        """
        if data.current_water_home > data.initial_water_home:
            return "升水"
        elif data.current_water_home < data.initial_water_home:
            return "降水"
        return "平水"

    @classmethod
    def get_asian_risk_score(cls, data: AsianHandicapData) -> float:
        """
        计算亚盘风险评分 (0~1)
        识别“降盘 + 升水”或“升盘 + 降水”异常
        """
        score = 0.0
        h_change = cls.analyze_handicap_change(data)
        w_change = cls.analyze_water_change(data)
        
        # 异常模式: 降盘 + 升水 (通常表示主队极度不稳)
        if h_change == "降盘" and w_change == "升水":
            score = 0.9
        # 异常模式: 升盘 + 降水 (通常表示主队诱导过热)
        elif h_change == "升盘" and w_change == "降水":
            score = 0.5
        # 盘口未变但水位巨变
        elif h_change == "平盘" and abs(data.current_water_home - data.initial_water_home) > 0.15:
            score = 0.4
            
        return score

    @staticmethod
    def detect_euro_asian_conflict(euro_companies: List[EuroCompanyOdds], asian_data: AsianHandicapData) -> float:
        """
        欧亚冲突检测模块: 
        如果欧赔主胜概率高(或赔率下降), 但亚盘降盘 -> 标记高风险
        返回冲突得分 (0~1)
        """
        if not euro_companies:
            return 0.0
            
        # 市场平均欧赔趋势
        avg_ini_win = sum(co.initial.win for co in euro_companies) / len(euro_companies)
        avg_cur_win = sum(co.current.win for co in euro_companies) / len(euro_companies)
        
        euro_win_trending_down = avg_cur_win < avg_ini_win
        asian_handicap_down = asian_data.current_handicap < asian_data.initial_handicap
        
        # 欧赔示好主队, 亚盘却降盘退让, 极其反常
        if euro_win_trending_down and asian_handicap_down:
            return 1.0
        # 欧赔主胜本身极低, 但亚盘给出的盘口很浅且降盘
        if avg_cur_win < 1.7 and asian_data.current_handicap < 0.5:
            return 0.7
            
        return 0.0
