import datetime
from zoneinfo import ZoneInfo
import requests
from flask import Flask, request

app = Flask(__name__)

# Informacje o autorze
AUTHOR = "Patryk Pawelec"
PORT = 5000

# Logowanie informacji o uruchomieniu serwera
start_time = datetime.datetime.now()
with open("server.log", "a") as log_file:
    log_file.write(f"Server started on: {start_time}\n")
    log_file.write(f"Author: {AUTHOR}\n")
    log_file.write(f"Listening on port: {PORT}\n")


@app.route('/')
def index():
    # Pobranie adresu IP klienta
    client_ip = request.remote_addr

    # Ustalenie strefy czasowej na podstawie adresu IP
    try:
        response = requests.get(f'https://ipinfo.io/{client_ip}/json')
        data = response.json()
        timezone_str = data.get('timezone', 'Europe/Warsaw')  # Domyślnie 'Europe/Warsaw' jeśli brak danych
        timezone = ZoneInfo(timezone_str)
        client_time = datetime.datetime.now(timezone)
        location = data.get('city', 'Unknown location')
    except Exception as e:
        # W razie błędu ustaw domyślne wartości
        timezone = ZoneInfo('Europe/Warsaw')
        client_time = datetime.datetime.now(timezone)
        location = 'Unknown location'
        print(f"Error determining timezone: {e}")

    return f"<h1>Your IP: {client_ip}</h1><p>Current time in your timezone: {client_time}</p><p>Location: {location}</p>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
