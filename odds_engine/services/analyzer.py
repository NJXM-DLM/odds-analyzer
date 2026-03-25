from typing import Dict
from odds_engine.models.match_data import MatchData
from odds_engine.core.probability import ProbabilityCalculator
from odds_engine.core.kelly import KellyAnalyzer
from odds_engine.core.divergence import DivergenceAnalyzer
from odds_engine.core.trend import TrendAnalyzer
from odds_engine.core.asian import AsianAnalyzer
from odds_engine.core.conflict import ConflictDetector
from odds_engine.core.cold_risk import ColdRiskModel
from odds_engine.core.recommendation import RecommendationModel

class AnalyzerService:
    """
    分析服务: 协调各核心模块完成完整分析流程
    """
    
    @staticmethod
    def analyze(match: MatchData) -> Dict:
        """
        全量分析入口
        """
        # 1. 基础数据计算
        prob = ProbabilityCalculator.get_market_average_probability(match.euros)
        min_kelly = KellyAnalyzer.get_min_kelly(match.euros)
        
        # 2. 核心指标分析
        euro_div = DivergenceAnalyzer.calculate_euro_divergence(match.euros)
        kelly_anomaly = KellyAnalyzer.calculate_kelly_anomaly(match.euros)
        trend_conflict = TrendAnalyzer.get_trend_conflict_score(match.euros)
        win_trend = TrendAnalyzer.analyze_win_trend(match.euros)
        asian_anomaly = AsianAnalyzer.calculate_asian_anomaly_score(match.asians)
        has_conflict = ConflictDetector.detect_euro_asian_conflict(match.euros, match.asians)
        
        # 3. 冷门模型评分
        cold_score = ColdRiskModel.calculate_cold_score(
            euro_div, kelly_anomaly, trend_conflict, asian_anomaly, has_conflict
        )
        risk_level = ColdRiskModel.get_risk_level(cold_score)
        signals = ColdRiskModel.generate_signals(
            euro_div, kelly_anomaly, trend_conflict, asian_anomaly, has_conflict
        )
        
        # 4. 推荐结果
        rec_data = RecommendationModel.calculate_recommendation(prob, min_kelly)
        
        # 5. 组装结果
        return {
            "cold_score": cold_score,
            "risk_level": risk_level,
            "trend": win_trend,
            "recommendation": rec_data["recommendation"],
            "probability": {k: round(v, 4) for k, v in prob.items()},
            "signals": signals,
            "confidence_indices": rec_data["indices"]
        }
