CARD_W, CARD_H = 70, 100
GAP = 18
FONT_RANK = ("Arial", 14, "bold")
FONT_SCORE = ("Arial", 12)
CHIP_VALUES = [1, 5, 25, 50, 100, 500]

RANKS = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
SUITS = ['♠','♥','♦','♣']
VAL = {r: 10 if r in {'J','Q','K'} else (1 if r == 'A' else int(r)) for r in RANKS}