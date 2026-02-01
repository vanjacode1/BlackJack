from config import VAL

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def has_ace(self):
        return any(r == 'A' for r, _ in self.cards)
    
    def value_hand(self):
        t = sum(VAL[r] for r,_ in self.cards)
        if self.has_ace() and t + 10 <= 21:
            return t + 10
        return t
    
    def is_blackjack(self):
        return len(self.cards) == 2 and self.value_hand() == 21
        
    def is_bust(self):
        return self.value_hand() > 21