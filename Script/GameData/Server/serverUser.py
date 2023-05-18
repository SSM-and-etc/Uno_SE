import pygame
from Lobby.lobbyWrapper import LobbyWrapper


class ServerUser:
    def __init__(self, ip_address, password):
        self.lobby = LobbyWrapper()
        # List of connected users (including yourself)
        self.connected_users = []
        self.ip_address = ip_address
        self.password = password
        self.name = "Default Server Name"  # Default server name

    def set_name(self, new_name):
        self.name = new_name

    def player_ban(self, player_name):
        # Implement player ban logic here
        pass

    def start_game(self):
        if len(self.connected_users) >= 2:
            # Implement game start logic here
            pass
