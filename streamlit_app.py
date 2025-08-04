import streamlit as st
import pandas as pd
import re
from faker import Faker
import random
from io import StringIO

def parse_ddl(ddl_text):
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

def generate_consistent_row(columns, fake):
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
        if col_name in ['id', 'user_id', 'product_id', 'order_id']:
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
        elif col_name == 'created_at':
            row[col['name']] = fake.date_time_this_year()
        elif col_name == 'updated_at':
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
            row[col['name']] = random.choice(['active', 'inactive', 'pending', 'completed'])
        elif col_name in ['description', 'comment', 'notes']:
            row[col['name']] = fake.text(max_nb_chars=100)
        elif col_name in ['url', 'website', 'link']:
            row[col['name']] = fake.url()
        elif col_name in ['password', 'password_hash']:
            row[col['name']] = fake.password()
        elif col_name in ['quantity', 'stock', 'count']:
            row[col['name']] = random.randint(0, 1000)
        elif col['type'] in ['INT', 'INTEGER', 'BIGINT']:
            row[col['name']] = random.randint(1, 999999)
        elif col['type'] == 'BOOLEAN':
            row[col['name']] = fake.boolean()
        elif col['type'] in ['FLOAT', 'DOUBLE']:
            row[col['name']] = fake.pyfloat()
        elif col['type'] == 'DECIMAL':
            row[col['name']] = fake.pydecimal(left_digits=5, right_digits=2)
        elif col['type'] == 'DATE':
            row[col['name']] = fake.date_this_decade()
        elif col['type'] in ['DATETIME', 'TIMESTAMP']:
            row[col['name']] = fake.date_time_this_year()
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