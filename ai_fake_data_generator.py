import streamlit as st
import pandas as pd
import re
import anthropic
import os
from io import StringIO

def parse_ddl(ddl_text):
    """Parse DDL to extract table name and columns"""
    ddl_text = re.sub(r'--.*$', '', ddl_text, flags=re.MULTILINE)
    ddl_text = re.sub(r'/\*.*?\*/', '', ddl_text, flags=re.DOTALL)
    ddl_text = re.sub(r'\s+', ' ', ddl_text).strip()
    
    table_match = re.search(r'CREATE\s+TABLE\s+`?(\w+)`?', ddl_text, re.IGNORECASE)
    if not table_match:
        return None, []
    
    table_name = table_match.group(1)
    columns_match = re.search(r'CREATE\s+TABLE\s+.*?\((.*)\)', ddl_text, re.IGNORECASE | re.DOTALL)
    if not columns_match:
        return table_name, []
    
    column_section = columns_match.group(1)
    columns = []
    current = ""
    paren_count = 0
    
    for char in column_section:
        if char == '(':
            paren_count += 1
        elif char == ')':
            paren_count -= 1
        elif char == ',' and paren_count == 0:
            if current.strip():
                col_info = parse_column(current.strip())
                if col_info:
                    columns.append(col_info)
            current = ""
            continue
        current += char
    
    if current.strip():
        col_info = parse_column(current.strip())
        if col_info:
            columns.append(col_info)
    
    return table_name, columns

def parse_column(col_def):
    """Parse individual column definition"""
    if col_def.startswith(('PRIMARY KEY', 'UNIQUE', 'INDEX', 'KEY', 'CONSTRAINT')):
        return None
    
    name_match = re.match(r'`?(\w+)`?\s+(.+)', col_def)
    if not name_match:
        return None
    
    name = name_match.group(1)
    spec = name_match.group(2)
    type_match = re.match(r'(\w+)(?:\(([^)]+)\))?', spec)
    if not type_match:
        return None
    
    data_type = type_match.group(1).upper()
    size = type_match.group(2) if type_match.group(2) else None
    
    return {'name': name, 'type': data_type, 'size': size}

def generate_ai_prompt(table_name, columns, num_rows):
    """Generate AI prompt for data generation"""
    column_definitions = []
    for col in columns:
        col_def = f"{col['name']} ({col['type']}"
        if col['size']:
            col_def += f"({col['size']})"
        col_def += ")"
        column_definitions.append(col_def)
    
    columns_str = ",\n    ".join(column_definitions)
    
    prompt = f"""Generate {num_rows} rows of realistic, consistent fake data for this table:

CREATE TABLE {table_name} (
    {columns_str}
);

IMPORTANT RULES:
1. Geographic consistency: If city is 'Ahmedabad', state must be 'Gujarat' and country 'India'
2. Name consistency: If name is 'John Smith', email should be 'john.smith@domain.com'
3. Age consistency: If age is 25, birth_date should be around 1999
4. Phone consistency: Phone area codes should match the geographic location
5. All data must be logically consistent within each row
6. Use realistic values for all fields
7. Ensure data types match the DDL specifications

Return ONLY the CSV data (no explanations, no headers, just the data rows).
Each row should be on a new line with comma-separated values.
Do not include column headers in the output."""

    return prompt

def generate_data_with_ai(ddl_text, num_rows, api_key):
    """Generate fake data using AI"""
    try:
        # Parse DDL
        table_name, columns = parse_ddl(ddl_text)
        if not columns:
            return None, "Could not parse columns from DDL"
        
        # Generate AI prompt
        prompt = generate_ai_prompt(table_name, columns, num_rows)
        
        # Call Claude API
        client = anthropic.Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4000,
            temperature=0.7,
            system="You are a data generation expert. Generate realistic, consistent fake data based on the provided DDL schema. Always ensure geographic and logical consistency. Return ONLY CSV data without any explanations or headers.",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Extract CSV data from response
        csv_data = response.content[0].text.strip()
        
        # Parse CSV data
        df = pd.read_csv(StringIO(csv_data), header=None)
        
        # Set column names
        df.columns = [col['name'] for col in columns]
        
        return df, None
        
    except Exception as e:
        return None, f"Error generating data: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="AI Fake Data Generator", layout="wide")
st.title("🤖 Claude-Powered Fake Data Generator")
st.write("Paste your DDL and let Claude generate accurate, consistent fake data!")

def main():
    # API Key input
    api_key = st.text_input("Claude API Key", type="password", help="Enter your Claude API key")
    
    if not api_key:
        st.warning("Please enter your Claude API key to continue")
        st.info("Get your API key from: https://console.anthropic.com/")
        return
    
    # DDL input
    ddl = st.text_area("Paste your CREATE TABLE DDL here:", height=200, 
                       placeholder="CREATE TABLE customers (\n    id INT PRIMARY KEY,\n    first_name VARCHAR(50),\n    last_name VARCHAR(50),\n    email VARCHAR(200),\n    city VARCHAR(100),\n    state VARCHAR(50),\n    country VARCHAR(50)\n);")
    
    # Number of rows
    n_rows = st.number_input("Number of rows", min_value=1, max_value=1000, value=10)
    
    # Generate button
    generate = st.button("🤖 Generate Claude Data", type="primary")
    
    if generate and ddl.strip():
        with st.spinner("Claude is generating consistent fake data..."):
            df, error = generate_data_with_ai(ddl, n_rows, api_key)
            
            if error:
                st.error(error)
                return
            
            if df is not None:
                st.success(f"✅ Generated {len(df)} rows of Claude-powered consistent data!")
                
                # Display data
                st.dataframe(df)
                
                # Download button
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"ai_generated_data.csv",
                    mime="text/csv"
                )
                
                # Show consistency examples
                if len(df) > 0:
                    st.subheader("🔍 Data Consistency Examples")
                    sample_row = df.iloc[0]
                    st.write("**Sample row showing consistency:**")
                    st.json(sample_row.to_dict())

if __name__ == "__main__":
    main() 