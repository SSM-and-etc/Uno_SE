from uno.game import *
import random

def select_color():
    return random.choice([x for x in CardColor])

def test_game():
    callback = {
        "select_color": select_color
    }
    players = [Player(i) for i in range(4)]
    game = Game(players, callback)

    for i in range(10):
        current_player = game.turn()
        card = random.choice(current_player.hand)

        print("-"*100)
        print("TABLE: ", game.table)
        print("TURN: ", game.turn())
        print("CARD: ", card)
        for player in players:
            print(player)
        print("-"*100)

        print(game.play(current_player, card))

    current_player = game.turn()
    print(game.play(current_player))
    print("-"*100)
    print("TABLE: ", game.table)
    print("TURN: ", game.turn())
    for player in players:
        print(player)
    print("-"*100)


test_game()