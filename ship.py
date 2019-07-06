"""
Modulo que contiene la clase nave
"""
import sys
import pygame

class Ship():
    """
    Clase que define las propiedades de la
    nave que pilota el jugador
    """
    def __init__(self, screen, settings, inmune=False):
        """
        Inicializamos la nave, indicando su posicion
        inicial
        """
        self.screen = screen
        self.settings = settings
        # Carga la imagen de la nave
        self.image = []
        self.image_inmune = []
        self.image.append(pygame.image.load(".\\resources\\ship.bmp"))       # Apuntando arriba
        self.image.append(pygame.image.load(".\\resources\\ship90.bmp"))     # Apuntando izquierda
        self.image.append(pygame.image.load(".\\resources\\ship180.bmp"))    # Apuntando abajo
        self.image.append(pygame.image.load(".\\resources\\ship270.bmp"))    # Apuntando derecha
        self.image_inmune.append(pygame.image.load(".\\resources\\ship_inmune.bmp"))
        self.image_inmune.append(pygame.image.load(".\\resources\\ship90_inmune.bmp"))
        self.image_inmune.append(pygame.image.load(".\\resources\\ship180_inmune.bmp"))
        self.image_inmune.append(pygame.image.load(".\\resources\\ship270_inmune.bmp"))
        self.inmune = inmune
        if self.inmune:
            self.rect = self.image_inmune[0].get_rect()
        else:
            self.rect = self.image[0].get_rect()
        self.position = 0
        self.screen_rect = screen.get_rect()
        self.speed_factor = settings.ship_speed_factor
        self.max_health = settings.ship_maximun_health
        self.health = self.max_health
        self.health_text = self.settings.my_font.render(str(self.health) + " / " +
                                                        str(self.max_health), False,
                                                        (255, 255, 255))
        self.health_rect = pygame.Rect(0, 0, 200, 50)
        self.health_rect_background = pygame.Rect(0, 0, 200, 50)
        self.health_rect.left = self.settings.screen_width - 225
        self.health_rect.top = self.settings.screen_height - 75
        self.health_rect_background.left = self.settings.screen_width - 225
        self.health_rect_background.top = self.settings.screen_height - 75
        self.bullet_damage = settings.ship_bullet_damage
        self.bullet_speed_factor = settings.ship_bullet_speed_factor
        self.time = pygame.time.get_ticks()
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
            self.centery -= self.speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.speed_factor
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.centerx -= self.speed_factor

        if self.inmune:
            if pygame.time.get_ticks() - self.time > 5000:
                self.inmune = False
        # Actualizamos el objeto rectangulo a partir de los valores de
        # self.centerx (posicion en el eje x) y self.centery (posicion
        # en el eje y)
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

        self.health_text = self.settings.my_font.render(str(self.health) + " / " +
                                                        str(self.max_health), False,
                                                        (255, 255, 255))
        self.health_rect = pygame.Rect(0, 0, 200 * self.health/self.max_health, 50)
        self.health_rect.left = self.settings.screen_width - 225
        self.health_rect.top = self.settings.screen_height - 75


    def blitme(self):
        """
        Dibuja el barco en su posicion actual
        """
        if self.inmune:
            self.screen.blit(self.image_inmune[self.position], self.rect)
        else:
            self.screen.blit(self.image[self.position], self.rect)
        pygame.draw.rect(self.screen, (255, 0, 0), self.health_rect_background)
        pygame.draw.rect(self.screen, (0, 255, 0), self.health_rect)
        self.screen.blit(self.health_text, (self.settings.screen_width - 175,
                                            self.settings.screen_height - 67))

    def hit(self, bullet, player):
        """
        Ejecutamos este metodo cuando un alien alcanza con
        un proyectil a la nave del jugador
        """
        if not self.inmune:
            self.health -= bullet.damage

        if self.health <= 0:
            if player.lifes <= 0:
                print("FIN DEL JUEGO")
                sys.exit()
            else:
                player.lifes -= 1
                player.create_ship()
