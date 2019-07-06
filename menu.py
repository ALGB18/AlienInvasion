"""
Este modulo contiene todo lo necesario para
dar soporte al menu de inicio, de pausa y
de compra
"""
import pygame

class Shop():
    """
    Esta clase da soporte a la tienda del juego
    """
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        # Establecemos el tiempo entre rondas
        self.time_between_rounds = 30
        self.shop_background = None
        self.shop_background_rect = None
        # Almacenaremos las imagenes y los rects que las contendran simultaneamente
        self.shop_items = []
        self.shop_items_rects = []
        # Guardamos el progreso de la tienda
        self.shop_progress = [0, 0, 0, 0, 0, 0]
        # En funcion del numero de vidas que hayamos comprado en una ronda aumentara
        #cada vez mas el precio de estas. En una nueva ronda se reinicia
        self.lifes_progress = 0
        self.shop_open = False

        # Cargamos el icono para abrir la tienda
        self.shop_icon = pygame.image.load(".\\resources\\shop_icon.bmp")
        self.shop_icon_rect = self.shop_icon.get_rect()
        self.shop_icon_rect.left = self.settings.screen_width - 80
        self.shop_icon_rect.top = 10

        # Cargamos los iconos de la tienda
        # Primero el tablero de la tienda
        self.shop_background = pygame.image.load(".\\resources\\shop_board.bmp")
        self.shop_background_rect = self.shop_background.get_rect()
        self.shop_background_rect.centerx = settings.screen_width / 2
        self.shop_background_rect.centery = settings.screen_height / 2

        # Ahora el boton de salir de la tienda
        self.exit_icon = pygame.image.load(".\\resources\\exit_shop.png")
        self.exit_icon_rect = self.exit_icon.get_rect()
        self.exit_icon_rect.centerx = self.shop_background_rect.right - 40
        self.exit_icon_rect.centery = self.shop_background_rect.top + 40

        # Ahora cargaremos las imagenes de los diferentes items de la tienda
        # junto con sus mejoras
        for i in range(6):
            self.shop_items.append([])
            self.shop_items_rects.append([])

        self.shop_items[0].append(pygame.image.load(".\\resources\\repair_lvl1.bmp"))
        self.shop_items_rects[0].append(self.shop_items[0][0].get_rect())
        self.shop_items_rects[0][0].centerx = self.shop_background_rect.left + 218
        self.shop_items_rects[0][0].centery = self.shop_background_rect.top + 178
        self.shop_items[0].append(pygame.image.load(".\\resources\\repair_lvl2.bmp"))
        self.shop_items_rects[0].append(self.shop_items[0][1].get_rect())
        self.shop_items_rects[0][1].centerx = self.shop_background_rect.left + 218
        self.shop_items_rects[0][1].centery = self.shop_background_rect.top + 178
        self.shop_items[0].append(pygame.image.load(".\\resources\\repair_lvl3.bmp"))
        self.shop_items_rects[0].append(self.shop_items[0][2].get_rect())
        self.shop_items_rects[0][2].centerx = self.shop_background_rect.left + 218
        self.shop_items_rects[0][2].centery = self.shop_background_rect.top + 178

        self.shop_items[1].append(pygame.image.load(".\\resources\\speed_lvl1.bmp"))
        self.shop_items_rects[1].append(self.shop_items[1][0].get_rect())
        self.shop_items_rects[1][0].centerx = self.shop_background_rect.left + 500
        self.shop_items_rects[1][0].centery = self.shop_background_rect.top + 178
        self.shop_items[1].append(pygame.image.load(".\\resources\\speed_lvl2.bmp"))
        self.shop_items_rects[1].append(self.shop_items[1][1].get_rect())
        self.shop_items_rects[1][1].centerx = self.shop_background_rect.left + 500
        self.shop_items_rects[1][1].centery = self.shop_background_rect.top + 178
        self.shop_items[1].append(pygame.image.load(".\\resources\\speed_lvl3.bmp"))
        self.shop_items_rects[1].append(self.shop_items[1][2].get_rect())
        self.shop_items_rects[1][2].centerx = self.shop_background_rect.left + 500
        self.shop_items_rects[1][2].centery = self.shop_background_rect.top + 178
        self.shop_items[1].append(pygame.image.load(".\\resources\\speed_no_upgrades.bmp"))
        self.shop_items_rects[1].append(self.shop_items[1][3].get_rect())
        self.shop_items_rects[1][3].centerx = self.shop_background_rect.left + 500
        self.shop_items_rects[1][3].centery = self.shop_background_rect.top + 178

        self.shop_items[2].append(pygame.image.load(".\\resources\\ship_health_lvl1.bmp"))
        self.shop_items_rects[2].append(self.shop_items[2][0].get_rect())
        self.shop_items_rects[2][0].centerx = self.shop_background_rect.left + 782
        self.shop_items_rects[2][0].centery = self.shop_background_rect.top + 178
        self.shop_items[2].append(pygame.image.load(".\\resources\\ship_health_lvl2.bmp"))
        self.shop_items_rects[2].append(self.shop_items[2][1].get_rect())
        self.shop_items_rects[2][1].centerx = self.shop_background_rect.left + 782
        self.shop_items_rects[2][1].centery = self.shop_background_rect.top + 178
        self.shop_items[2].append(pygame.image.load(".\\resources\\ship_health_lvl3.bmp"))
        self.shop_items_rects[2].append(self.shop_items[2][2].get_rect())
        self.shop_items_rects[2][2].centerx = self.shop_background_rect.left + 782
        self.shop_items_rects[2][2].centery = self.shop_background_rect.top + 178
        self.shop_items[2].append(pygame.image.load(".\\resources\\ship_health_no_upgrades.bmp"))
        self.shop_items_rects[2].append(self.shop_items[2][3].get_rect())
        self.shop_items_rects[2][3].centerx = self.shop_background_rect.left + 782
        self.shop_items_rects[2][3].centery = self.shop_background_rect.top + 178

        self.shop_items[3].append(pygame.image.load(".\\resources\\damage_lvl1.bmp"))
        self.shop_items_rects[3].append(self.shop_items[3][0].get_rect())
        self.shop_items_rects[3][0].centerx = self.shop_background_rect.left + 218
        self.shop_items_rects[3][0].centery = self.shop_background_rect.top + 420
        self.shop_items[3].append(pygame.image.load(".\\resources\\damage_lvl2.bmp"))
        self.shop_items_rects[3].append(self.shop_items[3][1].get_rect())
        self.shop_items_rects[3][1].centerx = self.shop_background_rect.left + 218
        self.shop_items_rects[3][1].centery = self.shop_background_rect.top + 420
        self.shop_items[3].append(pygame.image.load(".\\resources\\damage_lvl3.bmp"))
        self.shop_items_rects[3].append(self.shop_items[3][2].get_rect())
        self.shop_items_rects[3][2].centerx = self.shop_background_rect.left + 218
        self.shop_items_rects[3][2].centery = self.shop_background_rect.top + 420
        self.shop_items[3].append(pygame.image.load(".\\resources\\damage_no_upgrades.bmp"))
        self.shop_items_rects[3].append(self.shop_items[3][3].get_rect())
        self.shop_items_rects[3][3].centerx = self.shop_background_rect.left + 218
        self.shop_items_rects[3][3].centery = self.shop_background_rect.top + 420

        self.shop_items[4].append(pygame.image.load(".\\resources\\bpm_lvl1.bmp"))
        self.shop_items_rects[4].append(self.shop_items[4][0].get_rect())
        self.shop_items_rects[4][0].centerx = self.shop_background_rect.left + 500
        self.shop_items_rects[4][0].centery = self.shop_background_rect.top + 420
        self.shop_items[4].append(pygame.image.load(".\\resources\\bpm_no_upgrades.bmp"))
        self.shop_items_rects[4].append(self.shop_items[4][1].get_rect())
        self.shop_items_rects[4][1].centerx = self.shop_background_rect.left + 500
        self.shop_items_rects[4][1].centery = self.shop_background_rect.top + 420

        self.shop_items[5].append(pygame.image.load(".\\resources\\1up.bmp"))
        self.shop_items_rects[5].append(self.shop_items[5][0].get_rect())
        self.shop_items_rects[5][0].centerx = self.shop_background_rect.left + 782
        self.shop_items_rects[5][0].centery = self.shop_background_rect.top + 420

    def blitme(self):
        """
        Muestra la tienda en pantalla
        """
        if self.shop_open:
            self.screen.blit(self.shop_background, self.shop_background_rect)
            self.screen.blit(self.exit_icon, self.exit_icon_rect)
            for i in range(len(self.shop_items)):
                self.screen.blit(self.shop_items[i][self.shop_progress[i]],
                                 self.shop_items_rects[i][self.shop_progress[i]])

    def upgrade(self, upgrade, ship, player):
        """
        Realizamos una accion u otra en funcion del input del usuario,
        que viene en el campo 'upgrade'
        """
        if upgrade == "repair":
            ship.health = ship.max_health
        elif upgrade == "speed" and self.shop_progress[1] < 3:
            ship.speed_factor += 3
            self.shop_progress[1] += 1
        elif upgrade == "health" and self.shop_progress[2] < 3:
            ship.max_health += 50
            ship.health = ship.max_health
            self.shop_progress[2] += 1
            if self.shop_progress[2] < 3:
                self.shop_progress[0] += 1
        elif upgrade == "damage" and self.shop_progress[3] < 3:
            ship.bullet_damage += 5
            self.shop_progress[3] += 1
        elif upgrade == "bpm" and self.shop_progress[1] < 1:
            self.settings.bullets_allowed += 2
            ship.bullet_speed_factor += 5
            self.shop_progress[4] += 1
        elif upgrade == "life":
            player.lifes += 1
            self.lifes_progress += 1
