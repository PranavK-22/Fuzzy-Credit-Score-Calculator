import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import messagebox

# Define fuzzy variables
income = ctrl.Antecedent(np.arange(0, 16, 1), 'income')  # in lakhs
loan_amount = ctrl.Antecedent(np.arange(0, 31, 1), 'loan_amount')  # in lakhs
dti = ctrl.Antecedent(np.arange(0, 101, 1), 'dti')  # percentage
credit_history = ctrl.Antecedent(np.arange(0, 16, 1), 'credit_history')  # in years
credit_score = ctrl.Consequent(np.arange(0, 901, 1), 'credit_score')

# Income MFs
income['low'] = fuzz.trimf(income.universe, [0, 0, 3])
income['medium'] = fuzz.trimf(income.universe, [2, 5, 8])
income['high'] = fuzz.trimf(income.universe, [6, 10, 15])

# Loan Amount MFs
loan_amount['small'] = fuzz.trimf(loan_amount.universe, [0, 0, 5])
loan_amount['moderate'] = fuzz.trimf(loan_amount.universe, [4, 8, 12])
loan_amount['large'] = fuzz.trimf(loan_amount.universe, [10, 20, 30])

# DTI MFs
dti['low'] = fuzz.trimf(dti.universe, [0, 0, 20])
dti['moderate'] = fuzz.trimf(dti.universe, [15, 30, 45])
dti['high'] = fuzz.trimf(dti.universe, [40, 60, 80])

# Credit History MFs
credit_history['short'] = fuzz.trimf(credit_history.universe, [0, 0, 2])
credit_history['medium'] = fuzz.trimf(credit_history.universe, [1.5, 4, 6.5])
credit_history['long'] = fuzz.trimf(credit_history.universe, [5, 10, 15])

# Credit Score MFs
credit_score['poor'] = fuzz.trimf(credit_score.universe, [0, 0, 400])
credit_score['fair'] = fuzz.trimf(credit_score.universe, [300, 500, 650])
credit_score['good'] = fuzz.trimf(credit_score.universe, [600, 750, 850])
credit_score['excellent'] = fuzz.trimf(credit_score.universe, [800, 900, 900])

# Define rules
rules = [
    ctrl.Rule(income['high'] & dti['low'] & credit_history['long'], credit_score['excellent']),
    ctrl.Rule(income['medium'] & dti['moderate'] & credit_history['medium'], credit_score['good']),
    ctrl.Rule(income['low'] & loan_amount['large'] & dti['high'], credit_score['poor']),
    ctrl.Rule(income['low'] & dti['moderate'], credit_score['fair']),
    ctrl.Rule(income['high'] & loan_amount['small'] & credit_history['medium'], credit_score['excellent']),
    ctrl.Rule(dti['high'] & credit_history['short'], credit_score['poor']),
    ctrl.Rule(loan_amount['moderate'] & dti['moderate'], credit_score['fair']),
    ctrl.Rule(income['medium'] & credit_history['long'], credit_score['good']),
    ctrl.Rule(loan_amount['small'] & dti['low'], credit_score['good']),
    ctrl.Rule(income['low'] & credit_history['short'], credit_score['poor']),
    ctrl.Rule(credit_history['medium'] & dti['moderate'], credit_score['fair']),
    ctrl.Rule(income['high'] & loan_amount['large'], credit_score['fair']),
]

# Build control system
credit_ctrl = ctrl.ControlSystem(rules)
credit_sim = ctrl.ControlSystemSimulation(credit_ctrl)

# GUI
root = tk.Tk()
root.title("Fuzzy Credit Score Calculator")

fields = {}

def calculate_score():
    try:
        credit_sim.input['income'] = float(fields['Income'].get())
        credit_sim.input['loan_amount'] = float(fields['Loan Amount'].get())
        credit_sim.input['dti'] = float(fields['DTI'].get())
        credit_sim.input['credit_history'] = float(fields['Credit History'].get())

        credit_sim.compute()
        result = round(credit_sim.output['credit_score'], 2)
        messagebox.showinfo("Credit Score", f"Estimated Credit Score: {result}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

inputs = ['Income', 'Loan Amount', 'DTI', 'Credit History']
for i, label in enumerate(inputs):
    tk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=5, sticky='e')
    entry = tk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    fields[label] = entry

tk.Button(root, text="Calculate Credit Score", command=calculate_score).grid(row=len(inputs), columnspan=2, pady=10)

root.mainloop()