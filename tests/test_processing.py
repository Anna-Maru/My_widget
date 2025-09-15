from src.processing import filter_by_state


def test_filter_by_state_default():
    records = [
        {"id": 41428829, "state": "EXECUTED", "date": "..."},
        {"id": 594226727, "state": "CANCELED", "date": "..."},
        {"id": 939719570, "state": "EXECUTED", "date": "..."},
    ]

    assert filter_by_state(records) == [
        {"id": 41428829, "state": "EXECUTED", "date": "..."},
        {"id": 939719570, "state": "EXECUTED", "date": "..."},
    ]


def test_filter_by_state_canceled():
    records = [
        {"id": 41428829, "state": "EXECUTED", "date": "..."},
        {"id": 594226727, "state": "CANCELED", "date": "..."},
        {"id": 939719570, "state": "EXECUTED", "date": "..."},
    ]

    assert filter_by_state(records, state="CANCELED") == [
        {"id": 594226727, "state": "CANCELED", "date": "..."}
    ]
