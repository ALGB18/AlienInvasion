"""
Modulo central del videojuego:
    - Bucle principal
    - Codigo principal (main)
    - Para correr el videojuego se debe ejecutar este archivo
"""
import random as r
import time
import pygame

from pygame.sprite import Group

from settings import Settings
from alien import Alien
from player import Player

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
    ship_bullets = Group()
    aliens = Group()

    player = Player(screen, settings)

    # Para el contador de fps
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
        gf.check_events(settings, screen, player.current_ship, ship_bullets)
        # Actualizamos la nave, aliens y proyectiles
        player.current_ship.update()
        gf.update_aliens(aliens, player.current_ship, settings)
        gf.update_bullets(ship_bullets, player.current_ship, aliens, settings, player)
        # Actualizamos la pantalla
        gf.update_screen(settings, screen, player, aliens, ship_bullets)
        # Incrementamos el contador de frames
        counter += 1
        # Imprimimos los fps (solo se muestran por segundo)
        if (time.time() - start_time) > seconds:
            print("FPS: ", counter / (time.time() - start_time))
            counter = 0
            start_time = time.time()
        # Limitamos los fps a 60
        clock.tick(settings.fps)

# Codigo principal (main)
if __name__ == "__main__":
    run_game()
