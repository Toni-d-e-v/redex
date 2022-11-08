import hashlib

from chain import Balance

class State():
    def __init__(self, chains, balances): # chains is an array of the publickeys of the chains referenced in this state, balances is an array of the balance objects
        if (len(chains) != len(balances)): # There must be a balance obejct for every chain
            return
        self.chains = chains
        self.balances = balances

        self.checksum = self.hash()

    def hash(self):
        hasher = hashlib.sha256()
        for chain in self.chains:
            hasher.update(chain.encode())
        
        for balance in self.balances:
            hasher.update(str(balance.spendable).encode())
            hasher.update(str(balance.locked).encode())
            
        return hasher.hexdigest()

    def apply_state_delta(self, state_delta):
        # Applys a state delta to this state
        bal_pos = None
        try:
            bal_pos = self.chains.index(state_delta.chain)
        except:
            # Chain is not currently in this state
            bal_pos = len(self.chains)
            self.chains.append(state_delta.chain)
            self.balances.append(Balance(0, 0))
        
        if (not self.balances[bal_pos].delta_spendable(state_delta.spendable_delta)):
            return False # Failed to delta spendable balance (results in a spendable balance < 0)
        else:
            return self.balances[bal_pos].delta_locked(state_delta.locked_delta)


class StateDelta():
    def __init__(self, chain, spendable_delta, locked_delta):
        self.chain = chain
        self.spendable_delta = spendable_delta
        self.locked_delta = locked_delta