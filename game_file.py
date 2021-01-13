from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

import random

app = Flask(__name__)

app.config['SECRET_KEY'] = '09412da809127wdawwar'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class ActionCard:
    name = ''
    image = ''


cardEnemy = ActionCard()
cardEnemy.name = 'Demon'
cardEnemy.image = '/static/DarkSoulsCard/enemy.png'


class PlayerCharacter:
    def __init__(self, name):
        self.name = name

    health = 3
    active_field = [0, 0]
    keys = {
        "toxic": 0,
        "death": 0,
        "bone": 0,
        "madness": 0,
    }
    souls = {
        "toxic": 0,
        "death": 0,
        "bone": 0,
        "madness": 0,
    }


player1 = PlayerCharacter(name=None)
player2 = PlayerCharacter(name=None)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    has_torch = db.Column(db.Boolean)
    has_toxic = db.Column(db.Boolean)
    has_death = db.Column(db.Boolean)
    has_madness = db.Column(db.Boolean)
    has_bones = db.Column(db.Boolean)
    health = db.Column(db.Integer)

    def __repr__(self):
        return f"Player('{self.username}')"


@app.route('/')
def home():
    return render_template('game_mode.html')


@app.route('/solo/')
def solo():
    return render_template('game_solo.html', player1=player1, cardEnemy=cardEnemy)


@app.route('/createPlayer', methods=['GET', 'POST'])
def createCharacter():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('solo', name=form.username))
    return render_template('characterCreation.html', form=form)


@app.route('/loadPlayer', methods=['GET', 'POST'])
def LoadCharacter():
    form = LoginForm()
    return render_template('characterLoading.html', form=form)


@app.route('/hotseat')
def hotseat():
    return render_template('game_hotseat.html')


@app.route('/online')
def online():
    return render_template('game_online.html')


@app.route('/reset')
def reset():
    player1.active_field[0] = 0
    player1.active_field[1] = 0
    return redirect(url_for('solo'))


@app.route('/move')
def move():
    result = random.randint(1, 6)
    first_field = player1.active_field[0]
    second_field = player1.active_field[1]
    keep = 0
    if (player1.active_field[0] == 0 and player1.active_field[1] == 0) \
            or player1.active_field[0] in range(1, 8) and player1.active_field[1] == 0:  # pozycja startowa i lewy pion
        player1.active_field[0] += result
        if player1.active_field[0] > 8 and player1.active_field[1] == 0:  # lewa strona w dol
            player1.active_field[0] = 8
            keep = player1.active_field[0] - first_field
            player1.active_field[1] += keep

    if (player1.active_field[0] == 8 and player1.active_field[1] in range(1, 8))\
            or player1.active_field[0] == 8 and player1.active_field[1] == 0:  # dolny poziom
        player1.active_field[1] += result
        if player1.active_field[1] > 8 and player1.active_field[0] == 8:  # dolny poziom w gore
            player1.active_field[1] = 8
            keep = player1.active_field[1] - second_field
            player1.active_field[0] -= keep
    if (player1.active_field[0] in range(1, 8) and player1.active_field[1] == 8) \
            or player1.active_field[0] == 8 and player1.active_field[1] == 8:  # prawy pion
        player1.active_field[0] -= result
        if player1.active_field[0] < 0 and player1.active_field[1] == 8:
            player1.active_field[0] = 0
            keep = result - player1.active_field[0]
            player1.active_field[1] -= keep

    if (player1.active_field[0] == 0 and player1.active_field[1] in range(1, 8)) \
            or player1.active_field[0] == 0 and player1.active_field[1] == 8:  # gorny poziom
        player1.active_field[1] -= result
        if player1.active_field[1] < 0 and player1.active_field[0] == 0:
            player1.active_field[1] = 0
            keep = result - player1.active_field[1]
            player1.active_field[0] += keep
    first_field = 0
    second_field = 0
    return redirect(url_for('solo'))

