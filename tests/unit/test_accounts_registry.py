import pytest
from src.account import Account
from src.account import AccountsRegistry

@pytest.fixture
def registry():
    return AccountsRegistry()

@pytest.fixture
def personal_account():
    return Account("Jan", "Kowalski", pesel="12345678901")

def test_add_and_count(registry, personal_account):
    registry.add_account(personal_account)
    assert registry.count() == 1

def test_find_by_pesel(registry, personal_account):
    registry.add_account(personal_account)
    found = registry.find_by_pesel("12345678901")
    assert found is personal_account

def test_get_all(registry, personal_account):
    registry.add_account(personal_account)
    accounts = registry.get_all()
    assert personal_account in accounts
