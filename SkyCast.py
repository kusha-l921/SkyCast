import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather Forecast")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.city_label = QLabel("Enter City Name:")
        layout.addWidget(self.city_label)

        self.city_input = QLineEdit()
        layout.addWidget(self.city_input)

        self.get_weather_btn = QPushButton("Get Weather")
        self.get_weather_btn.clicked.connect(self.get_weather)
        layout.addWidget(self.get_weather_btn)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def get_weather(self):
        city = self.city_input.text()
        API_KEY = "0455c907764d76d00d2b78e7616f2898"  # Replace with your OpenWeatherMap API key
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

        params = {"q": city, "appid": API_KEY, "units": "metric"}

        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            weather = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            weather_info = (f"Weather: {weather}\n"
                            f"Temperature: {temp}°C\n"
                            f"Humidity: {humidity}%\n"
                            f"Wind Speed: {wind_speed} m/s")
            self.result_label.setText(weather_info)
        else:
            self.result_label.setText(f"Error: {data['message']}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())