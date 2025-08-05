import streamlit as st
import pandas as pd
import re
from faker import Faker
import random
from io import StringIO

def parse_ddl(ddl_text):
    """Parse DDL to extract table name and columns - handles both MySQL and Oracle formats"""
    ddl_text = re.sub(r'--.*$', '', ddl_text, flags=re.MULTILINE)
    ddl_text = re.sub(r'/\*.*?\*/', '', ddl_text, flags=re.DOTALL)
    ddl_text = re.sub(r'\s+', ' ', ddl_text).strip()
    
    # Handle both MySQL and Oracle table names
    table_match = re.search(r'CREATE\s+TABLE\s+`?(\w+)`?', ddl_text, re.IGNORECASE)
    if not table_match:
        # Try Oracle format without CREATE TABLE
        table_match = re.search(r'(\w+)\s*\(', ddl_text, re.IGNORECASE)
        if not table_match:
            return None, []
    
    table_name = table_match.group(1)
    
    # Extract column section - handle both formats
    columns_match = re.search(r'CREATE\s+TABLE\s+.*?\((.*)\)', ddl_text, re.IGNORECASE | re.DOTALL)
    if not columns_match:
        # Try Oracle format without CREATE TABLE
        columns_match = re.search(r'(\w+)\s*\((.*)\)', ddl_text, re.IGNORECASE | re.DOTALL)
        if not columns_match:
            return table_name, []
        columns_match = re.search(r'\((.*)\)', ddl_text, re.IGNORECASE | re.DOTALL)
    
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
    """Parse individual column definition - handles both MySQL and Oracle formats"""
    if col_def.startswith(('PRIMARY KEY', 'UNIQUE', 'INDEX', 'KEY', 'CONSTRAINT')):
        return None
    
    # Handle quoted column names like "REF", "FIRST", "LAST" (Oracle style)
    name_match = re.match(r'"?(\w+)"?\s+(.+)', col_def)
    if not name_match:
        return None
    
    name = name_match.group(1)
    spec = name_match.group(2)
    
    # Handle Oracle data types
    type_match = re.match(r'(\w+)(?:\(([^)]+)\))?', spec)
    if not type_match:
        return None
    
    data_type = type_match.group(1).upper()
    size = type_match.group(2) if type_match.group(2) else None
    
    # Map Oracle types to standard types
    type_mapping = {
        'VARCHAR2': 'VARCHAR',
        'NUMBER': 'INT',
        'DATE': 'DATE',
        'TIMESTAMP': 'TIMESTAMP',
        'CHAR': 'CHAR'
    }
    
    mapped_type = type_mapping.get(data_type, data_type)
    
    return {'name': name, 'type': mapped_type, 'size': size}

def generate_consistent_row(columns, fake):
    """Generate consistent row data - handles both MySQL and Oracle formats"""
    # Generate a profile for the row
    profile = fake.simple_profile()
    first_name = profile['name'].split()[0]
    last_name = profile['name'].split()[-1]
    email = f"{first_name.lower()}.{last_name.lower()}@{fake.free_email_domain()}"
    phone = fake.phone_number()
    age = random.randint(18, 80)
    city = fake.city()
    is_active = fake.boolean(chance_of_getting_true=80)
    
    row = {}
    for col in columns:
        col_name = col['name'].lower()
        col_type = col['type']
        
        # Handle Oracle-specific fields
        if col_name == 'prospect_id':
            row[col['name']] = f"PROSP_{fake.uuid4()[:8].upper()}"
        elif col_name == 'ref':
            row[col['name']] = f"REF_{fake.random_number(digits=6)}"
        elif col_name == 'first':
            row[col['name']] = first_name
        elif col_name == 'last':
            row[col['name']] = last_name
        elif col_name == 'gender':
            row[col['name']] = random.choice(['M', 'F', None])
        elif col_name == 'dob':
            row[col['name']] = fake.date_of_birth(minimum_age=18, maximum_age=80)
        elif col_name == 'displayname':
            # Remove special characters, keep only letters, numbers, spaces
            display_name = re.sub(r'[^a-zA-Z0-9\s]', '', profile['name'])
            # Limit to 1 character if specified
            if col.get('size') == '1':
                display_name = display_name[:1]
            row[col['name']] = display_name
        # Handle standard fields
        elif col_name in ['id', 'user_id', 'product_id', 'order_id']:
            row[col['name']] = None  # Will fill later with index
        elif col_name == 'first_name':
            row[col['name']] = first_name
        elif col_name == 'last_name':
            row[col['name']] = last_name
        elif col_name in ['name', 'full_name']:
            row[col['name']] = profile['name']
        elif col_name in ['email', 'mail']:
            row[col['name']] = email
        elif col_name in ['phone', 'telephone']:
            row[col['name']] = phone
        elif col_name == 'age':
            row[col['name']] = age
        elif col_name == 'city':
            row[col['name']] = city
        elif col_name == 'is_active':
            row[col['name']] = is_active
        elif col_name in ['created_at', 'created']:
            row[col['name']] = fake.date_time_this_year()
        elif col_name in ['updated_at', 'updated']:
            row[col['name']] = fake.date_time_this_year()
        elif col_name == 'rundate':
            row[col['name']] = fake.date_time_this_year()
        elif col_name == 'address':
            row[col['name']] = fake.address()
        elif col_name == 'state':
            row[col['name']] = fake.state()
        elif col_name == 'country':
            row[col['name']] = fake.country()
        elif col_name == 'zipcode':
            row[col['name']] = fake.zipcode()
        elif col_name == 'status':
            row[col['name']] = random.choice(['active', 'inactive', 'pending', 'completed', 'Inquiry', 'Prospect'])
        elif col_name in ['description', 'comment', 'notes']:
            row[col['name']] = fake.text(max_nb_chars=100)
        elif col_name in ['url', 'website', 'link']:
            row[col['name']] = fake.url()
        elif col_name in ['password', 'password_hash']:
            row[col['name']] = fake.password()
        elif col_name in ['quantity', 'stock', 'count']:
            row[col['name']] = random.randint(0, 1000)
        elif col_type in ['INT', 'INTEGER', 'BIGINT', 'NUMBER']:
            row[col['name']] = random.randint(1, 999999)
        elif col_type == 'BOOLEAN':
            row[col['name']] = fake.boolean()
        elif col_type in ['FLOAT', 'DOUBLE']:
            row[col['name']] = fake.pyfloat()
        elif col_type == 'DECIMAL':
            row[col['name']] = fake.pydecimal(left_digits=5, right_digits=2)
        elif col_type == 'DATE':
            row[col['name']] = fake.date_this_decade()
        elif col_type in ['DATETIME', 'TIMESTAMP']:
            row[col['name']] = fake.date_time_this_year()
        elif col_type in ['VARCHAR', 'VARCHAR2', 'CHAR']:
            row[col['name']] = fake.text(max_nb_chars=50)
        else:
            row[col['name']] = fake.text(max_nb_chars=20)
    
    return row

def generate_data(columns, n_rows, fake):
    data = []
    for i in range(n_rows):
        row = generate_consistent_row(columns, fake)
        # Fill in auto-increment id if present
        for col in columns:
            if col['name'].lower() in ['id', 'user_id', 'product_id', 'order_id']:
                row[col['name']] = i + 1
        data.append(row)
    return pd.DataFrame(data)

st.set_page_config(page_title="DDL Fake Data Generator", layout="wide")
st.title("DDL Fake Data Generator (Consistent Rows)")
st.write("Paste your CREATE TABLE DDL below. Choose number of rows. Download CSV!")

def main():
    ddl = st.text_area("Paste your CREATE TABLE DDL here:", height=200)
    n_rows = st.number_input("Number of rows", min_value=1, max_value=10000, value=100)
    generate = st.button("Generate Fake Data")
    if generate and ddl.strip():
        table_name, columns = parse_ddl(ddl)
        if not columns:
            st.error("Could not parse columns from DDL. Please check your CREATE TABLE statement.")
            return
        fake = Faker()
        Faker.seed(42)
        random.seed(42)
        df = generate_data(columns, n_rows, fake)
        st.success(f"Generated {n_rows} rows for table '{table_name}'!")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{table_name}_fake_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main() 