import pandas as pd

def get_real_player_data():
    print("Fetching deep player statistics from Open-Source Repository...")
    url = "https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/2023-24/players_raw.csv"
    
    try:
        df_raw = pd.read_csv(url)
        df_filtered = pd.DataFrame()
        
        # 1. المعلومات الأساسية
        df_filtered['Player_Name'] = df_raw['web_name']
        
        position_map = {1: 'GK', 2: 'DF', 3: 'MF', 4: 'FW'}
        df_filtered['Position'] = df_raw['element_type'].map(position_map)
        df_filtered['Market_Value_M'] = pd.to_numeric(df_raw['now_cost'], errors='coerce').fillna(0) / 10
        
        # 2. جلب وتحديد النادي (تحويل أرقام الأندية إلى أسمائها الحقيقية)
        team_map = {
            1: "Arsenal", 2: "Aston Villa", 3: "Bournemouth", 4: "Brentford", 5: "Brighton",
            6: "Burnley", 7: "Chelsea", 8: "Crystal Palace", 9: "Everton", 10: "Fulham",
            11: "Liverpool", 12: "Luton", 13: "Man City", 14: "Man Utd", 15: "Newcastle",
            16: "Nottingham Forest", 17: "Sheffield Utd", 18: "Tottenham", 19: "West Ham", 20: "Wolves"
        }
        df_filtered['Club'] = df_raw['team'].map(team_map).fillna("Unknown Club")
        
        # 3. إحصائيات الأداء التفصيلية الحقيقية
        df_filtered['Goals'] = df_raw['goals_scored'].fillna(0).astype(int)
        df_filtered['Assists'] = df_raw['assists'].fillna(0).astype(int)
        df_filtered['ICT_Index'] = pd.to_numeric(df_raw['ict_index'], errors='coerce').fillna(0)
        
        # 4. الحالة الطبية للاعب
        status_map = {'a': '🟢 جاهز', 'i': '🔴 مصاب', 's': '🟡 موقوف', 'd': '🟡 مشكوك بمشاركته'}
        df_filtered['Status'] = df_raw['status'].map(status_map).fillna("⚪ غير معروف")
        
        # 5. حساب الـ Form Index المتطور بناءً على الأرقام الحقيقية
        form_indices = []
        for idx, row in df_raw.iterrows():
            pos = position_map.get(row['element_type'], 'MF')
            gls = float(row.get('goals_scored', 0))
            ast = float(row.get('assists', 0))
            cs = float(row.get('clean_sheets', 0))
            saves = float(row.get('saves', 0))
            gc = float(row.get('goals_conceded', 0))
            ict = float(row.get('ict_index', 0))
            
            if pos == 'GK': score = 50 + (cs * 8) + (saves * 2) - (gc * 2)
            elif pos == 'DF': score = 50 + (cs * 6) + (gls * 6) + (ast * 3) + (ict * 0.1)
            elif pos == 'MF': score = 50 + (ast * 5) + (gls * 4) + (ict * 0.2)
            elif pos == 'FW': score = 50 + (gls * 7) + (ast * 4) + (ict * 0.2)
            else: score = 50
            form_indices.append(score)
            
        df_filtered['Form_Index'] = form_indices
        
        # حفظ الملف المليء بالمعلومات الجديدة
        df_filtered.to_csv("real_players_data.csv", index=False)
        print("\n✅ Deep data saved to 'real_players_data.csv' successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_real_player_data()