import os
import sys

import psycopg2 as dbapi2



INIT_STATEMENTS = [
    
    """CREATE TABLE IF NOT EXISTS users (
        tckn VARCHAR PRIMARY KEY,
        password VARCHAR NOT NULL
    )""",

    """CREATE TABLE IF NOT EXISTS POLICLINICS (
        ID VARCHAR,
        HOSPITAL_ID VARCHAR,
        NAME VARCHAR(50) NOT NULL,
        NUMBER_OF_EXAMINATION_ROOMS INTEGER,
        NUMBER_OF_OBSERVATION_ROOMS INTEGER,
        RECEPTIONIST VARCHAR(30) NOT NULL,
        PRIVATE BOOL DEFAULT FALSE,
        PRIMARY KEY (ID,HOSPITAL_ID)
    )
    """,


    #GOKTUG
    #False == Male
    """CREATE TABLE IF NOT EXISTS PATIENTS (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR(50) NOT NULL,
        AGE INTEGER,
        SEX BOOL DEFAULT FALSE, 
        TCKN VARCHAR NOT NULL,
        PHONE VARCHAR,
        CUR_COMPLAINT VARCHAR NOT NULL,
        INSURANCE INTEGER
    )
    """,
    """CREATE TABLE IF NOT EXISTS ALLERGIES (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL

    )""",
    """CREATE TABLE IF NOT EXISTS ALLERGIE_INDEX (
        PATIENT_ID INTEGER NOT NULL,
        ALLERGIES_ID INTEGER NOT NULL,
        CONSTRAINT c1 FOREIGN KEY (PATIENT_ID) REFERENCES PATIENTS(ID),
        CONSTRAINT c2 FOREIGN KEY (ALLERGIES_ID) REFERENCES ALLERGIES(ID)

    )""",


     """CREATE TABLE IF NOT EXISTS DRUG_COMPANIES (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL,
        FOUNDATION_YEAR INTEGER NOT NULL,
        FOUNDER VARCHAR NOT NULL,
        COUNTRY VARCHAR NOT NULL,
        WORKER_NUM INTEGER NOT NULL,
        FACTORY_NUM INTEGER NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS DRUG_TYPE (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS DRUGS (
        NAME VARCHAR NOT NULL,
        COMPANY_ID INTEGER NOT NULL,
        SIZE INTEGER NOT NULL,
        SHELF_LIFE INTEGER NOT NULL,
        PRICE VARCHAR NOT NULL,
        TYPE INTEGER NOT NULL,
        CONSTRAINT c1 FOREIGN KEY (TYPE) REFERENCES DRUG_TYPE(ID),
        CONSTRAINT c2 FOREIGN KEY (COMPANY_ID) REFERENCES DRUG_COMPANIES(ID)
    )""",

    # /GOKTUG

    """CREATE TABLE IF NOT EXISTS DETAILED_POLICLINICS (
        HOSPITAL_ID VARCHAR,
        POLICLINIC_ID VARCHAR,
        DOCTOR_ID VARCHAR,
        WORKING_HOURS VARCHAR(50),
        PRIMARY KEY (HOSPITAL_ID,POLICLINIC_ID,DOCTOR_ID),
        FOREIGN KEY (POLICLINIC_ID) REFERENCES POLICLINICS (ID)
    )
    """,
     """CREATE TABLE IF NOT EXISTS pharmacies (
        id SERIAL PRIMARY KEY,
        name VARCHAR NOT NULL,
        location VARCHAR,
        pharmacist INTEGER,
        helper INTEGER,
        next_night_shift DATE,
        tel_num INTEGER
    )""",
]

def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
