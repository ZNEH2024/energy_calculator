# energy_calculator.py

# Patent Pending, Copyright, All Rights Reserved, Service Mark (SM), 2022-2024
# John M. Willis, Turnaround Security, Inc., Zero Net Energy Homes

import streamlit as st

import streamlit as st

# Constants for cost calculations and system efficiency
COST_PER_KWH_BUY = 0.12  # Cost of buying electricity from the grid per kWh
AVERAGE_COST_PER_WATT_PV = 3  # Average cost per watt for PV installation
AVERAGE_SYSTEM_SIZE_KW = 6  # Average size of a residential solar PV system in kW
SOLAR_THERMAL_COST_PER_SQFT = 2  # Cost per square foot for solar thermal collectors
TES_EQUIPMENT_COST = 4000  # Fixed equipment cost for Thermal Energy Storage (TES)
SOLAR_THERMAL_CONTROL_SYSTEM_COST = 3000  # Cost for the Solar Thermal control system equipment
CHILLED_BEAM_COST_PER_SQFT = 22.5  # Cost per square foot for chilled beams
TYPICAL_HVAC_COST_PER_SQFT = 10  # Typical HVAC cost per square foot of conditioned area
TRADITIONAL_ANNUAL_KWH = 40000  # Estimated annual kWh for traditional construction

def calculate_energy_cost(construction_type):
    construction_types = {
        "Traditional": 1.0,
        "Energy Star": 0.9,
        "EnerPHit": 0.75,
        "Passive House": 0.5
    }
    base_energy_consumption = TRADITIONAL_ANNUAL_KWH * construction_types[construction_type]
    energy_cost = base_energy_consumption * COST_PER_KWH_BUY
    return base_energy_consumption, energy_cost

def calculate_pv_system_cost():
    return AVERAGE_SYSTEM_SIZE_KW * 1000 * AVERAGE_COST_PER_WATT_PV

def calculate_solar_pv_savings():
    annual_pv_production_kwh = AVERAGE_SYSTEM_SIZE_KW * 1400  # Assuming 1400 kWh per kW per year
    annual_savings = annual_pv_production_kwh * COST_PER_KWH_BUY
    lifetime_savings = annual_savings * 25  # Assuming a 25-year lifespan for the solar PV system
    return annual_savings, lifetime_savings

def calculate_solar_thermal_cost(square_footage):
    solar_thermal_cost = square_footage * SOLAR_THERMAL_COST_PER_SQFT + SOLAR_THERMAL_CONTROL_SYSTEM_COST
    tes_cost = TES_EQUIPMENT_COST
    total_cost = solar_thermal_cost + tes_cost
    return total_cost, solar_thermal_cost, tes_cost

def calculate_payback_period(initial_cost, annual_savings):
    if annual_savings > 0:
        return initial_cost / annual_savings
    return "Infinite"

def main():
    st.title("Zero Net Energy Home Calculator")

    construction_type = st.selectbox("Select the construction type:", ["Traditional", "Energy Star", "EnerPHit", "Passive House"])
    square_footage = st.slider("Home Square Footage", 1000, 3500, 2000, step=100)
    primary_energy_source = st.radio("Select Primary Energy Source", ["Solar PV", "Solar Thermal", "Electric Grid"])

    base_energy_consumption, traditional_grid_cost = calculate_energy_cost(construction_type)
    
    st.header(f"Energy Cost Analysis for {square_footage} SF Home")
    st.write(f"Construction type: {construction_type}")
    st.subheader("Traditional Energy Costs")
    st.write(f"Base energy consumption: {base_energy_consumption:,.2f} kWh/year")
    st.write(f"Traditional grid energy cost: ${traditional_grid_cost:,.2f}/year")

    if primary_energy_source == "Solar PV":
        pv_system_cost = calculate_pv_system_cost()
        annual_savings, lifetime_savings = calculate_solar_pv_savings()

        st.subheader("Solar PV Analysis")
        st.write(f"Solar PV System Cost: ${pv_system_cost:,.2f}")
        st.write(f"Annual Savings with Solar PV: ${annual_savings:,.2f}")
        st.write(f"Lifetime Savings with Solar PV: ${lifetime_savings:,.2f}")
        payback_period = calculate_payback_period(pv_system_cost, annual_savings)
        st.write(f"Payback period for Solar PV: {payback_period:.2f} years")

    elif primary_energy_source == "Solar Thermal":
        solar_thermal_cost, solar_thermal_component, tes_component = calculate_solar_thermal_cost(square_footage)

        st.subheader("Solar Thermal Analysis")
        st.write(f"Solar Thermal System Cost: ${solar_thermal_cost:,.2f}")
        st.write(f"Solar Thermal Component Cost: ${solar_thermal_component:,.2f}")
        st.write(f"TES Component Cost: ${tes_component:,.2f}")

        # Assuming solar thermal covers all energy needs
        annual_energy_savings = traditional_grid_cost
        payback_period = calculate_payback_period(solar_thermal_cost, annual_energy_savings)
        st.write(f"Payback period for Solar Thermal: {payback_period:.2f} years")

if __name__ == "__main__":
    main()
