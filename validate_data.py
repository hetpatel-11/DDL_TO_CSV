#!/usr/bin/env python3
"""
Data Validation Script
Validates the logical consistency of generated fake prospect data
"""

import csv
from collections import defaultdict
import re

def validate_csv_data(filename):
    """Validate the generated CSV data for logical consistency"""
    print(f"Validating {filename}...")
    print("=" * 50)
    
    records = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        records = list(reader)
    
    print(f"Total records: {len(records)}")
    print()
    
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
    
    for i, record in enumerate(records):
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
        
        # Simple date comparison (MM/DD/YY format)
        if prospect_date and inquiry_date:
            prospect_parts = prospect_date.split('/')
            inquiry_parts = inquiry_date.split('/')
            
            if len(prospect_parts) == 3 and len(inquiry_parts) == 3:
                # Convert to comparable format
                prospect_num = int(prospect_parts[2]) * 10000 + int(prospect_parts[0]) * 100 + int(prospect_parts[1])
                inquiry_num = int(inquiry_parts[2]) * 10000 + int(inquiry_parts[0]) * 100 + int(inquiry_parts[1])
                
                # Allow inquiry to be within 90 days of prospect date (more realistic)
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
            if year_part in ['06', '07', '08']:  # 2006-2008
                validation_results['birthdate_logic'] += 1
        
        # 7. Academic term logic check
        prospect_term = record['prospect_academic_term']
        inquiry_term = record['inquiry_academic_term']
        
        if prospect_term in ['202440', '202540'] and inquiry_term in ['202440', '202540']:
            validation_results['academic_term_logic'] += 1
    
    # Print validation results
    print("Validation Results:")
    print("-" * 30)
    
    for check, count in validation_results.items():
        percentage = (count / len(records)) * 100
        print(f"{check.replace('_', ' ').title()}: {count}/{len(records)} ({percentage:.1f}%)")
    
    print()
    
    # Overall assessment
    total_checks = len(validation_results)
    passed_checks = sum(1 for count in validation_results.values() if count == len(records))
    
    print(f"Overall Assessment:")
    print(f"Passed {passed_checks}/{total_checks} validation checks")
    
    if passed_checks == total_checks:
        print("✅ All validations passed! Data is logically consistent.")
    else:
        print("⚠️  Some validations failed. Check the data for inconsistencies.")
    
    return validation_results

def analyze_data_patterns(filename):
    """Analyze patterns in the generated data"""
    print(f"\nAnalyzing patterns in {filename}...")
    print("=" * 50)
    
    records = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        records = list(reader)
    
    # Analyze various patterns
    inquiry_sources = defaultdict(int)
    prospect_sources = defaultdict(int)
    academic_terms = defaultdict(int)
    schools = defaultdict(int)
    applicant_count = 0
    
    for record in records:
        inquiry_sources[record['inquiry_source']] += 1
        prospect_sources[record['prospect_source']] += 1
        academic_terms[record['prospect_academic_term']] += 1
        schools[record['hs_name']] += 1
        
        if record['applicant']:
            applicant_count += 1
    
    print(f"Applicant Rate: {applicant_count}/{len(records)} ({applicant_count/len(records)*100:.1f}%)")
    print()
    
    print("Inquiry Sources Distribution:")
    for source, count in sorted(inquiry_sources.items()):
        print(f"  {source}: {count} ({count/len(records)*100:.1f}%)")
    print()
    
    print("Prospect Sources Distribution:")
    for source, count in sorted(prospect_sources.items()):
        print(f"  {source}: {count} ({count/len(records)*100:.1f}%)")
    print()
    
    print("Academic Terms Distribution:")
    for term, count in sorted(academic_terms.items()):
        print(f"  {term}: {count} ({count/len(records)*100:.1f}%)")
    print()
    
    print("Top 10 Schools:")
    for school, count in sorted(schools.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {school}: {count}")

if __name__ == "__main__":
    validate_csv_data('fake_prospect_data.csv')
    analyze_data_patterns('fake_prospect_data.csv') 