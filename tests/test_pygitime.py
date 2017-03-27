import datetime
import pytest
from pygitime import _date_from_timestamp, _timeslot_from_timestamp


@pytest.mark.parametrize('epoch, expected_timeslot', ((0, 0), (899, 0), (900, 1), (1799, 1), (1800, 2)))
def test_timeslot_from_timestamp(epoch, expected_timeslot):
    assert expected_timeslot == _timeslot_from_timestamp(epoch)


@pytest.mark.parametrize('epoch, expected_date', (
    (1490577155, (2017, 3, 26)),
    (0, (1969, 12, 31)),
    (490577155, (1985, 7, 18)),
))
def test_date_from_timestamp(epoch, expected_date):
    expected_date = datetime.date(*expected_date)
    assert expected_date == _date_from_timestamp(epoch)
