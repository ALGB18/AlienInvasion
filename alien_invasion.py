"""
Modulo central del videojuego:
    - Bucle principal
    -
"""
import random as r
import time
import pygame

from pygame.sprite import Group


from settings import Settings
from ship import Ship
from alien import Alien

import game_functions as gf
import alien_generation as ag
def run_game():
    """
    Funcion que contiene el bucle principal del juego,
    entre otras cosas
    """
    # Iniciar el juego, opciones, y objeto pantalla
    pygame.init()
    clock = pygame.time.Clock()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Creamos un grupo para almacenar los proyectiles
    bullets = Group()
    aliens = Group()

    # Creamos una nave
    ship = Ship(screen, settings)
    seconds = 1.0
    counter = 0
    start_time = time.time()
    # Empezamos el bucle principal del juego
    while True:
        # Generamos un alien con una probabilidad del 10% y si no superamos
        # el limite de aliens en pantalla
        random_number = r.randint(0, 9)
        if random_number == 9 and len(aliens) < settings.max_aliens_in_game:
            x_position, y_position, position =\
                ag.start_position_algorithm("standart_alien", settings, aliens)
            new_alien = Alien(settings, screen, x_position, y_position, position)
            aliens.add(new_alien)
            print("DEBUG$$> An alien has been generated")
        # Escuchamos eventos de teclado y raton
        gf.check_events(settings, screen, ship, bullets)
        ship.update()
        gf.update_aliens(aliens, ship, settings)
        gf.update_bullets(bullets, ship, settings)
        #print("FPS: " + str(clock.get_fps()))
        # Actualizamos la pantalla
        gf.update_screen(settings, screen, ship, aliens, bullets)
        counter += 1
        if (time.time() - start_time) > seconds:
            print("FPS: ", counter / (time.time() - start_time))
            counter = 0
            start_time = time.time()
        clock.tick(settings.fps)

if __name__ == "__main__":
    run_game()
