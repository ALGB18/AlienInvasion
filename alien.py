"""
Define los distintos tipos de aliens
"""
import math
import random
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """
    Define las caracteristicas comunes de los
    aliens
    """
    def __init__(self, settings, screen, x_position, y_position, position):
        super().__init__()
        self.screen = screen
        self.settings = settings
        # Cargamos la imagen del alien y establece su posicion inicial
        self.image = pygame.image.load(".\\resources\\alien_estandar.bmp")
        self.rect = self.image.get_rect()

        # Los aliens comienzan cerca de la parte superior izquierda
        # de la pantalla
        self.rect.x = x_position
        self.rect.y = y_position
        self.position = position
        self.coordinates_to_move = None
        self.on_screen = False
        # Almacenamos la posicion del alien
        self.x_position = int(self.rect.x)
        self.y_position = int(self.rect.y)

    def update(self, ship, settings, alien_group):
        """
        Movemos al alien en funcion de la posicion de
        la nave del jugador
        """
        # Si la nave del jugador es visible en la pantalla,
        # movemos el alien por los dos ejes a la vez
        # En caso contrario, solamente movemos el eje que
        # nos acerce a la zona de la pantalla visible


        if self.on_screen:
            if (self.coordinates_to_move is None) or (self.reached_destination()):
                self.coordinates_to_move = (random.randint(0, settings.screen_width),
                                            random.randint(0, settings.screen_height))
            alien_group.remove(self)
            collisions = self.collide(alien_group)
            alien_group.add(self)
            if collisions:
                suma_x = 0.0
                suma_y = 0.0
                for alien in collisions:
                    suma_x += alien.rect.centerx
                    suma_y += alien.rect.centery
                distance = math.sqrt((suma_x / len(collisions) - self.rect.centerx) ** 2
                                     + (suma_y / len(collisions) - self.rect.centery) ** 2)
                try:
                    vector_unitario = (-(suma_x / len(collisions) - self.rect.centerx) / distance,
                                       -(suma_y / len(collisions) - self.rect.centery) / distance)
                except ZeroDivisionError:
                    return
                if vector_unitario:
                    self.rect.centerx += vector_unitario[0] * settings.standart_alien_speed_factor
                    self.rect.centery += vector_unitario[1] * settings.standart_alien_speed_factor
                    self.coordinates_to_move = None
            else:
                new_position = self.position_towards_destination()
                if new_position:
                    self.rect.centerx += new_position[0] * settings.standart_alien_speed_factor
                    self.rect.centery += new_position[1] * settings.standart_alien_speed_factor
        else:
            if self.position == 0:
                self.y_position += settings.standart_alien_speed_factor
            elif self.position == 1:
                self.y_position -= settings.standart_alien_speed_factor
            elif self.position == 2:
                self.x_position += settings.standart_alien_speed_factor
            elif self.position == 3:
                self.x_position -= settings.standart_alien_speed_factor
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

    def collide(self, sprite_group):
        """
        Determina si un alien colisiona con otros
        alien en un grupo de sprites
        """
        return pygame.sprite.spritecollide(self, sprite_group, False)

    def position_towards_destination(self):
        """
        Retorna el vector unitario que resulta del punto al que
        nos queremos mover (self.coordinates_to_move) y el actual
        """
        distance = math.sqrt((self.coordinates_to_move[0] - self.rect.centerx) ** 2
                             + (self.coordinates_to_move[1] - self.rect.centery) ** 2)
        try:
            x_position = (self.coordinates_to_move[0] - self.rect.centerx) / distance
            y_position = (self.coordinates_to_move[1] - self.rect.centery) / distance
        except ZeroDivisionError:
            return False
        return (x_position, y_position)

    def reached_destination(self):
        """
        Determina si el alien ha alcanzado el punto al que se
        quiere mover (self.coordinates_to_move)
        """
        return self.rect.centerx > self.coordinates_to_move[0] - 10 and\
            self.rect.centerx < self.coordinates_to_move[0] + 10 and\
            self.rect.centery > self.coordinates_to_move[1] - 10 and\
            self.rect.centery < self.coordinates_to_move[1] + 10
