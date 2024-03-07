import os
from datetime import datetime
from typing import Optional

import anaximander as nx


def get_request(func):
    def wrapper():
        pass # send out a get request and return


class City(nx.Entity):
    id: int = nx.id()
    name: str = nx.data()
    lat: float = nx.data()
    lon: float = nx.data()


class Visibility(nx.Measurement):
    unit = "miles"
    ge = 0


class Condition(nx.Measurement):
    pass


class Weather(nx.Sample):
    city_id: int = nx.key()
    timestamp: datetime = nx.timestamp()
    visibility: Visibility = nx.data(ge=0)
    condition: Condition = nx.data()

    @get_request
    def from_source(city: City):
        return f"https://api.openweathermap.org/data/2.5/weather?lat={city.lat}&lon={city.lon}&appid={os.environ['API_KEY']}"

