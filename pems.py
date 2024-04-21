from datetime import datetime
from typing import Dict

import anaximander as nx
import os

from requests import Session

BASE_URL = "https://pems.dot.ca.gov"
DISTRICT_ID = 4
WINDOW_SIZE = 900
WINDOW_PERIOD = 300


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
    BASE_URL = "https://pems.dot.ca.gov"

    @scheduler("1d")
    @csv
    @authentication(username=os.environ['USERNAME'], password=os.environ['PASSWORD'], url=BASE_URL)
    def from_link_source(cls, session: Session, scheduled_at: datetime):
        day_str = scheduled_at.strftime('%Y_%m_%d')

        # get information about available data within a year
        months = session.get(BASE_URL, params=
            {"srq": "clearinghouse", "district_id": DISTRICT_ID, "yy": day_str[:4],
             "type": "station_5min", "returnformat": "text"})
        months.raise_for_status()

        for files in months.json()['data'].values():
            for file in files:
                # if any file matches the date we want, download it
                if any(day_str in file['file_name']):
                    print(f"Upload {file['file_name']}.")
                    return session.get(BASE_URL + file['url'])


class SegmentPeMsJournal(nx.Journal):
    __station_to_segment: Dict
    segment_id: int = nx.key()
    timestamp: datetime = nx.timestamp()
    aggregated_speed: Speed = nx.data(ge=0)

    @nx.source
    def from_sample(cls):
        PeMSSample.map(
            cls.__station_to_segment, field="station_id", new_field="segment_ids"
        ).splitter(field="segment_ids", new_field="segment_id").group_by_key(
            key="segment_id"
        ).agg(
            get_pems_feature
        ).sliding_window(
            WINDOW_SIZE, WINDOW_PERIOD
        )
