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
    def __init__(self, settings, screen, position, center, top, damage, speed):
        """
        Creamos una bala en la posicion actial de la nave
        """
        super().__init__()
        self.screen = screen

        # Creamos un proyectil rectangulo en (0, 0) y luego
        # establecemos la posicion correcta
        self.position = position
        if self.position == 0 or self.position == 2:
            self.rect = pygame.Rect(0, 0, settings.bullet_width,
                                    settings.bullet_height)
        elif self.position == 1 or self.position == 3:
            self.rect = pygame.Rect(0, 0, settings.bullet_height,
                                    settings.bullet_width)
        # Establecemos la posicion correcta
        self.rect.centerx = center
        self.rect.top = top
        # Almacenamos la posicion del proyectil como un valor decimal
        self.x_position = float(self.rect.x)
        self.y_position = float(self.rect.y)
        self.color = settings.bullet_color
        self.speed_factor = speed
        self.damage = damage

    def update(self):
        """
        Mover el proyectil
        """
        # Calculamos la nueva posicion del proyectil
        if self.position == 0:
            self.y_position -= self.speed_factor
        elif self.position == 1:
            self.x_position -= self.speed_factor
        elif self.position == 2:
            self.y_position += self.speed_factor
        elif self.position == 3:
            self.x_position += self.speed_factor
            
        # Actualizar la posicion del rectangulo
        self.rect.x = self.x_position
        self.rect.y = self.y_position
        
    def draw_bullet(self):
        """
        Dibuja el proyectil en la pantalla
        """
        pygame.draw.rect(self.screen, self.color, self.rect)
