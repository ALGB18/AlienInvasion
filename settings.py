"""
Este modulo solamente contendra cosas relativas a las
opciones del juego
"""

import pygame

class Settings:
    """
    En esta clase estaran las opciones del juego
    para mantenerlas en un lugar accesible, y
    no desperdigadas por todo el codigo
    """

    def __init__(self):
        """
        Inicializar las opciones del juego
        """
        # Opciones de la pantalla
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)
        self.fps = 60
        self.updates_per_second = 60

        # Opciones de la nave del jugador
        self.ship_speed_factor = 12

        # Opciones de los aliens
        self.standart_alien_speed_factor = 7.5
        self.max_aliens_in_game = 15

        # Opciones de los lasers
        self.bullet_speed_factor = 15
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 3
