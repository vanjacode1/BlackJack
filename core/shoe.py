import random
from config import RANKS, SUITS

class Shoe:
    def __init__(self, n_decks=6):
        self.n_decks = n_decks
        self.cards = [(r, s) for _ in range(n_decks) for r in RANKS for s in SUITS]
        random.shuffle(self.cards)
    
    def deal_one(self):
        if not self.cards:  
            self.cards = [(r, s) for _ in range(self.n_decks) for r in RANKS for s in SUITS]
            random.shuffle(self.cards)
        return self.cards.pop()