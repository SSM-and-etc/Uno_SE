from Lobby import Lobby


class LobbyWrapper:
    def __init__(self):
        self.lobby = Lobby()

    def add_player(self, player_name):
        self.lobby.add_player(player_name)

    def remove_player(self, player_name):
        self.lobby.remove_player(player_name)

    def start_game(self):
        self.lobby.start_game()

    # Add any additional methods you need to interact with the Lobby object


# Example usage
lobby_wrapper = LobbyWrapper()
lobby_wrapper.add_player("Player1")
lobby_wrapper.add_player("Player2")
lobby_wrapper.start_game()
