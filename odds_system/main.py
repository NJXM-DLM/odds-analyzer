import json
from odds_system.models.data_structures import EuroCompanyOdds, OddsValue, AsianHandicapData
from odds_system.services.analyzer import OddsAnalyzerService

def run_sample_analysis():
    """
    构造模拟数据并运行足球赔率分析系统
    """
    print("=== 足球赔率分析系统 (商用级) ===")
    print("正在构造模拟数据 (3家欧赔公司 + 亚盘数据)...")
    
    # 1. 构造多公司欧赔数据 (模拟数据: 胜平负概率存在分歧且凯利异常)
    euro_odds_data = [
        # 公司 1: Bet365
        EuroCompanyOdds(
            company="Bet365",
            initial=OddsValue(win=2.5, draw=3.2, lose=2.8),
            current=OddsValue(win=2.3, draw=3.3, lose=3.0),
            kelly=OddsValue(win=0.92, draw=0.96, lose=0.91),
            return_rate=0.93
        ),
        # 公司 2: 威廉希尔
        EuroCompanyOdds(
            company="William Hill",
            initial=OddsValue(win=2.45, draw=3.1, lose=2.9),
            current=OddsValue(win=2.35, draw=3.2, lose=3.1),
            kelly=OddsValue(win=0.93, draw=0.94, lose=0.92),
            return_rate=0.94
        ),
        # 公司 3: 立博
        EuroCompanyOdds(
            company="Ladbrokes",
            initial=OddsValue(win=2.4, draw=3.2, lose=2.85),
            current=OddsValue(win=2.25, draw=3.4, lose=3.2),
            kelly=OddsValue(win=0.90, draw=0.98, lose=0.89),
            return_rate=0.92
        )
    ]
    
    # 2. 构造亚盘数据 (模拟数据: 降盘 + 升水)
    asian_handicap_data = AsianHandicapData(
        initial_handicap=0.5,      # 初盘: 主让半球
        current_handicap=0.25,     # 即时: 降为平手/半球
        initial_water_home=0.85,   # 初盘主水: 低水
        current_water_home=1.02    # 即时主水: 升为高水
    )
    
    # 3. 初始化并调用分析服务
    analyzer = OddsAnalyzerService(euro_odds_data, asian_handicap_data)
    result = analyzer.analyze()
    
    # 4. 打印分析报告
    print("\n[分析报告]")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 打印简要结论
    res = result["analysis_result"]
    print("\n[简要结论]")
    print(f"推荐结果: {res['recommendation']['result']}")
    print(f"冷门风险: {res['risk_signals']['risk_level']} (评分: {res['risk_signals']['cold_score']})")
    print(f"核心信号: {', '.join(res['risk_signals']['signals'])}")

if __name__ == "__main__":
    run_sample_analysis()
