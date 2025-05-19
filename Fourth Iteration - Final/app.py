import requests
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from datetime import datetime
import math
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# === ROUTES ===

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logs')
def logs():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('SELECT username, message, timestamp FROM messages ORDER BY timestamp DESC LIMIT 100')
    logs = c.fetchall()
    conn.close()
    return "<br>".join([f"[{ts}] {user}: {msg}" for user, msg, ts in logs])

# === Keywords ===
intents = {
    'greeting': ['hello', 'hi', 'hey', 'greetings'],
    'time': ['time', 'clock', 'what time'],
    'weather': ['weather', 'forecast', 'temperature'],
    'math': ['calculate', 'what is', 'solve', '+', '-', '*', '/'],
    'help': ['help', 'commands', 'what can you do']
}

def detect_intent(msg):
    for intent, keywords in intents.items():
        if any(keyword in msg for keyword in keywords):
            return intent
    return None

# === MESSAGE HANDLING ===
@socketio.on('message')
def handle_message(data):
    username = data.get('username', 'User')
    msg = data.get('message', '')
    msg_lower = msg.lower().strip()

    full_msg = f"{username}: {msg}"
    print(full_msg)
    send(full_msg, broadcast=True)
    save_message(username, msg)

    # === Priority: / Command handlers (e.g. /weather) ===
    if msg_lower.startswith('/weather'):
        try:
            city = msg.split(' ', 1)[1].strip()
            weather_report = get_weather(city)
            send(f"ChatBot 🤖: {weather_report}", broadcast=True)
        except IndexError:
            send("ChatBot 🤖: Use /weather [city], e.g. /weather Limerick", broadcast=True)
        return  # stop here

    elif msg_lower.startswith('/calc'):
        try:
            expression = msg.split(' ', 1)[1].strip()
            answer = safe_eval(expression)
            send(f"ChatBot 🤖: {answer}", broadcast=True)
        except IndexError:
            send("ChatBot 🤖: Use /calc [expression], e.g. /calc 12 / (3 + 1)", broadcast=True)
        return  # stop here

    # === Then we check for general intent of the messages ===
    intent = detect_intent(msg_lower)

    if intent == 'greeting':
        send(f"ChatBot 🤖: Hello, {username}!", broadcast=True)
    elif intent == 'help':
        send("ChatBot 🤖: You can ask me about weather, time, math, or just say hello.", broadcast=True)
    elif intent == 'time':
        now = datetime.now().strftime("%H:%M:%S")
        send(f"ChatBot 🤖: The current time is {now}.", broadcast=True)
    elif intent == 'weather':
        send("ChatBot 🤖: Try typing '/weather [city]' for weather info!", broadcast=True)
    elif intent == 'math':
        send("ChatBot 🤖: Use '/calc 12 / (3 + 1)' or similar to calculate.", broadcast=True)
    else:
        send("ChatBot 🤖: I'm still learning! Try asking for help with /help", broadcast=True)


# === BOT Functionalities ===

def get_weather(city):
    api_key = "Replace_With_Your_Own"  # Replace with your own key
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

# === DATABASE ===

def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_message(username, message):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (username, message) VALUES (?, ?)', (username, message))
    conn.commit()
    conn.close()

# === START SERVER === View the logs on http://localhost:5000/logs

if __name__ == '__main__':
    init_db()
    socketio.run(app, debug=True)