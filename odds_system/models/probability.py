import numpy as np
from typing import List
from odds_system.models.data_structures import OddsValue, MarketProbability, EuroCompanyOdds

class ProbabilityCalculator:
    """
    概率计算模块: 处理赔率到隐含概率的转换(去水)以及多公司市场融合
    """

    @staticmethod
    def calculate_implied_probability(odds: OddsValue) -> MarketProbability:
        """
        将欧赔转换为隐含概率（去水/去抽水）
        算法: 1/赔率 / (1/win + 1/draw + 1/lose)
        """
        raw_prob_win = 1.0 / odds.win
        raw_prob_draw = 1.0 / odds.draw
        raw_prob_lose = 1.0 / odds.lose
        
        total_sum = raw_prob_win + raw_prob_draw + raw_prob_lose
        margin = total_sum - 1.0
        
        return MarketProbability(
            win=raw_prob_win / total_sum,
            draw=raw_prob_draw / total_sum,
            lose=raw_prob_lose / total_sum,
            margin=margin
        )

    @classmethod
    def fusion_market_probabilities(cls, companies_odds: List[EuroCompanyOdds]) -> MarketProbability:
        """
        多公司融合模块: 计算市场平均概率，支持基于返还率的加权融合
        """
        if not companies_odds:
            return MarketProbability(0, 0, 0, 0)
            
        all_probs = [cls.calculate_implied_probability(co.current) for co in companies_odds]
        weights = [co.return_rate for co in companies_odds]
        
        # 归一化权重
        total_weight = sum(weights)
        norm_weights = [w / total_weight for w in weights]
        
        fused_win = sum(p.win * w for p, w in zip(all_probs, norm_weights))
        fused_draw = sum(p.draw * w for p, w in zip(all_probs, norm_weights))
        fused_lose = sum(p.lose * w for p, w in zip(all_probs, norm_weights))
        avg_margin = sum(p.margin * w for p, w in zip(all_probs, norm_weights))
        
        return MarketProbability(win=fused_win, draw=fused_draw, lose=fused_lose, margin=avg_margin)
