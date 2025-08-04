#!/usr/bin/env python3
"""
Fake Prospect Data Generator
Generates logical fake data for college prospect tracking system
Maintains data relationships and consistency like the original dataset
"""

import csv
import random
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import re

class ProspectDataGenerator:
    def __init__(self):
        # Initialize comprehensive name databases with geographic consistency
        self.first_names = {
            'american': [
                'James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Christopher',
                'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen',
                'Daniel', 'Matthew', 'Anthony', 'Mark', 'Donald', 'Steven', 'Paul', 'Andrew', 'Joshua', 'Kenneth',
                'Nancy', 'Betty', 'Helen', 'Sandra', 'Donna', 'Carol', 'Ruth', 'Sharon', 'Michelle', 'Laura',
                'Kevin', 'Brian', 'George', 'Edward', 'Ronald', 'Timothy', 'Jason', 'Jeffrey', 'Ryan', 'Jacob',
                'Emily', 'Emma', 'Madison', 'Olivia', 'Hannah', 'Abigail', 'Isabella', 'Samantha', 'Elizabeth', 'Ashley'
            ],
            'indian': [
                'Aarav', 'Arjun', 'Vivaan', 'Aditya', 'Vihaan', 'Arnav', 'Vedant', 'Dhruv', 'Kabir', 'Arush',
                'Aisha', 'Zara', 'Ananya', 'Pari', 'Myra', 'Aaradhya', 'Anvi', 'Diya', 'Pihu', 'Riya',
                'Rohan', 'Pranav', 'Pratik', 'Aryan', 'Krishna', 'Ishaan', 'Shaurya', 'Advait', 'Arhan', 'Ved',
                'Priya', 'Anjali', 'Kavya', 'Saanvi', 'Aaradhya', 'Ishita', 'Avni', 'Kyra', 'Mira', 'Tara'
            ],
            'chinese': [
                'Wei', 'Chen', 'Bo', 'Xiao', 'Li', 'Wang', 'Zhang', 'Liu', 'Yang', 'Huang',
                'Mei', 'Xue', 'Jie', 'Ying', 'Hui', 'Fang', 'Ling', 'Xia', 'Yan', 'Min',
                'Jian', 'Ming', 'Feng', 'Tao', 'Bin', 'Lei', 'Gang', 'Hao', 'Jun', 'Peng',
                'Xia', 'Yu', 'Hong', 'Jing', 'Qing', 'Yan', 'Xia', 'Hui', 'Fang', 'Ling'
            ],
            'japanese': [
                'Takumi', 'Hiroto', 'Yuto', 'Haruto', 'Sota', 'Yuki', 'Kento', 'Riku', 'Yamato', 'Kazuki',
                'Sakura', 'Yui', 'Aiko', 'Mia', 'Hana', 'Rin', 'Aki', 'Mie', 'Kazehiro', 'Yuki',
                'Kenji', 'Taro', 'Jiro', 'Saburo', 'Ichiro', 'Goro', 'Rokuro', 'Shichiro', 'Hachiro', 'Kuro',
                'Akiko', 'Yoko', 'Keiko', 'Michiko', 'Noriko', 'Tomoko', 'Yumiko', 'Kumiko', 'Ayako', 'Eiko'
            ],
            'korean': [
                'Min-jun', 'Seo-jun', 'Do-yoon', 'Si-woo', 'Jun-seo', 'Dong-hyun', 'Ji-hun', 'Min-seok', 'Ye-jun', 'Joon-ho',
                'Min-seo', 'Ji-woo', 'Seo-yeon', 'Ye-eun', 'Ji-min', 'Hae-in', 'Da-eun', 'Soo-jin', 'Ji-yeon', 'Ye-rin',
                'Jin-woo', 'Hyun-woo', 'Min-woo', 'Jun-woo', 'Seung-woo', 'Dong-woo', 'Ji-woo', 'Min-woo', 'Ye-woo', 'Joon-woo',
                'Ji-eun', 'Ye-eun', 'Min-eun', 'Seo-eun', 'Hae-eun', 'Da-eun', 'Soo-eun', 'Ji-eun', 'Ye-eun', 'Joon-eun'
            ],
            'french': [
                'Lucas', 'Hugo', 'Louis', 'Jules', 'Léo', 'Gabriel', 'Arthur', 'Raphaël', 'Paul', 'Antoine',
                'Emma', 'Léa', 'Chloé', 'Jade', 'Alice', 'Lola', 'Manon', 'Camille', 'Inès', 'Sarah',
                'Pierre', 'Jean', 'François', 'Michel', 'Philippe', 'Nicolas', 'David', 'Thomas', 'Laurent', 'Sébastien',
                'Marie', 'Sophie', 'Isabelle', 'Catherine', 'Nathalie', 'Valérie', 'Sandrine', 'Céline', 'Audrey', 'Caroline'
            ],
            'german': [
                'Lukas', 'Felix', 'Maximilian', 'Leon', 'Paul', 'Jonas', 'Julian', 'Niklas', 'Jan', 'Tim',
                'Emma', 'Hannah', 'Lea', 'Anna', 'Leonie', 'Lena', 'Sarah', 'Laura', 'Mia', 'Sophie',
                'Alexander', 'Michael', 'Andreas', 'Christian', 'Stefan', 'Martin', 'Thomas', 'Klaus', 'Wolfgang', 'Hans',
                'Maria', 'Petra', 'Sabine', 'Monika', 'Angela', 'Ursula', 'Gisela', 'Renate', 'Brigitte', 'Helga'
            ],
            'british': [
                'Oliver', 'Harry', 'Jack', 'Charlie', 'Thomas', 'Jacob', 'Alfie', 'Riley', 'William', 'James',
                'Olivia', 'Amelia', 'Isla', 'Ava', 'Emily', 'Sophia', 'Grace', 'Lily', 'Evie', 'Chloe',
                'George', 'Noah', 'Oscar', 'Arthur', 'Muhammad', 'Leo', 'Henry', 'Ethan', 'Lucas', 'Mason',
                'Sophie', 'Isabella', 'Grace', 'Lily', 'Evie', 'Chloe', 'Poppy', 'Daisy', 'Freya', 'Phoebe'
            ],
            'australian': [
                'Liam', 'Noah', 'Oliver', 'William', 'Jack', 'Lucas', 'Mason', 'Logan', 'Alexander', 'Ethan',
                'Charlotte', 'Olivia', 'Ava', 'Mia', 'Amelia', 'Harper', 'Evelyn', 'Abigail', 'Emily', 'Elizabeth',
                'James', 'Benjamin', 'Sebastian', 'Michael', 'Elijah', 'Daniel', 'Henry', 'Matthew', 'Jackson', 'Samuel',
                'Sofia', 'Avery', 'Ella', 'Madison', 'Scarlett', 'Victoria', 'Aria', 'Grace', 'Chloe', 'Camila'
            ],
            'brazilian': [
                'João', 'Pedro', 'Gabriel', 'Lucas', 'Matheus', 'Rafael', 'Daniel', 'Bruno', 'Carlos', 'Eduardo',
                'Maria', 'Ana', 'Julia', 'Beatriz', 'Carolina', 'Amanda', 'Mariana', 'Fernanda', 'Isabella', 'Camila',
                'Thiago', 'Felipe', 'Leonardo', 'Guilherme', 'Rodrigo', 'Marcelo', 'André', 'Ricardo', 'Diego', 'Roberto',
                'Patrícia', 'Sandra', 'Claudia', 'Cristina', 'Vanessa', 'Renata', 'Monica', 'Tatiana', 'Luciana', 'Adriana'
            ],
            'south_african': [
                'Liam', 'Ethan', 'Mason', 'Noah', 'William', 'James', 'Benjamin', 'Lucas', 'Henry', 'Alexander',
                'Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Mia', 'Charlotte', 'Amelia', 'Harper', 'Evelyn',
                'John', 'Michael', 'David', 'Robert', 'Christopher', 'Daniel', 'Matthew', 'Anthony', 'Mark', 'Donald',
                'Sarah', 'Jessica', 'Ashley', 'Emily', 'Samantha', 'Elizabeth', 'Madison', 'Nicole', 'Kayla', 'Lauren'
            ]
        }
        
        self.last_names = {
            'american': [
                'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
                'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
                'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores'
            ],
            'indian': [
                'Patel', 'Kumar', 'Singh', 'Sharma', 'Verma', 'Gupta', 'Malhotra', 'Kapoor', 'Joshi', 'Chopra',
                'Mehta', 'Reddy', 'Naik', 'Iyer', 'Menon', 'Nair', 'Pillai', 'Kaur', 'Kaur', 'Kaur',
                'Bhatt', 'Desai', 'Shah', 'Mishra', 'Tiwari', 'Yadav', 'Khan', 'Ali', 'Hussain', 'Ahmed',
                'Rao', 'Prasad', 'Saxena', 'Trivedi', 'Sinha', 'Banerjee', 'Mukherjee', 'Chatterjee', 'Das', 'Bose'
            ],
            'chinese': [
                'Wang', 'Li', 'Zhang', 'Liu', 'Chen', 'Yang', 'Huang', 'Zhao', 'Wu', 'Zhou',
                'Sun', 'Ma', 'Zhu', 'Hu', 'Guo', 'Lin', 'He', 'Gao', 'Luo', 'Zheng',
                'Liang', 'Xie', 'Tang', 'Han', 'Feng', 'Cao', 'Deng', 'Yuan', 'Jiang', 'Xia',
                'Shi', 'Cheng', 'Tian', 'Fan', 'Pan', 'Yu', 'Jin', 'Qian', 'Du', 'Bai'
            ],
            'japanese': [
                'Sato', 'Suzuki', 'Takahashi', 'Tanaka', 'Watanabe', 'Ito', 'Yamamoto', 'Nakamura', 'Kobayashi', 'Kato',
                'Yoshida', 'Yamada', 'Sasaki', 'Yamaguchi', 'Saito', 'Matsumoto', 'Inoue', 'Kimura', 'Hayashi', 'Shimizu',
                'Yamazaki', 'Mori', 'Abe', 'Ikeda', 'Hashimoto', 'Yamashita', 'Ishikawa', 'Nakajima', 'Maeda', 'Fujita',
                'Ogawa', 'Goto', 'Okada', 'Hasegawa', 'Murakami', 'Kondo', 'Ishii', 'Saito', 'Sakamoto', 'Endo'
            ],
            'korean': [
                'Kim', 'Lee', 'Park', 'Choi', 'Jung', 'Kang', 'Cho', 'Yoon', 'Jang', 'Lim',
                'Han', 'Oh', 'Shin', 'Seo', 'Kwon', 'Hwang', 'Ahn', 'Song', 'Yoo', 'Jeong',
                'Bae', 'Moon', 'Ryu', 'Kwon', 'Chung', 'Nam', 'Min', 'Hong', 'Ko', 'Yang',
                'Son', 'Baek', 'Go', 'Kwon', 'Jung', 'Choi', 'Park', 'Kim', 'Lee', 'Choi'
            ],
            'french': [
                'Martin', 'Bernard', 'Dubois', 'Thomas', 'Robert', 'Richard', 'Petit', 'Durand', 'Leroy', 'Moreau',
                'Simon', 'Michel', 'Lefebvre', 'Leroy', 'Roux', 'David', 'Bertrand', 'Roux', 'Vincent', 'Fournier',
                'Morel', 'Girard', 'Andre', 'Lefevre', 'Mercier', 'Dupont', 'Lambert', 'Bonnet', 'Francois', 'Martinez',
                'Legrand', 'Garnier', 'Faure', 'Rousseau', 'Blanc', 'Guerin', 'Muller', 'Henry', 'Roussel', 'Nicolas'
            ],
            'german': [
                'Müller', 'Schmidt', 'Schneider', 'Fischer', 'Weber', 'Meyer', 'Wagner', 'Becker', 'Schulz', 'Hoffmann',
                'Schäfer', 'Koch', 'Bauer', 'Richter', 'Klein', 'Wolf', 'Schröder', 'Neumann', 'Schwarz', 'Zimmermann',
                'Braun', 'Krüger', 'Hofmann', 'Hartmann', 'Lange', 'Schmitt', 'Werner', 'Schmitz', 'Krause', 'Meier',
                'Lehmann', 'Schmid', 'Schulze', 'Maier', 'Köhler', 'Herrmann', 'König', 'Walter', 'Mayer', 'Huber'
            ],
            'british': [
                'Smith', 'Jones', 'Williams', 'Taylor', 'Davies', 'Brown', 'Wilson', 'Evans', 'Thomas', 'Roberts',
                'Johnson', 'Lewis', 'Walker', 'Robinson', 'Wood', 'Thompson', 'White', 'Watson', 'Jackson', 'Wright',
                'Green', 'Harris', 'Cooper', 'King', 'Lee', 'Martin', 'Clarke', 'James', 'Morgan', 'Hughes',
                'Edwards', 'Hill', 'Moore', 'Clark', 'Harrison', 'Scott', 'Young', 'Morris', 'Hall', 'Lewis'
            ],
            'australian': [
                'Smith', 'Jones', 'Williams', 'Brown', 'Taylor', 'Davies', 'Wilson', 'Evans', 'Thomas', 'Roberts',
                'Johnson', 'Lewis', 'Walker', 'Robinson', 'Wood', 'Thompson', 'White', 'Watson', 'Jackson', 'Wright',
                'Green', 'Harris', 'Cooper', 'King', 'Lee', 'Martin', 'Clarke', 'James', 'Morgan', 'Hughes',
                'Edwards', 'Hill', 'Moore', 'Clark', 'Harrison', 'Scott', 'Young', 'Morris', 'Hall', 'Lewis'
            ],
            'brazilian': [
                'Silva', 'Santos', 'Oliveira', 'Souza', 'Rodrigues', 'Ferreira', 'Alves', 'Pereira', 'Lima', 'Gomes',
                'Costa', 'Ribeiro', 'Martins', 'Carvalho', 'Almeida', 'Lopes', 'Soares', 'Fernandes', 'Vieira', 'Barbosa',
                'Rocha', 'Dias', 'Nascimento', 'Cavalcanti', 'Castro', 'Cardoso', 'Melo', 'Correia', 'Cunha', 'Moreira',
                'Duarte', 'Freitas', 'Mendes', 'Araujo', 'Lima', 'Ramos', 'Reis', 'Teixeira', 'Mendes', 'Andrade'
            ],
            'south_african': [
                'Nkosi', 'Dlamini', 'Ndlovu', 'Botha', 'Molefe', 'Van der Merwe', 'Mokoena', 'Pieterse', 'Smit', 'Van Wyk',
                'Mabaso', 'Ntuli', 'Van Niekerk', 'Maseko', 'Mthembu', 'Van der Walt', 'Mkhize', 'Molewa', 'Steyn', 'Mabena',
                'Maseko', 'Mthembu', 'Van der Walt', 'Mkhize', 'Molewa', 'Steyn', 'Mabena', 'Maseko', 'Mthembu', 'Van der Walt',
                'Mkhize', 'Molewa', 'Steyn', 'Mabena', 'Maseko', 'Mthembu', 'Van der Walt', 'Mkhize', 'Molewa', 'Steyn'
            ]
        }
        
        # High schools with geographic and cultural consistency
        self.high_schools = {
            'american': [
                'San Jose High School', 'San Diego Charter High School', 'Bakersfield High School', 'Dallas Science and Engineering Magnet',
                'Galileo Academy of Science and Technology', 'Anaheim High School', 'Oakland Technical High School', 'Austin High School',
                'Lane Tech College Prep', 'Central High School', 'Stuyvesant High School', 'Fresno High School', 'Bellaire High School',
                'Paxon School for Advanced Studies', 'C.K. McClatchy High School', 'Los Angeles Center for Enriched Studies',
                'Phoenix Union Bioscience High School', 'Folsom High School', 'Rocklin High School'
            ],
            'indian': [
                'Delhi Public School R.K. Puram', 'Delhi Public School R.K. Puram', 'Delhi Public School R.K. Puram'
            ],
            'chinese': [
                'Beijing No. 4 High School', 'Beijing No. 4 High School', 'Beijing No. 4 High School'
            ],
            'japanese': [
                'Tokyo Metropolitan Kokusai High School', 'Tokyo Metropolitan Kokusai High School', 'Tokyo Metropolitan Kokusai High School'
            ],
            'french': [
                'Lycee Louis-le-Grand', 'Lycee Louis-le-Grand', 'Lycee Louis-le-Grand'
            ],
            'british': [
                'The London Oratory School', 'The London Oratory School', 'The London Oratory School'
            ],
            'german': [
                'Heinrich-Hertz-Gymnasium', 'Heinrich-Hertz-Gymnasium', 'Heinrich-Hertz-Gymnasium'
            ],
            'brazilian': [
                'Colegio Pedro II', 'Colegio Pedro II', 'Colegio Pedro II'
            ],
            'australian': [
                'Sydney Boys High School', 'Sydney Boys High School', 'Sydney Boys High School'
            ],
            'south_african': [
                'Rondebosch Boys High School', 'Rondebosch Boys High School', 'Rondebosch Boys High School'
            ]
        }
        
        # Inquiry and prospect sources with logical relationships
        self.inquiry_sources = [
            'college board', 'high school visit', 'campus visit', 'college fair', 'social media', 'email'
        ]
        
        self.prospect_sources = [
            'college board', 'campus visit', 'social media', 'email', 'college fair'
        ]
        
        # Source relationship mapping (inquiry_source -> likely prospect_source)
        self.source_relationships = {
            'college board': ['college board', 'email', 'campus visit'],
            'high school visit': ['college board', 'campus visit', 'college fair'],
            'campus visit': ['campus visit', 'college board', 'email'],
            'college fair': ['college fair', 'college board', 'campus visit'],
            'social media': ['social media', 'college board', 'email'],
            'email': ['email', 'college board', 'campus visit']
        }
        
        # Academic terms
        self.academic_terms = ['202440', '202540']  # Fall 2024, Spring 2025
        
        # Date ranges for 2024
        self.date_ranges = {
            '202440': (datetime(2024, 8, 1), datetime(2024, 12, 31)),  # Fall 2024
            '202540': (datetime(2024, 1, 1), datetime(2024, 7, 31))    # Spring 2025
        }
        
        # Birth year ranges for high school students (2006-2008)
        self.birth_years = [2006, 2007, 2008]
        
        # Used IDs to avoid duplicates
        self.used_prospect_ids = set()
        
    def generate_prospect_id(self) -> str:
        """Generate unique 7-digit prospect ID"""
        while True:
            prospect_id = str(random.randint(3000000, 3999999))
            if prospect_id not in self.used_prospect_ids:
                self.used_prospect_ids.add(prospect_id)
                return prospect_id
    
    def determine_culture_from_name(self, first_name: str, last_name: str) -> str:
        """Determine culture based on name patterns"""
        # Enhanced pattern matching for cultural identification
        name_lower = f"{first_name} {last_name}".lower()
        
        # Check for Indian names (both first and last names)
        indian_patterns = ['pranav', 'pratik', 'rohan', 'aarav', 'priya', 'ananya', 'patel', 'kumar', 'singh', 'sharma', 'verma', 'gupta']
        if any(pattern in name_lower for pattern in indian_patterns):
            return 'indian'
        
        # Check for Chinese names
        chinese_patterns = ['wei', 'chen', 'bo', 'xiao', 'mei', 'xue', 'wang', 'li', 'zhang', 'liu', 'yang', 'huang']
        if any(pattern in name_lower for pattern in chinese_patterns):
            return 'chinese'
        
        # Check for Japanese names
        japanese_patterns = ['takumi', 'sakura', 'aiko', 'yui', 'kazehiro', 'mie', 'sato', 'suzuki', 'tanaka', 'watanabe', 'yamamoto']
        if any(pattern in name_lower for pattern in japanese_patterns):
            return 'japanese'
        
        # Check for French names
        french_patterns = ['hugo', 'luc', 'claire', 'sophie', 'martin', 'bernard', 'dubois', 'thomas', 'robert', 'richard']
        if any(pattern in name_lower for pattern in french_patterns):
            return 'french'
        
        # Check for German names
        german_patterns = ['mia', 'jonas', 'heinrich', 'müller', 'schmidt', 'schneider', 'fischer', 'weber', 'meyer']
        if any(pattern in name_lower for pattern in german_patterns):
            return 'german'
        
        # Check for Brazilian names
        brazilian_patterns = ['camila', 'gabriel', 'isabela', 'silva', 'santos', 'oliveira', 'souza', 'rodrigues', 'ferreira']
        if any(pattern in name_lower for pattern in brazilian_patterns):
            return 'brazilian'
        
        # Check for British names
        british_patterns = ['william', 'james', 'emma', 'olivia', 'smith', 'jones', 'williams', 'taylor', 'davies']
        if any(pattern in name_lower for pattern in british_patterns):
            return 'british'
        
        # Check for Australian names
        australian_patterns = ['liam', 'noah', 'oliver', 'charlotte', 'ava', 'mia', 'amelia', 'harper']
        if any(pattern in name_lower for pattern in australian_patterns):
            return 'australian'
        
        # Check for South African names
        south_african_patterns = ['nkosi', 'dlamini', 'ndlovu', 'botha', 'molefe', 'van der merwe', 'mokoena']
        if any(pattern in name_lower for pattern in south_african_patterns):
            return 'south_african'
        
        # Default to American
        return 'american'
    
    def generate_name(self) -> Tuple[str, str, str]:
        """Generate culturally consistent names"""
        culture = random.choice(list(self.first_names.keys()))
        first_name = random.choice(self.first_names[culture])
        last_name = random.choice(self.last_names[culture])
        full_name = f"{first_name} {last_name}"
        return first_name, last_name, full_name
    
    def generate_birthdate(self) -> str:
        """Generate birthdate for high school student (2006-2008)"""
        year = random.choice(self.birth_years)
        month = random.randint(1, 12)
        day = random.randint(1, 28)  # Safe day range
        return f"{month}/{day}/{str(year)[-2:]}"
    
    def generate_email(self, first_name: str, last_name: str) -> str:
        """Generate email from name"""
        return f"{first_name.lower()}.{last_name.lower()}@email.com"
    
    def generate_dates(self, academic_term: str) -> Tuple[str, str]:
        """Generate logical prospect and inquiry dates"""
        start_date, end_date = self.date_ranges[academic_term]
        
        # Prospect date
        prospect_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        
        # Inquiry date (can be before or after prospect date, but within reasonable range)
        # Most inquiries happen before or around the same time as prospect creation
        days_offset = random.randint(-60, 30)  # Allow inquiry up to 60 days before or 30 days after
        inquiry_date = prospect_date + timedelta(days=days_offset)
        
        # Ensure inquiry date is within the academic term
        if inquiry_date < start_date:
            inquiry_date = start_date + timedelta(days=random.randint(0, 30))
        elif inquiry_date > end_date:
            inquiry_date = end_date - timedelta(days=random.randint(0, 30))
        
        return prospect_date.strftime("%-m/%-d/%y"), inquiry_date.strftime("%-m/%-d/%y")
    
    def generate_sources(self) -> Tuple[str, str]:
        """Generate logically related inquiry and prospect sources"""
        inquiry_source = random.choice(self.inquiry_sources)
        prospect_source = random.choice(self.source_relationships[inquiry_source])
        return inquiry_source, prospect_source
    
    def generate_high_school(self, culture: str) -> str:
        """Generate culturally appropriate high school"""
        return random.choice(self.high_schools[culture])
    
    def generate_single_record(self) -> Dict[str, str]:
        """Generate a single prospect record"""
        # Generate names
        first_name, last_name, full_name = self.generate_name()
        culture = self.determine_culture_from_name(first_name, last_name)
        
        # Generate IDs
        prospect_id = self.generate_prospect_id()
        applicant = prospect_id if random.random() < 0.3 else ""  # 30% chance to be applicant
        
        # Generate personal info
        birthdate = self.generate_birthdate()
        email = self.generate_email(first_name, last_name)
        
        # Generate academic term
        academic_term = random.choice(self.academic_terms)
        
        # Generate dates
        prospect_date, inquiry_date = self.generate_dates(academic_term)
        
        # Generate sources
        inquiry_source, prospect_source = self.generate_sources()
        
        # Generate high school
        high_school = self.generate_high_school(culture)
        
        return {
            'id': '',
            'prospect_id': prospect_id,
            'applicant': applicant,
            'full_name': full_name,
            'first_name': first_name,
            'last_name': last_name,
            'birthdate': birthdate,
            'email_address': email,
            'inquiry_source': inquiry_source,
            'date_first_prospect': prospect_date,
            'prospect_academic_term': academic_term,
            'date_first_inquire': inquiry_date,
            'inquiry_academic_term': academic_term,
            'prospect_source': prospect_source,
            'hs_name': high_school,
            'school_type': '',
            'feeder_engagement': '',
            'socal_expansion': ''
        }
    
    def generate_dataset(self, num_records: int = 150) -> List[Dict[str, str]]:
        """Generate complete dataset"""
        records = []
        for _ in range(num_records):
            records.append(self.generate_single_record())
        return records
    
    def save_to_csv(self, records: List[Dict[str, str]], filename: str = 'fake_prospect_data.csv'):
        """Save records to CSV file"""
        if not records:
            return
        
        fieldnames = records[0].keys()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
        
        print(f"Generated {len(records)} records and saved to {filename}")

def main():
    """Main function to generate fake prospect data"""
    print("Generating fake prospect data...")
    
    # Initialize generator
    generator = ProspectDataGenerator()
    
    # Generate dataset
    records = generator.generate_dataset(150)
    
    # Save to CSV
    generator.save_to_csv(records, 'fake_prospect_data.csv')
    
    # Print sample records
    print("\nSample records:")
    for i, record in enumerate(records[:5]):
        print(f"\nRecord {i+1}:")
        for key, value in record.items():
            print(f"  {key}: {value}")

if __name__ == "__main__":
    main() 