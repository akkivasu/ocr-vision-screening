import streamlit as st
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import pandas as pd
import io
import os

# Azure Form Recognizer endpoint
endpoint = "https://document4.cognitiveservices.azure.com/"

st.title("Document Extraction")
st.subheader("Vision Screening")

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''

# Function to prompt for API key
def get_api_key():
    key = st.text_input("Enter your Azure Form Recognizer API Key:", type="password", key="api_key_input")
    if key:
        st.session_state.api_key = key
    return st.session_state.api_key

# Get API key
key = get_api_key()

# Function definitions (docType, sanitizeSLNO, removeEmptyRows, sanitizeClass, sanitizeSex) should be here
def docType(table):
    if (table[0] == ['SI. No.', 'STUDENT NAME', 'CLASS', 'SECTION', 'AGE', 'M/F', 'PARENTS NAME', 'RE VISION', 'LE VISION', 'REMARKS']): 
        return 1
    elif (table[0] == ['Sl. No.', 'STUDENT NAME', 'CLASS', 'SECTION', 'AGE', 'M/F', 'PARENTS NAME', 'RE VISION', 'LE VISION', 'REMARKS']):
        return 1
    elif (table[0] == ['Sl. No.', 'STUDENT NAME', 'CLASS / SEC.', 'DOB', 'M/F', 'PARENTS NAME', 'MOBILE NUMBER', 'RIGHT EYE', '', '', '', 'LEFT EYE', '', '', '', 'SATS ID', 'REMARKS']):
        return 2
    elif (table[0] == ['SI. No.', 'STUDENT NAME', 'CLASS / SEC.', 'DOB', 'M/F', 'PARENTS NAME', 'MOBILE NUMBER', 'RIGHT EYE', '', '', '', 'LEFT EYE', '', '', '', 'SATS ID', 'REMARKS']):
        return 2
    else:
        return 0
    
def sanitizeSLNO(table):
    if len(table) < 2:  # If table has less than 2 rows, no need to sanitize
        return table
    
    for i in range(1, len(table)):  # Start from the second row (index 1)
        table[i][0] = str(i)  # Set the first column to the row index (as a string)
    
    return table

# def removeEmptyRows(table):
#     if len(table) < 2:  # If table has less than 2 rows, no need to process
#         return table
    
#     # Keep the header (first row) and filter the rest
#     if docType(table) == 1:
#         return [table[0]] + [row for row in table[1:] if row[1].strip() != ""]
#     elif docType(table) == 2:
#         return [table[0]] + [table[1]] + [row for row in table[2:] if row[1].strip() != ""]
def removeEmptyRows(table):
    # Start from the third row (index 2) and iterate backwards
    for i in range(len(table) - 1, 1, -1):
        # Check if the second column (index 1) is empty
        if not table[i][1].strip():
            # If it's empty, remove the entire row
            del table[i]
    
    return table

def sanitizeClass(table):
    if len(table) < 2:  # If table has less than 2 rows, no need to sanitize
        return table
    
    for i in range(1, len(table)):  # Start from the second row (index 1)
        if len(table[i]) > 2 and table[i][2].startswith('-') and table[i][2].endswith('-'):
            if len(table[i-1]) > 2:
                table[i][2] = table[i-1][2]
    
    return table

def sanitizeSex(table):
    if docType(table) == 1:
        for i in range(1, len(table)):
            table[i][5] = table[i][5].upper()
    elif docType(table) == 2:
        for i in range(1, len(table)):
            table[i][4] = table[i][4].upper()
    return table

def process_document(uploaded_file):
    file_name = os.path.splitext(uploaded_file.name)[0] + '.xlsx'
    
    # Create DocumentAnalysisClient
    document_analysis_client = DocumentAnalysisClient(
        endpoint=endpoint, credential=AzureKeyCredential(st.session_state.api_key)
    )

    # Analyze the uploaded document
    with st.spinner('Analyzing document...'):
        poller = document_analysis_client.begin_analyze_document("prebuilt-layout", document=uploaded_file)
        result = poller.result()

    # Display results
    st.success("Extraction complete!")

    all_tables_data = []  # List to store all table data
    for table_idx, table in enumerate(result.tables):
        table_data = []
        for cell in table.cells:
            while len(table_data) <= cell.row_index:
                table_data.append([])
            while len(table_data[cell.row_index]) <= cell.column_index:
                table_data[cell.row_index].append("")
            table_data[cell.row_index][cell.column_index] = cell.content
        
        if table_idx == 0:
            all_tables_data.extend(table_data)
        else:
            all_tables_data.extend(table_data[docType(table_data):])

    print(type(all_tables_data))
    print(all_tables_data)
    print(removeEmptyRows(all_tables_data))

    all_tables_data = sanitizeSex(sanitizeClass(sanitizeSLNO(removeEmptyRows(all_tables_data))))

    if all_tables_data:
        df = pd.DataFrame(all_tables_data)
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='All Tables', index=False, header=False)

        st.download_button(
            label="Download Excel File",
            data=output.getvalue(),
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("No tables found in the document.")

# Main app logic
if st.session_state.api_key:
    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Add an "Extract" button
        if st.button("Extract"):
            process_document(uploaded_file)
    else:
        st.info("Please upload a PDF file to analyze.")
else:
    st.warning("Please enter your API key to use the application.")