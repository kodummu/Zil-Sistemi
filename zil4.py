from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
import sqlite3
import datetime
import threading
import time
import os

app = Flask(__name__)

zilsistemi_bp = Blueprint('zilsistemi', __name__)
app.register_blueprint(zilsistemi_bp)
# Sqlite olacak

app.secret_key = 'cokgizlianahtar'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite database file path
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure random key


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)

# def create_app():
#     db.init_app(app)
#     return app

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
@app.route('/index') # hem sayfa belirtmeyince hem de index yazınca anasayfaya gitmeli
def index():
    if 'user_id' in session:
        return render_template('index.html', logged_in=True)
    return render_template('index.html')

@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    global alarm_time, alarm_active

    if 'user_id' not in session:
        flash('Zil ayarı yapabilmek için giriş yapınız.', 'error')
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
        try:
            db = sqlite3.connect("zilsistemi/zilsistemi.db")
            connection = db.cursor()
            insert_user_query = "insert into user (username, password) values (?, ?)"
            connection.execute(insert_user_query, (username, password))
            # database'e kullanıcı eklemek için
            # kullanıcı adı sistemde varsa uyarı atmalı
            db.commit()
            db.close()
            message = "Kullanıcı kaydı başarılı. Giriş yapabilirsiniz."
            flash(message, 'success')
            return redirect(url_for('login'))
        except sqlite3.Error as e:
            message = "kullanıcı zaten mevcut, 'error'"
            flash(message, 'error')
            # flash backend'ten (flask) frontend'e (html) data göndermek için


    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            db = sqlite3.connect("zilsistemi/zilsistemi.db")
            connection = db.cursor()
            select_user_query = "select * from user where username=? and password=?"
            connection.execute(select_user_query, (username, password))
            columns = [description[0] for description in connection.description]  # Sütun adlarını almak için cursor.description kullanılır

            # Sadece bir satırın değerlerini alma
            row = connection.fetchone()

            # Değerleri ve sütun adlarını birleştirme
            user = dict(zip(columns, row)) if row else None  # Değerleri ve sütun adlarını birleştirerek bir sözlük oluşturur
            db.commit()
            db.close()
            if user:
                print(user)
                session['user_id'] = user["id"]
                message = "Kullanıcı girişi başarılı."
                flash(message, 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password. Please try again.', 'error')

            return redirect(url_for('login'))
        except sqlite3.Error as e:
            message = "kullanıcı zaten mevcut, 'error'"
            flash(message, 'error')


    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)