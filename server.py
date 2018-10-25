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
 
