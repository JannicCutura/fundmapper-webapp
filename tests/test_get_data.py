from utils.get_data import get_data
import pytest

def test_get_data():
    assert not get_data().empty, "get_data() crashed"
    assert get_data().shape[0] > 4000, "Too few observations in data"
    assert (get_data().columns== ['date', 'type', 'investmenttypedomain', 'mean_yield', 'sum_amount']).all(), "Some columns are missing"


