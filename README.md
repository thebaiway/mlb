# ⚾ MLB Betting Dashboard

This is a Streamlit-based dashboard that helps generate daily MLB betting leans based on pitcher performance and team offense. It includes support for both full-game bets and F5 (First 5 innings) leans.

## 🔗 Live App

📲 [Click here to open the dashboard](https://your-streamlit-url.streamlit.app)  
> Replace this link with your Streamlit Cloud app URL once deployed.

---

## 🧠 Features

- Daily-updated dashboard using MLB API  
- Full Game and F5 ML toggles  
- ERA & WHIP from last 3 starts  
- OPS and RPG from last 7 games  
- Lean logic for ML, RL, and F5 bets  
- "Lean Reason" column shows stat differences  
- Weather & betting tip checklist included  

---

## 📁 Project Structure

```
mlb-betting-dashboard/
├── dashboard.py                      # Main Streamlit app
├── requirements.txt                  # Python packages for deployment
├── data/
│   └── mlb_dashboard_YYYY-MM-DD.csv  # Auto-generated daily CSV
└── README.md
```

---

## 🚀 How to Run Locally

1. Clone the repo:

```
git clone https://github.com/YOUR_USERNAME/mlb-betting-dashboard.git
cd mlb-betting-dashboard
```

2. Install requirements:

```
pip install -r requirements.txt
```

3. Run the dashboard:

```
streamlit run dashboard.py
```

---

## 🔁 Daily CSV Updates

The dashboard reads from:

```
/data/mlb_dashboard_YYYY-MM-DD.csv
```

To update:
- Run your Jupyter notebook each morning to generate the CSV  
- Replace the file in the `/data` folder  
- Push the update to GitHub:

```
git add data/
git commit -m "Update dashboard for 2025-05-08"
git push
```

---

## 🙋‍♀️ Made By

**Bailee Roby**  
A data-driven sports fanatic who never misses a Mariners game and lives for women’s basketball.  
Built this tool to help **bet smarter, not more.**

---

## 📬 Contact / Suggestions

Open an issue or email: your@email.com
