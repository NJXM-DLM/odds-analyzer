from typing import List
from odds_engine.models.asian_odds import AsianOdds

class AsianAnalyzer:
    """
    亚盘分析模块: 盘口水位变化及异常识别
    """
    
    @staticmethod
    def get_handicap_change(asian: AsianOdds) -> str:
        """
        判断盘口变化：升盘 / 降盘 / 平盘
        """
        if asian.current_handicap > asian.initial_handicap:
            return "升盘"
        elif asian.current_handicap < asian.initial_handicap:
            return "降盘"
        return "平盘"

    @classmethod
    def calculate_asian_anomaly_score(cls, asians: List[AsianOdds]) -> float:
        """
        计算亚盘异常评分 (0~1)
        识别“降盘 + 升水”等不利信号
        """
        if not asians:
            return 0.0
            
        anomaly_count = 0
        for a in asians:
            h_change = cls.get_handicap_change(a)
            # 降盘且即时水位高于初盘
            if h_change == "降盘" and a.current_water_home > a.initial_water_home:
                anomaly_count += 1
            # 盘口未变但水位大幅上升
            elif h_change == "平盘" and a.current_water_home > a.initial_water_home + 0.1:
                anomaly_count += 0.5
                
        return min(1.0, anomaly_count / len(asians))
