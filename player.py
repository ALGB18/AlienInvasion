"""
Este modulo contiene la clase jugador
"""
from ship import Ship

class Player():
    """
    Esta clase contiene propiedades del jugador, como
    la puntuacion, vidas, etc.
    """
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.lifes = 8
        self.lifes_text = settings.my_font.render("Lifes: " + str(self.lifes), False, (255, 255, 255))
        self.current_ship = Ship(screen, settings)


    def create_ship(self):
        self.lifes_text = self.settings.my_font.render("Lifes: " + str(self.lifes), False, (255, 255, 255))
        self.current_ship = Ship(self.screen, self.settings, inmune=True)
        