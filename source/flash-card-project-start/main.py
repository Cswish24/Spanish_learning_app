BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
# import pandas
import random
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from api_test import translate
from dotenv import load_dotenv

class Word_form(FlaskForm):
    word = StringField('word', validators=[DataRequired()])
    submit = SubmitField('submit words')



app = Flask(__name__)
app.config['SECRET_KEY'] = "S8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spanish_english_words.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Word_DB(db.Model):
    __tablename__ = "Word Database"
    id = db.Column(db.Integer, primary_key=True)
    English_word = db.Column(db.String(30), unique=True)
    Spanish_word = db.Column(db.String(30), unique=True)



# db.create_all()


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/add_words', methods=['POST', 'GET'])
def add_words():
    form = Word_form()
    if form.validate_on_submit():
        new_word = Word_DB(
            English_word=form.word.data,
            Spanish_word=translate(form.word.data)
        )
        db.session.add(new_word)
        db.session.commit()
        flash("Word Added! \nwould you like to add another word?")
        return redirect(url_for('add_words'))
    return render_template("add_words.html", form=form)

@app.route('/database')
def database():
    words = Word_DB.query.all()
    for word in words:
        print(word.English_word)
    return render_template("database.html", words=words)

@app.route('/quiz_home')
def quiz_home():
    return render_template("quiz_home.html")

if __name__ == "__main__":
    app.run(debug=True)





# current_card = {}
# try:
#     data = pandas.read_csv("data/words_to_learn.csv")
# except FileNotFoundError:
#     data = pandas.read_csv("data/french_words.csv")
# data_dict = data.to_dict(orient="records")
#
#
# def check_func():
#     global data_dict
#     data_dict.remove(current_card)
#     next_word()
#
#
# def english_side():
#     canvas.itemconfig(card_title, text="English", fill="white")
#     canvas.itemconfig(card_word, text=current_card["English"], fill="white")
#     canvas.itemconfig(card_background, image=card_back_img)
#
#
# def next_word():
#     global current_card, flip_timer
#     window.after_cancel(flip_timer)
#     current_card = random.choice(data_dict)
#     canvas.itemconfig(card_title, text="French", fill="black")
#     canvas.itemconfig(card_word, text=current_card["French"], fill="black")
#     canvas.itemconfig(card_background, image=card_front_img)
#     flip_timer = window.after(3000, func=english_side)
#
#
# window = Tk()
# window.title("Flash Cards")
# window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
#
# canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
# card_front_img = PhotoImage(file="images/card_front.png")
# card_back_img = PhotoImage(file="images/card_back.png")
# card_background = canvas.create_image(400, 263, image=card_front_img)
# card_title = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
# card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
# canvas.grid(row=0, column=0, columnspan=2)
#
# check_img = PhotoImage(file="images/right.png")
# check_button = Button(image=check_img, highlightthickness=0, command=check_func)
# check_button.grid(row=1, column=1)
#
# x_img = PhotoImage(file="images/wrong.png")
# x_button = Button(image=x_img, highlightthickness=0, command=next_word)
# x_button.grid(row=1, column=0)
#
# flip_timer = window.after(3000, func=english_side)
# next_word()
#
# window.mainloop()
#
# data = pandas.DataFrame(data_dict)
# data.to_csv("data/words_to_learn.csv", index=False)
# print(data)
