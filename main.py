from anaximander.operators import Sessionizer

from bay_area_511_event import EventSample, EventSession
from pems import PeMSStation
from weather import Weather, City


class SpeedSample:
    pass


if __name__ == '__main__':
    city = City(name="Berkeley", lat=20.0, lon=25.0)
    weather = Weather.from_source(city)
    speed = SpeedSample.from_source([PeMSStation(id=50000), PeMSStation(id=50001)])
    events = EventSample.from_source()

    sessionizer = Sessionizer(EventSample, EventSession, feature="event_id")

    events.data[['Severity']] # pandas
