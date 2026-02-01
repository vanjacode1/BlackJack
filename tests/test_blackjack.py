import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] 
sys.path.insert(0, str(ROOT))

from main import Hand, Game

def make_hand(cards):
    h = Hand()
    for c in cards:
        h.add_card(c)
    return h

def test_count():
    cards1 = [('8', '♣'), ('A', '♥'), ('A', '♥'), ('2', '♥')]
    cards2 = [('8', '♣'), ('A', '♥'), ('2', '♥')]
    cards3 = [('A', '♣'), ('K', '♥')]
    cards4 = [('A', '♣'), ('8', '♥')]

    assert make_hand(cards1).value_hand() == 12
    assert make_hand(cards2).value_hand() == 21
    assert make_hand(cards3).value_hand() == 21
    assert make_hand(cards4).value_hand() == 19


def test_blackjack():
    cards1 = [('A','♠'), ('K','♦')]
    assert make_hand(cards1).is_blackjack() is True 

def test_is_bust():
    cards = [('8', '♣'), ('8', '♥'), ('2', '♥'), ('8', '♣')]
    cards2 = [('8', '♣'), ('A', '♥'), ('2', '♥'), ('8', '♣')]

    assert make_hand(cards).is_bust() is True 
    assert make_hand(cards2).is_bust() is False and make_hand(cards2).value_hand() == 19

def test_player_win():
    game = Game()

    player_cards = [('8', '♣'), ('A', '♥'), ('2', '♥'), ('8', '♣')]
    game.player.hand
    for card in player_cards:
        game.player.hand.add_card(card)

    dealer_cards = [('8', '♣'), ('8', '♥')]
    game.dealer.hand
    for card in dealer_cards:
        game.dealer.hand.add_card(card)

    assert game.outcome() == "win"
