import json
from odds_engine.models.match_data import MatchData
from odds_engine.parsers.parser import DataParser
from odds_engine.services.analyzer import AnalyzerService

def main():
    """
    足球赔率分析引擎入口
    """
    print("=== 足球赔率分析引擎 (Commercial Grade) ===")
    
    # 1. 模拟输入 JSON 数据
    euro_json = [
        {
            "company": "Bet365",
            "win_init": 2.5, "draw_init": 3.2, "lose_init": 2.8,
            "win_now": 2.3, "draw_now": 3.3, "lose_now": 3.0,
            "kelly_win": 0.92, "kelly_draw": 0.96, "kelly_lose": 0.91,
            "return_rate": 0.93
        },
        {
            "company": "William Hill",
            "win_init": 2.45, "draw_init": 3.1, "lose_init": 2.9,
            "win_now": 2.35, "draw_now": 3.2, "lose_now": 3.1,
            "kelly_win": 0.93, "kelly_draw": 0.94, "kelly_lose": 0.92,
            "return_rate": 0.94
        },
        {
            "company": "Ladbrokes",
            "win_init": 2.4, "draw_init": 3.2, "lose_init": 2.85,
            "win_now": 2.2, "draw_now": 3.4, "lose_now": 3.2,
            "kelly_win": 0.88, "kelly_draw": 0.98, "kelly_lose": 0.89,
            "return_rate": 0.92
        }
    ]
    
    asian_json = [
        {
            "company": "Bet365",
            "initial_handicap": 0.5,
            "current_handicap": 0.25,
            "initial_water_home": 0.85,
            "current_water_home": 1.05
        },
        {
            "company": "Crown",
            "initial_handicap": 0.5,
            "current_handicap": 0.25,
            "initial_water_home": 0.88,
            "current_water_home": 1.02
        }
    ]
    
    # 2. 解析数据
    euros = DataParser.parse_euro(euro_json)
    asians = DataParser.parse_asian(asian_json)
    match_data = MatchData(euros=euros, asians=asians)
    
    # 3. 执行分析
    result = AnalyzerService.analyze(match_data)
    
    # 4. 输出 JSON 结果
    print("\n[分析报告]")
    print(json.dumps(result, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main()
