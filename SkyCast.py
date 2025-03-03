import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather Forecast")
        self.setGeometry(100, 100, 350, 250)

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
        BASE_URL = "https://api.weatherapi.com/v1/forecast.json"  
        params = {"q": city, "key": API_KEY, "aqi": "no", "days": 3}  

        try:
            response = requests.get(BASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()

                current_weather = data["current"]["condition"]["text"]
                temp = data["current"]["temp_c"]
                humidity = data["current"]["humidity"]
                wind_speed = data["current"]["wind_kph"]

                forecast_info = "\n🔮 3-Day Forecast:\n"
                for day in data["forecast"]["forecastday"]:
                    date = day["date"]
                    condition = day["day"]["condition"]["text"]
                    max_temp = day["day"]["maxtemp_c"]
                    min_temp = day["day"]["mintemp_c"]
                    forecast_info += f"{date}: {condition}, {min_temp}°C - {max_temp}°C\n"

                weather_info = (f"🌤️ Current Weather: {current_weather}\n"
                                f"🌡 Temperature: {temp}°C\n"
                                f"💧 Humidity: {humidity}%\n"
                                f"🌬 Wind Speed: {wind_speed} kph\n"
                                f"{forecast_info}")
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
