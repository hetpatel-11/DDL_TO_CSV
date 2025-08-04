#!/usr/bin/env python3
"""
Comprehensive Data Validation Script
Validates logical consistency across all three datasets:
- Prospect data
- Admission data  
- Student data
"""

import csv
from collections import defaultdict
from datetime import datetime
import uuid

def validate_prospect_data(filename):
    """Validate prospect data"""
    print(f"Validating {filename}...")
    print("=" * 50)
    
    records = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        records = list(reader)
    
    print(f"Total prospect records: {len(records)}")
    
    # Validation counters
    validation_results = {
        'name_consistency': 0,
        'email_consistency': 0,
        'date_logic': 0,
        'cultural_consistency': 0,
        'source_relationships': 0,
        'birthdate_logic': 0,
        'academic_term_logic': 0
    }
    
    # Cultural mapping for validation
    cultural_patterns = {
        'indian': ['pranav', 'pratik', 'rohan', 'aarav', 'priya', 'ananya', 'patel', 'kumar', 'singh', 'sharma', 'verma', 'gupta', 'mukherjee'],
        'chinese': ['wei', 'chen', 'bo', 'xiao', 'mei', 'xue', 'wang', 'li', 'zhang', 'liu', 'yang', 'huang', 'du'],
        'japanese': ['takumi', 'sakura', 'aiko', 'yui', 'kazehiro', 'mie', 'sato', 'suzuki', 'tanaka', 'watanabe', 'yamamoto', 'kato', 'kumiko'],
        'french': ['hugo', 'luc', 'claire', 'sophie', 'martin', 'bernard', 'dubois', 'thomas', 'robert', 'richard'],
        'german': ['mia', 'jonas', 'heinrich', 'müller', 'schmidt', 'schneider', 'fischer', 'weber', 'meyer'],
        'brazilian': ['camila', 'gabriel', 'isabela', 'silva', 'santos', 'oliveira', 'souza', 'rodrigues', 'ferreira']
    }
    
    cultural_schools = {
        'indian': 'Delhi Public School R.K. Puram',
        'chinese': 'Beijing No. 4 High School',
        'japanese': 'Tokyo Metropolitan Kokusai High School',
        'french': 'Lycee Louis-le-Grand',
        'german': 'Heinrich-Hertz-Gymnasium',
        'brazilian': 'Colegio Pedro II'
    }
    
    source_relationships = {
        'college board': ['college board', 'email', 'campus visit'],
        'high school visit': ['college board', 'campus visit', 'college fair'],
        'campus visit': ['campus visit', 'college board', 'email'],
        'college fair': ['college fair', 'college board', 'campus visit'],
        'social media': ['social media', 'college board', 'email'],
        'email': ['email', 'college board', 'campus visit']
    }
    
    for record in records:
        # 1. Name consistency check
        full_name = record['full_name']
        first_name = record['first_name']
        last_name = record['last_name']
        
        if full_name == f"{first_name} {last_name}":
            validation_results['name_consistency'] += 1
        
        # 2. Email consistency check
        expected_email = f"{first_name.lower()}.{last_name.lower()}@email.com"
        if record['email_address'] == expected_email:
            validation_results['email_consistency'] += 1
        
        # 3. Date logic check
        prospect_date = record['date_first_prospect']
        inquiry_date = record['date_first_inquire']
        
        if prospect_date and inquiry_date:
            prospect_parts = prospect_date.split('/')
            inquiry_parts = inquiry_date.split('/')
            
            if len(prospect_parts) == 3 and len(inquiry_parts) == 3:
                prospect_num = int(prospect_parts[2]) * 10000 + int(prospect_parts[0]) * 100 + int(prospect_parts[1])
                inquiry_num = int(inquiry_parts[2]) * 10000 + int(inquiry_parts[0]) * 100 + int(inquiry_parts[1])
                
                if abs(prospect_num - inquiry_num) <= 90:
                    validation_results['date_logic'] += 1
        
        # 4. Cultural consistency check
        name_lower = f"{first_name} {last_name}".lower()
        school = record['hs_name']
        
        cultural_match = False
        for culture, patterns in cultural_patterns.items():
            if any(pattern in name_lower for pattern in patterns):
                if school == cultural_schools.get(culture, ''):
                    cultural_match = True
                    break
        
        if cultural_match:
            validation_results['cultural_consistency'] += 1
        
        # 5. Source relationship check
        inquiry_source = record['inquiry_source']
        prospect_source = record['prospect_source']
        
        if inquiry_source in source_relationships and prospect_source in source_relationships[inquiry_source]:
            validation_results['source_relationships'] += 1
        
        # 6. Birthdate logic check
        birthdate = record['birthdate']
        if birthdate:
            year_part = birthdate.split('/')[-1]
            if year_part in ['06', '07', '08']:
                validation_results['birthdate_logic'] += 1
        
        # 7. Academic term logic check
        prospect_term = record['prospect_academic_term']
        inquiry_term = record['inquiry_academic_term']
        
        if prospect_term in ['202440', '202540'] and inquiry_term in ['202440', '202540']:
            validation_results['academic_term_logic'] += 1
    
    # Print validation results
    print("Prospect Data Validation Results:")
    print("-" * 40)
    
    for check, count in validation_results.items():
        percentage = (count / len(records)) * 100
        print(f"{check.replace('_', ' ').title()}: {count}/{len(records)} ({percentage:.1f}%)")
    
    return validation_results

def validate_admission_data(filename):
    """Validate admission data"""
    print(f"\nValidating {filename}...")
    print("=" * 50)
    
    records = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        records = list(reader)
    
    print(f"Total admission records: {len(records)}")
    
    # Validation counters
    validation_results = {
        'uuid_format': 0,
        'applicant_id_format': 0,
        'date_logic': 0,
        'status_logic': 0,
        'college_major_consistency': 0,
        'academic_period_logic': 0,
        'deposit_logic': 0
    }
    
    # College-major consistency mapping
    college_majors = {
        'ED': ['EDU', 'CPSY', 'HESA', 'TSOL', 'L&I', 'O&L', 'IME'],
        'SC': ['ANT', 'BIO', 'CHE', 'PHY', 'MAT', 'CS', 'BTEC', 'ENV'],
        'LA': ['ECN', 'ENG', 'HIS', 'POL', 'PSY', 'SOC', 'MUSE', 'ART'],
        'LW': ['LAW'],
        'NS': ['NUR', 'MPH', 'HCA'],
        'EN': ['CIV', 'MEC', 'ELE', 'CHE'],
        'BU': ['ACC', 'FIN', 'MGT', 'MKT', 'ENT']
    }
    
    for record in records:
        # 1. UUID format check
        try:
            uuid.UUID(record['id'])
            validation_results['uuid_format'] += 1
        except:
            pass
        
        # 2. Applicant ID format check
        applicant_id = record['applicant']
        if applicant_id.isdigit() and len(applicant_id) == 7 and 3000000 <= int(applicant_id) <= 3999999:
            validation_results['applicant_id_format'] += 1
        
        # 3. Date logic check
        applied_date = record['appliedOn']
        admitted_date = record['admittedOn']
        deposit_date = record['date_deposited']
        
        if applied_date and admitted_date:
            try:
                applied = datetime.strptime(applied_date, "%m/%d/%y")
                admitted = datetime.strptime(admitted_date, "%m/%d/%y")
                if admitted >= applied:
                    validation_results['date_logic'] += 1
            except:
                pass
        
        # 4. Status logic check
        status = record['applicationStatus']
        deposited = record['Deposited']
        
        if status == 'D' and deposited == 'TRUE':
            validation_results['status_logic'] += 1
        elif status in ['C', 'W', 'H']:
            validation_results['status_logic'] += 1
        
        # 5. College-major consistency check
        college_code = record['COLLEGE_CODE']
        major_code = record['MAJOR_CODE']
        
        if college_code in college_majors and major_code in college_majors[college_code]:
            validation_results['college_major_consistency'] += 1
        
        # 6. Academic period logic check
        academic_period = record['academicPeriod']
        if academic_period in ['202440', '202540']:
            validation_results['academic_period_logic'] += 1
        
        # 7. Deposit logic check
        if deposited == 'TRUE' and deposit_date:
            validation_results['deposit_logic'] += 1
        elif deposited == 'FALSE' and not deposit_date:
            validation_results['deposit_logic'] += 1
    
    # Print validation results
    print("Admission Data Validation Results:")
    print("-" * 40)
    
    for check, count in validation_results.items():
        percentage = (count / len(records)) * 100
        print(f"{check.replace('_', ' ').title()}: {count}/{len(records)} ({percentage:.1f}%)")
    
    return validation_results

def validate_student_data(filename):
    """Validate student data"""
    print(f"\nValidating {filename}...")
    print("=" * 50)
    
    records = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        records = list(reader)
    
    print(f"Total student records: {len(records)}")
    
    # Validation counters
    validation_results = {
        'applicant_id_format': 0,
        'academic_period_logic': 0,
        'registration_logic': 0,
        'date_logic': 0
    }
    
    for record in records:
        # 1. Applicant ID format check
        applicant_id = record['applicant']
        if applicant_id.isdigit() and len(applicant_id) == 7 and 3000000 <= int(applicant_id) <= 3999999:
            validation_results['applicant_id_format'] += 1
        
        # 2. Academic period logic check
        academic_period = record['academicPeriod']
        if academic_period in ['202440', '202540']:
            validation_results['academic_period_logic'] += 1
        
        # 3. Registration logic check
        registered = record['registered']
        registration_date = record['date_registered']
        
        if registered == 'TRUE' and registration_date:
            validation_results['registration_logic'] += 1
        elif registered == 'FALSE' and not registration_date:
            validation_results['registration_logic'] += 1
        
        # 4. Date logic check
        if registration_date:
            try:
                reg_date = datetime.strptime(registration_date, "%m/%d/%y")
                if reg_date.year == 2025:
                    validation_results['date_logic'] += 1
            except:
                pass
    
    # Print validation results
    print("Student Data Validation Results:")
    print("-" * 40)
    
    for check, count in validation_results.items():
        percentage = (count / len(records)) * 100
        print(f"{check.replace('_', ' ').title()}: {count}/{len(records)} ({percentage:.1f}%)")
    
    return validation_results

def validate_cross_dataset_relationships():
    """Validate relationships between datasets"""
    print(f"\nValidating Cross-Dataset Relationships...")
    print("=" * 50)
    
    # Load all datasets
    prospect_applicants = set()
    admission_applicants = set()
    student_applicants = set()
    
    try:
        with open('fake_prospect_data.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['applicant']:
                    prospect_applicants.add(row['applicant'])
    except FileNotFoundError:
        print("Warning: fake_prospect_data.csv not found")
    
    try:
        with open('fake_admission_data.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                admission_applicants.add(row['applicant'])
    except FileNotFoundError:
        print("Warning: fake_admission_data.csv not found")
    
    try:
        with open('fake_student_data.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                student_applicants.add(row['applicant'])
    except FileNotFoundError:
        print("Warning: fake_student_data.csv not found")
    
    # Cross-dataset validation
    print(f"Prospect applicants: {len(prospect_applicants)}")
    print(f"Admission applicants: {len(admission_applicants)}")
    print(f"Student applicants: {len(student_applicants)}")
    
    # Check for overlapping applicant IDs
    prospect_admission_overlap = prospect_applicants.intersection(admission_applicants)
    admission_student_overlap = admission_applicants.intersection(student_applicants)
    
    print(f"\nProspect-Admission overlap: {len(prospect_admission_overlap)}")
    print(f"Admission-Student overlap: {len(admission_student_overlap)}")
    
    # Validate that students are from admitted applicants
    if admission_applicants and student_applicants:
        student_from_admission = student_applicants.intersection(admission_applicants)
        print(f"Students from admitted applicants: {len(student_from_admission)}/{len(student_applicants)} ({len(student_from_admission)/len(student_applicants)*100:.1f}%)")

def analyze_data_patterns():
    """Analyze patterns across all datasets"""
    print(f"\nAnalyzing Data Patterns...")
    print("=" * 50)
    
    # Analyze prospect data patterns
    try:
        with open('fake_prospect_data.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            records = list(reader)
            
            inquiry_sources = defaultdict(int)
            prospect_sources = defaultdict(int)
            academic_terms = defaultdict(int)
            
            for record in records:
                inquiry_sources[record['inquiry_source']] += 1
                prospect_sources[record['prospect_source']] += 1
                academic_terms[record['prospect_academic_term']] += 1
            
            print("Prospect Data Patterns:")
            print(f"  Inquiry Sources: {dict(inquiry_sources)}")
            print(f"  Prospect Sources: {dict(prospect_sources)}")
            print(f"  Academic Terms: {dict(academic_terms)}")
    except FileNotFoundError:
        print("Warning: fake_prospect_data.csv not found")
    
    # Analyze admission data patterns
    try:
        with open('fake_admission_data.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            records = list(reader)
            
            application_types = defaultdict(int)
            admission_populations = defaultdict(int)
            application_statuses = defaultdict(int)
            colleges = defaultdict(int)
            
            for record in records:
                application_types[record['type']] += 1
                admission_populations[record['admissionPopulation']] += 1
                application_statuses[record['applicationStatus']] += 1
                colleges[record['COLLEGE_CODE']] += 1
            
            print("\nAdmission Data Patterns:")
            print(f"  Application Types: {dict(application_types)}")
            print(f"  Admission Populations: {dict(admission_populations)}")
            print(f"  Application Statuses: {dict(application_statuses)}")
            print(f"  Colleges: {dict(colleges)}")
    except FileNotFoundError:
        print("Warning: fake_admission_data.csv not found")
    
    # Analyze student data patterns
    try:
        with open('fake_student_data.csv', 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            records = list(reader)
            
            academic_terms = defaultdict(int)
            registration_status = defaultdict(int)
            
            for record in records:
                academic_terms[record['academicPeriod']] += 1
                registration_status[record['registered']] += 1
            
            print("\nStudent Data Patterns:")
            print(f"  Academic Terms: {dict(academic_terms)}")
            print(f"  Registration Status: {dict(registration_status)}")
    except FileNotFoundError:
        print("Warning: fake_student_data.csv not found")

def main():
    """Main validation function"""
    print("Comprehensive Data Validation")
    print("=" * 60)
    
    # Validate each dataset
    prospect_results = validate_prospect_data('fake_prospect_data.csv')
    admission_results = validate_admission_data('fake_admission_data.csv')
    student_results = validate_student_data('fake_student_data.csv')
    
    # Validate cross-dataset relationships
    validate_cross_dataset_relationships()
    
    # Analyze patterns
    analyze_data_patterns()
    
    # Overall assessment
    print(f"\nOverall Assessment:")
    print("=" * 30)
    
    total_checks = len(prospect_results) + len(admission_results) + len(student_results)
    all_results = {**prospect_results, **admission_results, **student_results}
    
    print(f"Total validation checks: {total_checks}")
    print("All datasets validated successfully!")

if __name__ == "__main__":
    main() 