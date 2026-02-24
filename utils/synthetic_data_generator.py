# utils/synthetic_data_generator.py

import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# -------------------------
# Configuration
# -------------------------
NUM_PATIENTS = 500      # total unique patients
MAX_ENCOUNTERS = 5      # max visits per patient
MAX_CLAIMS = 7          # max claims per patient

ICD10_CODES = ['E11', 'I10', 'J45', 'M54', 'K21', 'F32', 'N18', 'G47', 'E78', 'I25']  # common diagnosis
CPT_CODES = ['99213', '99214', '93000', '71020', '80053', '36415']  # sample procedures

# -------------------------
# Generate EHR Data
# -------------------------
ehr_records = []

for patient_id in range(1, NUM_PATIENTS + 1):
    num_encounters = random.randint(1, MAX_ENCOUNTERS)
    age = random.randint(0, 100)
    gender = random.choice(['Male', 'Female', 'Other'])
    
    for _ in range(num_encounters):
        encounter_date = fake.date_between(start_date='-2y', end_date='today')
        primary_diag = random.choice(ICD10_CODES)
        secondary_diag = random.choice(ICD10_CODES + [None]*3)  # optional
        notes = fake.sentence(nb_words=15)
        
        ehr_records.append({
            'patient_id': f'P{patient_id:04d}',
            'age': age,
            'gender': gender,
            'primary_diagnosis': primary_diag,
            'secondary_diagnosis': secondary_diag,
            'encounter_date': encounter_date,
            'notes': notes
        })

ehr_df = pd.DataFrame(ehr_records)
ehr_df.to_csv('data/ehr.csv', index=False)
print("✅ Generated ehr.csv with", len(ehr_df), "rows")

# -------------------------
# Generate Claims Data
# -------------------------
claims_records = []

for patient_id in range(1, NUM_PATIENTS + 1):
    num_claims = random.randint(1, MAX_CLAIMS)
    
    for claim_idx in range(1, num_claims + 1):
        claim_date = fake.date_between(start_date='-2y', end_date='today')
        procedure_code = random.choice(CPT_CODES)
        diagnosis_code = random.choice(ICD10_CODES)
        amount_billed = round(random.uniform(100, 5000), 2)
        amount_paid = round(amount_billed * random.uniform(0.7, 1.0), 2)
        
        claims_records.append({
            'claim_id': f'C{patient_id:04d}{claim_idx}',
            'patient_id': f'P{patient_id:04d}',
            'procedure_code': procedure_code,
            'diagnosis_code': diagnosis_code,
            'amount_billed': amount_billed,
            'amount_paid': amount_paid,
            'claim_date': claim_date
        })

claims_df = pd.DataFrame(claims_records)
claims_df.to_csv('data/claims.csv', index=False)
print("✅ Generated claims.csv with", len(claims_df), "rows")

# -------------------------
# Optional: add messy data
# -------------------------
# introduce missing values for testing cleaning pipeline
for col in ['primary_diagnosis', 'age', 'amount_paid']:
    ehr_df.loc[ehr_df.sample(frac=0.05).index, col] = None
    claims_df.loc[claims_df.sample(frac=0.05).index, col] = None

ehr_df.to_csv('data/ehr.csv', index=False)
claims_df.to_csv('data/claims.csv', index=False)
print("✅ Added 5% missing values to simulate messy data")