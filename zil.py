# Başlangıçta pip install Flask 
# python zil2.py


import time
import datetime

def set_alarm():
    try:
        alarm_time_str = input("Enter the alarm time (format HH:MM): ")
        alarm_time = datetime.datetime.strptime(alarm_time_str, "%H:%M")
        return alarm_time
    except ValueError:
        print("Invalid time format. Please use HH:MM.")
        return set_alarm()

def sound_alarm():
    print("\nAlarm! Alarm! Wake up!")

def main():
    print("Welcome to the Alarm System")
    alarm_time = set_alarm()

    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        print(f"Current time: {current_time}")

        if current_time == alarm_time.strftime("%H:%M"):
            sound_alarm()
            break

        time.sleep(60)  # Check the time every minute

if __name__ == "__main__":
    main()
