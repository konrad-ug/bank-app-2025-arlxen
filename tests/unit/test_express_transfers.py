import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from src.account import Account, BusinessAccount


import pytest

@pytest.fixture
def personal_acc():
    return Account("Jan", "Kowalski", pesel="12345678901")

@pytest.fixture
def business_acc():
    return BusinessAccount(company_name="FirmaX", nip="1234567890")

@pytest.mark.parametrize("acc_type, start_balance, transfer, expected_balance", [
    ("personal", 100, 20, 79),
    ("business", 100, 20, 75),
    ("personal", 1, 1, -1),
    ("business", 2, 2, -5)
])
def test_express_transfer(acc_type, start_balance, transfer, expected_balance, personal_acc, business_acc):
    acc = personal_acc if acc_type == "personal" else business_acc
    acc.balance = start_balance
    acc.express_transfer_out(transfer)
    assert acc.balance == expected_balance

def test_cannot_go_below_fee(personal_acc):
    personal_acc.balance = 0
    with pytest.raises(ValueError):
        personal_acc.express_transfer_out(1)
