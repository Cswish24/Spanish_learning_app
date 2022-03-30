
from tkinter import *
import pandas
import random

current_card = {}
BACKGROUND_COLOR = "#B1DDC6"
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")
data_dict = data.to_dict(orient="records")


def check_func(data_dict, current_card, flip_timer):

    data_dict.remove(current_card)
    next_word(flip_timer, current_card)


def english_side(current_card):
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def next_word(flip_timer, current_card):
    window.after_cancel(flip_timer)
    current_card.update(random.choice(data_dict))
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=lambda: english_side(current_card))
    return current_card


window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

check_img = PhotoImage(file="images/right.png")
check_button = Button(image=check_img, highlightthickness=0, command=lambda: check_func(data_dict, current_card, flip_timer))
check_button.grid(row=1, column=1)

x_img = PhotoImage(file="images/wrong.png")
x_button = Button(image=x_img, highlightthickness=0, command=lambda: next_word(flip_timer, current_card))
x_button.grid(row=1, column=0)

flip_timer = window.after(3000, func=english_side)
print(current_card)
next_word(flip_timer, current_card)
print(current_card)
window.mainloop()