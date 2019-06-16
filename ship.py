"""
Modulo que contiene la clase nave
"""
import pygame
import sys
class Ship():
    """
    Clase que define las propiedades de la
    nave que pilota el jugador
    """
    def __init__(self, screen, settings):
        """
        Inicializamos la nave, indicando su posicion
        inicial
        """
        self.screen = screen
        self.settings = settings
        # Carga la imagen de la nave
        self.image = []
        self.image.append(pygame.image.load(".\\resources\\ship.bmp"))       # Apuntando arriba
        self.image.append(pygame.image.load(".\\resources\\ship90.bmp"))     # Apuntando izquierda
        self.image.append(pygame.image.load(".\\resources\\ship180.bmp"))    # Apuntando abajo
        self.image.append(pygame.image.load(".\\resources\\ship270.bmp"))    # Apuntando derecha
        self.rect = self.image[0].get_rect()
        self.position = 0
        self.screen_rect = screen.get_rect()
        self.health = 100
        self.max_health = 100
        self.health_rect = pygame.Rect(0, 0, 200, 50)
        self.health_rect_background = pygame.Rect(0, 0, 200, 50)
        self.health_rect.left = self.settings.screen_width - 225
        self.health_rect.top = self.settings.screen_height - 75
        self.health_rect_background.left = self.settings.screen_width - 225
        self.health_rect_background.top = self.settings.screen_height - 75
        self.bullet_damage = 10
        # Posicionar cada nave que creemos en la parte inferior central de la pantalla
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # Almacenamos un valor decimal con el centro de la nave
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)
        # Flags de movimiento
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """
        Actualizamos la posicion de la nave basandonos en los flags de
        movimiento
        """
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.centery -= self.settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.settings.ship_speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.centerx -= self.settings.ship_speed_factor

        # Actualizamos el objeto rectangulo a partir de los valores de
        # self.centerx (posicion en el eje x) y self.centery (posicion
        # en el eje y)
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery


    def blitme(self):
        """
        Dibuja el barco en su posicion actual
        """
        self.screen.blit(self.image[self.position], self.rect)
        pygame.draw.rect(self.screen, (255, 0, 0), self.health_rect_background)
        pygame.draw.rect(self.screen, (0, 255, 0), self.health_rect)

    def hit(self, bullet):
        """
        Ejecutamos este metodo cuando un alien alcanza con
        un proyectil a la nave del jugador
        """
        self.health -= bullet.damage
        if self.health <= 0:
            print("FIN DEL JUEGO")
            sys.exit()

        self.health_rect = pygame.Rect(0, 0, 200 * self.health/self.max_health, 50)
        self.health_rect.left = self.settings.screen_width - 225
        self.health_rect.top = self.settings.screen_height - 75
