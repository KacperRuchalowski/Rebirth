import cards
import random

from flask import Flask, render_template, redirect, url_for

from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '09412da809127wdawwar'

Deck = cards.build_deck()
ConstantDeck = cards.ConstantDeck

result = 0
keep = 0
card = None


class PlayerCharacter:
    def __init__(self, name):
        self.name = name

    health = 3
    active_field = [0, 0]
    strength = 0
    resistance = 0
    is_attacked = 0
    has_drawn = 0
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


@app.route('/')
def home():
    return render_template('game_mode.html')


@app.route('/createPlayer', methods=['GET', 'POST'])
def createCharacter():
    form = RegistrationForm()
    if form.validate_on_submit():
        global player1
        global player2
        player1 = PlayerCharacter(name=form.username.data)
        player2 = PlayerCharacter(name=None)
        return redirect(url_for('solo'))
    return render_template('characterCreation.html', form=form)


@app.route('/move')
def move():
    player1.is_attacked = 0
    player1.has_drawn = 0
    global result, keep, card
    result = random.randint(1, 6)
    if player1.active_field[1] == 0 and player1.active_field[0] == 0:  # pole 0,0
        player1.active_field[1] += result
    elif player1.active_field[1] in range(1, 8) and player1.active_field[0] == 0:  # górny wiersz
        player1.active_field[1] += result
        if player1.active_field[1] > 8 and player1.active_field[0] == 0:
            keep = player1.active_field[1] - 8
            player1.active_field[1] = 8
            player1.active_field[0] += keep
    elif player1.active_field[0] == 0 and player1.active_field[1] == 8:  # pole 0,8
        player1.active_field[0] += result
    elif player1.active_field[0] in range(1, 8) and player1.active_field[1] == 8:  # prawa kolumna
        player1.active_field[0] += result
        if player1.active_field[0] > 8 and player1.active_field[1] == 8:
            keep = player1.active_field[0] - 8
            player1.active_field[0] = 8
            player1.active_field[1] -= keep
    elif player1.active_field[0] == 8 and player1.active_field[1] == 8:  # pole 8,8
        player1.active_field[1] -= result
    elif player1.active_field[1] in range(1, 8) and player1.active_field[0] == 8:  # dolny wiersz
        player1.active_field[1] -= result
        if player1.active_field[1] < 0 and player1.active_field[0] == 8:
            keep = player1.active_field[1] * -1
            player1.active_field[1] = 0
            player1.active_field[0] = 8
            player1.active_field[0] -= keep
    elif player1.active_field[0] == 8 and player1.active_field[1] == 0:  # pole 8,0
        player1.active_field[0] -= result
    elif player1.active_field[0] in range(1, 8) and player1.active_field[1] == 0:
        player1.active_field[0] -= result
        if player1.active_field[0] < 0 and player1.active_field[1] == 0:
            keep = player1.active_field[0] * -1
            player1.active_field[0] = 0
            player1.active_field[1] = 0
            player1.active_field[1] += keep

    chance = random.randint(1, 100)
    if chance <= 20:
        player1.is_attacked = 1
    card = None
    return redirect(url_for('solo'))


@app.route('/battle')
def battle():
    attack_power = random.randint(1, 6) + player1.strength
    enemy_attack = random.randint(1, 6) - player1.resistance
    if attack_power > enemy_attack:
        check = random.randint(1, 2)
        if check == 1:
            player1.resistance += 1
        else:
            player1.strength += 1
    else:
        player1.health -= 1
    player1.is_attacked = 0

    return redirect(url_for('solo'))


@app.route('/draw')
def draw():
    player1.has_drawn = 1
    global Deck
    random.shuffle(Deck)
    global card
    if Deck:
        card = Deck.pop()
    else:
        Deck = cards.build_deck()
        card = Deck.pop()
    if card.name == 'loseHealth':
        player1.health -= 1
    elif card.name == 'KeyBone':
        player1.keys["bone"] = 1
    elif card.name == 'KeyDeath':
        player1.keys["death"] = 1
    elif card.name == 'KeyToxic':
        player1.keys["toxic"] = 1
    elif card.name == 'KeyMadness':
        player1.keys["madness"] = 1

    return redirect(url_for('solo'))


@app.route('/solo/')
def solo():
    return render_template('game_solo.html', player1=player1, Deck=Deck,
                           keep=keep, result=result, ConstantDeck=ConstantDeck, card=card)


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5129, debug=True)
