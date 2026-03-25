from typing import List
from odds_engine.models.euro_odds import EuroOdds
from odds_engine.models.asian_odds import AsianOdds

class ConflictDetector:
    """
    欧亚冲突检测模块: 识别欧赔与亚盘方向背离
    """
    
    @staticmethod
    def detect_euro_asian_conflict(euros: List[EuroOdds], asians: List[AsianOdds]) -> bool:
        """
        核心规则：
        - 欧赔支持主胜（赔率下降）
        - 亚盘降盘（退让不足）
        判定为“欧亚冲突”
        """
        if not euros or not asians:
            return False
            
        # 欧赔主胜是否整体下降
        avg_win_init = sum(e.win_init for e in euros) / len(euros)
        avg_win_now = sum(e.win_now for e in euros) / len(euros)
        euro_supports_home = avg_win_now < avg_win_init
        
        # 亚盘是否整体降盘
        asian_drops = sum(1 for a in asians if a.current_handicap < a.initial_handicap)
        asian_handicap_down = asian_drops > (len(asians) / 2)
        
        return euro_supports_home and asian_handicap_down
