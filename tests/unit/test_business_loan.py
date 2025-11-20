import pytest
from src.account import BusinessAccount

@pytest.mark.parametrize("balance, history, amount, expected", [
    (5000, [-1775], 2000, True),  # enough balance, ZUS transfer
    (4000, [-1000, -1775], 1500, True),  # enough balance, ZUS transfer
    (3000, [-1000, -500], 1000, False),  # no ZUS transfer
    (3000, [-1775], 2000, False),  # not enough balance
    (5000, [], 2000, False),  # no ZUS transfer
])
def test_take_loan(balance, history, amount, expected):
    acc = BusinessAccount(company_name="FirmaX", nip="1234567890")
    acc.balance = balance
    for h in history:
        if h > 0:
            acc.transfer_in(h)
        else:
            acc.historia.append(h)  # direct append for ZUS transfer
    result = acc.take_loan(amount)
    assert result is expected
    if expected:
        assert acc.balance == balance + amount
    else:
        assert acc.balance == balance
