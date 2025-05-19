# Real-Time Flask Chat App with AI & Weather Features

A real-time web-based chat application built with Flask, Socket.IO, and SQLite. The chat bot can respond to greetings, calculate math expressions, display the current time, and fetch weather data via the OpenWeatherMap API.

---

## Features

-  Real-time messaging with WebSockets
-  AI-style chatbot with basic intent detection
-  Persistent chat history (saved to SQLite)
-  Live weather info using OpenWeatherMap API
-  Math calculator with safe expression parsing
-  Toggleable Dark Mode (optional UI feature)
- 🗃 View past chat logs (`/logs` route)

---

## 🖥 Demo

> Local demo instructions below. Optional: Deploy to Render, Vercel, or Replit for live showcase.

---

## Tech Stack

| Tech           | Purpose                      |
|----------------|------------------------------|
| Python + Flask | Web framework & routing      |
| Flask-SocketIO | Real-time communication      |
| SQLite         | Persistent chat message log  |
| JavaScript     | Frontend interactivity       |
| HTML + CSS     | Basic frontend UI            |
| OpenWeatherMap | Weather API integration      |

---

## Setup & Installation

1. **Clone the repository**
2. Create a virtual environment: python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
3. Install dependencies: pip install -r requirements.txt
4. Run the app
5. Visit http://localhost:5000 in your browser.

---

## API Key for Weather
To enable the weather feature:
Get a free API key from OpenWeatherMap.
Open app.py and replace the placeholder key: api_key = "REPLACE_ME_WITH_YOUR_API_KEY"

---

## Chat Commands
Command	// Description
hello, hi, etc	// Basic greeting
/help	// Show available features
/time	// Display current system time
/calc (? + ?, * / - +)	// Evaluate a math expression safely (No Algebra)
/weather (city)	// Get current weather in specified location
