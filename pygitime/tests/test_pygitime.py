import datetime
import pytz
import pytest
from pygitime import date_from_timestamp, timeslot_from_timestamp


@pytest.mark.parametrize('epoch, expected_timeslot', ((0, 0), (899, 0), (900, 1), (1799, 1), (1800, 2)))
def test_timeslot_from_timestamp(epoch, expected_timeslot):
    assert expected_timeslot == timeslot_from_timestamp(epoch)


@pytest.mark.parametrize('epoch, expected_date', (
    (1490577155, (2017, 3, 27)),
    (0, (1970, 1, 1)),
    (490577155, (1985, 7, 18)),
))
def test_date_from_timestamp(epoch, expected_date):
    expected_date = datetime.datetime(*expected_date, tzinfo=pytz.utc).date()
    assert expected_date == date_from_timestamp(epoch)
