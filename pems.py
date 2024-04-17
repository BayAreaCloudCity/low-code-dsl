from datetime import datetime
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
    BASE_URL = "https://pems.dot.ca.gov"

    @scheduler("1d")
    def from_link_source(cls):
        """
        same as collect_pems
        """


MINUTE = 60 * 60


class SegmentPeMsJournal(nx.Journal):
    segment_id: int = nx.key()
    timestamp: datetime = nx.timestamp()
    aggregated_speed: Speed = nx.data(ge=0)

    @nx.source
    def from_sample(cls):
        PeMSSample.map(
            __station_to_segment, field="station_id", new_field="segment_ids"
        ).splitter(field="segment_ids", new_field="segment_id").group_by_key(
            key="segment_id"
        ).agg(
            get_pems_feature
        ).fixed_windows(
            window_size, window_period
        )
