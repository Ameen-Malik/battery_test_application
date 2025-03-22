import streamlit as st
import httpx
import pandas as pd
from datetime import datetime
from uuid import UUID

# Configure page
st.set_page_config(
    page_title="Battery Test Application",
    page_icon="🔋",
    layout="wide"
)

# Initialize session state
if "api_base_url" not in st.session_state:
    st.session_state.api_base_url = "http://localhost:8000/api/v1"

def fetch_tests():
    """Fetch all tests from the API."""
    try:
        with httpx.Client() as client:
            response = client.get(f"{st.session_state.api_base_url}/tests")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        st.error(f"Error fetching tests: {str(e)}")
        return []

def format_test_status(status):
    """Format test status with color."""
    if status == "completed":
        return "✅ Completed"
    elif status == "in_progress":
        return "🔄 In Progress"
    return "⏳ Scheduled"

# Title and description
st.title("🔋 Battery Test Application")
st.markdown("""
Welcome to the Battery Test Application. This application helps you manage and track battery testing processes.

### Features:
- Create and manage battery tests
- Record OCV and CCV readings
- Track test progress
- Generate test reports
""")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Recent Tests")
    tests = fetch_tests()
    
    if tests:
        # Convert tests to DataFrame for better display
        test_data = []
        for test in tests:
            test_data.append({
                "Job Number": test["job_number"],
                "Customer": test["customer_name"],
                "Status": format_test_status(test["status"]),
                "Start Date": datetime.fromisoformat(test["start_date"]).strftime("%Y-%m-%d"),
                "Cycles": test["number_of_cycles"],
                "ID": test["id"]
            })
        
        df = pd.DataFrame(test_data)
        st.dataframe(
            df.drop("ID", axis=1),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No tests found. Create a new test to get started.")

with col2:
    st.subheader("Quick Actions")
    
    # Create New Test button
    if st.button("➕ Create New Test", use_container_width=True):
        st.switch_page("pages/test_setup.py")
    
    # View Reports button
    if st.button("📊 View Reports", use_container_width=True):
        st.switch_page("pages/reports.py")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Battery Test Application v1.0</p>
</div>
""", unsafe_allow_html=True) 