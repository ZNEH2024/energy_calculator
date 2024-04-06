# energy_calculator.py

import streamlit as st

# Constants for cost calculations
COST_PER_KWH_BUY = 0.12  # Cost of buying electricity from the grid per kWh
COST_PER_KWH_SELL = 0.10  # Revenue from selling electricity back to the grid per kWh

def calculate_net_energy(construction_type, solar_panels, solar_thermal, stirling_chiller, stirling_generator, excess_capacity):
    construction_types = {
        "Traditional": 1.0,
        "Energy Star": 0.9,
        "EnerPHit": 0.75,
        "Passive House": 0.5
    }
    
    # Energy use estimates (placeholder values)
    base_energy_consumption = 12000  # kWh annually for a 2,000 sq ft house
    solar_energy_generation = 3000 if solar_panels else 0
    solar_thermal_savings = 2000 if solar_thermal else 0
    stirling_chiller_savings = 500 if stirling_chiller else 0
    stirling_generator_output = 4000 if stirling_generator else 0  # Assuming a fixed output for demonstration
    
    # Calculate net energy consumption
    net_energy = (base_energy_consumption * construction_types[construction_type]
                  - solar_energy_generation
                  - solar_thermal_savings
                  - stirling_chiller_savings
                  - stirling_generator_output
                  + excess_capacity)
    
    return net_energy

def main():
    st.title("Zero Net Energy Home Calculator")

    st.header("Home Specifications")
    construction_type = st.selectbox("Select the construction type:",
                                     ("Traditional", "Energy Star", "EnerPHIt", "Passive House"))
    solar_panels = st.checkbox("Solar Panels Installed")
    solar_thermal = st.checkbox("Solar Thermal for Hot Water and Heating")
    stirling_chiller = st.checkbox("Stirling Chiller for Air Conditioning")
    stirling_generator = st.checkbox("Stirling Engine Generator")
    excess_capacity = st.number_input("Excess Electricity Capacity to Grid (kWh)", min_value=0, value=0, step=100)

    if st.button("Calculate Energy Needs and Costs"):
        net_energy = calculate_net_energy(construction_type, solar_panels, solar_thermal, stirling_chiller, stirling_generator, excess_capacity)
        
        if net_energy >= 0:
            total_cost = net_energy * COST_PER_KWH_BUY
            st.success(f"Total energy needed from the grid: {net_energy} kWh")
            st.success(f"Total cost for energy: ${total_cost:.2f}")
        else:
            total_earnings = -net_energy * COST_PER_KWH_SELL
            st.success(f"Total energy provided to the grid: {-net_energy} kWh")
            st.success(f"Total earnings from energy: ${total_earnings:.2f}")

if __name__ == "__main__":
    main()
