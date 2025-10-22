class Account:
    def __init__(self, first_name, last_name, pesel=None, promo_code=None):
        self.first_name = first_name
        self.last_name = last_name
        self.balance = 0
        if pesel is not None and len(pesel) != 11:
            self.pesel = "Invalid"
        else:
            self.pesel = pesel
        if promo_code is not None and isinstance(promo_code, str) and promo_code.startswith("PROM_"):
            if self._is_eligible_for_promo():
                self.balance += 50

    def transfer_in(self, amount):
        self.balance += amount

    def transfer_out(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def express_transfer_out(self, amount):
        fee = 1
        if self.balance - amount - fee < -fee:
            raise ValueError("Insufficient funds for express transfer")
        self.balance -= (amount + fee)

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

    def transfer_in(self, amount):
        self.balance += amount

    def transfer_out(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def express_transfer_out(self, amount):
        fee = 5
        if self.balance - amount - fee < -fee:
            raise ValueError("Insufficient funds for express transfer")
        self.balance -= (amount + fee)