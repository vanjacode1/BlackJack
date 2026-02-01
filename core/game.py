from .shoe import Shoe
from .player_dealer import Player, Dealer
from .hand import Hand

class Game:
    def __init__(self, n_decks=2, bankroll=1000, current_bet=0):
        self.shoe = Shoe(n_decks)
        self.player = Player(bankroll)
        self.dealer = Dealer()
        self.current_bet = current_bet

    def reset_round(self):
        self.player.hand = Hand()
        self.dealer.hand = Hand()

    def initial_deal(self):
        for _ in range(2):
            self.player.hand.add_card(self.shoe.deal_one())
            self.dealer.hand.add_card(self.shoe.deal_one())

    def start_round(self):
        while True:
            bet_amount = input("Place bet (1, 5, 25, 50, 100, 500, all-in): ").strip().lower()
            if bet_amount in ["1", "5", "25", "50", "100", "500"]:
                bet_amount = int(bet_amount)
                if bet_amount <= self.player.bankroll:
                    self.current_bet = bet_amount
                    break
                else:
                    print("Not enough funds")
            elif bet_amount in ["all", "allin", "all-in"]:
                bet_amount = "all-in"
                self.current_bet = self.player.bankroll
                break
            else:
                print("Invalid bet")

    def player_turn(self):
        if self.player.hand.is_bust() or self.player.hand.is_blackjack():
            return "done" 
        
        fmt = lambda cs: ", ".join(f"{r}{s}" for r, s in cs)
        print(f"\nYour hand:  [{fmt(self.player.hand.cards)}] = {self.player.hand.value_hand()}")
        print(f"Dealer shows: [{fmt(self.dealer.hand.cards[:-1])}]")
        if not self.player.hand.is_bust() and not self.player.hand.is_blackjack():
            while True:
                user_input = input("[H]it or [S]tand: ").strip().lower()
                if user_input == "h" or user_input == "s":
                    break
            
            if user_input == "h":
                self.player.hand.add_card(self.shoe.deal_one())
                if self.player.hand.is_bust():
                    return "bust"
                if self.player.hand.value_hand() == 21:
                    return "s"
            return user_input

    def dealer_turn(self):
        if self.player.hand.is_bust():
            return
        if not self.dealer.hand.is_bust() and not self.dealer.hand.is_blackjack():
            self.dealer.hand.add_card(self.shoe.deal_one())

    def outcome(self):
        if self.player.hand.is_blackjack() and self.dealer.hand.is_blackjack():
            return "push"
        elif self.player.hand.is_blackjack():
            return "blackjack"
        elif self.player.hand.is_bust():
            return "lose"
        elif self.dealer.hand.is_bust():
            return "win"
        elif self.player.hand.value_hand() > self.dealer.hand.value_hand():
            return "win"
        elif self.player.hand.value_hand() < self.dealer.hand.value_hand():
            return "lose"
        elif self.player.hand.value_hand() == self.dealer.hand.value_hand():
            return "push"
        return "push"

    def payout(self, bet, result):
        if result == "blackjack":
            return bet * 3 // 2
        elif result == "win":
            return bet
        elif result == "push":
            return 0
        else:
            return -bet
        
    def place_bet(self, amount: int):
        if amount <= 0 or amount > self.player.bankroll:
            raise ValueError("Invalid bet")
        self.current_bet = amount

    def new_round(self):
        self.reset_round()
        self.initial_deal()

    def player_hit(self):
        self.player.hand.add_card(self.shoe.deal_one())

    def dealer_play(self):
        while self.dealer.hand.value_hand() < 17:
            self.dealer.hand.add_card(self.shoe.deal_one())

    def dealer_should_hit(self):
        return self.dealer.hand.value_hand() < 17

    def dealer_take_one(self):
        self.dealer.hand.add_card(self.shoe.deal_one())

    def settle(self):
        result = self.outcome()
        delta  = self.payout(self.current_bet, result) + self.current_bet
        self.player.bankroll += delta
        return result, delta