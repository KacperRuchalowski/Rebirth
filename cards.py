def build_deck():
    deck = [cardKeyBone, cardKeyBone, cardKeyBone,
            cardKeyMadness, cardKeyMadness, cardKeyMadness,
            cardKeyDeath, cardKeyDeath, cardKeyDeath,
            cardKeyToxic, cardKeyToxic, cardKeyToxic,
            cardTorch, cardTorch,
            cardThief, cardThief, cardThief,
            cardMagicArrow, cardMagicArrow, cardMagicArrow, cardMagicArrow,
            cardLoseHealth, cardLoseHealth,
            cardLoseItem, cardLoseItem,
            cardRecoverHealth, cardRecoverHealth, cardRecoverHealth,

            ]
    return deck


class ActionCard:
    name = ''
    image = ''


cardEnemy = ActionCard()
cardEnemy.name = 'Enemy'
cardEnemy.image = '/static/DarkSoulsCard/enemy.png'

cardKeyBone = ActionCard()
cardKeyBone.name = 'KeyBone'
cardKeyBone.image = '/static/DarkSoulsCard/key_bone.png'

cardKeyDeath = ActionCard()
cardKeyDeath.name = 'KeyDeath'
cardKeyDeath.image = '/static/DarkSoulsCard/key_death.png'

cardKeyMadness = ActionCard()
cardKeyMadness.name = 'KeyMadness'
cardKeyMadness.image = '/static/DarkSoulsCard/key_madness.png'

cardKeyToxic = ActionCard()
cardKeyToxic.name = 'KeyToxic'
cardKeyToxic.image = '/static/DarkSoulsCard/key_toxic.png'

cardKeyToxic = ActionCard()
cardKeyToxic.name = 'KeyToxic'
cardKeyToxic.image = '/static/DarkSoulsCard/key_toxic.png'

cardLordSoul = ActionCard()
cardLordSoul.name = 'lordSoul'
cardLordSoul.image = '/static/DarkSoulsCard/lord_Soul.png'

cardLoseHealth = ActionCard()
cardLoseHealth.name = 'loseHealth'
cardLoseHealth.image = '/static/DarkSoulsCard/lose_health.png'

cardLoseItem = ActionCard()
cardLoseItem.name = 'loseItem'
cardLoseItem.image = '/static/DarkSoulsCard/lose_item.png'

cardMagicArrow = ActionCard()
cardMagicArrow.name = 'magicArrow'
cardMagicArrow.image = '/static/DarkSoulsCard/magic_arrow.png'

cardRecoverHealth = ActionCard()
cardRecoverHealth.name = 'recoverHealth'
cardRecoverHealth.image = '/static/DarkSoulsCard/recover_health.png'

cardStasis = ActionCard()
cardStasis.name = 'stasis'
cardStasis.image = '/static/DarkSoulsCard/stasis.png'

cardThief = ActionCard()
cardThief.name = 'thief'
cardThief.image = '/static/DarkSoulsCard/thief.png'

cardTorch = ActionCard()
cardTorch.name = 'torch'
cardTorch.image = '/static/DarkSoulsCard/torch.png'

ConstantDeck = [cardEnemy, cardLordSoul]
