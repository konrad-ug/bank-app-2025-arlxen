import pytest
from src.account import Account

@pytest.mark.parametrize("history,amount,expected", [
    ([100, 200, 300], 1000, True),
    ([100, 200, -50, 300, 400], 500, True),
    ([100, -50, 200, -30, 400], 800, False), 
    ([100, 200], 100, False),
])
def test_submit_for_loan(history, amount, expected):
    account = Account("Jan", "Kowalski")
    for h in history:
        if h > 0:
            account.transfer_in(h)
        else:
            account.transfer_out(-h)
    result = account.submit_for_loan(amount)
    assert result is expected
    if expected:
        assert account.balance == sum(history) + amount
    else:
        assert account.balance == sum(history)
