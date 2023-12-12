from flask import Flask, render_template, request
import datetime
import threading
import time

app = Flask(__name__)

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
    return render_template('index.html')

@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    global alarm_time, alarm_active

    alarm_hour = int(request.form['hour'])
    alarm_minute = int(request.form['minute'])
    
    alarm_time = datetime.datetime(2023, 1, 1, alarm_hour, alarm_minute)

    # Start a thread to check the alarm
    alarm_active = True
    threading.Thread(target=check_alarm).start()

    return render_template('index.html', alarm_set=True)

if __name__ == '__main__':
    app.run(debug=True)
