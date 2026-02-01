from .hand import Hand

class Player:
    def __init__(self, bankroll = 1000):
        self.bankroll = bankroll
        self.hand = Hand()

class Dealer:
    def __init__(self):
        self.hand = Hand()