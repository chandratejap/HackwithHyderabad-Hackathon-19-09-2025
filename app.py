import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.calculations import load_finances, simulate_scenario, pretty_summary

st.set_page_config(page_title="CFO Helper (MVP)", layout="wide")
st.title("CFO Helper — MVP")
st.markdown("Simulate simple budget scenarios: hiring, marketing changes and price changes — see runway & profit impact.\n\n**Quick demo:** adjust inputs and click **Run simulation**.")

# Load finances
finances = load_finances("data/finances.csv")

# Sidebar for inputs
with st.sidebar:
    st.header("Inputs")
    hires_add = st.number_input("Add hires (employees)", min_value=0, max_value=20, value=0, step=1)
    marketing_change = st.number_input("Change in monthly marketing (₹)", min_value=-200000, max_value=200000, value=0, step=1000)
    price_change_pct = st.slider("Price change (%)", -50, 100, 0, 1)
    st.markdown("---")
    st.write("Use this button to simulate a mock live data update (Pathway demo).")
    simulate_update = st.button("Simulate live data update (mock)")

# Main layout: baseline and results
st.header("Baseline financials")
col1, col2, col3 = st.columns(3)
col1.metric("Cash (₹)", f"{int(finances['cash']):,}")
col2.metric("Monthly burn (₹)", f"{int(finances['monthly_burn']):,}")
runway_text = f"{finances['runway']:.1f}" if finances['runway'] != float('inf') else "∞"
col3.metric("Runway (months)", runway_text)

st.markdown("**Details**")
c1, c2 = st.columns(2)
c1.write(f"Revenue: ₹{int(finances['revenue']):,}")
c2.write(f"Expenses: ₹{int(finances['expenses']):,}")
st.write(f"Current hires: {int(finances.get('current_hires',0))} — avg cost per hire ₹{int(finances.get('avg_cost_per_hire',0)):,}")

# session counter
if 'counter' not in st.session_state:
    st.session_state['counter'] = 0

# Run simulation button in main area
if st.button("Run simulation"):
    result = simulate_scenario(finances, add_hires=hires_add, delta_marketing=marketing_change, price_change_pct=price_change_pct)
    st.session_state['counter'] += 1

    st.subheader("Simulation Result")
    st.markdown(pretty_summary(result))

    # Chart: before vs after runway
    df_chart = pd.DataFrame({
        'Before': [finances['runway'] if finances['runway'] != float('inf') else 0],
        'After': [result['new_runway'] if result['new_runway'] != float('inf') else 0]
    }, index=['Runway (months)'])

    fig, ax = plt.subplots()
    df_chart.plot.bar(ax=ax)
    ax.set_ylabel("Months")
    ax.set_xticklabels(['Runway'])
    st.pyplot(fig)

    st.success(f"Scenarios tested: {st.session_state['counter']}")
    # prepare a tiny report CSV
    report = {
        'metric': ['runway_before','runway_after','revenue_before','revenue_after','expenses_before','expenses_after'],
        'value': [finances['runway'], result['new_runway'], finances['revenue'], result['new_revenue'], finances['expenses'], result['new_expenses']]
    }
    report_df = pd.DataFrame(report)
    csv = report_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download short report (CSV)", data=csv, file_name="cfo_helper_report.csv", mime="text/csv")

# Simulate live data update (mock Pathway)
if simulate_update:
    # This action will reload the finances from CSV (which you can edit) and show a small message.
    finances2 = load_finances("data/finances.csv")
    st.info("Mock update loaded from data/finances.csv — re-running baseline calculations.")
    st.write("If you want to demo 'live updates', edit data/finances.csv in the repo (or replace it) and then click this button again.")
    st.write(f"New baseline revenue: ₹{int(finances2['revenue']):,}")
    st.write(f"New baseline runway: {finances2['runway']:.1f} months")

st.markdown("---")
st.caption("MVP: assumptions are simplified. See README.md for details and how to tweak parameters.")