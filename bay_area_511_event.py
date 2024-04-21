import os
from datetime import datetime
from typing import Optional

import anaximander as nx

BASE_URL = "https://511.org"

class Event(nx.Entity):
    pass


class EventSample(nx.Sample):
    pass


class EventSession(nx.Session):
    machine_id: int = nx.key()
    start_time: datetime = nx.start_time()
    end_time: datetime = nx.end_time()