import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

# Load today's CSV
today = datetime.now(ZoneInfo("America/Los_Angeles")).strftime('%Y-%m-%d')
file_path = f"data/mlb_dashboard_{today}.csv"

st.set_page_config(page_title="Pick-5 Daily Dashboard", layout="wide")
st.title("⚾ Bailee's Dashboard")
st.caption(f"Updated for {today}")

try:
    df = pd.read_csv(file_path)

    # Choose Bet Type: Full Game or F5 ML
    bet_type = st.radio("Choose Bet Type View:", ["Full Game", "F5"])

    # Optional: filter by team
    selected_team = st.selectbox("Filter by Team", ["All"] + sorted(df["Team"].unique().tolist()))
    if selected_team != "All":
        df = df[df["Team"] == selected_team]

    # Safe formatting for mixed data (numbers & strings)
    def safe_format(val, precision=2):
        if isinstance(val, (int, float)):
            return f"{val:.{precision}f}"
        return val

    # Define columns for each view
    full_game_columns = [
        "Team", "Opponent", "Pitcher", "Pitcher Handedness", 
        "ERA (Last 3 Starts)", "WHIP (Last 3 Starts)",
        "Opponent Pitcher", "Opponent Handedness", 
        "Opponent ERA (Last 3 Starts)", "Opponent WHIP (Last 3 Starts)",
        "Team RPG (L7)", "Team OPS (L7)", "Opp RPG (L7)", "Opp OPS (L7)",
        "Lean Call", "Lean Reason"
    ]

    f5_columns = [
        "Team", "Opponent", "Pitcher", "Pitcher Handedness", 
        "ERA (Last 3 Starts)", "WHIP (Last 3 Starts)",
        "Opponent Pitcher", "Opponent Handedness", 
        "Opponent ERA (Last 3 Starts)", "Opponent WHIP (Last 3 Starts)"
    ]

    # Add F5 Call & Reason columns if user selected F5 view
    if bet_type == "F5 ML":
        def generate_f5_call(row):
            try:
                era = float(row["ERA (Last 3 Starts)"])
                whip = float(row["WHIP (Last 3 Starts)"])
                opp_era = float(row["Opponent ERA (Last 3 Starts)"])
                opp_whip = float(row["Opponent WHIP (Last 3 Starts)"])
            except:
                return "Stay Away"

            era_diff = opp_era - era
            whip_diff = opp_whip - whip

            if era_diff >= 1.0 and whip_diff >= 0.15:
                return "Lean ML (Strong)"
            elif era_diff >= 0.6 and whip_diff >= 0.10:
                return "Lean ML (Moderate)"
            elif era_diff <= -1.0 and whip_diff <= -0.15:
                return "Fade ML (Strong)"
            elif era_diff <= -0.6 and whip_diff <= -0.10:
                return "Fade ML (Moderate)"
            else:
                return "Stay Away"

        def explain_f5_reason(row):
            try:
                era_diff = float(row["Opponent ERA (Last 3 Starts)"]) - float(row["ERA (Last 3 Starts)"])
                whip_diff = float(row["Opponent WHIP (Last 3 Starts)"]) - float(row["WHIP (Last 3 Starts)"])
                return f"ERA {era_diff:+.2f} / WHIP {whip_diff:+.2f}"
            except:
                return ""

        df["F5 Call"] = df.apply(generate_f5_call, axis=1)
        df["F5 Reason"] = df.apply(explain_f5_reason, axis=1)
        f5_columns.extend(["F5 Call", "F5 Reason"])

    # Choose columns to show
    columns_to_display = full_game_columns if bet_type == "Full Game" else f5_columns
    df = df[[col for col in columns_to_display if col in df.columns]]

    # Show formatted table
    st.dataframe(df.style.format({
        "ERA (Last 3 Starts)": lambda x: safe_format(x, 2),
        "WHIP (Last 3 Starts)": lambda x: safe_format(x, 2),
        "Opponent ERA (Last 3 Starts)": lambda x: safe_format(x, 2),
        "Opponent WHIP (Last 3 Starts)": lambda x: safe_format(x, 2),
        "Team RPG (L7)": lambda x: safe_format(x, 2),
        "Team OPS (L7)": lambda x: safe_format(x, 3),
        "Opp RPG (L7)": lambda x: safe_format(x, 2),
        "Opp OPS (L7)": lambda x: safe_format(x, 3)
    }))

    # ✅ Weather Checklist
    with st.expander("📝 MLB Weather Checklist – ML vs RL", expanded=False):
        st.markdown("""
        **Run through this checklist before placing a bet:**

        - **Wind out (10+ mph):** More runs expected → *Better for RL*
        - **Wind in (10+ mph):** Fewer runs expected → *ML safer*
        - **Rain delay risk:** Watch for scratches/postponements
        - **Hot temps (80°F+):** Ball carries more → *RL edge*
        - **Cold temps (below 60°F):** Pitcher-friendly → *ML edge*
        - **Humidity:** Boosts carry → *slight edge to RL*
        - **High elevation (e.g., COL):** More runs → *RL edge*
        """)

    # 💡 F5 Cheat Sheet (only appears if F5 is selected)
    if bet_type == "F5 ML":
        with st.expander("🧠 F5 ML Cheat Sheet", expanded=False):
            st.markdown("""
            **F5 ML Betting Tips:**

            - 🎯 Focus on **starting pitchers only** — bullpen doesn’t matter
            - 🔍 Compare **ERA & WHIP (Last 3 Starts)** — better = edge
            - 🔄 Use **handedness** to judge lineup matchup risk
            - 🚫 Ignore full-game RPG or OPS — they don’t affect F5 bets
            - ⏱️ Great for teams with strong starters but shaky bullpens
            """)

        with st.expander("📊 F5 Call Key", expanded=False):
            st.markdown("""
            **Lean Call Meaning:**

            - **Lean ML (Strong):** Your starter is better by ≥ 1.00 ERA and ≥ 0.15 WHIP  
            - **Lean ML (Moderate):** Your starter is better by ≥ 0.60 ERA and ≥ 0.10 WHIP  
            - **Fade ML (Strong):** Opponent starter better by same margins  
            - **Fade ML (Moderate):** Opponent slightly better  
            - **Stay Away:** No meaningful edge — toss-up
            """)

    # 📊 Full Game Key
    if bet_type == "Full Game":
        with st.expander("📊 Full Game Call Key", expanded=False):
            st.markdown("""
            **Lean Call Meaning:**

            - **Lean RL (Strong):** You have both a pitching and offensive edge  
            - **Lean ML (Moderate):** You have at least one edge (pitching or offense)  
            - **Fade ML (Strong):** Opponent has both pitching and offensive edge  
            - **Stay Away:** No meaningful gap — let it go  
            - **Lean Reason column:** Explains differences in ERA, WHIP, OPS, and RPG
            """)

    # Download button
    st.download_button("📥 Download CSV", df.to_csv(index=False), file_name=f"mlb_dashboard_{today}.csv")

except FileNotFoundError:
    st.error("No dashboard CSV found for today. Make sure you've run your notebook to generate it first.")
