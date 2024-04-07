# energy_calculator.py

# Patent Pending, Copyright, All Rights Reserved, Service Mark (SM), 2022-2024
# John M. Willis, Turnaround Security, Inc., Zero Net Energy Homes

import streamlit as st

# Constants for cost calculations and system efficiency
COST_PER_KWH_BUY = 0.12  # Cost of buying electricity from the grid per kWh
AVERAGE_COST_PER_WATT_PV = 3.25  # Average cost per watt for PV panels
SOLAR_THERMAL_COST_PER_SQFT = 2  # Cost per square foot for solar thermal collectors
TES_COST_PER_KWH = 0.15  # Cost per kWh for thermal energy storage capacity
CHILLED_BEAM_COST_PER_SQFT = 22.5  # Cost per square foot for chilled beams
CHILLED_BEAM_COVERAGE_FACTOR = 0.75  # Coverage factor for chilled beams
TYPICAL_HVAC_COST_PER_SQFT = 10  # Typical HVAC cost per square foot of conditioned area
CONDITIONED_AREA_PERCENTAGE = 0.75  # Percentage of the house that is conditioned
TRADITIONAL_ANNUAL_KWH = 40000  # Estimated annual kWh for traditional construction

def calculate_energy_cost(construction_type, square_footage, primary_energy_source):
    construction_types = {
        "Traditional": 1.0,
        "Energy Star": 0.9,
        "EnerPHit": 0.75,
        "Passive House": 0.5
    }
    base_energy_consumption = TRADITIONAL_ANNUAL_KWH * (square_footage / 1422)
    
    if primary_energy_source == "Solar Thermal":
        # Assume some efficiency and coverage for solar thermal to electricity conversion
        energy_consumption = base_energy_consumption * (1 - construction_types[construction_type])
    elif primary_energy_source == "Solar PV":
        # Assuming Solar PV covers a certain percentage of the energy needs
        solar_pv_coverage = 0.30
        energy_consumption = base_energy_consumption * (1 - solar_pv_coverage)
    else:
        energy_consumption = base_energy_consumption * construction_types[construction_type]
    
    return energy_consumption, energy_consumption * COST_PER_KWH_BUY

def calculate_system_cost(square_footage, primary_energy_source, reserve_capacity):
    solar_pv_cost = square_footage * AVERAGE_COST_PER_WATT_PV if primary_energy_source == "Solar PV" else 0
    solar_thermal_cost = tes_cost = chilled_beam_cost = 0
    
    if primary_energy_source == "Solar Thermal":
        solar_thermal_cost = square_footage * SOLAR_THERMAL_COST_PER_SQFT
        tes_cost = reserve_capacity * TES_COST_PER_KWH
        chilled_beam_cost = square_footage * CHILLED_BEAM_COVERAGE_FACTOR * CHILLED_BEAM_COST_PER_SQFT
    
    traditional_hvac_cost = square_footage * CONDITIONED_AREA_PERCENTAGE * TYPICAL_HVAC_COST_PER_SQFT

    return solar_pv_cost, solar_thermal_cost, tes_cost, chilled_beam_cost, traditional_hvac_cost

def calculate_payback_period(net_system_cost, traditional_grid_cost, annual_energy_savings):
    if annual_energy_savings <= 0:
        return "Infinite (no savings)"
    
    payback_period = net_system_cost / annual_energy_savings
    return f"{payback_period:.2f} years"

def main():
    st.title("Zero Net Energy Home Calculator")

    construction_type = st.selectbox("Select the construction type:", ("Traditional", "Energy Star", "EnerPHit", "Passive House"))
    square_footage = st.slider("Home Square Footage", 1000, 3500, step=100)
    primary_energy_source = st.radio("Select Primary Energy Source", ["Solar PV", "Solar Thermal", "Electric Grid"])
    reserve_capacity = st.slider("Days of Reserve Capacity", 0, 7, step=1) if primary_energy_source == "Solar Thermal" else 0

    traditional_energy_kWh, traditional_grid_cost = calculate_energy_cost("Traditional", square_footage, "Electric Grid")
    renewable_energy_kWh, renewable_energy_cost = calculate_energy_cost(construction_type, square_footage, primary_energy_source)
    
    st.write(f"Traditional grid energy cost: ${traditional_grid_cost:.2f}")

    solar_pv_cost, solar_thermal_cost, tes_cost, chilled_beam_cost, traditional_hvac_cost = calculate_system_cost(square_footage, primary_energy_source, reserve_capacity)
    net_system_cost = 0
    annual_energy_savings = traditional_grid_cost - renewable_energy_cost

    if primary_energy_source == "Solar PV":
        net_system_cost = solar_pv_cost - traditional_hvac_cost
        st.write(f"Solar PV System Cost: ${solar_pv_cost:.2f}")
        st.write(f"Net System Cost (after HVAC offset): ${net_system_cost:.2f}")
        st.write(f"Savings with Solar PV: ${annual_energy_savings:.2f}")
        
    elif primary_energy_source == "Solar Thermal":
        total_solar_thermal_cost = solar_thermal_cost + tes_cost + chilled_beam_cost
        net_system_cost = total_solar_thermal_cost - traditional_hvac_cost
        st.write(f"Solar Thermal System Cost: ${total_solar_thermal_cost:.2f}")
        st.write(f"Net System Cost (after HVAC offset): ${net_system_cost:.2f}")
        st.write(f"Savings with Solar Thermal: ${annual_energy_savings:.2f}")
        
    payback_period = calculate_payback_period(net_system_cost, traditional_grid_cost, annual_energy_savings)
    st.write(f"Payback period: {payback_period} years")

    if primary_energy_source == "Electric Grid":
        st.write(f"Traditional HVAC Cost: ${traditional_hvac_cost:.2f}")

if __name__ == "__main__":
    main()
