import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from src.account import Account, BusinessAccount

class TestExpressTransfers:
    def test_personal(self):
        acc = Account("Jan", "Kowalski", pesel="12345678901")
        acc.balance = 100
        acc.express_transfer_out(20)
        assert acc.balance == 79

    def test_business(self):
        acc = BusinessAccount(company_name="FirmaX", nip="1234567890")
        acc.balance = 100
        acc.express_transfer_out(20)
        assert acc.balance == 75

    def test_personal_negative_fee(self):
        acc = Account("Jan", "Kowalski", pesel="12345678901")
        acc.balance = 1
        acc.express_transfer_out(1)
        assert acc.balance == -1

    def test_business_negative_fee(self):
        acc = BusinessAccount(company_name="FirmaX", nip="1234567890")
        acc.balance = 2
        acc.express_transfer_out(2)
        assert acc.balance == -5

    def test_cannot_go_below_fee(self):
        acc = Account("Jan", "Kowalski", pesel="12345678901")
        acc.balance = 0
        with pytest.raises(ValueError):
            acc.express_transfer_out(1)
