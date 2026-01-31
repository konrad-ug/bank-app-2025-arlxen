import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from src.account import BusinessAccount


import pytest

@pytest.fixture
def business_acc():
    return BusinessAccount(company_name="FirmaX", nip="1234567890")

@pytest.mark.parametrize("company_name,nip,expected_nip", [
    ("ACME Sp. z o.o.", "1234567890", "1234567890"),
    ("FirmaX", "123", "Invalid")
])
def test_company_fields(company_name, nip, expected_nip):
    acc = BusinessAccount(company_name=company_name, nip=nip)
    assert acc.company_name == company_name
    assert acc.nip == expected_nip

def test_business_history_incoming(business_acc):
    business_acc.transfer_in(1000)
    assert business_acc.historia == [1000]

def test_business_history_outgoing(business_acc):
    business_acc.transfer_in(1000)
    business_acc.transfer_out(400)
    assert business_acc.historia == [1000, -400]

def test_business_history_express(business_acc):
    business_acc.transfer_in(1000)
    business_acc.express_transfer_out(400)
    assert business_acc.historia == [1000, -400, -5]

def test_transfer_in_and_out(business_acc):
    business_acc.balance = 100
    business_acc.transfer_in(50)
    assert business_acc.balance == 150
    business_acc.transfer_out(30)
    assert business_acc.balance == 120

def test_no_promo_for_business():
    acc = BusinessAccount(company_name="FirmaX", nip="1234567890", promo_code="PROM_ABC")
    assert acc.balance == 0
