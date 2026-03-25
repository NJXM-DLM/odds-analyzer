import requests
import pandas as pd
import sys
import re
import json

def get_fixture_id(url):
    # Match id from URL like https://odds.500.com/fenxi/ouzhi-1366307.shtml
    match = re.search(r'ouzhi-(\d+)\.shtml', url)
    if match:
        return match.group(1)
    return None

def download_and_parse_odds(url):
    fixture_id = get_fixture_id(url)
    if not fixture_id:
        return {"error": "Invalid URL format. Could not find fixture ID."}

    export_url = "https://odds.500.com/fenxi/europe_xls.php"
    payload = {
        "fixtureid": fixture_id,
        "excelst": "1",
        "style": "0",
        "ctype": "1",
        "dcid": "",
        "scid": "",
        "r": "1"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": url
    }
    
    try:
        response = requests.post(export_url, data=payload, headers=headers)
        response.raise_for_status()
        
        filename = f"temp_odds_{fixture_id}.xls"
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        # Read the second sheet (index 1) without header initially
        df = pd.read_excel(filename, sheet_name=1, header=None)
        
        # Cleanup temp file
        if os.path.exists(filename):
            os.remove(filename)

        company_odds_list = []
        
        for index, row in df.iterrows():
            company = str(row[0]).strip()
            if company == 'nan' or company == '欧赔公司' or company == 'None' or not company:
                continue
                
            if company in ['最高值', '最低值', '平均值', '离散值']:
                continue
            
            entry = {
                "company": company,
                "win_init": float(row[11]) if not pd.isna(row[11]) else 0.0,
                "draw_init": float(row[12]) if not pd.isna(row[12]) else 0.0,
                "lose_init": float(row[13]) if not pd.isna(row[13]) else 0.0,
                "win_now": float(row[1]) if not pd.isna(row[1]) else 0.0,
                "draw_now": float(row[2]) if not pd.isna(row[2]) else 0.0,
                "lose_now": float(row[3]) if not pd.isna(row[3]) else 0.0,
                "kelly_win": float(row[8]) if not pd.isna(row[8]) else 0.0,
                "kelly_draw": float(row[9]) if not pd.isna(row[9]) else 0.0,
                "kelly_lose": float(row[10]) if not pd.isna(row[10]) else 0.0,
                "return_rate": float(row[7]) if not pd.isna(row[7]) else 0.0
            }
            company_odds_list.append(entry)
            
        return company_odds_list
        
    except Exception as e:
        return {"error": str(e)}

import os

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = "https://odds.500.com/fenxi/ouzhi-1366307.shtml"
    
    result = download_and_parse_odds(target_url)
    print(json.dumps(result, ensure_ascii=False, indent=4))
