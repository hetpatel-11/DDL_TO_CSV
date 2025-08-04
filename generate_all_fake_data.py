#!/usr/bin/env python3
"""
Master Fake Data Generator
Generates all three datasets in sequence to maintain logical relationships:
1. Prospect Data (base dataset)
2. Admission Data (uses prospect applicant IDs)
3. Student Data (uses admission applicant IDs)
"""

import subprocess
import sys
import os

def run_generator(script_name, description):
    """Run a specific generator script"""
    print(f"\n{'='*60}")
    print(f"Generating {description}...")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def main():
    """Generate all fake datasets in sequence"""
    print("🎯 Master Fake Data Generator")
    print("Generating all three datasets with logical relationships...")
    
    # Step 1: Generate Prospect Data
    if not run_generator('fake_prospect_data_generator.py', 'Prospect Data'):
        print("❌ Failed to generate prospect data. Exiting.")
        return
    
    # Step 2: Generate Admission Data
    if not run_generator('fake_admission_data_generator.py', 'Admission Data'):
        print("❌ Failed to generate admission data. Exiting.")
        return
    
    # Step 3: Generate Student Data
    if not run_generator('fake_student_data_generator.py', 'Student Data'):
        print("❌ Failed to generate student data. Exiting.")
        return
    
    # Step 4: Validate all data
    print(f"\n{'='*60}")
    print("Validating all generated data...")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, 'validate_all_data.py'], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error during validation:")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
    
    # Step 5: Show file summary
    print(f"\n{'='*60}")
    print("Generated Files Summary")
    print(f"{'='*60}")
    
    files_to_check = [
        'fake_prospect_data.csv',
        'fake_admission_data.csv', 
        'fake_student_data.csv'
    ]
    
    total_records = 0
    for filename in files_to_check:
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    record_count = len(lines) - 1  # Subtract header
                    file_size = os.path.getsize(filename)
                    print(f"✅ {filename}: {record_count} records ({file_size:,} bytes)")
                    total_records += record_count
            except Exception as e:
                print(f"❌ {filename}: Error reading file - {e}")
        else:
            print(f"❌ {filename}: File not found")
    
    print(f"\n📊 Total Records Generated: {total_records:,}")
    print(f"🎉 All datasets generated successfully!")
    
    print(f"\n📁 Files created:")
    print(f"  • fake_prospect_data.csv - College prospect information")
    print(f"  • fake_admission_data.csv - College admission applications")
    print(f"  • fake_student_data.csv - Student registration data")
    print(f"  • validate_all_data.py - Comprehensive validation script")
    
    print(f"\n🔍 To validate the data, run:")
    print(f"  python3 validate_all_data.py")

if __name__ == "__main__":
    main() 