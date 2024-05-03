from flask import Flask, render_template, request, url_for, flash, redirect, session
import traceback
from db import Db
import sqlite3
from config import Config

app = Flask(__name__, static_folder='static')
con = sqlite3.connect("account.db")
cur = con.cursor()
app.config.from_object(Config)


@app.route("/", methods=['GET', 'POST'])
def home():
    """Home page """
    return render_template('index.html',
                           title="Cooking App Home Page",
                           heading="Home Page")

@app.route("/register_page", methods=['GET', 'POST'])
def load_register():
    """register page (add new user)"""
    return render_template('register.html',
                           title="Register",
                           heading="Create a new account")

@app.route("/register", methods=['GET', 'POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    user_data = Db.register(username, password)
    if user_data == 0:
        # invalid username
        error_message = "Username is already taken or empty"
        flash("Wrong username")
        return render_template('register.html',
                           title="Register",
                           heading="Create a new account", error_message=error_message)
    elif user_data == 1:
        # invalid password
        error_message = "Password isn't strong enough"
        flash("Wrong password")
        return render_template('register.html',
                           title="Register",
                           heading="Create a new account", error_message=error_message)
    elif type(user_data) == tuple:
        # Authentication successful, you can now access user's information
        # Redirect to login_success route with user id
        session['user_data'] = user_data
        return redirect(url_for('login_success', id_=user_data[0]))
    else:
        error_message = True
        flash("Something went wrong with registration")
        return render_template('register.html',
                           title="Register",
                           heading="Create a new account", error_message=error_message)
        

@app.route("/login", methods=['GET', 'POST'])
def login_route():
    """
    Handle user login request.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if 'login_attempts' not in session:
            session['login_attempts'] = 0
            
        if session['login_attempts'] >= 3:
            error_message = "Too many failed attempts, try again later"
            return render_template('index.html', 
                        error_message=error_message)
        else:
            print(session['login_attempts'])
            user_data = Db.login(username, password)
            print("this is the user", user_data)
            if user_data:
                # Authentication successful, you can now access user's information
                # Redirect to login_success route with user id
                session['user_data'] = user_data
                return redirect(url_for('login_success', id_=user_data[0]))
            else:
                session['login_attempts'] += 1
                flash("Invalid username or password")
            error_message = "Invalid username or password"
            return render_template('index.html', 
                                error_message=error_message)

@app.route("/homepage/<string:id_>", methods=['GET', ])
def login_success(id_):
    """
    Route for successful login.
    """
    user_data = session.get('user_data')
    print("user data", user_data)
    flash(f"Welcome {id_}! You have logged in!", 'alert-success')
    return render_template('user_home.html',
                           title="User Home",
                           heading="User Home", user=user_data)

@app.route("/homepage", methods=['GET', ])
def user_home():
    """
    Route for successful login.
    """
    user_data = session.get('user_data')
    flash(f"Welcome {user_data[1]}! You have logged in!", 'alert-success')
    return render_template('user_home.html',
                           title="User Home",
                           heading="User Home", user=user_data)

@app.route("/level", methods=['POST'])
def level_change():
    user_data = session.get('user_data')
    level = request.form.get('level')
    user_change = Db.level_update(user_data[1], level)
    if user_change:
        session['user_data'] = user_change
        return render_template('user_home.html',
                           title="User Home",
                           heading="User Home", user=session['user_data'])
    else:
        error_message = "could not update user level"
        flash("Something went wrong")
        return render_template('user_home.html',
                           title="User Home",
                           heading="User Home", error_message=error_message, user=user_data)

@app.route("/account", methods=['GET', 'POST'])
def account_page():
    user_data = session.get('user_data')
    return render_template('account.html', user=user_data)

if __name__ == '__main__':
    # pylint: disable=W0703
    try:
        app.run(debug=app.debug, host='localhost', port=8000)
    except Exception as err:
        traceback.print_exc()