import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from src.account import Account


@pytest.fixture
def acc():
    a = Account("Jan", "Kowalski", pesel="12345678901")
    return a

@pytest.mark.parametrize("start_balance,transfer,expected_balance", [
    (100, 30, 70),
    (10, -50, 60)
])
def test_transfer_balance(acc, start_balance, transfer, expected_balance):
    acc.balance = start_balance
    if transfer > 0:
        acc.transfer_out(transfer)
    else:
        acc.transfer_in(-transfer)
    assert acc.balance == expected_balance

def test_cannot_transfer_out_more_than_balance(acc):
    acc.balance = 20
    with pytest.raises(ValueError):
        acc.transfer_out(25)
