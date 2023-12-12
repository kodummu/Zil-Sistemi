from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import datetime
import threading
import time
import os
"""python
from zil(sql) import db
db.create_all()
exit()

Başlangıçta pip install Flask 
pip install Flask-SQLAlchemy pyodbc --- SQL kullanmak için indirdik

"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://your_username:your_password@your_server/your_database?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure random key

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

def create_app():
    db.init_app(app)
    return app

alarm_time = None
alarm_active = False

def check_alarm():
    global alarm_active
    while alarm_active:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time.strftime("%H:%M"):
            print("Alarm! Alarm! Wake up!")
            alarm_active = False
        time.sleep(1)

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html', logged_in=True)
    return render_template('index.html')

@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    global alarm_time, alarm_active

    if 'user_id' not in session:
        flash('Please log in to set an alarm.', 'error')
        return redirect(url_for('login'))

    alarm_hour = int(request.form['hour'])
    alarm_minute = int(request.form['minute'])
    
    alarm_time = datetime.datetime(2023, 1, 1, alarm_hour, alarm_minute)

    # Start a thread to check the alarm
    alarm_active = True
    threading.Thread(target=check_alarm).start()

    flash('Alarm set successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
