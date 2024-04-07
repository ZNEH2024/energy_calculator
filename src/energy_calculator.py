# energy_calculator.py

# Patent Pending, Copyright, All Rights Reserved, Service Mark (SM), 2022-2024
# John M. Willis, Turnaround Security, Inc., Zero Net Energy Homes

import streamlit as st

# Constants for cost calculations and system efficiency
COST_PER_KWH_BUY = 0.12  # Cost of buying electricity from the grid per kWh
COST_PER_WATT_PV = 3  # Cost per watt for PV installation
SOLAR_THERMAL_COST_PER_SQFT = 2  # Cost per square foot for solar thermal collectors
TES_EQUIPMENT_COST = 4000  # Fixed equipment cost for Thermal Energy Storage (TES)
SOLAR_THERMAL_CONTROL_SYSTEM_COST = 3000  # Cost for the Solar Thermal control system equipment
CHILLED_BEAM_COST_PER_SQFT = 22.5  # Cost per square foot for chilled beams
TYPICAL_HVAC_COST_PER_SQFT = 10  # Typical HVAC cost per square foot of conditioned area
TRADITIONAL_ANNUAL_KWH = 40000  # Estimated annual kWh for traditional construction
STIRLING_GENERATOR_CAPACITY_PER_1000_SF = 5  # Capacity in kW per 1,000 square feet
STIRLING_ENGINE_COST_PER_KW = 500  # Equipment cost per kW for the Stirling Engine
STIRLING_CHILLER_COST_PER_KW = 600  # Equipment cost per kW for the Stirling Chiller

def calculate_energy_cost(construction_type, square_footage):
    construction_types = {
        "Traditional": 1.0,
        "Energy Star": 0.9,
        "EnerPHit": 0.75,
        "Passive House": 0.5
    }
    base_energy_consumption = TRADITIONAL_ANNUAL_KWH * construction_types[construction_type] * (square_footage / 1422)
    energy_cost = base_energy_consumption * COST_PER_KWH_BUY
    
    return base_energy_consumption, energy_cost

def calculate_pv_system_cost():
    # Average system size based on typical roof area for U.S. single-family homes
    average_system_size_kw = 6  # kW
    return average_system_size_kw * 1000 * COST_PER_WATT_PV

def calculate_system_cost(square_footage, primary_energy_source):
    solar_pv_cost = 0
    solar_thermal_cost = tes_cost = chilled_beam_cost = 0
    stirling_engine_cost = stirling_chiller_cost = solar_thermal_control_system_cost = 0

    if primary_energy_source == "Solar PV":
        solar_pv_cost = calculate_pv_system_cost()

    if primary_energy_source == "Solar Thermal":
        stirling_engine_capacity = STIRLING_GENERATOR_CAPACITY_PER_1000_SF * (square_footage / 1000)
        solar_thermal_cost = square_footage * SOLAR_THERMAL_COST_PER_SQFT
        tes_cost = TES_EQUIPMENT_COST
        solar_thermal_control_system_cost = SOLAR_THERMAL_CONTROL_SYSTEM_COST
        chilled_beam_cost = square_footage * CHILLED_BEAM_COST_PER_SQFT
        stirling_engine_cost = stirling_engine_capacity * STIRLING_ENGINE_COST_PER_KW
        stirling_chiller_cost = stirling_engine_capacity * STIRLING_CHILLER_COST_PER_KW

    traditional_hvac_cost = square_footage * TYPICAL_HVAC_COST_PER_SQFT

    return {
        'solar_pv_cost': solar_pv_cost,
        'solar_thermal_cost': solar_thermal_cost,
        'tes_cost': tes_cost,
        'solar_thermal_control_system_cost': solar_thermal_control_system_cost,
        'stirling_engine_cost': stirling_engine_cost,
        'stirling_chiller_cost': stirling_chiller_cost,
        'chilled_beam_cost': chilled_beam_cost,
        'traditional_hvac_cost': traditional_hvac_cost
    }

def calculate_solar_thermal_area(square_footage):
    return square_footage * 0.5

def calculate_payback_period(net_system_cost, annual_energy_savings):
    if annual_energy_savings <= 0:
        return "Infinite (no savings)"
    
    payback_period = net_system_cost / annual_energy_savings
    return f"{payback_period:.2f} years"

def main():
    st.title("Zero Net Energy Home Calculator")

    with st.sidebar:
        construction_type = st.selectbox("Select the construction type:", 
                                         ["Traditional", "Energy Star", "EnerPHit", "Passive House"])
        square_footage = st.slider("Home Square Footage", 1000, 3500, 1422, step=100)
        primary_energy_source = st.radio("Select Primary Energy Source", 
                                         ["Solar PV", "Solar Thermal", "Electric Grid"], index=2)

    if st.button('Calculate'):
        base_energy_consumption, traditional_grid_cost = calculate_energy_cost(construction_type, square_footage)
        costs = calculate_system_cost(square_footage, primary_energy_source)

        st.header(f"Energy Cost Analysis for {square_footage} SF Home")
        st.write(f"Construction type: {construction_type}")
        st.write(f"Square footage: {square_footage}")
        st.subheader("Traditional Energy Costs")
        st.write(f"Base energy consumption: {base_energy_consumption:,.2f} kWh")
        st.write(f"Traditional grid energy cost: ${traditional_grid_cost:,.2f}")

        if primary_energy_source == "Solar PV":
            st.subheader("Solar PV Analysis")
            st.write(f"Solar PV System Cost: ${costs['solar_pv_cost']:,.2f}")
            savings = traditional_grid_cost - costs['solar_pv_cost']
            st.write(f"Savings with Solar PV: ${savings:,.2f}")
            payback_period = calculate_payback_period(costs['solar_pv_cost'], savings)
            st.write(f"Payback period for Solar PV: {payback_period}")
            
        elif primary_energy_source == "Solar Thermal":
            st.subheader("Solar Thermal Analysis")
            with st.expander("Solar Thermal System Cost Breakdown"):
                st.write(f"Solar Thermal Array: ${costs['solar_thermal_cost']:,.2f}")
                st.write(f"Thermal Energy Storage (TES): ${costs['tes_cost']:,.2f}")
                st.write(f"Solar Thermal Control System: ${costs['solar_thermal_control_system_cost']:,.2f}")
                st.write(f"Stirling Engine: ${costs['stirling_engine_cost']:,.2f}")
                st.write(f"Stirling Chiller: ${costs['stirling_chiller_cost']:,.2f}")
                st.write(f"Chilled Beams: ${costs['chilled_beam_cost']:,.2f}")

            total_solar_thermal_cost = costs['solar_thermal_cost'] + costs['tes_cost'] + \
                                       costs['solar_thermal_control_system_cost'] + \
                                       costs['stirling_engine_cost'] + costs['stirling_chiller_cost'] + \
                                       costs['chilled_beam_cost']
            st.write(f"Total Solar Thermal System Cost: ${total_solar_thermal_cost:,.2f}")
            
            net_system_cost = total_solar_thermal_cost - costs['traditional_hvac_cost']
            st.write(f"Net System Cost (after traditional HVAC offset): ${net_system_cost:,.2f}")
            
            solar_thermal_area = calculate_solar_thermal_area(square_footage)
            st.write(f"Yard space required for Solar Thermal: {solar_thermal_area:,.2f} square feet")

            annual_energy_savings = traditional_grid_cost
            st.write(f"Annual Energy Savings: ${annual_energy_savings:,.2f}")
            
            payback_period = calculate_payback_period(net_system_cost, annual_energy_savings)
            st.write(f"Payback period for Solar Thermal: {payback_period}")

if __name__ == "__main__":
    main()
