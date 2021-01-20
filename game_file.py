import cards
import random
import pickle
from flask import Flask, render_template, redirect, url_for

from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '09412da809127wdawwar'

Deck = cards.build_deck()
ConstantDeck = cards.ConstantDeck

result = 0
keep = 0
card = None
active_player = 1


class PlayerCharacter:
    def __init__(self, name):
        self.name = name

    health = 3
    active_field = [0, 0]
    strength = 0
    resistance = 0
    is_attacked = 0
    has_drawn = 0
    has_torch = 0
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
        player2 = PlayerCharacter(name='CPU')
        player2.active_field = [8, 8]
        return redirect(url_for('solo'))
    return render_template('characterCreation.html', form=form)


@app.route('/move/<player>/<int:torchAmount>')
def move(player, torchAmount):
    global result, keep, card, active_player

    if player == '1':
        player1.is_attacked = 0
        player1.has_drawn = 0
        if torchAmount == 0:
            result = random.randint(1, 6)
        elif torchAmount > 0:
            result = torchAmount
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
        active_player = active_player * -1
    elif player == '2':
        player2.is_attacked = 0
        player2.has_drawn = 0
        result = random.randint(1, 6)
        if player2.active_field[1] == 0 and player2.active_field[0] == 0:  # pole 0,0
            player2.active_field[1] += result
        elif player2.active_field[1] in range(1, 8) and player2.active_field[0] == 0:  # górny wiersz
            player2.active_field[1] += result
            if player2.active_field[1] > 8 and player2.active_field[0] == 0:
                keep = player2.active_field[1] - 8
                player2.active_field[1] = 8
                player2.active_field[0] += keep
        elif player2.active_field[0] == 0 and player2.active_field[1] == 8:  # pole 0,8
            player2.active_field[0] += result
        elif player2.active_field[0] in range(1, 8) and player2.active_field[1] == 8:  # prawa kolumna
            player2.active_field[0] += result
            if player2.active_field[0] > 8 and player2.active_field[1] == 8:
                keep = player2.active_field[0] - 8
                player2.active_field[0] = 8
                player2.active_field[1] -= keep
        elif player2.active_field[0] == 8 and player2.active_field[1] == 8:  # pole 8,8
            player2.active_field[1] -= result
        elif player2.active_field[1] in range(1, 8) and player2.active_field[0] == 8:  # dolny wiersz
            player2.active_field[1] -= result
            if player2.active_field[1] < 0 and player2.active_field[0] == 8:
                keep = player2.active_field[1] * -1
                player2.active_field[1] = 0
                player2.active_field[0] = 8
                player2.active_field[0] -= keep
        elif player2.active_field[0] == 8 and player2.active_field[1] == 0:  # pole 8,0
            player2.active_field[0] -= result
        elif player2.active_field[0] in range(1, 8) and player2.active_field[1] == 0:
            player2.active_field[0] -= result
            if player2.active_field[0] < 0 and player2.active_field[1] == 0:
                keep = player2.active_field[0] * -1
                player2.active_field[0] = 0
                player2.active_field[1] = 0
                player2.active_field[1] += keep

        chance = random.randint(1, 100)
        if chance <= 20:
            player2.is_attacked = 1
        card = None
        active_player = active_player * -1
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


@app.route('/battleBoss/<bossID>')
def battleBoss(bossID=None):
    attack_power = random.randint(1, 6) + player1.strength
    boss_attack = random.randint(1, 10) - player1.resistance
    if attack_power > boss_attack:
        if bossID == 'death':
            player1.souls['death'] = 1
        elif bossID == 'bone':
            player1.souls['bone'] = 1
        elif bossID == 'toxic':
            player1.souls['toxic'] = 1
        elif bossID == 'madness':
            player1.souls['madness'] = 1
    else:
        player1.health -= 1

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
    elif card.name == 'magicArrow':
        player2.health -= 1
    elif card.name == 'recoverHealth':
        player1.health += 1
    elif card.name == 'thief':
        for item in player2.keys:
            if player2.keys[item] == 1:
                player2.keys[item] = 0
                break
    elif card.name == 'loseItem':
        for item in player1.keys:
            if player1.keys[item] == 1:
                player1.keys[item] = 0
                break
    elif card.name == "torch":
        player1.has_torch = 1
    return redirect(url_for('solo'))


@app.route('/solo/')
def solo():
    return render_template('game_solo.html', player1=player1, player2=player2, Deck=Deck,
                           keep=keep, result=result, ConstantDeck=ConstantDeck, card=card, active_player=active_player)


@app.route('/loadPlayer', methods=['GET', 'POST'])
def LoadCharacter():
    form = LoginForm()
    return render_template('characterLoading.html', form=form)


@app.route('/save')
def save():
    data = [player1, player2]
    with open(player1.name, 'wb') as gameSave:
        pickle.dump(data, gameSave)
    return redirect(url_for('solo'))


@app.route('/load')
def load():
    with open(player1.name, "rb") as gameSave:
        pickle.load(gameSave)
    return redirect(url_for('solo'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5129, debug=True)
