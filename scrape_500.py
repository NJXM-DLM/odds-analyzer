import requests
from bs4 import BeautifulSoup
import json
import re

def get_matches():
    url = "https://live.500.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        
        html_content = response.text
        soup = BeautifulSoup(html_content, 'lxml')
        
        # Extract liveOddsList from script tags
        odds_data = {}
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string and 'var liveOddsList' in script.string:
                match = re.search(r'var liveOddsList = (\{.*?\});', script.string)
                if match:
                    try:
                        odds_data = json.loads(match.group(1))
                    except:
                        pass
                break
        
        match_table = soup.find('tbody', id='match_list_body')
        if not match_table:
            match_table = soup.find('table', id='table_match')
            
        if not match_table:
            matches = soup.find_all('tr', attrs={'data-mid': True})
            if not matches:
                matches = soup.find_all('tr', id=lambda x: x and x.startswith('tr_'))
        else:
            matches = match_table.find_all('tr')
            if not matches:
                matches = match_table.find_all('tr', recursive=False)
        
        not_started_matches = []
        
        for match in matches:
            tds = match.find_all('td')
            if len(tds) < 8:
                continue
            
            if tds[0].get_text(strip=True) == '场次':
                continue

            status_text = tds[4].get_text(strip=True)
            
            if status_text == '未' or status_text == '':
                league = tds[1].get_text(strip=True)
                match_time = tds[3].get_text(strip=True)
                
                # Extract clean team names from <a> tags
                home_a = tds[5].find('a')
                away_a = tds[7].find('a')
                
                home_team = home_a.get_text(strip=True) if home_a else tds[5].get_text(strip=True)
                away_team = away_a.get_text(strip=True) if away_a else tds[7].get_text(strip=True)
                
                mid = match.get('fid')
                
                # Extract odds
                win, draw, loss = "", "", ""
                if mid and mid in odds_data:
                    m_odds = odds_data[mid]
                    # Try 'sp' first (Chinese Sports Lottery), then '0' (Average)
                    odds_val = m_odds.get('sp') or m_odds.get('0') or m_odds.get('3')
                    if odds_val and len(odds_val) >= 3:
                        win, draw, loss = odds_val[0], odds_val[1], odds_val[2]
                
                analysis_url = f"https://odds.500.com/fenxi/shuju-{mid}.shtml" if mid else ""
                euro_odds_url = f"https://odds.500.com/fenxi/ouzhi-{mid}.shtml" if mid else ""
                asian_odds_url = f"https://odds.500.com/fenxi/yazhi-{mid}.shtml" if mid else ""
                
                not_started_matches.append({
                    '赛事': league,
                    '时间': match_time,
                    '主队': home_team,
                    '客队': away_team,
                    '胜': win,
                    '平': draw,
                    '负': loss,
                    '分析URL': analysis_url,
                    '欧赔URL': euro_odds_url,
                    '亚赔URL': asian_odds_url
                })
        
        # 输出标准的 JSON 格式
        print(json.dumps(not_started_matches, ensure_ascii=False, indent=4))
            
    except Exception as e:
        # 如果出错，也以 JSON 格式输出错误信息
        print(json.dumps({"error": str(e)}, ensure_ascii=False))

if __name__ == "__main__":
    get_matches()
