from my_widget.processing import filter_by_state

records = [
    {"id": 41428829, "state": "EXECUTED", "date": "..."},
    {"id": 594226727, "state": "CANCELED", "date": "..."},
    {"id": 939719570, "state": "EXECUTED", "date": "..."},
]

assert filter_by_state(records) == [
    {"id": 41428829, "state": "EXECUTED", "date": "..."},
    {"id": 939719570, "state": "EXECUTED", "date": "..."},
]

assert filter_by_state(records, state="CANCELED") == [
    {"id": 594226727, "state": "CANCELED", "date": "..."}
]
