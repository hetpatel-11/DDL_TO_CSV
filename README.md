# DDL to CSV Fake Data Generator

A powerful Python application that converts DDL (Data Definition Language) schemas into realistic, consistent fake data in CSV format. Built with Streamlit for an intuitive web interface.

## 🚀 Features

- **DDL Parsing**: Automatically parses CREATE TABLE statements
- **Consistent Data Generation**: Ensures related fields make logical sense together
- **Flexible Schema Support**: Works with any DDL structure
- **Web Interface**: Easy-to-use Streamlit UI
- **CSV Export**: Download generated data as CSV files
- **Realistic Data**: Uses Faker library for authentic-looking data

## 📋 Requirements

- Python 3.8+
- Streamlit
- Pandas
- Faker

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hetpatel-11/DDL_TO_CSV.git
   cd DDL_TO_CSV
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install streamlit pandas faker
   ```

## 🎯 Usage

### Quick Start

1. **Run the application**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Open your browser** and navigate to the provided URL (usually `http://localhost:8501`)

3. **Paste your DDL** in the text area

4. **Set the number of rows** you want to generate

5. **Click "Generate Fake Data"** and download the CSV

### Example DDL

```sql
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(200) UNIQUE NOT NULL,
    phone VARCHAR(20),
    age INT CHECK (age >= 18),
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(50) DEFAULT 'USA',
    zipcode VARCHAR(10),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    status ENUM('active', 'inactive', 'pending') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 🔧 How It Works

### Current Data Consistency Features

The application currently ensures basic consistency by:

1. **Profile Generation**: Creates a complete profile for each row
2. **Name-Email Consistency**: Ensures names and emails match (e.g., John Smith → john.smith@domain.com)
3. **Basic Field Mapping**: Maps common field names to appropriate data types

### Current Limitations

⚠️ **Important**: The current version has limited consistency beyond name-email matching:

- **Geographic Inconsistency**: City, state, and country may not be logically related
- **Phone-Location Mismatch**: Phone area codes may not match the geographic location
- **Age-Date Inconsistency**: Age and birth dates may not align properly
- **Limited Cross-field Validation**: Most fields are generated independently

### Supported Data Types

- **Text**: VARCHAR, CHAR, TEXT
- **Numbers**: INT, INTEGER, BIGINT, FLOAT, DOUBLE, DECIMAL
- **Dates**: DATE, DATETIME, TIMESTAMP
- **Booleans**: BOOLEAN, BOOL
- **Enums**: ENUM values

### Smart Field Detection

The app intelligently maps common field names:

- `first_name`, `last_name` → Realistic names
- `email`, `mail` → Matching email addresses (consistent with names)
- `phone`, `telephone` → Phone numbers (may not match location)
- `city`, `state`, `country` → Individual realistic values (may not be geographically consistent)
- `age`, `birth_date` → Realistic values (may not be chronologically consistent)
- `created_at`, `updated_at` → Realistic timestamps

## 📊 Output

The generated CSV will contain:
- **Basic consistency** between names and emails
- **Realistic individual values** for each field
- **Proper formatting** matching the DDL specifications
- **Auto-incrementing IDs** where appropriate

⚠️ **Note**: While individual fields contain realistic data, cross-field consistency (geographic, chronological, etc.) is limited in the current version.

## 🎨 UI Features

- **Real-time DDL parsing**
- **Data preview** before download
- **Error handling** for invalid DDL
- **Responsive design** for all screen sizes
- **Download functionality** for generated CSV files

## 🔍 Example Output

| id | first_name | last_name | email | phone | age | city | state | is_active |
|----|------------|-----------|-------|-------|-----|------|-------|-----------|
| 1 | John | Smith | john.smith@example.com | +1-555-123-4567 | 28 | New York | NY | true |
| 2 | Sarah | Johnson | sarah.johnson@example.com | +1-555-987-6543 | 34 | Los Angeles | CA | true |

**Note**: In this example, the name-email consistency is maintained, but geographic consistency (city/state combinations) and phone area codes may not match the actual locations.

## 🚀 Advanced Usage

### Custom Field Mapping

The application automatically detects field patterns, but you can extend it by modifying the `generate_consistent_row` function in `streamlit_app.py`.

### Improving Data Consistency

To enhance cross-field consistency, consider:

1. **Geographic Consistency**: Implement location-based phone number generation
2. **Age-Date Alignment**: Ensure birth dates match the specified age
3. **Regional Data**: Use location-specific data providers
4. **Cross-field Validation**: Add validation rules for related fields

### Batch Processing

For multiple tables, run the application multiple times or modify the code to handle multiple DDL statements.

### Alternative: AI-Powered Version

For better consistency, try the AI-powered version (`ai_fake_data_generator.py`) which uses Claude to generate more contextually consistent data.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Het Patel**
- GitHub: [@hetpatel-11](https://github.com/hetpatel-11)
- Email: hetkp8044@gmail.com

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the web framework
- [Faker](https://faker.readthedocs.io/) for realistic data generation
- [Pandas](https://pandas.pydata.org/) for data manipulation

---

**⭐ Star this repository if you find it helpful!** 