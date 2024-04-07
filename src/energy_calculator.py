# energy_calculator.py

# Patent Pending, Copyright, All Rights Reserved, Service Mark (SM), 2022-2024
# John M. Willis, Turnaround Security, Inc., Zero Net Energy Homes

import streamlit as st

# Constants for cost calculations and system efficiency
COST_PER_KWH_BUY = 0.12  # Cost of buying electricity from the grid per kWh
AVERAGE_COST_PER_WATT_PV = 3  # Average cost per watt for PV installation
AVERAGE_SYSTEM_SIZE_KW = 6  # Average size of a residential solar PV system in kW
SOLAR_THERMAL_COST_PER_SQFT = 2  # Cost per square foot for solar thermal collectors
TES_EQUIPMENT_COST = 4000  # Fixed equipment cost for Thermal Energy Storage (TES)
STIRLING_ENGINE_COST = 5000  # Estimated cost for Stirling Engine Generator
STIRLING_CHILLER_COST = 3000  # Estimated cost for Stirling Engine Chiller
CHILLED_BEAM_COST_PER_SQFT = 22.5  # Cost per square foot for chilled beams
TYPICAL_HVAC_COST_PER_SQFT = 10  # Typical HVAC cost per square foot of conditioned area
SYSTEM_LIFESPAN_YEARS = 25  # Lifespan of the solar systems in years

# Reference point: $400 per month for 1,422 square feet
REFERENCE_SQUARE_FEET = 1422
REFERENCE_MONTHLY_COST = 400
REFERENCE_ANNUAL_COST = REFERENCE_MONTHLY_COST * 12
REFERENCE_ANNUAL_KWH = REFERENCE_ANNUAL_COST / COST_PER_KWH_BUY  # Calculate kWh based on reference cost

def calculate_energy_cost(construction_type, square_footage):
    construction_types = {
        "Traditional": 1.0,
        "Energy Star": 0.9,
        "EnerPHit": 0.75,
        "Passive House": 0.5
    }
    # Scale the baseline energy consumption based on square footage
    base_energy_consumption = REFERENCE_ANNUAL_KWH * (square_footage / REFERENCE_SQUARE_FEET) * construction_types[construction_type]
    energy_cost = base_energy_consumption * COST_PER_KWH_BUY
    return base_energy_consumption, energy_cost

def calculate_pv_system_cost():
    return AVERAGE_SYSTEM_SIZE_KW * 1000 * AVERAGE_COST_PER_WATT_PV

def calculate_solar_pv_savings():
    annual_pv_production_kwh = AVERAGE_SYSTEM_SIZE_KW * 1400  # Assuming 1400 kWh per kW per year
    annual_savings = annual_pv_production_kwh * COST_PER_KWH_BUY
    lifetime_savings = annual_savings * SYSTEM_LIFESPAN_YEARS
    return annual_savings, lifetime_savings

def calculate_solar_thermal_cost(square_footage):
    solar_thermal_array_cost = square_footage * SOLAR_THERMAL_COST_PER_SQFT
    tes_cost = TES_EQUIPMENT_COST
    stirling_engine_cost = STIRLING_ENGINE_COST
    stirling_chiller_cost = STIRLING_CHILLER_COST
    chilled_beam_cost = square_footage * CHILLED_BEAM_COST_PER_SQFT
    traditional_hvac_cost = square_footage * TYPICAL_HVAC_COST_PER_SQFT
    total_cost = solar_thermal_array_cost + tes_cost + stirling_engine_cost + stirling_chiller_cost + chilled_beam_cost
    net_cost = total_cost - traditional_hvac_cost  # Offsetting with traditional HVAC cost
    return net_cost, solar_thermal_array_cost, tes_cost, stirling_engine_cost, stirling_chiller_cost, chilled_beam_cost, traditional_hvac_cost

def calculate_solar_thermal_savings(traditional_grid_cost):
    annual_savings = traditional_grid_cost
    lifetime_savings = annual_savings * SYSTEM_LIFESPAN_YEARS
    return annual_savings, lifetime_savings

def calculate_payback_period(initial_cost, annual_savings):
    if annual_savings > 0:
        return initial_cost / annual_savings
    return "Infinite"

def main():
    st.title("Zero Net Energy Home Calculator")

    with st.sidebar:
        construction_type = st.selectbox("Select the construction type:", ["Traditional", "Energy Star", "EnerPHit", "Passive House"])
        square_footage = st.slider("Home Square Footage", 1000, 3500, 2000, step=100)
        primary_energy_source = st.radio("Select Primary Energy Source", ["Solar PV", "Solar Thermal", "Electric Grid"])

    if st.button('Calculate'):
        base_energy_consumption, traditional_grid_cost = calculate_energy_cost(construction_type, square_footage)
        
        st.header("Energy Cost Analysis")
        st.write(f"**Construction type:** {construction_type}")
        st.write(f"**Square footage:** {square_footage} sq ft")

        st.subheader("Traditional Electrical Grid Option")
        st.write(f"**Base energy consumption:** {base_energy_consumption:,.2f} kWh/year")
        st.write(f"**Traditional grid energy cost:** ${traditional_grid_cost:,.2f}/year")

        if primary_energy_source == "Solar PV":
            pv_system_cost = calculate_pv_system_cost()
            annual_pv_savings, lifetime_pv_savings = calculate_solar_pv_savings()

            st.subheader("Solar PV Analysis")
            st.write(f"**Solar PV System Cost:** ${pv_system_cost:,.2f}")
            st.write(f"**Annual Savings with Solar PV:** ${annual_pv_savings:,.2f}")
            st.write(f"**Lifetime Savings with Solar PV:** ${lifetime_pv_savings:,.2f}")
            payback_period = calculate_payback_period(pv_system_cost, annual_pv_savings)
            st.write(f"**Payback period for Solar PV:** {payback_period:.2f} years")

        elif primary_energy_source == "Solar Thermal":
            net_cost, solar_thermal_array_cost, tes_cost, stirling_engine_cost, stirling_chiller_cost, chilled_beam_cost, traditional_hvac_cost = calculate_solar_thermal_cost(square_footage)
            annual_st_savings, lifetime_st_savings = calculate_solar_thermal_savings(traditional_grid_cost)

            st.subheader("Solar Thermal Analysis")
            st.write(f"**Net Solar Thermal System Cost (after HVAC offset):** ${net_cost:,.2f}")
            with st.expander("Total System Cost Breakdown"):
                st.write(f"**Solar Thermal Collector array:** ${solar_thermal_array_cost:,.2f}")
                st.write(f"**Thermal Energy Storage (TES):** ${tes_cost:,.2f}")
                st.write(f"**Stirling Engine Generator:** ${stirling_engine_cost:,.2f}")
                st.write(f"**Stirling Engine Chiller:** ${stirling_chiller_cost:,.2f}")
                st.write(f"**Chilled Beams:** ${chilled_beam_cost:,.2f}")
                st.write(f"**Offset Traditional HVAC Cost:** ${traditional_hvac_cost:,.2f}")
            st.write(f"**Annual Savings with Solar Thermal:** ${annual_st_savings:,.2f}")
            st.write(f"**Lifetime Savings with Solar Thermal:** ${lifetime_st_savings:,.2f}")
            payback_period = calculate_payback_period(net_cost, annual_st_savings)
            st.write(f"**Payback period for Solar Thermal:** {payback_period:.2f} years")

if __name__ == "__main__":
    main()
