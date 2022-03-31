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
    word = db.session.query(Word_DB).order_by(Word_DB.id.desc()).first()
    if form.validate_on_submit():
        new_word = Word_DB(
            English_word=form.word.data,
            Spanish_word=translate(form.word.data)
        )
        db.session.add(new_word)
        db.session.commit()
        print(add_list)
        flash("Word Added! \nwould you like to add another word?")
        return redirect(url_for('add_words'))
    return render_template("add_words.html", word=word, form=form)

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
    import flashcard_gui
    return render_template("quiz_home.html")

@app.route("/delete/<int:word_id>")
def delete_word(word_id):
    word_to_delete = Word_DB.query.get(word_id)
    db.session.delete(word_to_delete)
    db.session.commit()
    return redirect(url_for('database'))

if __name__ == "__main__":
    app.run(debug=True)


# data = pandas.DataFrame(data_dict)
# data.to_csv("data/words_to_learn.csv", index=False)
# print(data)
