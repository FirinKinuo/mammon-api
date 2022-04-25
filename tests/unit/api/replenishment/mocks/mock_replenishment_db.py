from datetime import datetime
from typing import Callable

import pytest

from pytest_mock import MockerFixture

from mammon_api.db import replenishment

from tests.utils.generators import random_int


@pytest.fixture()
def mock_get_pool_by_datetime(mocker: MockerFixture) -> Callable:
    def mock(datetime_start: datetime, datetime_end: datetime):
        return_value = [
            replenishment.ReplenishmentHistory(
                id=random_int(2),
                datetime=datetime_,
                currency=random_int(4)
            ) for datetime_ in [datetime_start, datetime_end]
        ]

        mocker.patch.object(
            replenishment.ReplenishmentHistory,
            'get_pool_by_datetime',
            return_value=return_value
        )

    return mock
