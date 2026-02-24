# utils/data_cleaning.py
import pandas as pd
import numpy as np

def clean_healthcare_data(ehr_df, claims_df):
    """
    Clean and normalize EHR and Claims data.
    """

    # -------------------------
    # EHR Cleaning
    # -------------------------
    if 'age' in ehr_df.columns:
        ehr_df['age'] = pd.to_numeric(ehr_df['age'], errors='coerce')
        ehr_df['age'] = ehr_df['age'].fillna(ehr_df['age'].median())

    for col in ['primary_diagnosis', 'secondary_diagnosis']:
        if col in ehr_df.columns:
            ehr_df[col] = ehr_df[col].fillna('Unknown')

    if 'encounter_date' in ehr_df.columns:
        ehr_df['encounter_date'] = pd.to_datetime(ehr_df['encounter_date'], errors='coerce')

    # -------------------------
    # Claims Cleaning
    # -------------------------
    for col in ['amount_billed', 'amount_paid']:
        if col in claims_df.columns:
            claims_df[col] = pd.to_numeric(claims_df[col], errors='coerce').fillna(0)

    if 'claim_date' in claims_df.columns:
        claims_df['claim_date'] = pd.to_datetime(claims_df['claim_date'], errors='coerce')

    # -------------------------
    # Ensure patient_id exists
    # -------------------------
    if 'patient_id' not in ehr_df.columns:
        ehr_df['patient_id'] = [f"P{i}" for i in range(1, len(ehr_df)+1)]
    if 'patient_id' not in claims_df.columns:
        claims_df['patient_id'] = [f"P{i}" for i in range(1, len(claims_df)+1)]

    # Optional synthetic risk flag
    if 'risk_flag' not in ehr_df.columns:
        np.random.seed(42)
        ehr_df['risk_flag'] = np.random.randint(0, 2, size=len(ehr_df))

    return ehr_df, claims_df