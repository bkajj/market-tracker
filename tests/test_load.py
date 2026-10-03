import json
import pytest

from market_tracker.load import _to_record, load_to_db


SAMPLE_RECORD = {
    "date": "2026-09-24T09:00:00.000Z",
    "ticker": "AAPL",
    "data": {
        "open": 336.38,
        "high": 337.48,
        "low": 334.33,
        "close": 337.33,
        "volume": 116352,
        "is_extended_hours": True
    }
}

EMPTY_RESPONSE = {
    "meta": {
        "date_from": "2026-09-28",
        "date_to": "2026-09-28",
        "max_period_days": 180
    },
    "data": []
}

def test_to_record_maps_api_fields():
    assert _to_record(SAMPLE_RECORD, "hour") == {
        'ticker': "AAPL",
        'timestamp': "2026-09-24T09:00:00.000Z",
        'interval': "hour",
        "open": 336.38,
        "high": 337.48,
        "low": 334.33,
        "close": 337.33,
        'volume': 116352,
        'ext_hours': True,
    }

def test_load_to_db_raises_on_empty_data(tmp_path):
    path = tmp_path / "file.json"
    path.write_text(json.dumps(EMPTY_RESPONSE))

    with pytest.raises(RuntimeError, match="No data"):
        load_to_db(path, "hour", None)

