from flask import Flask,render_template,redirect,url_for,flash
from forms import LoginForm
import psycopg2 as db
app = Flask(__name__)
app.config['SECRET_KEY'] = '9ioJbIGGH6ndzWOi3vEW' 

'''
connection = db.connect("dbname='postgres' user='postgres' host='localhost' password='hastayimpw'")
cursor = connection.cursor()
for statement in INIT_STATEMENTS:
    cursor.execute(statement)
connection.commit()
cursor.close()
'''

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
    app.run()
 
