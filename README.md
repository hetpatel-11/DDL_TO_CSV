# Fake Prospect Data Generator

A sophisticated Python script that generates logical and consistent fake data for college prospect tracking systems. This generator maintains realistic relationships between data fields to avoid the common pitfalls of AI-generated fake data.

## Features

### 🎯 **Logical Data Relationships**
- **Cultural Consistency**: Names match appropriate high schools and geographic locations
- **Date Logic**: Inquiry dates are logically related to prospect dates
- **Source Relationships**: Inquiry sources and prospect sources follow realistic patterns
- **Academic Terms**: Proper academic term formatting (202440 = Fall 2024, 202540 = Spring 2025)

### 🌍 **Multi-Cultural Support**
- **American**: Common US names and high schools
- **Indian**: Indian names with Delhi Public School
- **Chinese**: Chinese names with Beijing No. 4 High School
- **Japanese**: Japanese names with Tokyo Metropolitan Kokusai High School
- **French**: French names with Lycee Louis-le-Grand
- **German**: German names with Heinrich-Hertz-Gymnasium
- **British**: British names with The London Oratory School
- **Brazilian**: Brazilian names with Colegio Pedro II
- **Australian**: Australian names with Sydney Boys High School
- **South African**: South African names with Rondebosch Boys High School

### 📊 **Data Fields Generated**
- `id`: Empty field (matches original)
- `prospect_id`: Unique 7-digit identifier
- `applicant`: Sometimes matches prospect_id (30% probability)
- `full_name`, `first_name`, `last_name`: Culturally consistent names
- `birthdate`: Appropriate for high school students (2006-2008)
- `email_address`: Generated from name (firstname.lastname@email.com)
- `inquiry_source`: College board, high school visit, campus visit, etc.
- `date_first_prospect`: Date when prospect was first recorded
- `prospect_academic_term`: Academic term (202440/202540)
- `date_first_inquire`: Date of first inquiry
- `inquiry_academic_term`: Academic term for inquiry
- `prospect_source`: Source that led to prospect creation
- `hs_name`: Culturally appropriate high school name
- `school_type`, `feeder_engagement`, `socal_expansion`: Empty fields (matches original)

## Installation

No external dependencies required! This script uses only Python standard library modules.

```bash
# Clone or download the script
# Ensure you have Python 3.7+ installed
python --version
```

## Usage

### Basic Usage
```bash
python fake_prospect_data_generator.py
```

This will generate 150 records and save them to `fake_prospect_data.csv`.

### Custom Usage
```python
from fake_prospect_data_generator import ProspectDataGenerator

# Initialize generator
generator = ProspectDataGenerator()

# Generate custom number of records
records = generator.generate_dataset(500)

# Save to custom filename
generator.save_to_csv(records, 'my_custom_data.csv')
```

## Example Output

```csv
id,prospect_id,applicant,full_name,first_name,last_name,birthdate,email_address,inquiry_source,date_first_prospect,prospect_academic_term,date_first_inquire,inquiry_academic_term,prospect_source,hs_name,school_type,feeder_engagement,socal_expansion
,3977661,,Jason Rhodes,Jason,Rhodes,8/27/08,jason.rhodes@email.com,high school visit,8/16/24,202540,10/20/24,202540,college board,San Jose High School,,,
,3701212,3701212,Pranav Kumar,Pranav,Kumar,2/13/06,pranav.kumar@email.com,college board,5/14/24,202540,5/17/24,202540,college board,Delhi Public School R.K. Puram,,,
```

## Key Logic Implemented

### 1. **Name-School Consistency**
- Indian names → Delhi Public School
- Chinese names → Beijing No. 4 High School
- Japanese names → Tokyo Metropolitan Kokusai High School
- etc.

### 2. **Source Relationship Logic**
- `college board` inquiry → likely `college board`, `email`, or `campus visit` prospect
- `high school visit` inquiry → likely `college board`, `campus visit`, or `college fair` prospect
- `social media` inquiry → likely `social media`, `college board`, or `email` prospect

### 3. **Date Logic**
- Academic terms: 202440 (Fall 2024), 202540 (Spring 2025)
- Inquiry dates can be before or after prospect dates but within reasonable range
- All dates fall within appropriate academic term periods

### 4. **Email Consistency**
- Always follows pattern: `firstname.lastname@email.com`
- Matches the actual first and last names

### 5. **Birthdate Logic**
- Only generates birthdates for 2006-2008 (appropriate for high school students)
- Format: MM/DD/YY

## Why This Approach is Better

### ❌ **Common AI Fake Data Problems**
- Names don't match school locations
- Dates are illogical or impossible
- Email addresses don't match names
- No relationship between inquiry and prospect sources
- Birthdates inappropriate for context

### ✅ **This Generator's Solutions**
- Cultural and geographic consistency
- Logical date relationships
- Proper email formatting
- Realistic source progression
- Age-appropriate birthdates

## Customization

You can easily modify the generator by:

1. **Adding new cultures**: Extend the `first_names`, `last_names`, and `high_schools` dictionaries
2. **Changing probabilities**: Modify the applicant probability (currently 30%)
3. **Adjusting date ranges**: Modify the `date_ranges` dictionary
4. **Adding new sources**: Extend the `inquiry_sources` and `prospect_sources` lists

## License

This script is provided as-is for educational and development purposes.

## Contributing

Feel free to enhance the generator by:
- Adding more cultural backgrounds
- Improving the logic for source relationships
- Adding more realistic high school names
- Implementing additional data validation rules 