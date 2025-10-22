import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from src.account import Account

class TestAccountTransfers:
    def test_outgoing_transfer_reduces_balance(self):
        acc = Account("Jan", "Kowalski", pesel="12345678901")
        acc.balance = 100
        acc.transfer_out(30)
        assert acc.balance == 70

    def test_incoming_transfer_increases_balance(self):
        acc = Account("Jan", "Kowalski", pesel="12345678901")
        acc.balance = 10
        acc.transfer_in(50)
        assert acc.balance == 60

    def test_cannot_transfer_out_more_than_balance(self):
        acc = Account("Jan", "Kowalski", pesel="12345678901")
        acc.balance = 20
        with pytest.raises(ValueError):
            acc.transfer_out(25)
