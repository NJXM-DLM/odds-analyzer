from typing import List, Dict, Any
from odds_engine.models.euro_odds import EuroOdds
from odds_engine.models.asian_odds import AsianOdds

class DataParser:
    """
    解析模块: 校验字段并转换为 DataClass
    """
    
    @staticmethod
    def parse_euro(data: List[Dict[str, Any]]) -> List[EuroOdds]:
        """
        解析并校验欧赔数据
        """
        required_keys = {
            "company", "win_init", "draw_init", "lose_init", 
            "win_now", "draw_now", "lose_now", 
            "kelly_win", "kelly_draw", "kelly_lose", "return_rate"
        }
        
        parsed = []
        for item in data:
            if not required_keys.issubset(item.keys()):
                continue
            
            # 过滤异常值 (例如赔率不能为0)
            if any(item[k] <= 0 for k in ["win_init", "win_now", "return_rate"]):
                continue
                
            parsed.append(EuroOdds(**item))
        return parsed

    @staticmethod
    def parse_asian(data: List[Dict[str, Any]]) -> List[AsianOdds]:
        """
        解析并校验亚盘数据
        """
        required_keys = {"company", "initial_handicap", "current_handicap", "initial_water_home", "current_water_home"}
        
        parsed = []
        for item in data:
            if not required_keys.issubset(item.keys()):
                continue
            parsed.append(AsianOdds(**item))
        return parsed
