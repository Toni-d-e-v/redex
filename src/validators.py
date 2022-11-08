class Fullnode():
    def __init__(self, publickey, eclosed, online, stagnation_epochs_remaining):
        self.publickey = publickey
        self.stagnated = stagnation_epochs_remaining == 0
        self.eclosed = eclosed
        self.online = online
        self.stagnation_epochs_remaining = stagnation_epochs_remaining
        