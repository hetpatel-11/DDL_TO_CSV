#!/usr/bin/env python3
"""
Fake Admission Data Generator
Generates logical fake data for college admission tracking system
Maintains data relationships and consistency with prospect data
"""

import csv
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class AdmissionDataGenerator:
    def __init__(self):
        # Application types and their descriptions
        self.application_types = {
            'Regular Decision': 'Regular Decision',
            'Early Decision I': 'Early Decision I',
            'Early Decision II': 'Early Decision II',
            'Early Action': 'Early Action'
        }
        
        # Academic periods and descriptions
        self.academic_periods = {
            '202440': 'Fall 2024',
            '202540': 'Fall 2025'
        }
        
        # Admission populations and descriptions
        self.admission_populations = {
            'D': 'Doctoral',
            'G': 'Graduate',
            'U': 'Undergraduate',
            '1': 'First-Year Law',
            'I': 'International'
        }
        
        # USF admission population descriptions
        self.usf_admission_populations = {
            'D': 'Non Resident Alien',
            'U': 'U.S Citizen',
            'I': 'International'
        }
        
        # Residency types and descriptions
        self.residency_types = {
            'F': 'Non Resident Alien',
            'U': 'U.S Citizen',
            'I': 'International'
        }
        
        # Academic loads and descriptions
        self.academic_loads = {
            'F': 'fullTime',
            'P': 'partTime'
        }
        
        # Application statuses and descriptions
        self.application_statuses = {
            'C': 'Complete ready for review',
            'D': 'Decision Made',
            'W': 'Withdrawn',
            'H': 'Hold'
        }
        
        # Levels and descriptions
        self.levels = {
            'UG': 'Undergraduate',
            'GR': 'Graduate',
            'GR-Law': 'GR-Law',
            'Law': 'Law'
        }
        
        # Colleges and their codes
        self.colleges = {
            'ED': 'School of Education',
            'SC': 'College of Arts and Sci (Sci)',
            'LA': 'College of Arts and Sci (Arts)',
            'LW': 'School of Law',
            'NS': 'School of Nursing',
            'EN': 'School of Engineering',
            'BU': 'School of Business',
            'AR': 'School of Architecture',
            'PH': 'School of Pharmacy',
            'ME': 'School of Medicine'
        }
        
        # Degrees and their codes
        self.degrees = {
            'BA': 'Bachelor of Arts',
            'BS': 'Bachelor of Science',
            'MA': 'Master of Arts',
            'MS': 'Master of Science',
            'MBA': 'Master of Business Administration',
            'MPH': 'Master of Public Health',
            'JD': 'Juris Doctor',
            'MD': 'Doctor of Medicine',
            'PhD': 'Doctor of Philosophy',
            'EDD': 'Doctor of Education',
            'PSM': 'Professional Science Master\'s'
        }
        
        # Majors and their codes (mapped to colleges)
        self.majors_by_college = {
            'ED': {
                'EDU': 'Education',
                'CPSY': 'Counseling Psychology',
                'HESA': 'Higher Ed / Student Affairs',
                'TSOL': 'Teach Engl/Speakers Other Lang',
                'L&I': 'Learning and Instruction',
                'O&L': 'Organization and Leadership',
                'IME': 'Intl and Multicultural Educ.'
            },
            'SC': {
                'ANT': 'Anthropology',
                'BIO': 'Biology',
                'CHE': 'Chemistry',
                'PHY': 'Physics',
                'MAT': 'Mathematics',
                'CS': 'Computer Science',
                'BTEC': 'Biotechnology',
                'ENV': 'Environmental Science'
            },
            'LA': {
                'ECN': 'Economics',
                'ENG': 'English',
                'HIS': 'History',
                'POL': 'Political Science',
                'PSY': 'Psychology',
                'SOC': 'Sociology',
                'MUSE': 'Museum Studies',
                'ART': 'Art History'
            },
            'LW': {
                'LAW': 'Law'
            },
            'NS': {
                'NUR': 'Nursing',
                'MPH': 'Public Health',
                'HCA': 'Health Care Administration'
            },
            'EN': {
                'CIV': 'Civil Engineering',
                'MEC': 'Mechanical Engineering',
                'ELE': 'Electrical Engineering',
                'CHE': 'Chemical Engineering'
            },
            'BU': {
                'ACC': 'Accounting',
                'FIN': 'Finance',
                'MGT': 'Management',
                'MKT': 'Marketing',
                'ENT': 'Entrepreneurship'
            }
        }
        
        # Campus codes and descriptions
        self.campuses = {
            'MAIN': 'Main Campus',
            'STP': 'St. Petersburg Campus',
            'SAR': 'Sarasota-Manatee Campus'
        }
        
        # Date ranges for different application types
        self.application_date_ranges = {
            'Early Decision I': (datetime(2024, 9, 1), datetime(2024, 11, 15)),
            'Early Decision II': (datetime(2024, 11, 16), datetime(2025, 1, 15)),
            'Early Action': (datetime(2024, 9, 1), datetime(2024, 12, 1)),
            'Regular Decision': (datetime(2024, 9, 1), datetime(2025, 2, 1))
        }
        
        # Decision date ranges (after application submission)
        self.decision_date_ranges = {
            'Early Decision I': (datetime(2024, 12, 1), datetime(2024, 12, 31)),
            'Early Decision II': (datetime(2025, 1, 15), datetime(2025, 2, 28)),
            'Early Action': (datetime(2024, 12, 15), datetime(2025, 1, 31)),
            'Regular Decision': (datetime(2025, 2, 1), datetime(2025, 4, 30))
        }
        
        # Deposit date ranges (after admission)
        self.deposit_date_ranges = {
            'Early Decision I': (datetime(2024, 12, 15), datetime(2025, 1, 15)),
            'Early Decision II': (datetime(2025, 2, 1), datetime(2025, 3, 1)),
            'Early Action': (datetime(2025, 1, 15), datetime(2025, 2, 15)),
            'Regular Decision': (datetime(2025, 4, 1), datetime(2025, 5, 1))
        }
        
        # Used applicant IDs to avoid duplicates
        self.used_applicant_ids = set()
        
    def generate_uuid(self) -> str:
        """Generate a UUID for the admission record"""
        return str(uuid.uuid4())
    
    def generate_applicant_id(self) -> str:
        """Generate unique applicant ID (7-digit number)"""
        while True:
            applicant_id = str(random.randint(3000000, 3999999))
            if applicant_id not in self.used_applicant_ids:
                self.used_applicant_ids.add(applicant_id)
                return applicant_id
    
    def generate_application_type(self) -> Tuple[str, str]:
        """Generate application type and description"""
        app_type = random.choice(list(self.application_types.keys()))
        return app_type, self.application_types[app_type]
    
    def generate_academic_period(self) -> Tuple[str, str]:
        """Generate academic period and description"""
        period = random.choice(list(self.academic_periods.keys()))
        return period, self.academic_periods[period]
    
    def generate_admission_population(self) -> Tuple[str, str]:
        """Generate admission population and description"""
        population = random.choice(list(self.admission_populations.keys()))
        return population, self.admission_populations[population]
    
    def generate_residency_type(self) -> Tuple[str, str]:
        """Generate residency type and description"""
        residency = random.choice(list(self.residency_types.keys()))
        return residency, self.residency_types[residency]
    
    def generate_academic_load(self) -> Tuple[str, str]:
        """Generate academic load and description"""
        load = random.choice(list(self.academic_loads.keys()))
        return load, self.academic_loads[load]
    
    def generate_application_status(self, app_type: str, applied_date: datetime) -> Tuple[str, str, datetime]:
        """Generate application status, description, and status date"""
        # Most applications are either complete or decision made
        if random.random() < 0.8:  # 80% chance of complete or decision made
            status = random.choice(['C', 'D'])
        else:
            status = random.choice(['W', 'H'])
        
        status_desc = self.application_statuses[status]
        
        # Status date should be after application date
        if status == 'C':
            # Complete status date is usually close to application date
            status_date = applied_date + timedelta(days=random.randint(1, 30))
        elif status == 'D':
            # Decision date follows the decision date ranges
            date_range = self.decision_date_ranges.get(app_type, 
                (applied_date + timedelta(days=30), applied_date + timedelta(days=120)))
            status_date = date_range[0] + timedelta(days=random.randint(0, (date_range[1] - date_range[0]).days))
        else:
            # Withdrawn or hold can happen anytime after application
            status_date = applied_date + timedelta(days=random.randint(10, 90))
        
        return status, status_desc, status_date
    
    def generate_level_info(self, admission_population: str) -> Tuple[str, str]:
        """Generate level and description based on admission population"""
        if admission_population == 'U':
            return 'UG', 'Undergraduate'
        elif admission_population == '1':
            return 'UG', 'Law'
        elif admission_population in ['G', 'D']:
            return 'GR', 'Graduate'
        else:
            return 'GR', 'Graduate'
    
    def generate_college_and_major(self) -> Tuple[str, str, str, str, str, str]:
        """Generate college, degree, and major information"""
        college_code = random.choice(list(self.colleges.keys()))
        college_desc = self.colleges[college_code]
        
        # Get available degrees for this college
        available_majors = self.majors_by_college.get(college_code, {})
        if not available_majors:
            # Default majors if college not in mapping
            available_majors = {'GEN': 'General Studies'}
        
        major_code = random.choice(list(available_majors.keys()))
        major_desc = available_majors[major_code]
        
        # Generate appropriate degree based on major
        if 'Law' in major_desc:
            degree_code = 'JD'
            degree_desc = 'Juris Doctor'
        elif 'Doctor' in major_desc or 'PhD' in major_desc:
            degree_code = 'EDD' if 'Education' in college_desc else 'PhD'
            degree_desc = 'Doctor of Education' if 'Education' in college_desc else 'Doctor of Philosophy'
        elif 'Master' in major_desc or 'MS' in major_code or 'MA' in major_code:
            degree_code = random.choice(['MA', 'MS', 'MPH', 'MBA'])
            degree_desc = self.degrees[degree_code]
        else:
            degree_code = random.choice(['BA', 'BS'])
            degree_desc = self.degrees[degree_code]
        
        return college_code, college_desc, degree_code, degree_desc, major_code, major_desc
    
    def generate_dates(self, app_type: str) -> Tuple[str, str, str, str]:
        """Generate application, admission, and deposit dates"""
        # Application date
        app_date_range = self.application_date_ranges[app_type]
        applied_date = app_date_range[0] + timedelta(days=random.randint(0, (app_date_range[1] - app_date_range[0]).days))
        
        # Admission date (only if status is 'D' - Decision Made)
        admitted_date = ""
        admitted_date_usf = ""
        if random.random() < 0.6:  # 60% chance of being admitted
            decision_range = self.decision_date_ranges[app_type]
            admitted_date = decision_range[0] + timedelta(days=random.randint(0, (decision_range[1] - decision_range[0]).days))
            admitted_date_usf = admitted_date.strftime("%-m/%-d/%y")
        
        # Deposit date (only if admitted and deposited)
        deposit_date = ""
        deposited = "FALSE"
        if admitted_date and random.random() < 0.7:  # 70% of admitted students deposit
            deposit_range = self.deposit_date_ranges[app_type]
            deposit_date = deposit_range[0] + timedelta(days=random.randint(0, (deposit_range[1] - deposit_range[0]).days))
            deposited = "TRUE"
        
        return (applied_date.strftime("%-m/%-d/%y"), 
                admitted_date.strftime("%-m/%-d/%y") if admitted_date else "",
                admitted_date_usf,
                deposit_date.strftime("%-m/%-d/%y") if deposit_date else "")
    
    def generate_single_record(self) -> Dict[str, str]:
        """Generate a single admission record"""
        # Generate basic information
        applicant_id = self.generate_applicant_id()
        app_type, app_type_desc = self.generate_application_type()
        academic_period, academic_period_desc = self.generate_academic_period()
        admission_pop, admission_pop_desc = self.generate_admission_population()
        residency_type, residency_type_desc = self.generate_residency_type()
        academic_load, academic_load_desc = self.generate_academic_load()
        
        # Generate dates
        applied_date, admitted_date, admitted_date_usf, deposit_date = self.generate_dates(app_type)
        
        # Generate status information
        status, status_desc, status_date = self.generate_application_status(app_type, 
            datetime.strptime(applied_date, "%m/%d/%y") if applied_date else datetime.now())
        
        # Generate level information
        level, level_desc = self.generate_level_info(admission_pop)
        
        # Generate college and major information
        college_code, college_desc, degree_code, degree_desc, major_code, major_desc = self.generate_college_and_major()
        
        # Generate campus information
        campus_code = random.choice(list(self.campuses.keys()))
        campus_desc = self.campuses[campus_code]
        
        # Determine if deposited
        deposited = "TRUE" if deposit_date else "FALSE"
        
        return {
            'id': self.generate_uuid(),
            'applicant': applicant_id,
            'type': app_type,
            'typeDescription': app_type_desc,
            'applicationNumber': '',
            'academicPeriod': academic_period,
            'academicPeriodDescription': academic_period_desc,
            'admissionPopulation': admission_pop,
            'admissionPopulationDescription': admission_pop_desc,
            'USFadmissionPopulationDescription': self.usf_admission_populations.get(admission_pop, ''),
            'residencyType': residency_type,
            'residencyTypeDescription': residency_type_desc,
            'academicLoad': academic_load,
            'academicLoadDescription': academic_load_desc,
            'appliedOn': applied_date,
            'submitted_application': '',
            'admittedOn': admitted_date,
            'admittedDateUSF': admitted_date_usf,
            'admittedUSF': '',
            'meltUSF': '',
            'applicationStatus': status,
            'applicationStatusDescription': status_desc,
            'applicationStatusDate': status_date.strftime("%-m/%-d/%y"),
            'LEVEL': level,
            'levelDescription': level_desc,
            'COLLEGE_CODE': college_code,
            'COLLEGE_DESC': college_desc,
            'USF_COLLEGE_NAME': '',
            'DEGREE_CODE': degree_code,
            'DEGREE_DESC': degree_desc,
            'MAJOR_CODE': major_code,
            'MAJOR_DESC': major_desc,
            'CAMPUS_CODE': campus_code,
            'CAMPUS_DESC': campus_desc,
            'date_deposited': deposit_date,
            'Deposited': deposited
        }
    
    def generate_dataset(self, num_records: int = 38) -> List[Dict[str, str]]:
        """Generate complete admission dataset"""
        records = []
        for _ in range(num_records):
            records.append(self.generate_single_record())
        return records
    
    def save_to_csv(self, records: List[Dict[str, str]], filename: str = 'fake_admission_data.csv'):
        """Save records to CSV file"""
        if not records:
            return
        
        fieldnames = records[0].keys()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
        
        print(f"Generated {len(records)} admission records and saved to {filename}")

def main():
    """Main function to generate fake admission data"""
    print("Generating fake admission data...")
    
    # Initialize generator
    generator = AdmissionDataGenerator()
    
    # Generate dataset
    records = generator.generate_dataset(38)
    
    # Save to CSV
    generator.save_to_csv(records, 'fake_admission_data.csv')
    
    # Print sample records
    print("\nSample admission records:")
    for i, record in enumerate(records[:5]):
        print(f"\nRecord {i+1}:")
        for key, value in record.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    main() 