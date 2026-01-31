from src.account import Account



class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe")
        assert account.first_name == "John"
        assert account.last_name == "Doe"

    def test_account_history_incoming(self):
        account = Account("Anna", "Nowak")
        account.transfer_in(500)
        assert account.historia == [500]

    def test_account_history_outgoing(self):
        account = Account("Anna", "Nowak")
        account.transfer_in(500)
        account.transfer_out(300)
        assert account.historia == [500, -300]

    def test_account_history_express(self):
        account = Account("Anna", "Nowak")
        account.transfer_in(500)
        account.express_transfer_out(300)
        # -300 za przelew, -1 za opłatę
        assert account.historia == [500, -300, -1]
