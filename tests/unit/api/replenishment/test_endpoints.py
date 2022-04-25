import pytest

from datetime import datetime

from starlette import status

from .mocks.mock_replenishment_db import (
    mock_get_pool_by_datetime
)
from tests.unit.api import client


def test_read_replenishments_by_date(mock_get_pool_by_datetime):
    replenishments_dates = {'start': datetime.now(), 'end': datetime.now()}
    mock_get_pool_by_datetime(datetime_start=replenishments_dates['start'], datetime_end=replenishments_dates['end'])

    response = client.get(
        '/api/v1/replenishments',
        json={
            'start': str(replenishments_dates['start']),
            'end': str(replenishments_dates['end'])
        }
    )
    response_body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert len(response_body) == 2
    assert datetime.strptime(response_body[0]['datetime'], "%Y-%m-%dT%H:%M:%S.%f") == replenishments_dates['start']
    assert datetime.strptime(response_body[1]['datetime'], "%Y-%m-%dT%H:%M:%S.%f") == replenishments_dates['end']

    for response_ in response_body:
        assert isinstance(response_['id'], int)
        assert isinstance(response_['currency'], int)
