from datetime import datetime
from typing import Optional

import anaximander as nx


class PeMSStation(nx.Entity):
    id: int = nx.id()
    district: int = nx.data()
    freeway: str = nx.data()
    direction: str = nx.data()
    length: float = nx.data()


class Speed(nx.Measurement):
    unit = "mph"
    ge = 0


class Flow(nx.Measurement):
    unit = "vph"
    ge = 0


class PeMSSample(nx.Sample):
    station_id: int = nx.key()
    timestamp: datetime = nx.timestamp()
    average_speed: Speed = nx.data(ge=0)
    total_flow: Flow = nx.data(ge=0)
