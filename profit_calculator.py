# constants but this is optional

TAX_RATE = .153

# defining function, arg=True makes it optional

def calc_dds(gross_per_hour, miles_per_hour, mpg, tank_cost, waiting_time, tank_gallons,
              delivery_time_min, se_tax=True):
    
    cost_per_gal = tank_cost/tank_gallons
    cost_per_mile = cost_per_gal/mpg

    total_miles_hr = miles_per_hour * 1.20
    gas_cost_hr = cost_per_mile * total_miles_hr

    depreciation_hr = 0.15 * total_miles_hr # according to google depreciation my mile is 0.15

    orders_hr = 60/(delivery_time_min+waiting_time)

    pre_tax_net_hr = gross_per_hour - gas_cost_hr - depreciation_hr

    if se_tax:
        net_hr = pre_tax_net_hr * (1-TAX_RATE) # this is the self-employed tax rate 
    else:
        net_hr = pre_tax_net_hr
    return { "net_hr": round(net_hr, 2), "cost_per_mile": round(cost_per_mile, 2), 
            "orders_hr": round(orders_hr, 2), "gas_cost_hr": round(gas_cost_hr, 2), 
             "depreciation_hr": round(depreciation_hr,2), }
