# CFO Helper — MVP (Hackathon)

Quick MVP to simulate simple financial "what-if" scenarios: hiring, marketing changes, and price changes.
This Streamlit app demonstrates how small decisions affect runway and monthly profit.

## Project structure
```
cfo-helper/
├── app.py
├── data/finances.csv
├── utils/calculations.py
├── requirements.txt
└── README.md
```

## Quick start (Linux/macOS)
1. Clone this folder or copy files locally.
2. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```
4. Demo tips:
   - Use the sidebar to change hires/marketing/price and click **Run simulation**.
   - Click **Simulate live data update (mock)** to demo Pathway-like behavior (edit `data/finances.csv` to simulate a live update).

## Notes & assumptions (MVP)
- Revenue model: price changes scale revenue proportionally (units sold kept constant). This is a simplification for demo.
- Expenses update immediately when hires or marketing change.
- Runway computed as `cash / net_monthly_burn` (if net burn &gt; 0). If net burn ≤ 0, runway is shown as infinite.
- To extend:
  - Add realistic demand elasticity, dynamic units sold, persistence (SQLite), PDF export, and Flexprice billing.

## Files to edit for demo
- `data/finances.csv` — change numbers here to simulate updated data pulled by Pathway.