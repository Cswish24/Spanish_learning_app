BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas
import random
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from api_test import translate_en, translate_es
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

@app.route('/english_to_spanish', methods=['POST', 'GET'])
def english_to_spanish():
    form = Word_form()

    word = db.session.query(Word_DB).order_by(Word_DB.id.desc()).first()
    if form.validate_on_submit():
        new_word = Word_DB(
            English_word=form.word.data,
            Spanish_word=translate_en(form.word.data)
        )
        db.session.add(new_word)
        db.session.commit()
        flash("Word Added! \nwould you like to add another word?")
        return redirect(url_for('english_to_spanish'))
    return render_template("english_to_spanish.html", word=word, form=form)

@app.route('/spanish_to_english', methods=['POST', 'GET'])
def spanish_to_english():
    form = Word_form()
    word = db.session.query(Word_DB).order_by(Word_DB.id.desc()).first()
    if form.validate_on_submit():
        new_word = Word_DB(
            Spanish_word=form.word.data,
            English_word=translate_es(form.word.data)
        )
        db.session.add(new_word)
        db.session.commit()

        flash("Word Added! \nwould you like to add another word?")
        return redirect(url_for('spanish_to_english'))
    return render_template("spanish_to_english.html", word=word, form=form)

@app.route('/database')
def database():
    words = Word_DB.query.all()
    for word in words:
        print(word.English_word)
    return render_template("database.html", words=words)

@app.route('/quiz_home')
def quiz_home():
    return render_template("quiz_home.html")



@app.route('/flash_card_quiz')
def flash_card_quiz():
    current_card = {}
    BACKGROUND_COLOR = "#B1DDC6"
    words = Word_DB.query.all()

    word_list = []
    for word in words:
        word_list.append({"English": word.English_word, "Spanish": word.Spanish_word})
    print(word_list)
    def check_func(word_list, current_card, flip_timer):

        word_list.remove(current_card)
        next_word(flip_timer, current_card)

    def english_side(current_card):
        canvas.itemconfig(card_title, text="English", fill="white")
        canvas.itemconfig(card_word, text=current_card["English"], fill="white")
        canvas.itemconfig(card_background, image=card_back_img)

    def next_word(flip_timer, current_card):
        window.after_cancel(flip_timer)
        current_card.update(random.choice(word_list))
        canvas.itemconfig(card_title, text="Spanish", fill="black")
        canvas.itemconfig(card_word, text=current_card["Spanish"], fill="black")
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
    card_title = canvas.create_text(400, 150, text="Spanish", font=("Ariel", 40, "italic"))
    card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
    canvas.grid(row=0, column=0, columnspan=2)

    check_img = PhotoImage(file="images/right.png")
    check_button = Button(image=check_img, highlightthickness=0,
                          command=lambda: check_func(word_list, current_card, flip_timer))
    check_button.grid(row=1, column=1)

    x_img = PhotoImage(file="images/wrong.png")
    x_button = Button(image=x_img, highlightthickness=0, command=lambda: next_word(flip_timer, current_card))
    x_button.grid(row=1, column=0)

    flip_timer = window.after(3000, func=english_side)
    print(current_card)
    next_word(flip_timer, current_card)
    print(current_card)
    window.mainloop()
    return render_template("quiz_home.html")

@app.route("/delete/<int:word_id>")
def delete_word(word_id):
    word_to_delete = Word_DB.query.get(word_id)
    db.session.delete(word_to_delete)
    db.session.commit()
    return redirect(url_for('database'))

@app.route("/check_eng/<int:word_id>")
def check_eng(word_id):
    word_to_delete = Word_DB.query.get(word_id)
    db.session.delete(word_to_delete)
    db.session.commit()
    return redirect(url_for('english_to_spanish'))

@app.route("/check_sp/<int:word_id>")
def check_sp(word_id):
    word_to_delete = Word_DB.query.get(word_id)
    db.session.delete(word_to_delete)
    db.session.commit()
    return redirect(url_for('spanish_to_english'))

if __name__ == "__main__":
    app.run(debug=True)


# data = pandas.DataFrame(data_dict)
# data.to_csv("data/words_to_learn.csv", index=False)
# print(data)
