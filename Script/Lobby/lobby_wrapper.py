from Lobby.lobby import Lobby


class LobbyWrapper:
    def __init__(self,main):
        self.lobby = Lobby(self,main)

    def add_player(self, player_name):
        self.lobby.add_player(player_name)

    def remove_player(self, player_name):
        self.lobby.remove_player(player_name)

    def start_game(self):
        self.lobby.start_game()

    # Add any additional methods you need to interact with the Lobby object


