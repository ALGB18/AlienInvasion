"""
Define los distintos tipos de aliens
"""
import math
import random
import pygame
from pygame.sprite import Sprite, Group
import bullet

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
        # Definimos el conjunto de proyectiles y el maximo de estos en pantalla
        # Ademas definimos un timer para limitar la cadencia de los disparos
        self.bullets = Group()
        self.maximun_bullets = 5
        self.timer = 0.0
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
            # Comprobamos que el alien tenga una coordenadas a las que dirigirse o
            # si ya ha alcanzado estas coordenadas. En ambos casos calculamos
            # una nueva
            if (self.coordinates_to_move is None) or (self.reached_destination()):
                # Las coordenadas a las que moverse se calculan de forma aleatoria,
                # dentro de la pantalla
                self.coordinates_to_move = (random.randint(0, settings.screen_width),
                                            random.randint(0, settings.screen_height))
            # Comprobamos que el alien no haya colisionado con otros:
            # 1.- Primero hay que eliminar el propio alien de la lista de aliens
            #     para que no nos devuelva Verdadero siempre
            alien_group.remove(self)
            # 2.- Comprobamos las colisiones que se producen
            collisions = self.collide(alien_group)
            # 3.- Volvemos a añadir el alien actual a la lista de aliens
            alien_group.add(self)
            # 4.- Si ocurren colisiones (colissions != None) actuamos en consecuencia
            if collisions:
                # Calculamos la direccion opuesta a los aliens con los que colisionamos
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
                # No ocurren colisiones asi que movemos al alien normalmente
                # Necesitamos calcular el vector unitario para determinar la direccion en la que
                # mover el alien
                new_position = self.position_towards_destination()
                if new_position:
                    self.rect.centerx += new_position[0] * settings.standart_alien_speed_factor
                    self.rect.centery += new_position[1] * settings.standart_alien_speed_factor

            # Comprobamos si podemos disparar (no nos excedemos del maximo de balas en pantalla)
            if len(self.bullets) < self.maximun_bullets:
                # Obtenemos los parametros de los proyectiles (direccion y sentido) y si
                # estamos en condiciones de disparar (el angulo que se forma entre la nave
                # del jugador y el alien es mayor que el establecido en las opciones)
                if pygame.time.get_ticks() - self.timer > 400.0:
                    self.timer = pygame.time.get_ticks()
                    bullet_parameters = self.check_for_shooting(ship, settings)
                    if bullet_parameters:
                        new_bullet = bullet.Bullet(self.settings, self.screen, bullet_parameters[0],
                                               bullet_parameters[1], bullet_parameters[2])
                        self.bullets.add(new_bullet)

        else:
            # Si el alien no esta el la pantalla reducimos una de las coordenadas
            # hasta que aparezca en pantalla
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
            # Comprobamos si el alien esta en pantalla
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

    def check_for_shooting(self, ship, settings):
        """
        Metodo que retorna lso parametros para crear una bala
        si el alien esta en condiciones de disparar, sino
        retorna falso
        """
        if math.fabs(self.rect.centerx - ship.centerx) <=\
           math.fabs(self.rect.centery - ship.centery):
            # Disparamos hacia abajo o hacia arriba
            if self.rect.centery - ship.centery >= 0:
                # El alien esta debajo del jugador, disparamos hacia arriba
                position = 0
                center = self.rect.centerx
                top = self.rect.top
            else:
                # El alien esta encima del jugador, disparamos hacia abajo
                position = 2
                center = self.rect.centerx
                top = self.rect.bottom

        else:
            # Disparamos hacia la derecha o hacia la izquierda
            if self.rect.centerx - ship.centerx >= 0:
                # El alien esta a la derecha del jugador, disparamos hacia la izquierda
                position = 1
                center = self.rect.left
                top = self.rect.centery
            else:
                # El alien esta a la izquierda del jugador, disparamos hacia la derecha
                position = 3
                center = self.rect.right
                top = self.rect.centery

        # Calculamos el angulo que forma la nave del jugador con este alien
        hyperbole = math.sqrt((self.rect.centerx - ship.rect.centerx) ** 2
                              + (self.rect.centery - ship.rect.centery) ** 2)
        opposite_side = math.fabs(self.rect.centerx - ship.rect.centerx)
        try:
            degrees = math.degrees(math.asin(opposite_side/hyperbole))
        except ZeroDivisionError:
            return False

        # Comprobamos que el angulo sea lo suficientemente pequenio para los disparos desde
        # arriba y desde abajo, y que sea suficientemente grande para los disparos desde la
        # derecha y desde la izquierda
        if (position == 0 or position == 2) and degrees < settings.minimun_degrees_to_shoot:
            return (position, center, top)
        elif (position == 1 or position == 3) and \
            degrees > (90 - settings.minimun_degrees_to_shoot) and degrees < 90:
            return (position, center, top)
        return False
