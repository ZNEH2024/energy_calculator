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

def calculate_energy_cost(construction_type, square_footage, primary_energy_source):
    construction_types = {
        "Traditional": 1.0,
        "Energy Star": 0.9,
        "EnerPHit": 0.75,
        "Passive House": 0.5
    }
    base_energy_consumption = 12000 * (square_footage / 2000)  # Base annual kWh for traditional construction
    energy_consumption = base_energy_consumption * construction_types.get(construction_type, 1.0)
    
    if primary_energy_source == "Solar PV":
        solar_energy_generation = 3000 * (square_footage / 2000)  # Placeholder for solar PV generation
        energy_consumption -= solar_energy_generation
    
    return max(energy_consumption, 0) * COST_PER_KWH_BUY

def calculate_system_cost(square_footage, primary_energy_source, reserve_capacity):
    solar_pv_cost = square_footage * AVERAGE_COST_PER_WATT_PV if primary_energy_source == "Solar PV" else 0
    solar_thermal_cost = tes_cost = chilled_beam_cost = 0
    
    if primary_energy_source == "Solar Thermal":
        solar_thermal_cost = square_footage * SOLAR_THERMAL_COST_PER_SQFT
        tes_cost = reserve_capacity * TES_COST_PER_KWH
        chilled_beam_cost = square_footage * CHILLED_BEAM_COVERAGE_FACTOR * CHILLED_BEAM_COST_PER_SQFT
    
    hvac_cost = square_footage * CONDITIONED_AREA_PERCENTAGE * TYPICAL_HVAC_COST_PER_SQFT if primary_energy_source == "Electric Grid" else 0

    return solar_pv_cost, solar_thermal_cost, tes_cost, chilled_beam_cost, hvac_cost

def calculate_savings(traditional_cost, renewable_cost):
    return traditional_cost - renewable_cost

def main():
    st.title("Zero Net Energy Home Calculator")

    construction_type = st.selectbox("Select the construction type:", ("Traditional", "Energy Star", "EnerPHit", "Passive House"))
    square_footage = st.slider("Home Square Footage", 1000, 3500, step=100)
    primary_energy_source = st.radio("Select Primary Energy Source", ["Solar PV", "Solar Thermal", "Electric Grid"])
    reserve_capacity = st.slider("Days of Reserve Capacity", 0, 7, step=1) if primary_energy_source == "Solar Thermal" else 0

    if st.button("Calculate Energy Needs and Costs"):
        traditional_grid_cost = calculate_energy_cost("Traditional", square_footage, "Electric Grid")
        renewable_energy_cost = calculate_energy_cost(construction_type, square_footage, primary_energy_source)
        
        savings = calculate_savings(traditional_grid_cost, renewable_energy_cost)
        st.write(f"Traditional grid energy cost: ${traditional_grid_cost:.2f}")
        st.write(f"{primary_energy_source} energy cost: ${renewable_energy_cost:.2f}")
        st.write(f"Savings with {primary_energy_source}: ${savings:.2f}")

        solar_pv_cost, solar_thermal_cost, tes_cost, chilled_beam_cost, hvac_cost = calculate_system_cost(square_footage, primary_energy_source, reserve_capacity)
        net_cost = (solar_pv_cost + tes_cost + chilled_beam_cost) if primary_energy_source != "Electric Grid" else hvac_cost
        
        st.write(f"Total system cost for {primary_energy_source}: ${net_cost:.2f}")
        
        if primary_energy_source in ["Solar PV", "Solar Thermal"]:
            payback_period = calculate_payback_period(net_cost, traditional_grid_cost, renewable_energy_cost)
            st.write(f"Payback period for {primary_energy_source}: {payback_period} years")

if __name__ == "__main__":
    main()
