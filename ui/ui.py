import tkinter as tk
from core import Game
from tkinter import messagebox
from functools import partial
from config import CARD_H, CARD_W, CHIP_VALUES, GAP, FONT_RANK, FONT_SCORE

def draw_card(canvas, x, y, rank, suit, face_up=True):
    canvas.create_rectangle(x, y, x+CARD_W, y+CARD_H, outline="black", width=2,
                            fill=("white" if face_up else "gray70"))
    if face_up:
        canvas.create_text(x+10, y+12, text=rank, anchor="nw", font=FONT_RANK)
        canvas.create_text(x+CARD_W-10, y+CARD_H-12, text=suit, anchor="se", font=FONT_RANK)
    else:
        canvas.create_text(x+CARD_W/2, y+CARD_H/2, text="?", font=("Arial", 20, "bold"))

class App(tk.Tk):
    def __init__(self):
        super().__init__()                 
        self.title("Blackjack")  
        self.resizable(False, False)    
        self.game = Game(n_decks=2, bankroll=1000) 

        self.info = tk.StringVar(value="Welcome to Blackjack!\nPlace a bet and press Deal.")
        tk.Label(self, textvariable=self.info, font=("Arial", 12)).pack(pady=25)  

        top = tk.Frame(self)
        top.pack(pady=4)

        self.bank = tk.StringVar(value=f"Bankroll: {self.game.player.bankroll}")
        tk.Label(top, textvariable=self.bank, font=("Arial", 11)).pack(side="left", padx=20)

        #self.bet_var = tk.IntVar(value=min(25, self.game.player.bankroll))
        self.bet_var = tk.IntVar(value=0)
        self.bet_display = tk.StringVar(value="0")

        betbar = tk.Frame(self)
        betbar.pack(pady=2)
        tk.Label(betbar, text="Bet:", font=("Arial", 11)).pack(side="left")
        tk.Label(betbar, textvariable=self.bet_display, font=("Arial", 11, "bold")).pack(side="left", padx=5)

        chips = tk.Frame(self); chips.pack(pady=4)
        self.chip_btns = []
        for i, v in enumerate(CHIP_VALUES):
            b = tk.Button(chips, text=str(v), width=4,
                  command=partial(self.add_bet, v))
            b.grid(row=0, column=i, padx=1)
            self.chip_btns.append((v, b))

        self.allin_btn = tk.Button(chips, text="All-in", width=6, command=self.all_in)
        self.clear_btn = tk.Button(chips, text="Clear",  width=6, command=self.clear_bet)
        self.allin_btn.grid(row=1, column=0, columnspan=3, pady=4)
        self.clear_btn.grid(row=1, column=3, columnspan=3, pady=4)

        self.canvas = tk.Canvas(self, width=600, height=300, bg="darkgreen")
        self.canvas.pack(padx=10, pady=8)

        buttons = tk.Frame(self); buttons.pack(pady=8)
        self.deal_btn = tk.Button(buttons, text="Deal", width=10, command=self.on_deal)
        self.hit_btn = tk.Button(buttons, text="Hit", width=10, state="disabled", command=self.on_hit)
        self.stand_btn = tk.Button(buttons, text="Stand", width=10, state="disabled", command=self.on_stand)
        self.deal_btn.grid(row=0, column=0, padx=5)
        self.hit_btn.grid(row=0, column=1, padx=5)
        self.stand_btn.grid(row=0, column=2, padx=5)
        self.phase_idle()

    def fmt_cards(self, cards):
        return " ".join(f"{r}{s}" for r, s in cards)

    def phase_idle(self):
        self.deal_btn.config(state="normal")
        self.hit_btn.config(state="disabled")
        self.stand_btn.config(state="disabled")
        self.update_chip_states(enable=True)

    def phase_player(self):
        self.deal_btn.config(state="disabled")
        self.hit_btn.config(state="normal")
        self.stand_btn.config(state="normal")
        self.update_chip_states(enable=False)

    def phase_locked(self):
        self.deal_btn.config(state="disabled")
        self.hit_btn.config(state="disabled")
        self.stand_btn.config(state="disabled")
        self.update_chip_states(enable=False)

    def on_deal(self):
        if self.bet_var.get() > self.game.player.bankroll:
            self.bet_var.set(self.game.player.bankroll)
            self.update_bet_display()       
            self.update_chip_states()
        if self.game.player.bankroll == 0:
            messagebox.showerror("Bet error", "You have no more money")
            return
        if self.bet_var.get() <= 0:
            messagebox.showerror("Bet error", "Place a bet.")
            return
        # place bet & deal
        self.game.place_bet(self.bet_var.get())
        self.game.player.bankroll -= self.game.current_bet
        self.game.new_round()
        self.info.set("Your turn: Hit or Stand.")
        self.phase_player()
        #self.refresh_labels(hide_dealer_hole=True)
        self.render_table(hide_dealer_hole=True)
        if self.game.player.hand.is_blackjack():
            self.on_stand()

    def on_hit(self):
        self.game.player_hit()
        self.render_table(hide_dealer_hole=True)
        if self.game.player.hand.is_bust():
            self.info.set(f"You busted ({self.game.player.hand.value_hand()}).")
            self.finish_round()
        elif self.game.player.hand.value_hand() == 21:
            self.on_stand()

    def on_stand(self):
        self.phase_locked()
        self.info.set("Dealer plays...")
        self.render_table(hide_dealer_hole=False)
        self.after(1500, self.dealer_draw_step)

    def dealer_draw_step(self):
        if self.game.dealer_should_hit():
            self.game.dealer_take_one()
            self.render_table(hide_dealer_hole=False)
            self.after(1500, self.dealer_draw_step)
        else:
            self.finish_round()

    def finish_round(self):
        result, delta = self.game.settle()
        self.render_table(hide_dealer_hole=False)
        if self.game.player.bankroll == 0:
            self.info.set(f"Seems like luck is not on your side today. \n Better luck next time!")
        elif self.game.player.hand.value_hand() == self.game.dealer.hand.value_hand():
            self.info.set(f"Push!")
        else:
            self.info.set(f"Result: {result}  ({delta:+}). \n Place a bet and press deal for next hand.")
        self.bet_var.set(0)
        self.phase_idle()
        self.update_bet_display()
        self.update_chip_states()


    def render_table(self, hide_dealer_hole=True):
        self.canvas.delete("all") 
        self.bank.set(f"Bankroll: {self.game.player.bankroll}")

        self.canvas.create_text(20, 20,  text="Dealer", anchor="nw", fill="white", font=("Arial", 12, "bold"))
        self.canvas.create_text(20, 160, text="Player", anchor="nw", fill="white", font=("Arial", 12, "bold"))

        x0 = 100
        for i, (r, s) in enumerate(self.game.dealer.hand.cards):
            face_up = not (hide_dealer_hole and i == len(self.game.dealer.hand.cards)-1)
            draw_card(self.canvas, x0 + i*(CARD_W+20), 10, r, s, face_up=face_up)

        x0 = 100
        for i, (r, s) in enumerate(self.game.player.hand.cards):
            draw_card(self.canvas, x0 + i*(CARD_W+20), 150, r, s, face_up=True)

        pv = self.game.player.hand.value_hand()
        self.canvas.create_text(20, 190+CARD_H, text=f"Player: {pv}", anchor="sw", fill="white", font=FONT_SCORE)
        if not hide_dealer_hole:
            dv = self.game.dealer.hand.value_hand()
            self.canvas.create_text(20, 50+CARD_H, text=f"Dealer: {dv}", anchor="sw", fill="white", font=FONT_SCORE)

    def update_bet_display(self):
        self.bet_display.set(str(self.bet_var.get()))

    def add_bet(self, amount):
        new_bet = min(self.bet_var.get() + amount, self.game.player.bankroll)
        self.bet_var.set(new_bet)
        self.update_bet_display()
        self.update_chip_states()

    def clear_bet(self):
        self.bet_var.set(0)
        self.update_bet_display()
        self.update_chip_states()

    def all_in(self):
        self.bet_var.set(self.game.player.bankroll)
        self.update_bet_display()
        self.update_chip_states()

    def update_chip_states(self, enable=True):
        if not enable:
            for _, b in self.chip_btns:
                b.config(state="disabled")
            self.allin_btn.config(state="disabled")
            self.clear_btn.config(state="disabled")
            return

        remaining = self.game.player.bankroll - self.bet_var.get()

        for v, b in self.chip_btns:
            if v <= remaining:
                b.config(state="normal")
            else:
                b.config(state="disabled")

        if self.game.player.bankroll > 0:
            self.allin_btn.config(state="normal")
        else:
            self.allin_btn.config(state="disabled")

        if self.bet_var.get() > 0:
            self.clear_btn.config(state="normal")
        else:
            self.clear_btn.config(state="disabled")