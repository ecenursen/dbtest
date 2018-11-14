from flask import Flask,render_template,redirect,url_for,flash
from forms import LoginForm
import psycopg2 as db
app = Flask(__name__)
app.config['SECRET_KEY'] = '9ioJbIGGH6ndzWOi3vEW' 



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

        #Ecem
    """CREATE TABLE IF NOT EXISTS HOSPITAL_PERSONNEL (
        PERSONNEL_ID SERIAL PRIMARY KEY,
        WORKER_NAME VARCHAR,
        JOB_TITLE VARCHAR NOT NULL,
        JOB_EXPERIENCE INTEGER,
        DAYS_WORKED INTEGER,
        NIGHT_SHIFT INTEGER,
        PHONE_NUM VARCHAR,
        WORKING_FIELD VARCHAR,
        TCKN VARCHAR,
        FOREIGN KEY (DAYS_WORKED)  REFERENCES DAY_TABLE(GENERATED_KEY),
        FOREIGN KEY (NIGHT_SHIFT) REFERENCES DAY_TABLE(GENERATED_KEY)
    )""",

    """CREATE TABLE IF NOT EXISTS DAY_TABLE (
        GENERATED_KEY SERIAL PRIMARY KEY,
        WORK_DAY VARCHAR,
        WORKER_NAME VARCHAR,
        DAYSHIFT BOOL
    )"""

]


connection = db.connect("dbname='postgres' user='postgres' host='localhost' password='hastayimpw'")
cursor = connection.cursor()
for statement in INIT_STATEMENTS:
    cursor.execute(statement)
connection.commit()
cursor.close()

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home_page.html')

@app.route("/about")
def about_page():
    return render_template('about_page.html')
@app.route("/patients")
def patients_page():
    patients = []
    connection = db.connect("dbname='postgres' user='postgres' host='localhost' password='hastayimpw'")
    cursor = connection.cursor()
    statement = """SELECT * FROM PATIENTS"""""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        patients.append(row)
    cursor.close()
    return render_template('patients_page.html', Patients=patients)
    
@app.route("/drugs")
def drugs_page():
    drugs = []
    connection = db.connect("dbname='postgres' user='postgres' host='localhost' password='hastayimpw'")
    cursor = connection.cursor()
    statement = """SELECT * FROM DRUGS"""""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        drugs.append(row)
    cursor.close()
    return render_template('drugs_page.html', Drugs=drugs)


@app.route("/drug-companies")
def drug_companies_page():
    companies = []
    connection = db.connect("dbname='postgres' user='postgres' host='localhost' password='hastayimpw'")
    cursor = connection.cursor()
    statement = """SELECT * FROM DRUG_COMPANIES"""""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        companies.append(row)
    cursor.close()
    return render_template('drug_companies_page.html', DrugCompanies=companies)

@app.route("/pharmacy")
def pharmacy_page():
    pharmacies=[]
    connection = db.connect("dbname='postgres' user='postgres' host='localhost' password='hastayimpw'")
    cursor = connection.cursor()
    statement = """SELECT * FROM pharmacies"""""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        pharmacies.append(row)
    
    
    cursor.close()

    return render_template('pharmacy_page.html', Pharmacies=pharmacies)

@app.route("/hospital_personnel")
def hospital_personnel_page():
    workers =[]
    connection = db.connect("dbname='postgres' user='postgres' host='localhost' password='hastayimpw'")
    cursor = connection.cursor()
    statement = """SELECT * FROM HOSPITAL_PERSONNEL"""
    cursor.execute(statement)
    connection.commit()
    for row in cursor:
        workers.append(row)
    cursor.close()
    return render_template('hospital_personnel_page.html',hospital_personnel=workers)

    
@app.route("/ece_test")
def ece_test():
    try:
        connection = db.connect("dbname='postgres' user='postgres' host='localhost' password='hastayimpw'")
        cursor = connection.cursor()
        statement = """SELECT * FROM POLICLINICS"""
        cursor.execute(statement)
        connection.commit()

        for myrow in cursor:
            print(myrow)

    except db.DatabaseError:
        connection.rollback()
        flash('Unsuccessful to write the table!', 'danger')
    finally:
        connection.close()
    return render_template('policlinics.html',myrow=myrow)


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        tc = form.tckn.data
        pw = form.password.data
        try:
            connection = db.connect("dbname='postgres' user='postgres' host='localhost' password='hastayimpw'")
            cursor = connection.cursor()
            statement = """SELECT * FROM users WHERE tckn = '%s'
                    """ % tc
            cursor.execute(statement)
            result = cursor.fetchone()
            if(result[1] == pw):
                flash('You have been logged in!', 'success')
                return redirect(url_for('home_page'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        except db.DatabaseError:
            connection.rollback()
            flash('Login Unsuccessful. Please check username and password', 'danger')
        finally:
            connection.close()
    return render_template('login_page.html', title='Login', form=form)

if __name__ == "__main__":
    app.run(debug=True)
 
