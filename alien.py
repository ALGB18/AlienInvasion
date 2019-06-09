"""
Define los distintos tipos de aliens
"""

import pygame

from pygame.sprite import Sprite

class Alien(Sprite):
    """
    Define las caracteristicas comunes de los
    aliens
    """
    def __init__(self, settings, screen, alien_to_generate):
        super().__init__()
        self.screen = screen
        self.settings = settings

        # Cargamos la imagen del alien y establece su posicion inicial
        self.image = pygame.image.load(".\\resources\\alien_estandar.bmp")
        self.rect = self.image.get_rect()

        # Los aliens comienzan cerca de la parte superior izquierda
        # de la pantalla
        self.rect.x = alien_to_generate.x_position
        self.rect.y = alien_to_generate.x_position
        self.position = alien_to_generate.position
        self.on_screen = False
        # Almacenamos la posicion del alien
        self.x_position = float(self.rect.x)
        self.y_position = float(self.rect.y)

    def update(self, ship, settings):
        """
        Movemos al alien en funcion de la posicion de
        la nave del jugador
        """
        # Si la nave del jugador es visible en la pantalla,
        # movemos el alien por los dos ejes a la vez
        # En caso contrario, solamente movemos el eje que
        # nos acerce a la zona de la pantalla visible
        if self.on_screen:
            if self.x_position < ship.centerx:
                self.x_position += settings.standart_alien_speed_factor
                if self.y_position < ship.centery:
                    self.y_position += settings.standart_alien_speed_factor
                elif self.y_position > ship.centery:
                    self.y_position -= settings.standart_alien_speed_factor
            elif self.x_position > ship.centerx:
                self.x_position -= settings.standart_alien_speed_factor
                if self.y_position < ship.centery:
                    self.y_position += settings.standart_alien_speed_factor
                elif self.y_position > ship.centery:
                    self.y_position -= settings.standart_alien_speed_factor

            self.rect.centerx = self.x_position
            self.rect.centery = self.y_position
        else:
            if self.position == 0:
                self.x_position += settings.standart_alien_speed_factor
            elif self.position == 1:
                self.x_position -= settings.standart_alien_speed_factor
            elif self.position == 2:
                self.y_position += settings.standart_alien_speed_factor
            elif self.position == 3:
                self.y_position -= settings.standart_alien_speed_factor

            self.rect.centerx = self.x_position
            self.rect.centery = self.y_position
            if self.x_position >= 0 and self.x_position < settings.screen_width\
               and self.y_position >= 0 and self.y_position < settings.screen_height:
                self.on_screen = True

    def blitme(self):
        """
        Dibujamos el alien en su posicion actual
        """
        self.screen.blit(self.image, self.rect)
    