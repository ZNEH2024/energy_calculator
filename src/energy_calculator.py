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

def calculate_system_cost(square_footage, primary_energy_source):
    if primary_energy_source == "Solar Thermal":
        solar_thermal_cost = square_footage * SOLAR_THERMAL_COST_PER_SQFT
        tes_cost = TES_COST_FOR_2000SF_HOME_5DAYS
        chilled_beam_cost = square_footage * CHILLED_BEAM_COVERAGE_FACTOR * CHILLED_BEAM_COST_PER_SQFT
    else:
        solar_thermal_cost = tes_cost = chilled_beam_cost = 0
    
    hvac_cost = square_footage * CONDITIONED_AREA_PERCENTAGE * TYPICAL_HVAC_COST_PER_SQFT if primary_energy_source != "Solar Thermal" else 0

    return solar_thermal_cost, tes_cost, chilled_beam_cost, hvac_cost

def main():
    st.title("Zero Net Energy Home Calculator")

    construction_type = st.selectbox("Select the construction type:", ("Traditional", "Energy Star", "EnerPHit", "Passive House"))
    square_footage = st.slider("Home Square Footage", 1000, 3500, step=100)
    primary_energy_source = st.radio("Select Primary Energy Source", ["Solar PV", "Solar Thermal", "Electric Grid"])

    if st.button("Calculate Energy Needs and Costs"):
        grid_energy_cost = calculate_energy_cost(construction_type, square_footage, primary_energy_source)
        st.write(f"Energy cost from the grid: ${grid_energy_cost:.2f}")

        solar_thermal_cost, tes_cost, chilled_beam_cost, hvac_cost = calculate_system_cost(square_footage, primary_energy_source)
        
        if primary_energy_source == "Solar Thermal":
            st.write(f"Solar Thermal Cost: ${solar_thermal_cost:.2f}")
            st.write(f"TES Cost: ${tes_cost:.2f}")
            st.write(f"Chilled Beam Cost: ${chilled_beam_cost:.2f}")
        elif primary_energy_source in ["Solar PV", "Electric Grid"]:
            st.write(f"HVAC Cost: ${hvac_cost:.2f}")
        else:
            st.write("Costs for the selected energy source are not applicable.")

if __name__ == "__main__":
    main()
