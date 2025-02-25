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
        API_KEY = "95e1e75dacca4b929a0165428252502"
        BASE_URL = "https://api.weatherapi.com/v1/current.json"
        params = {"q": city, "key": API_KEY, "aqi": "no"}  

        try:
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()

                weather = data["current"]["condition"]["text"]
                temp = data["current"]["temp_c"]
                humidity = data["current"]["humidity"]
                wind_speed = data["current"]["wind_kph"]

                weather_info = (f"Weather: {weather}\n"
                                f"Temperature: {temp}°C\n"
                                f"Humidity: {humidity}%\n"
                                f"Wind Speed: {wind_speed} kph")
                self.result_label.setText(weather_info)
            else:
                data = response.json()
                error_message = data.get("error", {}).get("message", "Unknown error")
                self.result_label.setText(f"Error: {error_message}")

        except requests.exceptions.RequestException as e:
            self.result_label.setText(f"Request Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
