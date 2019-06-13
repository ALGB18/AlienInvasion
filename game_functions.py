"""
Este modilo contiene las funciones que permiten
a Alien Invasion funcionar, y para que sea mas
facil de modificar
"""
import sys
import pygame

from bullet import Bullet

def check_events(settings, screen, ship, bullets):
    """
    Responder ante eventos del teclado y raton
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event, settings, screen, ship, bullets):
    """
    Responder ante pulsaciones de teclado
    """
    if event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_w:
        ship.moving_up = True
    elif event.key == pygame.K_s:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)
    elif event.key == pygame.K_UP:
        ship.position = 0
        ship.rect = ship.image[ship.position].get_rect()
    elif event.key == pygame.K_LEFT:
        ship.position = 1
        ship.rect = ship.image[ship.position].get_rect()
    elif event.key == pygame.K_DOWN:
        ship.position = 2
        ship.rect = ship.image[ship.position].get_rect()
    elif event.key == pygame.K_RIGHT:
        ship.position = 3
        ship.rect = ship.image[ship.position].get_rect()
    elif event.key == pygame.K_ESCAPE:
        sys.exit()

def check_keyup_events(event, ship):
    """
    Responder al liberar teclas
    """
    if event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_a:
        ship.moving_left = False
    elif event.key == pygame.K_w:
        ship.moving_up = False
    elif event.key == pygame.K_s:
        ship.moving_down = False

def update_screen(settings, screen, ship, aliens, bullets):
    """
    Actualiza las imagenes de la pantalla y mostrar
    en la nueva pantalla
    """
    # Redibuja la pantalla
    screen.fill(settings.bg_color)
    # Redibuja todos los proyectiles detras de la nave y aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # Hace visible la pantalla mas reciente
    pygame.display.flip()

def update_bullets(bullets, ship, settings):
    """
    Actualiza la posicion de los proyectiles y se deshace
    de los proyectiles viejos (se salen de la pantalla)
    """
    # Actualizamos los proyectiles
    bullets.update(ship)
    # Nos deshacemos de los proyectiles que hayan desaparecido
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0 or bullet.rect.top >= settings.screen_height \
            or bullet.rect.right <= 0 or bullet.rect.left >= settings.screen_width:
            bullets.remove(bullet)

def update_aliens(aliens, ship, settings):
    """
    Se encarga de actualizar la posicion de los aliens en la pantalla
    """
    aliens.update(ship, settings, aliens)


def fire_bullet(settings, screen, ship, bullets):
    """
    Creamos un proyectil (si no excedemos el limite) y lo
    incluimos en el grupo de proyectiles
    """
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)
