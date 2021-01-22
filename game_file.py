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

    def move(self, torch):
        global result, keep, card, active_player
        self.is_attacked = 0
        self.has_drawn = 0
        if torch == 0:
            result = random.randint(1, 6)
        elif torch > 0:
            result = torch
        if self.active_field[1] == 0 and self.active_field[0] == 0:  # pole 0,0
            self.active_field[1] += result
        elif self.active_field[1] in range(1, 8) and self.active_field[0] == 0:  # górny wiersz
            self.active_field[1] += result
            if self.active_field[1] > 8 and self.active_field[0] == 0:
                keep = self.active_field[1] - 8
                self.active_field[1] = 8
                self.active_field[0] += keep
        elif self.active_field[0] == 0 and self.active_field[1] == 8:  # pole 0,8
            self.active_field[0] += result
        elif self.active_field[0] in range(1, 8) and self.active_field[1] == 8:  # prawa kolumna
            self.active_field[0] += result
            if self.active_field[0] > 8 and self.active_field[1] == 8:
                keep = self.active_field[0] - 8
                self.active_field[0] = 8
                self.active_field[1] -= keep
        elif self.active_field[0] == 8 and self.active_field[1] == 8:  # pole 8,8
            self.active_field[1] -= result
        elif self.active_field[1] in range(1, 8) and self.active_field[0] == 8:  # dolny wiersz
            self.active_field[1] -= result
            if self.active_field[1] < 0 and self.active_field[0] == 8:
                keep = self.active_field[1] * -1
                self.active_field[1] = 0
                self.active_field[0] = 8
                self.active_field[0] -= keep
        elif self.active_field[0] == 8 and self.active_field[1] == 0:  # pole 8,0
            self.active_field[0] -= result
        elif self.active_field[0] in range(1, 8) and self.active_field[1] == 0:
            self.active_field[0] -= result
            if self.active_field[0] < 0 and self.active_field[1] == 0:
                keep = self.active_field[0] * -1
                self.active_field[0] = 0
                self.active_field[1] = 0
                self.active_field[1] += keep
        chance = random.randint(1, 100)
        if chance <= 20:
            self.is_attacked = 1
        card = None
        active_player = active_player * -1

    def loseHealth(self):
        self.health -= 1
        if self.health <= 0:
            self.active_field = [0, 0]
            self.health = 3
            self.has_torch = 0
            for item in self.keys:
                if self.keys[item] == 1:
                    self.keys[item] = 0
                    break

    def drawCard(self, other_player):
        self.has_drawn = 1
        global Deck
        random.shuffle(Deck)
        global card
        if Deck:
            card = Deck.pop()
        else:
            Deck = cards.build_deck()
            card = Deck.pop()
        if card.name == 'KeyBone':
            self.keys["bone"] = 1
        elif card.name == 'KeyDeath':
            self.keys["death"] = 1
        elif card.name == 'KeyToxic':
            self.keys["toxic"] = 1
        elif card.name == 'KeyMadness':
            self.keys["madness"] = 1
        elif card.name == 'loseHealth':
            self.loseHealth()
        elif card.name == 'magicArrow':
            other_player.loseHealth()
        elif card.name == 'recoverHealth':
            self.health += 1
        elif card.name == "torch":
            self.has_torch = 1
        elif card.name == 'thief':
            for item in other_player.keys:
                if other_player.keys[item] == 1:
                    other_player.keys[item] = 0
                    break
        elif card.name == 'loseItem':
            for item in self.keys:
                if self.keys[item] == 1:
                    self.keys[item] = 0
                    break

    def battle(self):
        attack_power = random.randint(1, 6) + self.strength
        enemy_attack = random.randint(1, 6) - self.resistance
        if attack_power > enemy_attack:
            check = random.randint(1, 2)
            if check == 1:
                self.resistance += 1
            else:
                self.strength += 1
        else:
            self.loseHealth()
        self.is_attacked = 0

    def battleBoss(self, bossID):
        attack_power = random.randint(1, 6) + self.strength
        boss_attack = random.randint(1, 10) - self.resistance
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
            self.loseHealth()


class CPU:
    def __init__(self, name):
        self.name = name

    health = 3
    active_field = [8, 8]
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

    def move(self, torch):
        global result, keep, card, active_player
        self.is_attacked = 0
        self.has_drawn = 0
        if torch == 0:
            result = random.randint(1, 6)
        elif torch > 0:
            result = torch
        if self.active_field[1] == 0 and self.active_field[0] == 0:  # pole 0,0
            self.active_field[1] += result
        elif self.active_field[1] in range(1, 8) and self.active_field[0] == 0:  # górny wiersz
            self.active_field[1] += result
            if self.active_field[1] > 8 and self.active_field[0] == 0:
                keep = self.active_field[1] - 8
                self.active_field[1] = 8
                self.active_field[0] += keep
        elif self.active_field[0] == 0 and self.active_field[1] == 8:  # pole 0,8
            self.active_field[0] += result
        elif self.active_field[0] in range(1, 8) and self.active_field[1] == 8:  # prawa kolumna
            self.active_field[0] += result
            if self.active_field[0] > 8 and self.active_field[1] == 8:
                keep = self.active_field[0] - 8
                self.active_field[0] = 8
                self.active_field[1] -= keep
        elif self.active_field[0] == 8 and self.active_field[1] == 8:  # pole 8,8
            self.active_field[1] -= result
        elif self.active_field[1] in range(1, 8) and self.active_field[0] == 8:  # dolny wiersz
            self.active_field[1] -= result
            if self.active_field[1] < 0 and self.active_field[0] == 8:
                keep = self.active_field[1] * -1
                self.active_field[1] = 0
                self.active_field[0] = 8
                self.active_field[0] -= keep
        elif self.active_field[0] == 8 and self.active_field[1] == 0:  # pole 8,0
            self.active_field[0] -= result
        elif self.active_field[0] in range(1, 8) and self.active_field[1] == 0:
            self.active_field[0] -= result
            if self.active_field[0] < 0 and self.active_field[1] == 0:
                keep = self.active_field[0] * -1
                self.active_field[0] = 0
                self.active_field[1] = 0
                self.active_field[1] += keep
        chance = random.randint(1, 100)
        if chance <= 20:
            self.is_attacked = 1
            self.battle()
        special_field = [[0, 0], [0, 4], [0, 8], [4, 8], [8, 8], [8, 4], [8, 0], [4, 0]]
        if self.active_field in special_field:
            CPU_player.drawCard(player1)
        card = None
        active_player = active_player * -1

    def loseHealth(self):
        self.health -= 1
        if self.health <= 0:
            self.active_field = [0, 0]
            self.health = 3
            self.has_torch = 0
            for item in self.keys:
                if self.keys[item] == 1:
                    self.keys[item] = 0
                    break

    def drawCard(self, other_player):
        self.has_drawn = 1
        global Deck
        random.shuffle(Deck)
        global card
        if Deck:
            card = Deck.pop()
        else:
            Deck = cards.build_deck()
            card = Deck.pop()
        if card.name == 'KeyBone':
            self.keys["bone"] = 1
        elif card.name == 'KeyDeath':
            self.keys["death"] = 1
        elif card.name == 'KeyToxic':
            self.keys["toxic"] = 1
        elif card.name == 'KeyMadness':
            self.keys["madness"] = 1
        elif card.name == 'loseHealth':
            self.loseHealth()
        elif card.name == 'magicArrow':
            other_player.loseHealth()
        elif card.name == 'recoverHealth':
            self.health += 1
        elif card.name == "torch":
            self.has_torch = 1
        elif card.name == 'thief':
            for item in other_player.keys:
                if other_player.keys[item] == 1:
                    other_player.keys[item] = 0
                    break
        elif card.name == 'loseItem':
            for item in self.keys:
                if self.keys[item] == 1:
                    self.keys[item] = 0
                    break

    def battle(self):
        attack_power = random.randint(1, 6) + self.strength
        enemy_attack = random.randint(1, 6) - self.resistance
        if attack_power > enemy_attack:
            check = random.randint(1, 2)
            if check == 1:
                self.resistance += 1
            else:
                self.strength += 1
        else:
            self.loseHealth()
        self.is_attacked = 0

    def battleBoss(self, bossID):
        attack_power = random.randint(1, 6) + self.strength
        boss_attack = random.randint(1, 10) - self.resistance
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
            self.loseHealth()


@app.route('/')
def home():
    return render_template('game_mode.html')


@app.route('/createPlayer', methods=['GET', 'POST'])
def createCharacter():
    form = RegistrationForm()
    if form.validate_on_submit():
        global player1
        global CPU_player
        player1 = PlayerCharacter(name=form.username.data)
        CPU_player = CPU(name='CPU')
        CPU_player.active_field = [8, 8]
        return redirect(url_for('solo'))
    return render_template('characterCreation.html', form=form)


@app.route('/move/<player>/<int:torchAmount>')
def move(player, torchAmount):
    global result, keep, card, active_player
    if player == '1':
        player1.move(torchAmount)
    elif player == '2':
        CPU_player.move(torchAmount)
    return redirect(url_for('solo'))


@app.route('/battle')
def battle():
    player1.battle()
    return redirect(url_for('solo'))


@app.route('/battleBoss/<bossID>')
def battleBoss(bossID):
    player1.battleBoss(bossID)
    return redirect(url_for('solo'))


@app.route('/draw')
def draw():
    player1.drawCard(CPU_player)
    return redirect(url_for('solo'))


@app.route('/solo/')
def solo():
    return render_template('game_solo.html', player1=player1, player2=CPU_player, Deck=Deck,
                           keep=keep, ConstantDeck=ConstantDeck, card=card, active_player=active_player)


@app.route('/loadPlayer', methods=['GET', 'POST'])
def LoadCharacter():
    form = LoginForm()
    return render_template('characterLoading.html', form=form)


@app.route('/save')
def save():
    data = [player1, CPU_player]
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
