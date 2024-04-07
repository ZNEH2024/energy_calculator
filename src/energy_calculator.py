# energy_calculator.py

import streamlit as st

# Constants for cost calculations
COST_PER_KWH_BUY = 0.12  # Cost of buying electricity from the grid per kWh
AVERAGE_COST_PER_WATT_PV = 3.25  # Average cost per watt for PV panels
SOLAR_THERMAL_COST_PER_SQFT = 2  # Cost per square foot for solar thermal collectors
TES_COST_FOR_2000SF_HOME_5DAYS = 3000  # Cost for TES for a 2,000 SF home with 5 days reserve
CHILLED_BEAM_COST_PER_SQFT = 22.5  # Cost per square foot for chilled beams
CHILLED_BEAM_COVERAGE_FACTOR = 0.75  # Coverage factor for chilled beams
TYPICAL_HVAC_COST_PER_SQFT = 10  # Typical HVAC cost per square foot of conditioned area
CONDITIONED_AREA_PERCENTAGE = 0.75  # Percentage of the house that is conditioned

def calculate_energy_cost(construction_type, square_footage, primary_energy_source):
    # Energy consumption calculation (simplified)
    base_energy_consumption = 12000 * (square_footage / 2000)  # Base annual kWh for traditional construction

    # Adjust based on construction type
    energy_consumption = base_energy_consumption * {
        "Traditional": 1.0,
        "Energy Star": 0.9,
        "EnerPHit": 0.75,
        "Passive House": 0.5
    }.get(construction_type, 1.0)

    # For simplicity, assume grid electricity cost for all energy use
    return energy_consumption * COST_PER_KWH_BUY

def calculate_system_cost(square_footage, primary_energy_source, include_chilled_beams):
    solar_thermal_cost = square_footage * SOLAR_THERMAL_COST_PER_SQFT if primary_energy_source == "Solar Thermal" else 0
    tes_cost = TES_COST_FOR_2000SF_HOME_5DAYS if primary_energy_source == "Solar Thermal" else 0
    chilled_beam_cost = square_footage * CHILLED_BEAM_COVERAGE_FACTOR * CHILLED_BEAM_COST_PER_SQFT if include_chilled_beams else 0
    hvac_cost = square_footage * CONDITIONED_AREA_PERCENTAGE * TYPICAL_HVAC_COST_PER_SQFT if primary_energy_source != "Solar Thermal" else 0

    return solar_thermal_cost + tes_cost + chilled_beam_cost + hvac_cost

def calculate_payback_period(traditional_cost, solar_thermal_cost, annual_savings):
    additional_investment = solar_thermal_cost - traditional_cost
    if annual_savings <= 0:
        return "Infinite (no savings)"
    
    return additional_investment / annual_savings

def main():
    st.title("Zero Net Energy Home Calculator")

    construction_type = st.selectbox("Select the construction type:", ("Traditional", "Energy Star", "EnerPHit", "Passive House"))
    square_footage = st.slider("Home Square Footage", 1000, 3500, step=100)
    primary_energy_source = st.radio("Select Primary Energy Source", ["Solar PV", "Solar Thermal", "Electric Grid"])

    include_chilled_beams = primary_energy_source == "Solar Thermal"
    
    if st.button("Calculate Energy Needs and Costs"):
        traditional_cost = calculate_energy_cost("Traditional", square_footage, "Electric Grid")  # Cost using traditional construction with grid power
        solar_thermal_cost = calculate_system_cost(square_footage, primary_energy_source, include_chilled_beams)  # Total system cost for solar thermal
        annual_savings = traditional_cost - calculate_energy_cost(construction_type, square_footage, primary_energy_source)  # Annual savings compared to traditional

        st.write(f"Traditional Electric Grid Cost: ${traditional_cost:.2f}")
        st.write(f"Solar Thermal System Cost: ${solar_thermal_cost:.2f}")
        st.write(f"Annual Savings with {construction_type}: ${annual_savings:.2f}")

        payback_period = calculate_payback_period(traditional_cost, solar_thermal_cost, annual_savings)
        st.write(f"Payback period: {payback_period} years")

if __name__ == "__main__":
    main()
