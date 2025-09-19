import pandas as pd

def load_finances(path="data/finances.csv"):
    """Read finances from a simple key,value CSV and return a dict with computed runway."""
    df = pd.read_csv(path)
    finances = {}
    for _, row in df.iterrows():
        key = str(row['key']).strip()
        value = row['value']
        try:
            finances[key] = float(value)
        except:
            # if not numeric, store raw
            try:
                finances[key] = float(value.replace(',',''))
            except:
                finances[key] = value
    # ensure keys exist with defaults
    defaults = {
        'cash': 0.0,
        'monthly_burn': 0.0,
        'revenue': 0.0,
        'expenses': 0.0,
        'monthly_marketing': 0.0,
        'current_hires': 0.0,
        'avg_cost_per_hire': 0.0,
        'baseline_price': 0.0,
        'units_sold': 0.0
    }
    for k,v in defaults.items():
        finances.setdefault(k, v)
    finances['current_hires'] = int(finances.get('current_hires',0))
    finances['units_sold'] = int(finances.get('units_sold',0))
    finances['runway'] = compute_runway(finances['cash'], finances['monthly_burn'])
    return finances

def compute_runway(cash, monthly_burn):
    if monthly_burn <= 0:
        return float('inf')
    return cash / monthly_burn

def simulate_scenario(finances, add_hires=0, delta_marketing=0, price_change_pct=0):
    """Return a result dict containing before/after numbers and textable summary."""
    cash = finances['cash']
    monthly_burn = finances['monthly_burn']
    revenue = finances['revenue']
    expenses = finances['expenses']
    monthly_marketing = finances['monthly_marketing']
    current_hires = finances['current_hires']
    avg_cost_per_hire = finances['avg_cost_per_hire']
    baseline_price = finances['baseline_price']
    units_sold = finances['units_sold']

    add_hires = int(add_hires)
    hire_cost_change = add_hires * avg_cost_per_hire

    new_hires = current_hires + add_hires
    new_monthly_marketing = monthly_marketing + delta_marketing

    # update expenses (we assume added hires and marketing increase expenses immediately)
    new_expenses = expenses + hire_cost_change + delta_marketing

    # naive revenue model: price change scales revenue proportionally (units_sold kept constant in MVP)
    new_price = baseline_price * (1 + price_change_pct/100.0)
    new_revenue = new_price * units_sold

    # monthly net burn = expenses - revenue
    new_monthly_burn = new_expenses - new_revenue

    new_runway = compute_runway(cash, new_monthly_burn) if new_monthly_burn > 0 else float('inf')
    new_profit = new_revenue - new_expenses

    result = {
        'new_hires': new_hires,
        'hire_cost_change': hire_cost_change,
        'new_monthly_marketing': new_monthly_marketing,
        'new_expenses': new_expenses,
        'new_price': new_price,
        'new_revenue': new_revenue,
        'new_monthly_burn': new_monthly_burn,
        'new_runway': new_runway,
        'new_profit': new_profit,
        'baseline': {
            'cash': cash,
            'monthly_burn': monthly_burn,
            'revenue': revenue,
            'expenses': expenses,
            'runway': finances.get('runway', None)
        }
    }
    return result

def pretty_summary(result):
    baseline = result['baseline']
    old_runway = baseline.get('runway', None)
    new_runway = result['new_runway']
    lines = []
    lines.append(f"**Hires** → {int(result['new_hires'])} (added cost ₹{int(result['hire_cost_change']):,})")
    lines.append(f"**Marketing (monthly)** → ₹{int(result['new_monthly_marketing']):,}")
    lines.append(f"**Expenses (monthly)** → ₹{int(result['new_expenses']):,}")
    lines.append(f"**Revenue (monthly)** → ₹{int(result['new_revenue']):,}")
    if new_runway == float('inf'):
        lines.append("**Runway** → Non-positive net burn (profitable) — infinite runway.")
    else:
        if old_runway is not None:
            lines.append(f"**Runway** → {old_runway:.1f} months → {new_runway:.1f} months")
        else:
            lines.append(f"**Runway** → {new_runway:.1f} months")
    lines.append(f"**Monthly profit** → ₹{int(result['new_profit']):,}")
    return "\n\n".join(lines)