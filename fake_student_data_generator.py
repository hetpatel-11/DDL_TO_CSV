#!/usr/bin/env python3
"""
Fake Student Data Generator
Generates logical fake data for student registration tracking system
Maintains data relationships and consistency with admission data
"""

import csv
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class StudentDataGenerator:
    def __init__(self):
        # Academic periods
        self.academic_periods = ['202440', '202540']
        
        # Registration date ranges for different academic periods
        self.registration_date_ranges = {
            '202440': (datetime(2025, 1, 15), datetime(2025, 2, 28)),  # Spring 2025 registration
            '202540': (datetime(2025, 2, 1), datetime(2025, 4, 30))    # Fall 2025 registration
        }
        
        # Used applicant IDs to avoid duplicates
        self.used_applicant_ids = set()
        
        # Load admission data to maintain relationships
        self.admission_applicants = set()
        self.load_admission_data()
    
    def load_admission_data(self):
        """Load admission data to get valid applicant IDs"""
        try:
            with open('fake_admission_data.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.admission_applicants.add(row['applicant'])
        except FileNotFoundError:
            # If admission data doesn't exist, generate some sample applicant IDs
            print("Warning: fake_admission_data.csv not found. Generating sample applicant IDs.")
            for _ in range(20):
                self.admission_applicants.add(str(random.randint(3000000, 3999999)))
    
    def generate_applicant_id(self) -> str:
        """Generate applicant ID from admission data or create new one"""
        if self.admission_applicants:
            # Use existing applicant ID from admission data
            applicant_id = random.choice(list(self.admission_applicants))
            self.admission_applicants.remove(applicant_id)  # Remove to avoid duplicates
            return applicant_id
        else:
            # Generate new applicant ID if no admission data available
            while True:
                applicant_id = str(random.randint(3000000, 3999999))
                if applicant_id not in self.used_applicant_ids:
                    self.used_applicant_ids.add(applicant_id)
                    return applicant_id
    
    def generate_academic_period(self) -> str:
        """Generate academic period"""
        return random.choice(self.academic_periods)
    
    def generate_registration_info(self, academic_period: str) -> Tuple[str, str]:
        """Generate registration date and status"""
        # 70% chance of being registered
        registered = random.random() < 0.7
        
        if registered:
            # Generate registration date within appropriate range
            date_range = self.registration_date_ranges[academic_period]
            registration_date = date_range[0] + timedelta(days=random.randint(0, (date_range[1] - date_range[0]).days))
            date_str = registration_date.strftime("%-m/%-d/%y")
        else:
            # Not registered - no date
            date_str = ""
        
        return date_str, "TRUE" if registered else "FALSE"
    
    def generate_single_record(self) -> Dict[str, str]:
        """Generate a single student record"""
        applicant_id = self.generate_applicant_id()
        academic_period = self.generate_academic_period()
        registration_date, registered = self.generate_registration_info(academic_period)
        
        return {
            'id': '',
            'applicant': applicant_id,
            'academicPeriod': academic_period,
            'date_registered': registration_date,
            'registered': registered
        }
    
    def generate_dataset(self, num_records: int = 14) -> List[Dict[str, str]]:
        """Generate complete student dataset"""
        records = []
        for _ in range(num_records):
            records.append(self.generate_single_record())
        return records
    
    def save_to_csv(self, records: List[Dict[str, str]], filename: str = 'fake_student_data.csv'):
        """Save records to CSV file"""
        if not records:
            return
        
        fieldnames = records[0].keys()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
        
        print(f"Generated {len(records)} student records and saved to {filename}")

def main():
    """Main function to generate fake student data"""
    print("Generating fake student data...")
    
    # Initialize generator
    generator = StudentDataGenerator()
    
    # Generate dataset
    records = generator.generate_dataset(14)
    
    # Save to CSV
    generator.save_to_csv(records, 'fake_student_data.csv')
    
    # Print sample records
    print("\nSample student records:")
    for i, record in enumerate(records[:5]):
        print(f"\nRecord {i+1}:")
        for key, value in record.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    main() 