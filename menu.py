"""
Este modulo contiene todo lo necesario para
dar soporte al menu de inicio, de pausa y
de compra
"""

class Shop():
    """
    Esta clase da soporte a la tienda del juego
    """
    def __init__(self):
        self.time_between_rounds = 30
        self.shop_background = None
        self.shop_background_rect = None
        self.shop_items = []
        self.shop_items_rects = []
        self.shop_progress = [0, 0, 0, 0, 0, 0, 0]
