class Account:
    def __init__(self, first_name, last_name, pesel=None, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        self.historia = []
        if pesel is not None and len(pesel) != 11:
            self.pesel = "Invalid"
        else:
            self.pesel = pesel
        if promo_code is not None and isinstance(promo_code, str) and promo_code.startswith("PROM_"):
            if self._is_eligible_for_promo():
                self.balance += 50

    def transfer_in(self, amount):
        self.balance += amount
        self.historia.append(amount)

    def transfer_out(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.historia.append(-amount)

    def express_transfer_out(self, amount):
        fee = 1
        if self.balance - amount - fee < -fee:
            raise ValueError("Insufficient funds for express transfer")
        self.balance -= (amount + fee)
        self.historia.append(-amount)
        self.historia.append(-fee)


# Registry for personal accounts
class AccountsRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def find_by_pesel(self, pesel):
        for acc in self.accounts:
            if hasattr(acc, 'pesel') and acc.pesel == pesel:
                return acc
        return None

    def get_all(self):
        return self.accounts

    def count(self):
        return len(self.accounts)

    def submit_for_loan(self, amount):
        # Only for personal accounts
        # Condition 1: Last 3 transactions are deposits
        last_three = self.historia[-3:] if len(self.historia) >= 3 else []
        deposits_only = all(x > 0 for x in last_three)
        # Condition 2: Sum of last 5 transactions > amount
        last_five = self.historia[-5:] if len(self.historia) >= 5 else []
        sufficient_sum = sum(last_five) > amount if len(last_five) == 5 else False
        if deposits_only or sufficient_sum:
            self.balance += amount
            self.historia.append(amount)
            return True
        return False

    def _is_eligible_for_promo(self):
        if not self.pesel or self.pesel == "Invalid" or len(self.pesel) != 11:
            return False
        year = int(self.pesel[:2])
        month = int(self.pesel[2:4])
        if 1 <= month <= 12:
            birth_year = 1900 + year
        elif 21 <= month <= 32:
            birth_year = 2000 + year
        elif 81 <= month <= 92:
            birth_year = 1800 + year
        else:
            return False
        return birth_year > 1960


class BusinessAccount:
    def __init__(self, company_name, nip, promo_code=None):
        self.company_name = company_name
        if nip is not None and len(nip) != 10:
            self.nip = "Invalid"
        else:
            self.nip = nip
        self.balance = 0
        self.historia = []

    def transfer_in(self, amount):
        self.balance += amount
        self.historia.append(amount)

    def transfer_out(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.historia.append(-amount)

    def express_transfer_out(self, amount):
        fee = 5
        if self.balance - amount - fee < -fee:
            raise ValueError("Insufficient funds for express transfer")
        self.balance -= (amount + fee)
        self.historia.append(-amount)
        self.historia.append(-fee)

    def take_loan(self, amount):
        # Condition 1: balance at least 2x amount
        # Condition 2: at least one outgoing transfer of exactly 1775 (ZUS)
        has_zus = any(x == -1775 for x in self.historia)
        if self.balance >= 2 * amount and has_zus:
            self.balance += amount
            self.historia.append(amount)
            return True
        return False