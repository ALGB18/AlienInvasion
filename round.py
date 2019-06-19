"""
Este modulo contendra la clase Ronda
"""
import random
import math

class RoundManager():
    """
    Clase que determina el numero de aliens de cada ronda,
    y que ademas genera los tipos de aliens de forma aleatoria
    """
    def __init__(self):
        self.num_round = 0
        self.alien_points = 0
        self.total_alien_points = 0
        self.aliens_to_generate = []
    def new_round(self):
        """
        Incrementamos en uno la ronda y calculamos los aliens
        para esta ronda
        """
        # Incrementar la ronda actual
        self.num_round += 1
        # Actualizar los puntos de generacion de aliens
        if self.num_round == 1:
            self.total_alien_points = 3
        else:
            self.total_alien_points += int(self.num_round / 2)
        self.alien_points = self.total_alien_points

        # Establecemos los aliens que vamos a generar en esta ronda
        while self.alien_points > 0:
            max_interval_value = 3
            # Comprobamos que no haya pocos puntos para generar aliens
            # y limitamos la generacion de aliens de alto nivel
            if self.alien_points <= 2:
                max_interval_value = 2
            elif self.alien_points <= 2:
                max_interval_value = 1
            max_interval_value = min(max_interval_value, self.round_based_alien_limitation())
            number = random.randint(0, 1)
            if number == 0 or number == 1:
                self.aliens_to_generate.append(0)
                self.alien_points -= 1
            elif number == 2:
                self.aliens_to_generate.append(1)
                self.alien_points -= 2
            elif number == 3:
                self.aliens_to_generate.append(2)
                self.alien_points -= 3

    def round_based_alien_limitation(self):
        """
        Retorna el maximo valor de intervalo permitido en funcion de
        la ronda en la que estemos. Por ejemplo:
        Por debajo de la ronda 5 no generaremos a los aliens
        "suicidas", por lo que limitamos el intervalo de numero
        aleatorio para que no se generen. Idem para los aliens
        cazas, que no apareceran hasta la ronda 10
        """
        if self.num_round < 5:
            return 1
        elif self.num_round < 10:
            return 2
        else:
            return 3

    def round_end(self, aliens):
        """
        Esta funcion retorna si la ronda ha terminado o no
        """
        return not (aliens or self.aliens_to_generate)
