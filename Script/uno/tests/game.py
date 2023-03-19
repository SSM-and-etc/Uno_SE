from uno.game import *
import random

def test_game():
    players = [Player(i) for i in range(4)]
    game = Game(players)

    for i in range(10):
        current_player = game.turn()
        card = random.choice(current_player.hand)
        print("TABLE: ", game.table)
        print("TURN: ", current_player)
        print("CARD: ", card)

        for player in players:
            print(player)

        print(game.play(current_player, card))


test_game()