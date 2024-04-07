# energy_calculator.py

# Patent Pending, Copyright, All Rights Reserved, Service Mark (SM), 2022-2024
# John M. Willis, Turnaround Security, Inc., Zero Net Energy Homes

import streamlit as st

# Constants for cost calculations
COST_PER_KWH_BUY = 0.12  # Cost of buying electricity from the grid per kWh
COST_PER_KWH_SELL = 0.10  # Revenue from selling electricity back to the grid per kWh
AVERAGE_COST_PER_WATT_PV = 3.25  # Average cost per watt for PV panels
SOLAR_THERMAL_COST_PER_SQFT = 2  # Cost per square foot for solar thermal collectors
TES_COST_FOR_2000SF_HOME_5DAYS = 3000  # Cost for TES for a 2,000 SF home with 5 days reserve
CHILLED_BEAM_COST_PER_SQFT = 22.5  # Cost per square foot for chilled beams
CHILLED_BEAM_COVERAGE_FACTOR = 0.75  # Coverage factor for chilled beams
TYPICAL_HVAC_COST_PER_SQFT = 10  # Typical HVAC cost per square foot of conditioned area
CONDITIONED_AREA_PERCENTAGE = 0.75  # Percentage of the house that is conditioned

def calculate_net_energy(construction_type, primary_energy_source, solar_thermal, stirling_chiller, stirling_generator, excess_capacity):
    construction_types = {
        "Traditional": 1.0,
        "Energy Star": 0.9,
        "EnerPHit": 0.75,
        "Passive House": 0.5
    }
    
    base_energy_consumption = 12000  # kWh annually for a 2,000 sq ft house
    solar_energy_generation = 3000 if primary_energy_source == "Solar PV" else 0
    solar_thermal_savings = 2000 if solar_thermal else 0
    stirling_chiller_savings = 500 if stirling_chiller else 0
    stirling_generator_output = 4000 if stirling_generator else 0
    
    net_energy = (base_energy_consumption * construction_types[construction_type]
                  - solar_energy_generation
                  - solar_thermal_savings
                  - stirling_chiller_savings
                  - stirling_generator_output
                  + excess_capacity)
    
    return net_energy

def calculate_cost_for_components(square_footage, primary_energy_source, include_tes):
    solar_pv_cost = square_footage * AVERAGE_COST_PER_WATT_PV if primary_energy_source == "Solar PV" else 0
    solar_thermal_cost = square_footage * SOLAR_THERMAL_COST_PER_SQFT if primary_energy_source == "Solar Thermal" else 0
    tes_cost = (square_footage / 2000 * TES_COST_FOR_2000SF_HOME_5DAYS) if include_tes else 0
    chilled_beam_cost = square_footage * CHILLED_BEAM_COVERAGE_FACTOR * CHILLED_BEAM_COST_PER_SQFT if primary_energy_source == "Solar Thermal" else 0
    conditioned_area = square_footage * CONDITIONED_AREA_PERCENTAGE
    hvac_cost = conditioned_area * TYPICAL_HVAC_COST_PER_SQFT if primary_energy_source in ["Solar PV", "Electric Grid"] else 0

    return solar_pv_cost, solar_thermal_cost, tes_cost, chilled_beam_cost, hvac_cost

def main():
    st.title("Zero Net Energy Home Calculator")

    st.header("Home Specifications")
    construction_type = st.selectbox("Select the construction type:", ("Traditional", "Energy Star", "EnerPHit", "Passive House"))
    square_footage = st.slider("Home Square Footage", 1000, 3500, step=100)
    primary_energy_source = st.radio("Select Primary Energy Source", ["Solar PV", "Solar Thermal", "Electric Grid"])
    
    solar_thermal = primary_energy_source == "Solar Thermal"
    stirling_chiller = solar_thermal
    stirling_generator = solar_thermal

    excess_capacity = st.number_input("Excess Electricity Capacity to Grid (kWh)", min_value=0, value=0, step=100)

    include_tes = solar_thermal
    include_chilled_beams = solar_thermal

    if st.button("Calculate Energy Needs and Costs"):
        net_energy = calculate_net_energy(construction_type, primary_energy_source, solar_thermal, stirling_chiller, stirling_generator, excess_capacity)
        if net_energy >= 0:
            total_cost = net_energy * COST_PER_KWH_BUY
            st.success(f"Total energy needed from the grid: {net_energy} kWh")
            st.success(f"Total cost for energy: ${total_cost:.2f}")
        else:
            total_earnings = -net_energy * COST_PER_KWH_SELL
            st.success(f"Total energy provided to the grid: {-net_energy} kWh")
            st.success(f"Total earnings from energy: ${total_earnings:.2f}")

        solar_pv_cost, solar_thermal_cost, tes_cost, chilled_beam_cost, hvac_cost = calculate_cost_for_components(square_footage, primary_energy_source, include_tes)
        st.write(f"Solar PV Cost: ${solar_pv_cost:.2f}" if primary_energy_source == "Solar PV" else "Solar PV not selected as primary energy source.")
        st.write(f"Solar Thermal Cost: ${solar_thermal_cost:.2f}" if solar_thermal else "Solar Thermal not selected as primary energy source.")
        st.write(f"TES Cost: ${tes_cost:.2f}" if include_tes else "TES not included.")
        st.write(f"Chilled Beam Cost: ${chilled_beam_cost:.2f}" if include_chilled_beams else "Chilled Beams not included.")
        st.write(f"HVAC Cost: ${hvac_cost:.2f}" if primary_energy_source in ["Solar PV", "Electric Grid"] else "HVAC not applicable.")

if __name__ == "__main__":
    main()
