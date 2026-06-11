import streamlit as st
import pandas as pd
import pulp
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="AI Scouting & Tactical Analytics Platform", page_icon="⚽", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4AP1A1;'>📊 AI Sports Analytics & Squad Optimization Platform ⚽</h1>", unsafe_allow_html=True)
st.write("---")

def load_data():
    try: 
        return pd.read_csv("real_players_data.csv")
    except FileNotFoundError: 
        return None

df = load_data()

if df is None:
    st.error("❌ Data file not found. Please run 'scraper.py' first to collect real player data!")
else:
    # ---------------- Section 1: Detailed Player Scouting Card ----------------
    st.header("🔍 Detailed Player Scouting Card")
    
    all_players = sorted(df['Player_Name'].unique())
    selected_search_player = st.selectbox("Search or select a player to view their deep technical profile:", all_players)
    
    p_info = df[df['Player_Name'] == selected_search_player].iloc[0]
    
    card_col1, card_col2, card_col3, card_col4 = st.columns(4)
    with card_col1:
        st.markdown(f"### 🏃‍♂️ {p_info['Player_Name']}")
        st.markdown(f"**🏠 Real Club:** {p_info['Club']}")
        st.markdown(f"**🛡️ Tactical Position:** {p_info['Position']}")
    with card_col2:
        st.markdown("### 📈 Season Stats")
        st.markdown(f"**⚽ Goals Scored:** {p_info['Goals']} Goals")
        st.markdown(f"**🎯 Assists:** {p_info['Assists']} Assists")
    with card_col3:
        st.markdown("### 🧠 Tactical Intelligence")
        st.markdown(f"**⭐ Advanced Form Index:** {p_info['Form_Index']:.1f}")
        st.markdown(f"**📐 ICT Index (Influence):** {p_info['ICT_Index']:.1f}")
    with card_col4:
        st.markdown("### 💰 Value & Medical")
        st.markdown(f"**💵 Market Value:** ${p_info['Market_Value_M']:.1f} M")
        st.markdown(f"**🏥 Availability Status:** {p_info['Status']}")
        
    st.write("---")

    # ---------------- Section 2: Sidebar Tactical Controls ----------------
    st.sidebar.header("⚙️ AI Engine Settings")
    formation = st.sidebar.selectbox("Choose Tactical Formation:", ["4-3-3", "4-4-2", "3-5-2", "5-3-2"])
    
    if formation == "4-3-3": tactical_plan = {"GK": 1, "DF": 4, "MF": 3, "FW": 3}
    elif formation == "4-4-2": tactical_plan = {"GK": 1, "DF": 4, "MF": 4, "FW": 2}
    elif formation == "3-5-2": tactical_plan = {"GK": 1, "DF": 3, "MF": 5, "FW": 2}
    else: tactical_plan = {"GK": 1, "DF": 5, "MF": 3, "FW": 2}

    max_budget = st.sidebar.slider("Maximum Budget ($M):", 40.0, 120.0, 80.0, 2.0)
    exclude_injured = st.sidebar.checkbox("🚨 Auto-Exclude Injured/Suspended Players", value=True)
    
    if exclude_injured:
        # Filtering using the English status flags saved by your scraper
        df_ready = df[df['Status'].str.contains('Ready|جاهز', na=False)].reset_index(drop=True)
    else:
        df_ready = df.copy()

    # ---------------- Section 3: Mathematical Optimization Engine (MILP) ----------------
    prob = pulp.LpProblem("World_Cup_Squad_Optimizer", pulp.LpMaximize)
    player_vars = pulp.LpVariable.dicts("Select", df_ready.index, cat='Binary')
    
    # Objective function
    prob += pulp.lpSum(df_ready.loc[i, "Form_Index"] * player_vars[i] for i in df_ready.index)
    
    # Mathematical constraints
    prob += pulp.lpSum(player_vars[i] for i in df_ready.index) == 11
    prob += pulp.lpSum(df_ready.loc[i, "Market_Value_M"] * player_vars[i] for i in df_ready.index) <= max_budget
    
    for pos, required_count in tactical_plan.items():
        prob += pulp.lpSum(player_vars[i] for i in df_ready.index if df_ready.loc[i, "Position"] == pos) == required_count

    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # ---------------- Section 4: AI Results & Visualizations ----------------
    if pulp.LpStatus[status] == "Optimal":
        selected_players = [df_ready.iloc[i] for i in df_ready.index if player_vars[i].varValue == 1]
        df_selected = pd.DataFrame(selected_players)

        st.header("📋 AI-Optimized Squad & Advanced Analytics")
        
        # Key Performance Indicators (KPIs)
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1: 
            st.metric("📊 Total Team Form Index", f"{pulp.value(prob.objective):.1f}")
        with kpi2: 
            total_spent = df_selected['Market_Value_M'].sum()
            st.metric("💰 Total Squad Cost", f"${total_spent:.1f} M", f"Remaining: ${max_budget - total_spent:.1f} M")
        with kpi3: 
            st.metric("📋 Active Formation", formation)

        st.write("---")

        main_col1, main_col2 = st.columns([1, 1])

        with main_col1:
            st.subheader("📋 Optimized 11-Player Squad Roster")
            df_view = df_selected[['Player_Name', 'Club', 'Position', 'Form_Index', 'Market_Value_M']].rename(
                columns={
                    'Player_Name': 'Player Name', 
                    'Club': 'Real Club', 
                    'Position': 'Position', 
                    'Form_Index': 'Form Rating', 
                    'Market_Value_M': 'Value ($M)'
                }
            )
            st.dataframe(df_view, use_container_width=True, hide_index=True, height=400)

        with main_col2:
            # Multi-Chart Tabs Layout
            tab1, tab2, tab3 = st.tabs(["🍕 Club Distribution Cycle", "📊 Form Rating Analysis", "💰 Budget Allocation"])
            
            with tab1:
                club_counts = df_selected['Club'].value_counts().reset_index()
                club_counts.columns = ['Club', 'Count']
                
                fig_donut = px.pie(club_counts, values='Count', names='Club', hole=0.4,
                                   title="Donut Cycle: Squad Diversity by Real-World Clubs",
                                   color_discrete_sequence=px.colors.sequential.Teal)
                st.plotly_chart(fig_donut, use_container_width=True)
                
            with tab2:
                fig_bar = px.bar(df_selected, x='Player_Name', y='Form_Index', color='Position',
                                 labels={'Player_Name': 'Player', 'Form_Index': 'Form Rating'},
                                 title="Player Form Performance Comparison")
                st.plotly_chart(fig_bar, use_container_width=True)
                
            with tab3:
                fig_pie = px.pie(df_selected, values='Market_Value_M', names='Position',
                                 title="Financial Budget Allocation on the Pitch",
                                 color_discrete_sequence=px.colors.sequential.Blugrn)
                st.plotly_chart(fig_pie, use_container_width=True)
                
        # ---------------- Section 5: Learning Hub ----------------
        st.write("---")
        with st.expander("🎓 Click here to learn how the AI algorithm calculates this squad mathematically"):
            st.markdown("""
            ### 🛠️ The Operations Research behind this Dashboard (Linear Programming)
            This engine avoids random guessing by solving a formal **Mixed-Integer Linear Programming (MILP)** problem using the `PuLP` library. Here is how the computer thinks in pure math symbols:
            
            1. **Objective Function:** Maximize the accumulated form value of the 11 selected players:
               $$\max \sum (\text{Form\_Index}_i \times X_i)$$
               *Where $X_i \in \{0, 1\}$ represents whether a player is selected ($1$) or benched ($0$).*
               
            2. **Roster Size Constraint:** Ensure exactly 11 players are active on the pitch:
               $$\sum X_i = 11$$
               
            3. **Financial Budget Constraint:** The total market value of the chosen stars cannot exceed your slider input limit:
               $$\sum (\text{Market\_Value\_M}_i \times X_i) \le \text{Max\_Budget}$$
               
            4. **Tactical Architecture Constraints:** Forces the system to select precise positional counts based on your active formation (e.g., exactly 4 Defenders and 1 Goalkeeper for a 4-3-3 tactic).
            """)
            
    else:
        st.error("❌ Optimal solution not found! The selected budget is too tight to build an active 11-player lineup with your positional and medical rules. Please increase the budget slider.")

st.write("---")
st.markdown("<p style='text-align: center; color: gray;'>Engineered for Elite Football Performance Analytics • 2026 ⚽</p>", unsafe_allow_html=True)