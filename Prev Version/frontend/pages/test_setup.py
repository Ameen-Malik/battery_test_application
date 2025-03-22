import streamlit as st
import httpx
from datetime import datetime, date, time
import json

# Configure page
st.set_page_config(
    page_title="Create Test - Battery Test Application",
    page_icon="🔋",
    layout="wide"
)

# Initialize session state for form data
if "test_setup_form" not in st.session_state:
    st.session_state.test_setup_form = {
        "job_number": "",
        "customer_name": "",
        "cell_type": "KPL",
        "cell_rate": 0.0,
        "percentage_capacity": 0.0,
        "number_of_cells": 10,
        "number_of_cycles": 1,
        "bank_number": 1,
        "time_interval": 1,
        "start_date": date.today(),
        "start_time": time(hour=8, minute=0)
    }

def calculate_discharge_current(cell_rate: float, percentage_capacity: float) -> float:
    """Calculate discharge current based on cell rate and percentage capacity."""
    return (percentage_capacity * cell_rate) / 100

def create_test():
    """Create a new test via API."""
    form = st.session_state.test_setup_form
    
    # Combine date and time
    start_datetime = datetime.combine(form["start_date"], form["start_time"])
    
    # Prepare test data
    test_data = {
        "job_number": form["job_number"],
        "customer_name": form["customer_name"],
        "number_of_cycles": form["number_of_cycles"],
        "time_interval": form["time_interval"],
        "start_date": start_datetime.isoformat(),
        "start_time": start_datetime.isoformat()
    }
    
    # Prepare bank data
    bank_data = {
        "bank_number": form["bank_number"],
        "cell_type": form["cell_type"],
        "cell_rate": form["cell_rate"],
        "percentage_capacity": form["percentage_capacity"],
        "number_of_cells": form["number_of_cells"],
        "discharge_current": calculate_discharge_current(
            form["cell_rate"],
            form["percentage_capacity"]
        )
    }
    
    try:
        with httpx.Client() as client:
            # Create test
            response = client.post(
                f"{st.session_state.api_base_url}/tests",
                json=test_data
            )
            response.raise_for_status()
            test = response.json()
            
            # Create bank with test ID
            bank_data["test_id"] = test["id"]
            response = client.post(
                f"{st.session_state.api_base_url}/banks",
                json=bank_data
            )
            response.raise_for_status()
            
            return True, "Test created successfully!"
    except httpx.HTTPError as e:
        return False, f"Error creating test: {str(e)}"

# Title and navigation
col1, col2 = st.columns([3, 1])
with col1:
    st.title("Create New Test")
with col2:
    if st.button("← Back to Dashboard"):
        st.switch_page("Home.py")

# Test Setup Form
st.markdown("### Test Configuration")

col1, col2 = st.columns(2)

with col1:
    # Basic Information
    st.subheader("Basic Information")
    st.session_state.test_setup_form["job_number"] = st.text_input(
        "Job Number",
        value=st.session_state.test_setup_form["job_number"],
        help="Unique identifier for this test"
    )
    
    st.session_state.test_setup_form["customer_name"] = st.text_input(
        "Customer Name",
        value=st.session_state.test_setup_form["customer_name"]
    )
    
    st.session_state.test_setup_form["cell_type"] = st.selectbox(
        "Cell Type",
        options=["KPL", "KPM", "KPH"],
        index=["KPL", "KPM", "KPH"].index(st.session_state.test_setup_form["cell_type"])
    )

with col2:
    # Test Parameters
    st.subheader("Test Parameters")
    st.session_state.test_setup_form["cell_rate"] = st.number_input(
        "Cell Rate (Ah)",
        min_value=0.0,
        value=st.session_state.test_setup_form["cell_rate"],
        step=0.1
    )
    
    st.session_state.test_setup_form["percentage_capacity"] = st.number_input(
        "Percentage Capacity (%)",
        min_value=0.0,
        max_value=100.0,
        value=st.session_state.test_setup_form["percentage_capacity"],
        step=0.1
    )
    
    # Calculate and display discharge current
    discharge_current = calculate_discharge_current(
        st.session_state.test_setup_form["cell_rate"],
        st.session_state.test_setup_form["percentage_capacity"]
    )
    st.info(f"Calculated Discharge Current: {discharge_current:.2f} A")

# Test Configuration
st.markdown("### Test Configuration")
col1, col2, col3 = st.columns(3)

with col1:
    st.session_state.test_setup_form["number_of_cells"] = st.number_input(
        "Number of Cells",
        min_value=10,
        max_value=200,
        value=st.session_state.test_setup_form["number_of_cells"]
    )

with col2:
    st.session_state.test_setup_form["number_of_cycles"] = st.number_input(
        "Number of Test Cycles",
        min_value=1,
        max_value=5,
        value=st.session_state.test_setup_form["number_of_cycles"]
    )

with col3:
    st.session_state.test_setup_form["bank_number"] = st.radio(
        "Bank Number",
        options=[1, 2],
        index=st.session_state.test_setup_form["bank_number"] - 1,
        horizontal=True
    )

# Schedule
st.markdown("### Schedule")
col1, col2, col3 = st.columns(3)

with col1:
    st.session_state.test_setup_form["start_date"] = st.date_input(
        "Start Date",
        value=st.session_state.test_setup_form["start_date"],
        min_value=date.today()
    )

with col2:
    st.session_state.test_setup_form["start_time"] = st.time_input(
        "Start Time",
        value=st.session_state.test_setup_form["start_time"]
    )

with col3:
    st.session_state.test_setup_form["time_interval"] = st.radio(
        "Time Interval",
        options=[1, 2],
        index=st.session_state.test_setup_form["time_interval"] - 1,
        horizontal=True,
        format_func=lambda x: f"{x} hour{'s' if x > 1 else ''}"
    )

# Submit button
st.markdown("---")
if st.button("Create Test", type="primary", use_container_width=True):
    # Validate form
    if not st.session_state.test_setup_form["job_number"]:
        st.error("Job Number is required")
    elif not st.session_state.test_setup_form["customer_name"]:
        st.error("Customer Name is required")
    elif st.session_state.test_setup_form["cell_rate"] <= 0:
        st.error("Cell Rate must be greater than 0")
    elif st.session_state.test_setup_form["percentage_capacity"] <= 0:
        st.error("Percentage Capacity must be greater than 0")
    else:
        success, message = create_test()
        if success:
            st.success(message)
            st.session_state.test_setup_form = {
                "job_number": "",
                "customer_name": "",
                "cell_type": "KPL",
                "cell_rate": 0.0,
                "percentage_capacity": 0.0,
                "number_of_cells": 10,
                "number_of_cycles": 1,
                "bank_number": 1,
                "time_interval": 1,
                "start_date": date.today(),
                "start_time": time(hour=8, minute=0)
            }
            # Redirect to dashboard after 2 seconds
            st.rerun()
        else:
            st.error(message) 