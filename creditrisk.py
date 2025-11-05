# creditrisk.py
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# --- 1. Fuzzy variables ---
income = ctrl.Antecedent(np.arange(0, 10001, 1), 'income')       # AZN
debt_ratio = ctrl.Antecedent(np.arange(0, 101, 1), 'debt_ratio') # percent
risk = ctrl.Consequent(np.arange(0, 1.01, 0.01), 'risk')         # 0..1

# --- 2. Membership functions ---
income['low']    = fuzz.trapmf(income.universe, [0, 0, 800, 2000])
income['medium'] = fuzz.trimf(income.universe, [1500, 3500, 5500])
income['high']   = fuzz.trapmf(income.universe, [4000, 7000, 10000, 10000])

debt_ratio['low']    = fuzz.trapmf(debt_ratio.universe, [0, 0, 10, 30])
debt_ratio['medium'] = fuzz.trimf(debt_ratio.universe, [20, 40, 60])
debt_ratio['high']   = fuzz.trapmf(debt_ratio.universe, [50, 70, 100, 100])

risk['low']    = fuzz.trapmf(risk.universe, [0, 0, 0.2, 0.4])
risk['medium'] = fuzz.trimf(risk.universe, [0.3, 0.5, 0.7])
risk['high']   = fuzz.trapmf(risk.universe, [0.6, 0.8, 1, 1])

# --- 3. Rule base ---
r1 = ctrl.Rule(income['high']   & debt_ratio['low'],    risk['low'])
r2 = ctrl.Rule(income['low']    & debt_ratio['high'],   risk['high'])
r3 = ctrl.Rule(income['medium'] & debt_ratio['medium'], risk['medium'])
r4 = ctrl.Rule(debt_ratio['low'] & income['medium'],    risk['low'])
r5 = ctrl.Rule(debt_ratio['medium'] & income['low'],    risk['high'])
r6 = ctrl.Rule(income['high'] & debt_ratio['medium'],   risk['medium'])
r7 = ctrl.Rule(debt_ratio['high'] , risk['high'])  # if debt high -> high risk

# --- 4. Control system ---
risk_ctrl = ctrl.ControlSystem([r1, r2, r3, r4, r5, r6, r7])
risk_sim = ctrl.ControlSystemSimulation(risk_ctrl)


# --- 5. Calculation function ---
def calculate_risk(income_val, monthly_debt, experience_months):
    """
    Calculate fuzzy loan risk.
    Returns decision and risk value.
    """

    if experience_months < 6:
        return "❌ Rejected (less than 6 months of work experience)"

    if income_val <= 0:
        debt_ratio_val = 100.0
    else:
        debt_ratio_val = (monthly_debt / income_val) * 100.0
    debt_ratio_val = max(0.0, min(100.0, debt_ratio_val))

    risk_sim.input['income'] = income_val
    risk_sim.input['debt_ratio'] = debt_ratio_val
    risk_sim.compute()
    risk_value = round(float(risk_sim.output['risk']), 3)

    if risk_value <= 0.3:
        return f"✅ Approved (LOW risk: {risk_value})"
    elif risk_value <= 0.6:
        return f"⚠️ Guarantor required (MEDIUM risk: {risk_value})"
    else:
        return f"❌ Rejected (HIGH risk: {risk_value})"
