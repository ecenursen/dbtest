from flask import Flask,render_template,redirect,url_for,flash
from forms import LoginForm
import psycopg2 as db
app = Flask(__name__)
app.config['SECRET_KEY'] = '9ioJbIGGH6ndzWOi3vEW' 

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

    """CREATE TABLE IF NOT EXISTS DETAILED_POLICLINICS (
        HOSPITAL_ID VARCHAR,
        POLICLINIC_ID VARCHAR,
        DOCTOR_ID VARCHAR,
        WORKING_HOURS VARCHAR(50),
        PRIMARY KEY (HOSPITAL_ID,POLICLINIC_ID,DOCTOR_ID),
        FOREIGN KEY (POLICLINIC_ID) REFERENCES POLICLINICS (ID)
    )
    """,


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
 
