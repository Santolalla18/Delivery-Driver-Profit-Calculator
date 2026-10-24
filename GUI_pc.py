"""
gui.py
------
stage 2: Tkinter GUI for the DoorDash profit calculator.
Run with:  python gui.py in terminal or command line

imports calc_dds() from profit_calculator.py — both files must be
in the same folder.
"""

import tkinter as tk
from tkinter import messagebox
from profit_calculator import calc_dds


# ---------------------------------------------------------------------------
# Helper — build one label + entry row in the grid
# ---------------------------------------------------------------------------

def make_field(parent, label_text, default_value, row_num):
    """
    creates one row:  Label | Entry box
    returns the StringVar so we can read the value later.
    """
    tk.Label(parent, text=label_text, anchor="w").grid(
        row=row_num, column=0, sticky="w", padx=10, pady=4
    )

    var = tk.StringVar(value=str(default_value))  # pre-fill with default

    tk.Entry(parent, textvariable=var, width=12).grid(
        row=row_num, column=1, padx=10, pady=4
    )

    return var  # we hold onto this to call var.get() later


# ---------------------------------------------------------------------------
# The calculate button's job
# ---------------------------------------------------------------------------

def on_calculate():
    """
    Called when the user clicks Calculate.
    Reads all input boxes, calls calc_dds(), updates the result labels.
    """
    # --- Read inputs (all come in as strings, so we convert) ---
    try:
        mpg               = float(var_mpg.get())
        tank_cost         = float(var_tank_cost.get())
        tank_gallons      = float(var_tank_gallons.get())
        miles_per_hour    = float(var_miles.get())
        delivery_time_min = float(var_delivery.get())
        waiting_time      = float(var_wait.get())
        gross_per_hour    = float(var_gross.get())
        target            = float(var_target.get())
    except ValueError:
        # If any box has a non-number, show a popup and stop
        messagebox.showerror("Wrong value bro", "All fields must be numbers.")
        return

    # --- Call YOUR function ---
    r = calc_dds(
        gross_per_hour    = gross_per_hour,
        miles_per_hour    = miles_per_hour,
        mpg               = mpg,
        tank_cost         = tank_cost,
        waiting_time      = waiting_time,
        tank_gallons      = tank_gallons,
        delivery_time_min = delivery_time_min,
        se_tax            = se_tax_var.get(),   # reads the checkbox
    )

    net_hr = r["net_hr"]

    # --- Goal math ---
    if net_hr <= 0:
        messagebox.showwarning("Costs exceed earnings","Check your inputs")
        return

    hours_needed  = target / net_hr
    hours_per_day = hours_needed / 14
    miles_needed  = hours_needed * miles_per_hour * 1.20

    # --- Update result labels ---
    lbl_net_hr.config(      text=f"${net_hr:.2f}")
    lbl_orders_hr.config(   text=f"{r['orders_hr']}/hr")
    lbl_gas_cost.config(    text=f"-${r['gas_cost_hr']:.2f}")
    lbl_depreciation.config(text=f"-${r['depreciation_hr']:.2f}")
    lbl_hours.config(       text=f"{hours_needed:.1f} hrs")
    lbl_hpd.config(         text=f"{hours_per_day:.1f} hrs/day")
    lbl_miles.config(       text=f"{miles_needed:.0f} mi")

    # Color net/hr green if positive, red if low
    color = "green" if net_hr >= 10 else "orange" if net_hr >= 6 else "red"
    lbl_net_hr.config(fg=color)


# ---------------------------------------------------------------------------
# Build the window
# ---------------------------------------------------------------------------

window = tk.Tk()
window.title("DoorDash Profit Calculator")
window.resizable(False, False)   # fixed size for now

# ── Section: Inputs ─────────────────────────────────────────────────────────

input_frame = tk.LabelFrame(window, text="Your Numbers", padx=5, pady=5)
input_frame.grid(row=0, column=0, padx=15, pady=10, sticky="ew")

# Each make_field() call returns a StringVar we save in a var_ variable
var_mpg          = make_field(input_frame, "MPG (off-highway)",          22,    row_num=0)
var_tank_cost    = make_field(input_frame, "Cost to fill tank ($)",       50,    row_num=1)
var_tank_gallons = make_field(input_frame, "Tank size (gallons)",         12,    row_num=2)
var_miles        = make_field(input_frame, "Miles driven per hour",       10,    row_num=3)
var_delivery     = make_field(input_frame, "Avg delivery time (min)",     12,    row_num=4)
var_wait         = make_field(input_frame, "Avg wait between orders (min)", 5,   row_num=5)
var_gross        = make_field(input_frame, "Gross earned per hour ($)",   16.67, row_num=6)
var_target       = make_field(input_frame, "2-week target ($)",           600,   row_num=7)

# Checkbox for SE tax
se_tax_var = tk.BooleanVar(value=True)   # checked by default
tk.Checkbutton(
    input_frame,
    text="Deduct self-employment tax (15.3%)",
    variable=se_tax_var
).grid(row=8, column=0, columnspan=2, sticky="w", padx=10, pady=4)

# Calculate button
tk.Button(
    input_frame,
    text="Calculate",
    command=on_calculate,       # this is the callback — runs when clicked
    bg="#22c55e",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=10, pady=4
).grid(row=9, column=0, columnspan=2, pady=10)


# ── Section: Results ─────────────────────────────────────────────────────────

result_frame = tk.LabelFrame(window, text="Results", padx=5, pady=5)
result_frame.grid(row=1, column=0, padx=15, pady=5, sticky="ew")

def result_row(parent, label_text, row_num):
    """Creates one result row: Label | Value label. Returns the value label."""
    tk.Label(parent, text=label_text, anchor="w").grid(
        row=row_num, column=0, sticky="w", padx=10, pady=3
    )
    val_lbl = tk.Label(parent, text="—", anchor="e", width=14)
    val_lbl.grid(row=row_num, column=1, padx=10, pady=3)
    return val_lbl

lbl_net_hr       = result_row(result_frame, "Net per hour",          0)
lbl_orders_hr    = result_row(result_frame, "Orders per hour",         1)
lbl_gas_cost     = result_row(result_frame, "Gas cost per hour",       2)
lbl_depreciation = result_row(result_frame, "Depreciation per hour",   3)
lbl_hours        = result_row(result_frame, "Hours needed (total)",    4)
lbl_hpd          = result_row(result_frame, "Hours per day (14 days)", 5)
lbl_miles        = result_row(result_frame, "Miles you'll drive",      6)


# ── Start the app ────────────────────────────────────────────────────────────

window.mainloop()   # open the window and wait for events