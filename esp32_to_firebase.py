import serial
import time
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ropar-02-default-rtdb.firebaseio.com/'
})

SERIAL_PORT = 'COM5'
BAUD_RATE = 115200
DEVICE_ID = 'esp32_01'

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
    except Exception as e:
        print(f"Error opening serial port: {e}")
        return

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if not line:
                continue

            try:
                i1_str, i2_str = line.split(',')
                i1 = float(i1_str)
                i2 = float(i2_str)

                data = {"I1": i1, "I2": i2}
                ref = db.reference(f"/readings/{DEVICE_ID}")
                ref.push(data)

                print(f"Sent to Firebase: I1={i1}, I2={i2}")

            except Exception as e:
                print(f"Failed to parse/send data: '{line}', error: {e}")

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
