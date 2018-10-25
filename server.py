from flask import Flask,render_template,redirect,url_for,flash
from forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '9ioJbIGGH6ndzWOi3vEW' 
@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home_page.html')

@app.route("/about")
def about_page():
    return render_template('about_page.html')

@app.route("/login")
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        if form.tcnk.data == 'deneme_user' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login_page.html', title='Login', form=form)

if __name__ == "__main__":
    app.run(debug=True)
