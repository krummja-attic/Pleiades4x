from pleiades.client import Client
from pleiades.states.main_menu import MainMenu


if __name__ == '__main__':

    client = Client()
    client.initialize("MAIN", MainMenu())
    client.run()
