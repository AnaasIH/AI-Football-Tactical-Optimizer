import pandas as pd
import pulp

# 1. قراءة البيانات الحقيقية المستخرجة بواسطة الـ Scraper
try:
    df = pd.read_csv("real_players_data.csv")
    print(f"Successfully loaded {len(df)} real players for optimization.")
except FileNotFoundError:
    print("Error: 'real_players_data.csv' not found! Please run scraper.py first.")
    exit()

# 2. تحديد الخطة التكتيكية (4-3-3) وقيد الميزانية المتاحة
tactical_plan = {
    "GK": 1,
    "DF": 4,
    "MF": 3,
    "FW": 3
}
max_budget = 750.0  # الميزانية بالملايين (يمكنك رفعها أو خفضها لترى كيف تتغير التشكيلة!)

# 3. إعداد مسألة التحسين (تعظيم الجاهزية)
prob = pulp.LpProblem("World_Cup_Squad_Optimizer", pulp.LpMaximize)

# 4. متغيرات القرار (Binary: 1 للمختار، 0 للمستبعد)
player_vars = pulp.LpVariable.dicts("Select", df.index, cat='Binary')

# 5. دالة الهدف
prob += pulp.lpSum(df.loc[i, "Form_Index"] * player_vars[i] for i in df.index), "Total_Form"

# 6. إضافة القيود الرياضية

# قيد أ: اختيار 11 لاعباً تماماً
prob += pulp.lpSum(player_vars[i] for i in df.index) == 11, "Total_Players"

# قيد ب: قيد الميزانية المالية الإجمالية
prob += pulp.lpSum(df.loc[i, "Market_Value_M"] * player_vars[i] for i in df.index) <= max_budget, "Budget_Constraint"

# قيد ج: الالتزام بالمراكز (حارس، مدافعين، وسط، هجوم)
for pos, required_count in tactical_plan.items():
    prob += pulp.lpSum(player_vars[i] for i in df.index if df.loc[i, "Position"] == pos) == required_count, f"Pos_{pos}"

# 7. تشغيل الخوارزمية وحل المسألة
status = prob.solve()

# 8. طباعة التشكيلة المثالية المفتشة بالذكاء الاصطناعي
print("\n" + "="*50)
print(f"Optimization Status: {pulp.LpStatus[status]}")
print("="*50)

if pulp.LpStatus[status] == "Optimal":
    print("AI OPTIMIZED SQUAD LINEUP (FROM REAL DATA)")
    print("-" * 50)
    
    selected_players = []
    for i in df.index:
        if player_vars[i].varValue == 1:
            selected_players.append(df.iloc[i])
            
    df_selected = pd.DataFrame(selected_players)
    
    # عرض الجدول النهائي المصنوع بدقة
    print(df_selected[["Player_Name", "Position", "Form_Index", "Market_Value_M"]].to_string(index=False))
    
    print("-" * 50)
    print(f"Total Squad Form Index: {pulp.value(prob.objective):.2f}")
    print(f"Total Team Market Value: {df_selected['Market_Value_M'].sum():.2f} Million USD")
else:
    print("Could not find an optimal solution within the given constraints.")
    print("Try increasing the max_budget or checking the available positions.")

print("="*50 + "\n")