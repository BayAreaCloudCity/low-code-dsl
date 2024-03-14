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

MINUTE = 60 * 60

class PeMSJournal(nx.Journal):
    city_id: int = nx.key()
    timestamp: datetime = nx.timestamp()
    average_speed: Speed = nx.data(ge=0)
    total_flow: Flow = nx.data(ge=0)

    def from_sample(self, pemslist, timestamp):
        for pems in sorted(pemslist):
            if pems.timestamp <= timestamp + 5 * MINUTE and \
                pems.timestamp >= timestamp - 5 * MINUTE:
                self.average_speed = pems.average_speed
                self.total_flow = pems.total_flow

class SegmentPeMsJournal(nx.Journal):
    segment_id: int = nx.key()
    timestamp: datetime = nx.timestamp()
    average_speed: Speed = nx.data(ge=0)
    total_flow: Flow = nx.data(ge=0)

    def from_pems_journal(self, pems_journal_list, coefficients):
        for pems, coef in zip(pems_journal_list, coefficients):
            self.average_speed += coef * pems.average_speed
            self.total_flow = coef * pems.total_flow