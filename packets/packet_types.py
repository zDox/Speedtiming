from dataclasses import dataclass


@dataclass
class Start:
    start_time: float


@dataclass
class StartStarter:
    pass


@dataclass
class StatusRequest:
    status_type: str


@dataclass
class StatusAnswer:
    status_type: str
    track_clear: bool
