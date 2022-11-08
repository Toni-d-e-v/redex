class Chain():
    def __init__(self, publickey, balance, transactions):
        self.publickey = publickey
        self.balance = balance
        self.transactions = transactions
    
    def add_transaction(self, tx):
        self.transactions.append(tx)
    
class Balance():
    def __init__(self, spendable, locked):
        self.spendable = spendable
        self.locked = locked
    
    def delta_spendable(self, amount):
        self.spendable -= amount
        if (self.spendable < 0):
            return False
        else:
            return True
    
    def delta_locked(self, amount):
        self.locked -= amount
        if (self.locked < 0):
            return False
        else:
            return True