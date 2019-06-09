"""
En este modulo definiremos los proyectiles que
dispararan las naves
"""

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """
    Una clase que maneja los proyectiles disparadas desde la nave
    """
    def __init__(self, settings, screen, ship):
        """
        Creamos una bala en la posicion actial de la nave
        """
        super().__init__()
        self.screen = screen

        # Creamos un proyectil rectangulo en (0, 0) y luego
        # establecemos la posicion correcta
        self.position = ship.position
        if self.position == 0 or self.position == 2:
            self.rect = pygame.Rect(0, 0, settings.bullet_width,
                                    settings.bullet_height)
        elif self.position == 1 or self.position == 3:
            self.rect = pygame.Rect(0, 0, settings.bullet_height,
                                    settings.bullet_width)
        if self.position == 0:
            self.rect.centerx = ship.rect.centerx
            self.rect.top = ship.rect.top
        elif self.position == 1:
            self.rect.centerx = ship.rect.left
            self.rect.top = ship.rect.centery
        elif self.position == 2:
            self.rect.centerx = ship.rect.centerx
            self.rect.top = ship.rect.bottom
        elif self.position == 3:
            self.rect.centerx = ship.rect.right
            self.rect.top = ship.rect.centery
        # Almacenamos la posicion del proyectil como un valor decimal
        self.x_position = float(self.rect.x)
        self.y_position = float(self.rect.y)
        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor

    def update(self, ship):
        """
        Mover el proyectil
        """
        if self.position == 0:
            self.y_position -= self.speed_factor
        elif self.position == 1:
            self.x_position -= self.speed_factor
        elif self.position == 2:
            self.y_position += self.speed_factor
        elif self.position == 3:
            self.x_position += self.speed_factor
        # Actualizamos la posicion decimal del proyectil
        
        # Actualizar la posicion del rectangulo
        self.rect.x = self.x_position
        self.rect.y = self.y_position

    def draw_bullet(self):
        """
        Dibuja el proyectil en la pantalla
        """
        pygame.draw.rect(self.screen, self.color, self.rect)
