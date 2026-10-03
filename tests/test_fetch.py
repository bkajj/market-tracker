import json
from datetime import date

import pytest
import requests

from market_tracker.fetch import fetch_to_file, FetchAPIException

class FakeResponse:
    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"status {self.status_code}")

@pytest.fixture
def api_token(monkeypatch):
    monkeypatch.setenv("STOCKDATA_API_TOKEN", "test-token")

@pytest.fixture
def mock_api(monkeypatch):
    def _mock(payload, status_code=200):
        monkeypatch.setattr("market_tracker.fetch.requests.get", lambda *args, **kwargs: FakeResponse(payload, status_code))
    return _mock


def test_fetch_to_file_writes_partitioned_file(tmp_path, api_token, mock_api):
    payload = {"meta": {"date_from": "2026-09-25"}, "data": [{"ticker": "AAPL"}]}
    mock_api(payload)

    path = fetch_to_file("AAPL", "hour", date(2026, 9, 25), tmp_path)

    expected = tmp_path / "raw" / "intraday" / "interval=hour" / "ticker=AAPL" / "date=2026-09-25.json"
    assert path == expected
    assert json.loads(path.read_text()) == payload


def test_fetch_to_file_raises_on_api_error(tmp_path, api_token, mock_api):
    payload = {"error": {"code": "404", "message": "not found"}}
    mock_api(payload)

    with pytest.raises(FetchAPIException) as exc_info:
        fetch_to_file("AAPL", "hour", date(2026, 9, 25), tmp_path)

    assert exc_info.value.code == "404"
    assert str(exc_info.value) == "not found"
    assert len(list(tmp_path.rglob("*.json"))) == 0


def test_fetch_to_file_no_api_token(tmp_path, monkeypatch):
    monkeypatch.delenv("STOCKDATA_API_TOKEN", raising=False)

    with pytest.raises(RuntimeError, match="STOCKDATA_API_TOKEN"):
        fetch_to_file("AAPL", "hour", date(2026, 9, 25), tmp_path)


def test_fetch_to_file_idempotent(tmp_path, api_token, mock_api):
    payload = {"meta": {"date_from": "2026-09-25"}, "data":[{"ticker": "AAPL"}]}
    mock_api(payload)

    fetch_to_file("AAPL", "hour", date(2026, 9, 25), tmp_path)
    fetch_to_file("AAPL", "hour", date(2026, 9, 25), tmp_path)

    assert len(list(tmp_path.rglob("*.json"))) == 1
