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
    alien_request_count = 0
    # Inicializamos la clase del thread para la generacion de aliens
    alien_generation_thread = ag.AlienGeneration(settings, aliens)

    # Creamos una nave
    ship = Ship(screen, settings)
    seconds = 1.0
    counter = 0
    start_time = time.time()
    # Empezamos el bucle principal del juego
    while True:
        # Comprobamos si hay aliens para generar y si no nos excedemos del maximo de aliens
        if alien_generation_thread.generated_aliens and len(aliens) < settings.max_aliens_in_game:
            print("DEBUG$$> An alien has just spawned")
            alien_to_create = alien_generation_thread.generated_aliens.pop()
            # Generamos un alien
            new_alien = Alien(settings, screen, alien_to_create)
            aliens.add(new_alien)

        # Generamos un alien con una probabilidad del 10%
        random_number = r.randint(0, 9)
        if random_number == 9 and alien_request_count < alien_generation_thread.max_requests:      
            x_position, y_position, position =\
                ag.start_position_algorithm("standart_alien", settings, aliens)
            alien_generation_thread.generated_aliens.append(
                ag.GeneratedAlien(x_position, y_position, position))
            print("DEBUG$$> An alien request has been generated")
            alien_request_count += 1
        # Escuchamos eventos de teclado y raton
        gf.check_events(settings, screen, ship, bullets, alien_generation_thread)
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
