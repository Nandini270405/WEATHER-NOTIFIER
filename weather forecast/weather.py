import tkinter as tk
from tkinter import messagebox
from win10toast import ToastNotifier
import threading
import requests
import os

n = ToastNotifier()
API_KEY = os.getenv("OPENWEATHER_API_KEY", "6213ef27f819ad28bfcd42ce3f586b97")

def get_weather_data():
    location = location_entry.get()
    unit = unit_var.get()
    
    # Clear previous result
    result_label.config(text="")

    try:
        interval_min = int(interval_var.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid refresh interval selected.")
        return

    if not location:
        messagebox.showerror("Error", "Please enter a location.")
        return

    units = "metric" if unit == "Celsius" else "imperial"

    try:
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}"
        geo_response = requests.get(geo_url, timeout=10)
        geo_response.raise_for_status()
        loc_data = geo_response.json()

        if not loc_data:
            messagebox.showerror("Error", "Location not found!")
            return

        lat = loc_data[0]['lat']
        lon = loc_data[0]['lon']

        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={units}&appid={API_KEY}"
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        temp = weather_data['main']['temp']
        desc = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        wind = weather_data['wind']['speed']
        rain = weather_data.get('rain', {}).get('1h', "No rain data")

        result = (
            f"Temperature: {temp}°{'C' if units == 'metric' else 'F'}\n"
            f"Weather: {desc.capitalize()}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind} m/s\n"
            f"Rain: {rain}"
        )

        result_label.config(text=result)

        # Schedule toast notification
        root.after(0, lambda: n.show_toast(f"Weather Update - {location}", result, duration=10))

    except requests.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")

    # Schedule next update
    root.after(interval_min * 60 * 1000, get_weather_data)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Weather Notifier with Auto-Refresh")
root.geometry("400x300")

tk.Label(root, text="Enter Location:").pack()
location_entry = tk.Entry(root)
location_entry.pack()

unit_var = tk.StringVar(value="Celsius")
tk.Label(root, text="Select Unit:").pack()
tk.Radiobutton(root, text="Celsius", variable=unit_var, value="Celsius").pack()
tk.Radiobutton(root, text="Fahrenheit", variable=unit_var, value="Fahrenheit").pack()

tk.Label(root, text="Refresh Interval (minutes):").pack()
interval_var = tk.StringVar(value="60")
interval_menu = tk.OptionMenu(root, interval_var, "15", "30", "60", "120")
interval_menu.pack()

tk.Button(root, text="Start Weather Updates", command=get_weather_data).pack(pady=10)

result_label = tk.Label(root, text="", justify="left", wraplength=350)
result_label.pack()

root.mainloop()
