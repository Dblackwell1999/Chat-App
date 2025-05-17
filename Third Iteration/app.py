import requests
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from datetime import datetime
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    username = data.get('username', 'User')
    msg = data.get('message', '')
    msg_lower = msg.lower().strip()

    full_msg = f"{username}: {msg}"
    print(full_msg)

    # Broadcast user message
    send(full_msg, broadcast=True)

    # === Bot responses ===
    if 'hello' in msg_lower or 'hi' in msg_lower:
        send(f"ChatBot 🤖: Hello, {username}!", broadcast=True)

    elif 'help' in msg_lower:
        send("ChatBot 🤖: You can ask me about the weather, time, math, or just say hello!", broadcast=True)

    elif 'time' in msg_lower:
        now = datetime.now().strftime("%H:%M:%S")
        send(f"ChatBot 🤖: The time is {now}", broadcast=True)

    elif msg_lower.startswith('/weather'):
        try:
            city = msg.split(' ', 1)[1].strip()
            weather_report = get_weather(city)
            send(f"ChatBot 🤖: {weather_report}", broadcast=True)
        except IndexError:
            send("ChatBot 🤖: Use /weather [city], e.g. /weather Limerick", broadcast=True)

    elif msg_lower.startswith('/calc'):
        try:
            expression = msg.split(' ', 1)[1].strip()
            answer = safe_eval(expression)
            send(f"ChatBot 🤖: {answer}", broadcast=True)
        except IndexError:
            send("ChatBot 🤖: Use /calc [expression], e.g. /calc 12 / (3 + 1)", broadcast=True)

# Weather command
def get_weather(city):
    api_key = "01cfb40a7976974071668f7957a63ab1"  # ✅ Put your own key here
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            return f"Couldn't find weather for '{city.title()}'."
        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"]
        return f"The weather in {city.title()} is {temp}°C with {condition}."
    except Exception as e:
        return f"Error getting weather: {str(e)}"

# Safe calculator
def safe_eval(expr):
    try:
        allowed_chars = "0123456789+-*/(). "
        if any(char not in allowed_chars for char in expr):
            return "Invalid characters in expression."
        result = eval(expr)
        return f"The answer is {result}"
    except ZeroDivisionError:
        return "You can't divide by zero!"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    socketio.run(app, debug=True)
