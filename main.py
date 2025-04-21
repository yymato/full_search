import sys
import random
import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget

# Список городов
CITIES = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань",
    "Нижний Новгород", "Челябинск", "Самара", "Ростов-на-Дону", "Уфа"
]

YANDEX_STATIC_MAPS_API = "https://static-maps.yandex.ru/1.x/"
YANDEX_GEOCODE_API = "http://geocode-maps.yandex.ru/1.x/"
YANDEX_GEOCODE_KEY = "8013b162-6b42-4997-9691-77b7074026e0"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("крестики нолики")
        self.setFixedSize(600, 450)

        self.map_label = QLabel(self)
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.next_button = QPushButton("Следующий город")
        self.next_button.clicked.connect(self.show_city)
        layout = QVBoxLayout()
        layout.addWidget(self.map_label)
        layout.addWidget(self.next_button)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.rem_cities = CITIES.copy()
        random.shuffle(self.rem_cities)

        self.show_city()

    def show_city(self):
        if not self.rem_cities:
            self.rem_cities = CITIES.copy()
            random.shuffle(self.rem_cities)

        city = self.rem_cities.pop()
        coords = self.get_city_coords(city)
        if coords:
            self.display_map(coords)

    @staticmethod
    def get_city_coords(city):
        params = {
            "apikey": YANDEX_GEOCODE_KEY,
            "geocode": city,
            "format": "json"
        }
        response = requests.get(YANDEX_GEOCODE_API, params=params)
        if not response:
            return None
        json_data = response.json()
        pos = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
        lon, lat = pos.split()
        return float(lon), float(lat)


    def display_map(self, coords):
        lon, lat = coords
        map_params = {
            "ll": f"{lon},{lat}",
            "z": 12,
            "l": "sat"
        }

        response = requests.get(YANDEX_STATIC_MAPS_API, params=map_params)
        print(response.reason)
        print(response.url)
        if not response:
            return

        with open("city.jpg", "wb") as f:
            f.write(response.content)

        pixmap = QPixmap("city.jpg")
        self.map_label.setPixmap(pixmap)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    game_window = MainWindow()
    game_window.show()
    sys.exit(app.exec())
