import json
import os
import sys

# Add current directory to path so we can import parsers
sys.path.append(os.getcwd())

from parse_odds_xls import download_and_parse_odds
from parse_asian_xls import parse_asian_handicap
from odds_engine.models.match_data import MatchData
from odds_engine.parsers.parser import DataParser
from odds_engine.services.analyzer import AnalyzerService

def test_integration():
    fixture_id = "1206122"
    euro_url = f"https://odds.500.com/fenxi/ouzhi-{fixture_id}.shtml"
    asian_url = f"https://odds.500.com/fenxi/yazhi-{fixture_id}.shtml"
    
    print(f"--- 正在采集欧赔数据: {euro_url} ---")
    euro_data = download_and_parse_odds(euro_url)
    if isinstance(euro_data, dict) and "error" in euro_data:
        print(f"采集欧赔失败: {euro_data['error']}")
        return

    print(f"--- 正在采集亚盘数据: {asian_url} ---")
    asian_data = parse_asian_handicap(asian_url)
    if isinstance(asian_data, dict) and "error" in asian_data:
        print(f"采集亚盘失败: {asian_data['error']}")
        return

    print(f"--- 正在解析并构造分析模型 ---")
    # 使用 odds_engine 的解析器进行转换和校验
    euros = DataParser.parse_euro(euro_data)
    asians = DataParser.parse_asian(asian_data)
    
    if not euros:
        print("解析后的欧赔数据为空")
        return
    if not asians:
        print("解析后的亚盘数据为空")
        return
        
    match_data = MatchData(euros=euros, asians=asians)
    
    print(f"--- 正在调用 AnalyzerService 进行数据分析 ---")
    result = AnalyzerService.analyze(match_data)
    
    print("\n" + "="*50)
    print("足球赔率分析报告")
    print("="*50)
    print(json.dumps(result, ensure_ascii=False, indent=4))
    print("="*50)

if __name__ == "__main__":
    test_integration()
