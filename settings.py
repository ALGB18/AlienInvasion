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

        # Fuente para los textos
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Berlin Sans FB', 30)

        # Opciones de la nave del jugador
        self.ship_speed_factor = 7
        self.ship_bullet_speed_factor = 15
        self.ship_maximun_health = 100
        self.ship_bullet_damage = 10

        # Opciones de los aliens
        self.alien_bullet_speed_factor = 10
        self.standart_alien_speed_factor = 8
        self.max_aliens_in_game = 5
        self.minimun_degrees_to_shoot = 30
        self.standart_alien_health = 50
        self.standart_alien_bullet_damage = 10

        # Opciones generales de los lasers
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 3
