import requests
from bs4 import BeautifulSoup
import json
import re
import sys
import subprocess

def parse_asian_handicap(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": url
    }
    
    # 盘口转换映射表
    handicap_map = {
        "平手": 0.0,
        "平手/半球": 0.25,
        "半球": 0.5,
        "半球/一球": 0.75,
        "一球": 1.0,
        "一球/球半": 1.25,
        "球半": 1.5,
        "球半/两球": 1.75,
        "两球": 2.0,
        "两球/两球半": 2.25,
        "两球半": 2.5,
        "受平手/半球": -0.25,
        "受半球": -0.5,
        "受半球/一球": -0.75,
        "受一球": -1.0,
        "受一球/球半": -1.25,
        "受球半": -1.5,
        "受球半/两球": -1.75,
        "受两球": -2.0
    }

    def convert_handicap(h_str):
        if not h_str: return 0.0
        # 尝试直接映射
        if h_str in handicap_map:
            return handicap_map[h_str]
        # 尝试解析数字 (如 "0.5", "1/1.5")
        try:
            if '/' in h_str:
                parts = h_str.split('/')
                return (float(parts[0]) + float(parts[1])) / 2
            return float(h_str)
        except:
            return 0.0

    try:
        # Use curl to fetch the HTML as it seems more reliable for this site
        cmd = f"curl -s -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' '{url}'"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        try:
            html_content = stdout.decode('gbk')
        except:
            html_content = stdout.decode('utf-8', errors='ignore')
            
        soup = BeautifulSoup(html_content, 'html.parser')
        data_rows = soup.find_all('tr', attrs={'xls': 'row'})
        
        if not data_rows:
            data_rows = soup.find_all('tr', class_=lambda x: x in ['tr1', 'tr2'])
            data_rows = [tr for tr in data_rows if tr.get('id') and tr.get('id').isdigit()]

        results = []
        
        for tr in data_rows:
            tds = tr.find_all('td', recursive=False)
            if len(tds) < 6:
                continue
                
            company_td = tds[1]
            company_span = company_td.find('span', class_='quancheng')
            company = company_span.get_text(strip=True) if company_span else company_td.get_text(strip=True)
            company = re.sub(r'[\d\*]+$', '', company).strip()
            
            def get_raw_odds(td):
                nested_table = td.find('table')
                if nested_table:
                    nested_tds = nested_table.find_all('td')
                    if len(nested_tds) >= 3:
                        water_home = nested_tds[0].get_text(strip=True).replace('↑', '').replace('↓', '')
                        handicap = nested_tds[1].get_text(strip=True).replace('升', '').replace('降', '').strip()
                        return handicap, water_home
                return None, None

            current_raw = get_raw_odds(tds[2])
            initial_raw = get_raw_odds(tds[4])
            
            if current_raw[0] and initial_raw[0]:
                results.append({
                    "company": company,
                    "initial_handicap": convert_handicap(initial_raw[0]),
                    "current_handicap": convert_handicap(current_raw[0]),
                    "initial_water_home": float(initial_raw[1]) if initial_raw[1] else 0.0,
                    "current_water_home": float(current_raw[1]) if current_raw[1] else 0.0
                })
        
        print(f"DEBUG: Found {len(results)} rows.")
        return results
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = "https://odds.500.com/fenxi/yazhi-1337814.shtml"
    
    result = parse_asian_handicap(target_url)
    print(json.dumps(result, ensure_ascii=False, indent=4))
