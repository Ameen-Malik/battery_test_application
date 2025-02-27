import streamlit as st
import httpx
import pandas as pd
from datetime import datetime
from uuid import UUID
import io
import numpy as np

# Configure page
st.set_page_config(
    page_title="Test Reports - Battery Test Application",
    page_icon="🔋",
    layout="wide"
)

def fetch_tests():
    """Fetch all tests from API."""
    try:
        with httpx.Client() as client:
            response = client.get(f"{st.session_state.api_base_url}/tests")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        st.error(f"Error fetching tests: {str(e)}")
        return []

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

def fetch_readings(cycle_id: UUID):
    """Fetch readings for a cycle."""
    try:
        with httpx.Client() as client:
            response = client.get(f"{st.session_state.api_base_url}/readings/cycle/{cycle_id}")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        st.error(f"Error fetching readings: {str(e)}")
        return []

def generate_csv(test, bank, readings):
    """Generate CSV report for a bank."""
    # Create buffer
    output = io.StringIO()
    
    # Write metadata
    output.write(f"Job Number,{test['job_number']}\n")
    output.write(f"Customer Name,{test['customer_name']}\n")
    output.write(f"Bank Number,{bank['bank_number']}\n")
    output.write(f"Cell Type,{bank['cell_type']}\n")
    output.write(f"Cell Rate,{bank['cell_rate']}\n")
    output.write(f"Percentage Capacity,{bank['percentage_capacity']}\n")
    output.write(f"Discharge Current,{bank['discharge_current']}\n")
    output.write(f"Number of Cells,{bank['number_of_cells']}\n")
    output.write("\n")
    
    # Prepare readings data
    ocv_readings = [r for r in readings if r["is_ocv"]]
    ccv_readings = [r for r in readings if not r["is_ocv"]]
    
    # Create DataFrame columns
    columns = ["Cell Number", "OCV"]
    for i, _ in enumerate(ccv_readings):
        columns.append(f"CCV {i+1}")
    
    # Create data rows
    data = []
    for cell_num in range(bank["number_of_cells"]):
        row = [cell_num + 1]  # Cell number
        
        # Add OCV
        if ocv_readings:
            row.append(next(
                (v["value"] for v in ocv_readings[0]["cell_values"] if v["cell_number"] == cell_num + 1),
                None
            ))
        else:
            row.append(None)
        
        # Add CCVs
        for ccv in ccv_readings:
            row.append(next(
                (v["value"] for v in ccv["cell_values"] if v["cell_number"] == cell_num + 1),
                None
            ))
        
        data.append(row)
    
    # Create DataFrame and write to CSV
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output, index=False)
    
    return output.getvalue()

# Page header
st.title("Test Reports")

# Test selection
tests = fetch_tests()
if tests:
    test_id = st.selectbox(
        "Select Test",
        options=[test["id"] for test in tests],
        format_func=lambda x: next((f"{t['job_number']} - {t['customer_name']}" for t in tests if t["id"] == x), x)
    )
    
    if test_id:
        test = fetch_test(test_id)
        if test:
            # Display test information
            st.markdown(f"""
            ### Test Details
            - **Job Number**: {test['job_number']}
            - **Customer**: {test['customer_name']}
            - **Start Date**: {datetime.fromisoformat(test['start_date']).strftime('%Y-%m-%d')}
            - **Status**: {test['status'].title()}
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
                        # Display bank information
                        st.markdown(f"""
                        ### Bank Details
                        - **Cell Type**: {bank['cell_type']}
                        - **Cell Rate**: {bank['cell_rate']} Ah
                        - **Discharge Current**: {bank['discharge_current']} A
                        - **Number of Cells**: {bank['number_of_cells']}
                        """)
                        
                        # Get readings for all cycles
                        all_readings = []
                        for cycle in bank["cycles"]:
                            readings = fetch_readings(cycle["id"])
                            all_readings.extend(readings)
                        
                        if all_readings:
                            # Generate CSV
                            csv_data = generate_csv(test, bank, all_readings)
                            
                            # Download button
                            st.download_button(
                                label="📥 Download CSV Report",
                                data=csv_data,
                                file_name=f"{test['job_number']}_bank{bank['bank_number']}_report.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                            
                            # Preview data
                            st.markdown("### Data Preview")
                            df = pd.read_csv(io.StringIO(csv_data))
                            st.dataframe(df, use_container_width=True)
                            
                            # Show statistics
                            st.markdown("### Statistics")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("#### OCV Statistics")
                                ocv_stats = df["OCV"].describe()
                                st.dataframe(ocv_stats)
                            
                            with col2:
                                st.markdown("#### CCV Statistics")
                                ccv_cols = [col for col in df.columns if col.startswith("CCV")]
                                if ccv_cols:
                                    ccv_stats = df[ccv_cols].mean().describe()
                                    st.dataframe(ccv_stats)
                        else:
                            st.warning("No readings found for this bank.")
            else:
                st.warning("No banks found for this test.")
else:
    st.info("No tests found. Create a new test to generate reports.") 