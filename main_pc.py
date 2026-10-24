"""
main.py
-------
Stage 1: Console interface for the DoorDash profit calculator.
Run with:  python main_pc.py

Imports calc_dds() from profit_calculator.py — both files must be
in the same folder.
"""

from profit_calculator import calc_dds

print("DOORDASH PROFIT CALCULATOR")

# --- Inputs ---
mpg               = float(input("MPG: "))
tank_cost         = float(input("Cost to fill tank ($): "))
tank_gallons      = float(input("Tank size (gallons): "))
miles_per_hour    = float(input("Miles driven per hour: "))
delivery_time_min = float(input("Avg delivery time (min): "))
waiting_time      = float(input("Avg wait between orders (min): "))
gross_per_hour    = float(input("Gross earned per hour ($): "))
target            = float(input("2-week target ($): "))

# --- Calculate ---
r = calc_dds(
    gross_per_hour    = gross_per_hour,
    miles_per_hour    = miles_per_hour,
    mpg               = mpg,
    tank_cost         = tank_cost,
    waiting_time      = waiting_time,
    tank_gallons      = tank_gallons,
    delivery_time_min = delivery_time_min,
    se_tax            = True,
)

# --- Results ---
print("\n--- RESULTS ---")
print(f"Net per hour:     ${r['net_hr']}")
print(f"Orders per hour:  {r['orders_hr']}")
print(f"Gas cost/hr:      ${r['gas_cost_hr']}")
print(f"Depreciation/hr:  ${r['depreciation_hr']}")

# --- Goal ---
hours_needed  = target / r["net_hr"]
hours_per_day = hours_needed / 14
miles_needed  = hours_needed * miles_per_hour * 1.20

print("\n--- 2-WEEK GOAL ---")
print(f"Hours needed:     {round(hours_needed, 1)}")
print(f"Hours per day:    {round(hours_per_day, 1)}")
print(f"Miles driven:     {round(miles_needed, 0)}")