import streamlit as st
import httpx
import pandas as pd
from datetime import datetime
from uuid import UUID
import numpy as np

# Configure page
st.set_page_config(
    page_title="Test Readings - Battery Test Application",
    page_icon="🔋",
    layout="wide"
)

# Initialize session state
if "current_test" not in st.session_state:
    st.session_state.current_test = None
if "current_bank" not in st.session_state:
    st.session_state.current_bank = None
if "current_cycle" not in st.session_state:
    st.session_state.current_cycle = None
if "reading_values" not in st.session_state:
    st.session_state.reading_values = []

def fetch_test(test_id: UUID):
    """Fetch test details from API."""
    try:
        with httpx.Client() as client:
            response = client.get(f"{st.session_state.api_base_url}/tests/{test_id}")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        st.error(f"Error fetching test: {str(e)}")
        return None

def fetch_bank(bank_id: UUID):
    """Fetch bank details from API."""
    try:
        with httpx.Client() as client:
            response = client.get(f"{st.session_state.api_base_url}/banks/{bank_id}")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        st.error(f"Error fetching bank: {str(e)}")
        return None

def submit_readings(cycle_id: UUID, is_ocv: bool, values: list):
    """Submit readings to API."""
    try:
        reading_data = {
            "cycle_id": str(cycle_id),
            "reading_number": 1,  # This should be determined based on existing readings
            "is_ocv": is_ocv,
            "cell_values": values
        }
        
        with httpx.Client() as client:
            response = client.post(
                f"{st.session_state.api_base_url}/readings",
                json=reading_data
            )
            response.raise_for_status()
            return True, "Readings submitted successfully!"
    except httpx.HTTPError as e:
        return False, f"Error submitting readings: {str(e)}"

def create_reading_grid(num_cells: int, num_cols: int = 10):
    """Create a grid for entering cell readings."""
    num_rows = (num_cells + num_cols - 1) // num_cols
    
    # Initialize values if not already set
    if not st.session_state.reading_values:
        st.session_state.reading_values = [0.0] * num_cells
    
    # Create grid
    for row in range(num_rows):
        cols = st.columns(num_cols)
        for col in range(num_cols):
            cell_index = row * num_cols + col
            if cell_index < num_cells:
                with cols[col]:
                    st.session_state.reading_values[cell_index] = st.number_input(
                        f"Cell {cell_index + 1}",
                        min_value=0.0,
                        max_value=10.0,
                        value=st.session_state.reading_values[cell_index],
                        step=0.001,
                        format="%.3f"
                    )

def show_reading_summary():
    """Show summary statistics for the readings."""
    if st.session_state.reading_values:
        values = np.array(st.session_state.reading_values)
        stats = {
            "Minimum": np.min(values),
            "Maximum": np.max(values),
            "Average": np.mean(values),
            "Standard Deviation": np.std(values)
        }
        
        st.markdown("### Reading Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Minimum", f"{stats['Minimum']:.3f}V")
        with col2:
            st.metric("Maximum", f"{stats['Maximum']:.3f}V")
        with col3:
            st.metric("Average", f"{stats['Average']:.3f}V")
        with col4:
            st.metric("Std Dev", f"{stats['Standard Deviation']:.3f}V")

# Page header
st.title("Test Readings")

# Test selection
tests = []  # This should be fetched from API
test_id = st.selectbox(
    "Select Test",
    options=[test["id"] for test in tests] if tests else [],
    format_func=lambda x: next((t["job_number"] for t in tests if t["id"] == x), x)
)

if test_id:
    test = fetch_test(test_id)
    if test:
        st.session_state.current_test = test
        
        # Display test information
        st.markdown(f"""
        ### Test Details
        - **Job Number**: {test['job_number']}
        - **Customer**: {test['customer_name']}
        - **Start Date**: {datetime.fromisoformat(test['start_date']).strftime('%Y-%m-%d')}
        """)
        
        # Bank selection
        if test["banks"]:
            bank_id = st.selectbox(
                "Select Bank",
                options=[bank["id"] for bank in test["banks"]],
                format_func=lambda x: f"Bank {next((b['bank_number'] for b in test['banks'] if b['id'] == x), x)}"
            )
            
            if bank_id:
                bank = next((b for b in test["banks"] if b["id"] == bank_id), None)
                if bank:
                    st.session_state.current_bank = bank
                    
                    # Reading input
                    st.markdown("### Enter Readings")
                    reading_type = st.radio(
                        "Reading Type",
                        options=["OCV", "CCV"],
                        horizontal=True
                    )
                    
                    # Create reading grid
                    create_reading_grid(bank["number_of_cells"])
                    
                    # Show summary
                    show_reading_summary()
                    
                    # Submit button
                    if st.button("Submit Readings", type="primary", use_container_width=True):
                        if all(v > 0 for v in st.session_state.reading_values):
                            success, message = submit_readings(
                                bank["cycles"][0]["id"],  # This should be the current cycle
                                reading_type == "OCV",
                                st.session_state.reading_values
                            )
                            if success:
                                st.success(message)
                                st.session_state.reading_values = []
                            else:
                                st.error(message)
                        else:
                            st.error("All cells must have readings greater than 0") 