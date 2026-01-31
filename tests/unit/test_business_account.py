import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from src.account import BusinessAccount

class TestBusinessAccount:
    def test_company_fields(self):
        acc = BusinessAccount(company_name="ACME Sp. z o.o.", nip="1234567890")
        assert acc.company_name == "ACME Sp. z o.o."
        assert acc.nip == "1234567890"

    def test_business_history_incoming(self):
        acc = BusinessAccount(company_name="FirmaX", nip="1234567890")
        acc.transfer_in(1000)
        assert acc.historia == [1000]

    def test_business_history_outgoing(self):
        acc = BusinessAccount(company_name="FirmaX", nip="1234567890")
        acc.transfer_in(1000)
        acc.transfer_out(400)
        assert acc.historia == [1000, -400]

    def test_business_history_express(self):
        acc = BusinessAccount(company_name="FirmaX", nip="1234567890")
        acc.transfer_in(1000)
        acc.express_transfer_out(400)
        # -400 za przelew, -5 za opłatę
        assert acc.historia == [1000, -400, -5]

    def test_invalid_nip(self):
        acc = BusinessAccount(company_name="FirmaX", nip="123")
        assert acc.nip == "Invalid"

    def test_transfer_in_and_out(self):
        acc = BusinessAccount(company_name="FirmaX", nip="1234567890")
        acc.balance = 100
        acc.transfer_in(50)
        assert acc.balance == 150
        acc.transfer_out(30)
        assert acc.balance == 120
    
    def test_no_promo_for_business(self):
        acc = BusinessAccount(company_name="FirmaX", nip="1234567890", promo_code="PROM_ABC")
        assert acc.balance == 0
