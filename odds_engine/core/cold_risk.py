from typing import List, Dict
from odds_engine.models.match_data import MatchData

class ColdRiskModel:
    """
    冷门识别模型: 综合各项核心指标计算评分
    """
    
    @staticmethod
    def calculate_cold_score(
        euro_div: float,
        kelly_anomaly: float,
        trend_conflict: float,
        asian_anomaly: float,
        has_conflict: bool
    ) -> float:
        """
        综合评分算法：
        cold_score = 0.4 * 欧赔分歧 + 0.25 * 凯利异常 + 0.2 * 时间趋势冲突 + 0.15 * 亚盘异常
        """
        base_score = (
            0.4 * euro_div +
            0.25 * kelly_anomaly +
            0.2 * trend_conflict +
            0.15 * asian_anomaly
        )
        
        # 欧亚冲突作为一个额外的乘数或加分项 (商用逻辑通常更重信号)
        if has_conflict:
            base_score = min(1.0, base_score + 0.2)
            
        return round(base_score, 2)

    @staticmethod
    def get_risk_level(score: float) -> str:
        """
        风险等级映射
        """
        if score < 0.35: return "低"
        elif score < 0.7: return "中"
        return "高"

    @staticmethod
    def generate_signals(
        euro_div: float,
        kelly_anomaly: float,
        trend_conflict: float,
        asian_anomaly: float,
        has_conflict: bool
    ) -> List[str]:
        """
        产生解释信号
        """
        signals = []
        if euro_div > 0.6: signals.append("公司分歧大")
        if kelly_anomaly > 0.6: signals.append("凯利异常")
        if trend_conflict > 0.5: signals.append("趋势冲突信号")
        if asian_anomaly > 0.6: signals.append("盘口水位异常")
        if has_conflict: signals.append("欧亚冲突明显")
        
        if not signals:
            signals.append("数据波动平稳")
            
        return signals
