from typing import List, Dict
from odds_system.models.data_structures import EuroCompanyOdds, AsianHandicapData
from odds_system.models.divergence import DivergenceAnalyzer
from odds_system.models.kelly import KellyAnalyzer
from odds_system.models.trend import TrendAnalyzer
from odds_system.models.asian_handicap import AsianHandicapAnalyzer

class ColdRiskModel:
    """
    冷门识别模型: 综合各项指标计算冷门评分
    """
    
    @staticmethod
    def calculate_cold_score(
        divergence_idx: float,
        kelly_anomaly: float,
        trend_conflict: float,
        asian_risk: float,
        euro_asian_conflict: float
    ) -> float:
        """
        综合计算冷门评分 (0~1)
        权重: 0.4 * 分歧 + 0.25 * 凯利 + 0.2 * 趋势冲突 + 0.15 * 亚盘 + 0.1 * 欧亚冲突 (调整后)
        """
        # 加权融合
        score = (
            0.35 * divergence_idx + 
            0.2 * kelly_anomaly + 
            0.15 * trend_conflict + 
            0.15 * asian_risk + 
            0.15 * euro_asian_conflict
        )
        
        return min(1.0, max(0.0, score))

    @staticmethod
    def get_risk_level(score: float) -> str:
        """
        风险等级评定
        """
        if score < 0.35: return "低"
        elif score < 0.7: return "中"
        return "高"

    @staticmethod
    def explain_signals(
        divergence_idx: float,
        kelly_anomaly: float,
        trend_conflict: float,
        asian_risk: float,
        euro_asian_conflict: float
    ) -> List[str]:
        """
        冷门原因解释
        """
        signals = []
        if divergence_idx > 0.5: signals.append("公司分歧大")
        if kelly_anomaly > 0.5: signals.append("凯利指数异常")
        if trend_conflict > 0.5: signals.append("时间趋势冲突")
        if asian_risk > 0.5: signals.append("盘口异常波动")
        if euro_asian_conflict > 0.5: signals.append("欧亚冲突明显")
        
        if not signals:
            signals.append("数据波动正常")
            
        return signals
