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
from round import RoundManager
from menu import Shop

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
    round_ended = False
    round_manager = RoundManager()
    timer = pygame.time.get_ticks()
    shop_manager = Shop()

    player = Player(screen, settings)

    round_manager.new_round()
    # Para el contador de fps
    seconds = 1.0
    counter = 0
    start_time = time.time()
    # Empezamos el bucle principal del juego
    while True:
        # Generamos aliens si estamos en ronda, si no nos excedemos del numero de aliens
        # posibles y si hay aliens disponibles para generar (si no se han acabado los
        # aliens de la ronda)
        if not round_ended:
            if len(aliens) < settings.max_aliens_in_game and round_manager.aliens_to_generate:
                # Obtenemos el tipo de alien a generar
                alien = round_manager.aliens_to_generate.pop()
                # Calculamos la posicion del alien a generar
                x_position, y_position, position =\
                    ag.start_position_algorithm("standart_alien", settings, aliens)
                # Generamos un tipo de alien u otro:
                #   - Alien = 0 -> Alien estandar
                #   - Alien = 1 -> Alien highroller
                #   - Alien = 2 -> Alien caza
                if alien == 0:
                    new_alien = Alien(settings, screen, x_position, y_position, position)
                elif alien == 1:
                    new_alien = Alien(settings, screen, x_position, y_position, position)
                elif alien == 2:
                    new_alien = Alien(settings, screen, x_position, y_position, position)
                # Insertamos el alien generado en la lista de aliens que gestionamos en
                # la pantalla
                aliens.add(new_alien)
                print("DEBUG$$> An alien has been generated")
            # Comprobamos si se ha acabado la ronda
            round_ended = round_manager.round_end(aliens)
            # Si efectivamente se ha acabado la ronda, actualizamos el timer para
            # que podamos contar 30 segundos
            if round_ended:
                print("DEBUG$$> Fin de ronda")
                timer = pygame.time.get_ticks()
        else:
            # Comprobamos que hallamos excedido los 30 segundos entre rondas
            # para empezar una nueva
            if pygame.time.get_ticks() - timer > shop_manager.time_between_rounds * 1000:
                print("DEBUG$$> Comienzo de nueva ronda")
                # Iniciamos una nueva ronda
                round_manager.new_round()
                round_ended = False

        # Escuchamos eventos de teclado y raton
        gf.check_events(settings, screen, player.current_ship, ship_bullets)
        # Actualizamos la nave, aliens y proyectiles
        player.current_ship.update()
        gf.update_aliens(aliens, player.current_ship, settings)
        gf.update_bullets(ship_bullets, player.current_ship, aliens, settings, player)
        # Actualizamos la pantalla
        gf.update_screen(settings, screen, player, aliens, ship_bullets, round_manager.num_round,
                         round_ended, timer, shop_manager.time_between_rounds)
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
