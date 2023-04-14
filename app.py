# app.py
from flask import Flask, request, session, redirect, url_for, render_template, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import psycopg2
import psycopg2.extras
import re
import pandas as pd

app = Flask(__name__)
app.secret_key = 'aidi_extra'

# DB_HOST = "localhost"
# DB_NAME = "message_board"
# DB_USER = "postgres"
# DB_PASS = "asli2809"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'message_board'

conn = MySQL(app)

#conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port='5432')

my_dic = pd.read_excel('chyper-code.xlsx', index_col=0, usecols="A:B", engine="openpyxl").to_dict()
pwd_map = my_dic['SYSTEM CONVERT']


def convert(value, conversion_map):
    pwd = ""
    for token in str(value):
        if token in conversion_map:
            pwd += conversion_map[token]
        elif token.upper() in conversion_map:
            pwd += conversion_map[token.upper()].lower()
        else:
            pwd += token

    return pwd


def encrypt(value):
    encrypt_map = {str(key): str(value) for key, value in pwd_map.items()}
    return convert(value, encrypt_map)


def decrypt(value):
    decrypt_map = {str(value): str(key) for key, value in pwd_map.items()}
    return convert(value, decrypt_map)


@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', email=session['email'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    #cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor = conn.connection.cursor(MySQLdb.cursors.DictCursor)

    # Check if "email" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']

        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM tb_user WHERE email = %s', [email])
        # Fetch one record and return result
        account = cursor.fetchone()

        if account:
            password_rs = account['password']
            decrypted_pwd = decrypt(password_rs)

            # If account exists in users table in out database
            if password == decrypted_pwd:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['email'] = account['email']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect email/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect email/password')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    #cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor = conn.connection.cursor()
    # Check if "password", "password2" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'password' in request.form and 'password2' in request.form and 'email' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        encrypted_password = encrypt(password)

        # Check if account exists
        cursor.execute('SELECT * FROM tb_user WHERE email = %s', [email])
        account = cursor.fetchone()
        print(account)
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif password != password2:
            flash('Passwords do not match!')
        elif not password or not email:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            cursor.execute("INSERT INTO tb_user (email, password) VALUES (%s,%s)",
                           (email, encrypted_password))
            #conn.commit()
            conn.connection.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    # Redirect to login page
    return redirect(url_for('login'))


@app.route('/message',methods=['GET', 'POST'])
def message():
    #cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor = conn.connection.cursor()
    if 'loggedin' in session and 'id' in session:
        if request.method == 'POST' and 'msg_text' in request.form:
            # Create variables for easy access
            mail_content = request.form['msg_text']
            user_id = session['id']

            # Check if account exists
            cursor.execute('SELECT * FROM tb_user WHERE id = %s', [user_id])
            account = cursor.fetchone()

            # If account exists show error and validation checks
            if account:
                # insert message into tb_mail table
                cursor.execute("INSERT INTO tb_mail (user_id, mail_content) VALUES (%s,%s)",
                               (user_id, mail_content))
                #conn.commit()
                conn.connection.commit()
                flash('Hi ' + session['email'] + ', Message sent!')
            else:
                return render_template('login.html')
        elif request.method == 'POST':
            # message is empty... (no POST data)
            flash('Please type your message!')
    else:
        return render_template('login.html')
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
