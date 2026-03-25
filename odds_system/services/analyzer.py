from typing import List, Dict
import json
import numpy as np
from odds_system.models.data_structures import EuroCompanyOdds, AsianHandicapData, MarketProbability
from odds_system.models.probability import ProbabilityCalculator
from odds_system.models.kelly import KellyAnalyzer
from odds_system.models.divergence import DivergenceAnalyzer
from odds_system.models.trend import TrendAnalyzer
from odds_system.models.asian_handicap import AsianHandicapAnalyzer
from odds_system.models.cold_risk import ColdRiskModel
from odds_system.models.recommendation import RecommendationModel

class OddsAnalyzerService:
    """
    足球赔率分析系统 - 编排服务层
    """
    
    def __init__(self, euro_odds: List[EuroCompanyOdds], asian_odds: AsianHandicapData):
        self.euro_odds = euro_odds
        self.asian_odds = asian_odds

    def analyze(self) -> Dict:
        """
        全量流程分析
        """
        # 1. 概率计算与融合
        market_prob = ProbabilityCalculator.fusion_market_probabilities(self.euro_odds)
        
        # 2. 分歧分析
        divergence_idx = DivergenceAnalyzer.get_divergence_index(self.euro_odds)
        std_deviation = DivergenceAnalyzer.calculate_std_deviation(self.euro_odds)
        
        # 3. 凯利分析
        min_kelly = KellyAnalyzer.get_min_kelly(self.euro_odds)
        kelly_anomaly = KellyAnalyzer.identify_kelly_anomaly(self.euro_odds)
        
        # 4. 时间趋势与冲突检测
        trend_conflict = TrendAnalyzer.detect_conflict_signals(self.euro_odds)
        
        # 5. 亚盘分析
        asian_risk = AsianHandicapAnalyzer.get_asian_risk_score(self.asian_odds)
        euro_asian_conflict = AsianHandicapAnalyzer.detect_euro_asian_conflict(self.euro_odds, self.asian_odds)
        
        # 6. 冷门识别模型
        cold_score = ColdRiskModel.calculate_cold_score(
            divergence_idx, kelly_anomaly, trend_conflict, asian_risk, euro_asian_conflict
        )
        risk_level = ColdRiskModel.get_risk_level(cold_score)
        signals = ColdRiskModel.explain_signals(
            divergence_idx, kelly_anomaly, trend_conflict, asian_risk, euro_asian_conflict
        )
        
        # 7. 推荐算法
        rec_index = RecommendationModel.calculate_recommendation_index(market_prob, min_kelly)
        recommendation = RecommendationModel.get_recommendation_result(rec_index)
        
        # 8. 构造最终报告
        report = {
            "analysis_result": {
                "probability": {
                    "win": round(market_prob.win, 4),
                    "draw": round(market_prob.draw, 4),
                    "lose": round(market_prob.lose, 4)
                },
                "market_consensus": {
                    "divergence_index": round(divergence_idx, 4),
                    "std_deviation": {k: round(v, 4) for k, v in std_deviation.items()}
                },
                "risk_signals": {
                    "cold_score": round(cold_score, 4),
                    "risk_level": risk_level,
                    "signals": signals
                },
                "recommendation": {
                    "result": recommendation,
                    "confidence_index": {k: round(v, 4) for k, v in rec_index.items()}
                }
            }
        }
        
        return report
