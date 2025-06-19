# WEATHER-NOTIFIER

# 🌦️ Weather Notifier with Auto-Refresh

A simple Python desktop application that fetches and displays real-time weather updates for any city, using the OpenWeatherMap API. Built with `tkinter` for the GUI and `win10toast` for toast notifications, this app keeps you updated with live weather every few minutes—automatically.

---

## ✨ Features

- 🔍 Get current weather by entering a city name
- 🌡️ Choose between Celsius and Fahrenheit
- 🔁 Set auto-refresh intervals (15, 30, 60, or 120 minutes)
- 🔔 Receive Windows toast notifications with weather info
- 💨 Displays temperature, weather description, humidity, and wind speed

---

## 🛠 Technologies Used

- Python 3
- `tkinter` — GUI
- `requests` — API calls
- `win10toast` — Desktop notifications
- `threading` — Non-blocking toast alerts

---

## 📦 Installation

1. Clone the repository or download the `.py` file.
2. Install dependencies:
   ```bash
   pip install requests win10toast
