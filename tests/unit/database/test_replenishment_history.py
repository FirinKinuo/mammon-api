import pytest

from datetime import datetime as datetime_

from mammon_api.db import replenishment

from tests.utils.common_fixtures import preload_database
from tests.utils.generators import random_string, random_int


@pytest.fixture()
def set_testing_replenishment():
    def set_replenishment(
            datetime: datetime_ = datetime_.now(),
            currency: int = random_int(5)) -> replenishment.ReplenishmentHistory:
        return replenishment.ReplenishmentHistory.set_or_get(datetime=datetime, currency=currency)

    return set_replenishment


def test_set_replenishment(set_testing_replenishment):
    replenishment_history_payload = {'datetime': datetime_.now(), 'currency': random_int(5)}

    set_replenishment_history = set_testing_replenishment(**replenishment_history_payload)

    assert isinstance(set_replenishment_history, replenishment.ReplenishmentHistory)
    assert set_replenishment_history.datetime == replenishment_history_payload['datetime']
    assert set_replenishment_history.currency == replenishment_history_payload['currency']


@pytest.mark.parametrize('invalid_data', [
    {'datetime': random_string(4), 'currency': random_string(4)},
    {'datetime': None, 'currency': None},
])
def test_set_invalid_replenishment(invalid_data):
    with pytest.raises(ValueError):
        replenishment.ReplenishmentHistory.set(**invalid_data)


def test_get_replenishment(set_testing_replenishment):
    set_replenishment = set_testing_replenishment()

    get_replenishment = replenishment.ReplenishmentHistory.get_all(
        id=set_replenishment.id,
        datetime=set_replenishment.datetime,
        currency=set_replenishment.currency
    )

    assert len(get_replenishment) == 1

    assert set_replenishment.id == get_replenishment[0].id
    assert set_replenishment.datetime == get_replenishment[0].datetime
    assert set_replenishment.currency == get_replenishment[0].currency


@pytest.mark.parametrize('replenishment_data', [
    {'id': -1},
    {'id': None},
    {'datetime': datetime_.now()},
    {'datetime': None},
    {'currency': random_int(6)},
    {'currency': None}
])
def test_get_non_existent_one_c_bases(replenishment_data):
    get_one_c_bases = replenishment.ReplenishmentHistory.get_all(**replenishment_data)

    assert get_one_c_bases == []
