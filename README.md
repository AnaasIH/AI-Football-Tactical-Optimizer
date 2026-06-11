# 📊 AI-Driven Football Squad Optimizer & Technical Scouting Platform ⚽

An advanced, end-to-end sports analytics application that leverages **Mixed-Integer Linear Programming (MILP)** to construct mathematically optimal football lineups based on real-time fantasy data, market values, and medical availability.

---

## 🚀 Key Features

- **Advanced Technical Scouting DB:** A live analytics search card exposing realistic statistical values for every single player, including Goals, Assists, Value, and official Fantasy ICT (Influence, Creativity, Threat) metrics.
- **Dynamic Positional Weights:** A built-in feature engineering system computing custom Form Index metrics based on positional responsibilities (e.g., Clean Sheets for Defenders vs. Shot Conversion impact for Forwards).
- **Mathematical Multi-Constraint Optimization:** Leverages operations research algorithms to guarantee an optimal squad balance given tight budgetary limits and tactical formations (4-3-3, 4-4-2, 3-5-2, etc.).
- **Rich Business Intelligence Visualizations:** Built with interactive Plotly visuals mapping tactical money spend, club dependency donut cycles, and technical efficiency vs price scatter graphs.
- **Risk Mitigation Controls:** Sidebar option allowing recruiters to completely eliminate injured or suspended stars instantly before optimization occurs.

---

## 🧮 Mathematical Architecture (Operations Research)

This application treats squad selection as a formal mathematical optimization problem rather than a set of heuristic rules. Powered by the `PuLP` optimization library:

1. **Objective Function:** Maximize total squad technical efficiency:
   $$\max \sum_{i \in P} (\text{Form}_i \times X_i)$$
   *Where $X_i \in \{0, 1\}$ dictates whether player $i$ is selected ($1$) or not ($0$).*

2. **Roster Constraint:** Restricting the selection vector to exactly 11 players:
   $$\sum_{i \in P} X_i = 11$$

3. **Financial Knapsack Constraint:** Total price cannot exceed user budget limitations:
   $$\sum_{i \in P} (\text{Cost}_i \times X_i) \le \text{Budget}$$

4. **Positional Architecture Constraints:** Forcing explicit integer counts per sector according to the active tactic:
   $$\sum_{i \in \text{Position}_k} X_i = \text{Required}_k$$

---

## 🛠️ Tech Stack & Architecture

- **Language:** Python
- **GUI Dashboard:** Streamlit
- **Optimization Solver:** PuLP (COIN-OR CBC Solver)
- **Interactive Graphs:** Plotly Express
- **Data Engineering:** Pandas & NumPy

---

## ⚙️ How to Install & Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
   cd YOUR_REPOSITORY_NAME
   pip install -r requirements.txt
   python scraper.py
   streamlit run app.py
