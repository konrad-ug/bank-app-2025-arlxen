
import pytest
from src.account import Account




@pytest.fixture
def account():
    return Account("Anna", "Nowak")

def test_account_creation():
    acc = Account("John", "Doe")
    assert acc.first_name == "John"
    assert acc.last_name == "Doe"

def test_account_history_incoming(account):
    account.transfer_in(500)
    assert account.historia == [500]

def test_account_history_outgoing(account):
    account.transfer_in(500)
    account.transfer_out(300)
    assert account.historia == [500, -300]

def test_account_history_express(account):
    account.transfer_in(500)
    account.express_transfer_out(300)
    assert account.historia == [500, -300, -1]
