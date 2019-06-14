"""
En este modulo definiremos los algoritmos de
ubicacion inicial de los aliens en la pantalla
"""
import math
import random as r

def start_position_algorithm(request, settings, aliens):
    """
    Esta funcion calcula una ubicacion en la que
    ubicar un alien para su creacion
    """
    # Flag para controlar si la ubicacion del alien
    # no colisiona con otros
    flag_colision = True

    # Mientras que no sea una ubicacion correcta recalculamos
    # esta ubicacion

    while flag_colision:
        # Determinamos si se ubicara encima, debajo, a la izquierda o a la derecha
        # de la pantalla
        pos = r.randint(0, 3)
        # Si pos vale 0, el alien se generara en la parte superior de la pantalla
        # Si pos vale 1, el alien se generara en la parte inferior de la pantalla
        # Si pos vale 2, el alien se generara en la parte izquierda de la pantalla
        # Si pos vale 3, el alien se generara en la parte derecha de la pantalla
        if pos == 0:
            x_position = r.randint(0, settings.screen_width)
            y_position = r.randint(-1024, -128)
        elif pos == 1:
            x_position = r.randint(0, settings.screen_width)
            y_position = r.randint(settings.screen_height + 128,
                                   settings.screen_height + 1024)
        elif pos == 2:
            x_position = r.randint(-1024, -128)
            y_position = r.randint(0, settings.screen_height)
        elif pos == 3:
            x_position = r.randint(settings.screen_width + 128,
                                   settings.screen_width + 1024)
            y_position = r.randint(0, settings.screen_height)

        # Comprobamos que la ubicacion es correcta
        flag_colision = colision(x_position, y_position, aliens)
    # Llegados a este punto la ubicacion calculada es correcta y la retornamos
    return x_position, y_position, pos

def colision(x_position, y_position, aliens):
    """
    Esta funcion devuelve True si en las coordenadas proporcionadas
    se produce la colision con otro alien, False en caso contrario
    """
    for alien in aliens:
        if math.fabs(alien.x_position - x_position) < 64 or \
           math.fabs(alien.y_position - y_position) < 64:
            return True
    return False
