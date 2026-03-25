import requests
import json
import sys

def scrape_team_history(team_id="719", limit=100):
    # Using the AJAX API discovered for 500.com team fixtures
    url = f"https://liansai.500.com/index.php?c=teams&a=ajax_fixture&tid={team_id}&record={limit}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": f"https://liansai.500.com/team/{team_id}/teamfixture/",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # The response is JSON
        data = response.json()
        
        if 'list' not in data:
            print(json.dumps({"error": "No match list found in API response"}, ensure_ascii=False))
            return

        matches = []
        for item in data['list']:
            # Extract fields from the API response
            league = item.get('SIMPLEGBNAME', '')
            match_time = item.get('MATCHDATE', '')
            home_team = item.get('HOMETEAMSXNAME', '')
            away_team = item.get('AWAYTEAMSXNAME', '')
            
            # Scores might be strings or ints in the API
            try:
                home_score = int(item.get('HOMESCORE', 0))
                away_score = int(item.get('AWAYSCORE', 0))
            except (ValueError, TypeError):
                home_score = 0
                away_score = 0
            
            # Determine result for the target team (team_id)
            is_home = str(item.get('HOMETEAMID')) == str(team_id)
            
            if home_score > away_score:
                match_result = "胜" if is_home else "负"
            elif home_score < away_score:
                match_result = "负" if is_home else "胜"
            else:
                match_result = "平"
            
            # Odds
            odds_win = item.get('WIN', '')
            odds_draw = item.get('DRAW', '')
            odds_loss = item.get('LOST', '')
            
            score_str = f"{home_score}:{away_score}"
            
            matches.append({
                "赛事": league,
                "时间": match_time,
                "主队": home_team,
                "客队": away_team,
                "比分": score_str,
                "赛果": match_result,
                "胜赔": odds_win,
                "平赔": odds_draw,
                "负赔": odds_loss
            })
            
        # Output results
        print(json.dumps(matches, ensure_ascii=False, indent=4))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))

if __name__ == "__main__":
    # Default team_id 719, limit 100
    tid = "719"
    limit = 100
    if len(sys.argv) > 1:
        tid = sys.argv[1]
    if len(sys.argv) > 2:
        limit = sys.argv[2]
        
    scrape_team_history(tid, limit)
