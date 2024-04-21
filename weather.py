import os
from datetime import datetime

import anaximander as nx

MINUTE = 60 * 60
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class City(nx.Entity):
    id: int = nx.id()
    name: str = nx.data()
    lat: float = nx.data()
    lon: float = nx.data()


class Visibility(nx.Measurement):
    unit = "miles"
    ge = 0


class WeatherSample(nx.Sample):
    city_id: int = nx.key()
    timestamp: datetime = nx.timestamp()
    visibility: Visibility = nx.data(ge=0)

    @nx.source
    @scheduler("5m")
    @get_request
    @authentication(url_params={"appid": os.environ['API_KEY']})
    def from_source(city: City):
        return f"{BASE_URL}?lat={city.lat}&lon={city.lon}"


class WeatherJournal(nx.Journal):
    city_id: int = nx.key()
    timestamp: datetime = nx.timestamp()
    visibility: Visibility = nx.data()

    @nx.source
    def from_sample(self):
        return (
            WeatherSample.filter(lambda weather:
                                 weather.timestamp <= timestamp + 5 * MINUTE and \
                                 weather.timestamp >= timestamp - 5 * MINUTE))
