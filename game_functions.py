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
        if ship.inmune:
            ship.rect = ship.image_inmune[ship.position].get_rect()
        else:
            ship.rect = ship.image[ship.position].get_rect()
    elif event.key == pygame.K_LEFT:
        ship.position = 1
        if ship.inmune:
            ship.rect = ship.image_inmune[ship.position].get_rect()
        else:
            ship.rect = ship.image[ship.position].get_rect()
    elif event.key == pygame.K_DOWN:
        ship.position = 2
        if ship.inmune:
            ship.rect = ship.image_inmune[ship.position].get_rect()
        else:
            ship.rect = ship.image[ship.position].get_rect()
    elif event.key == pygame.K_RIGHT:
        ship.position = 3
        if ship.inmune:
            ship.rect = ship.image_inmune[ship.position].get_rect()
        else:
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

def update_screen(settings, screen, player, aliens, bullets):
    """
    Actualiza las imagenes de la pantalla y mostrar
    en la nueva pantalla
    """
    # Redibuja la pantalla
    screen.fill(settings.bg_color)
    # Redibuja todos los proyectiles detras de la nave y aliens
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    for alien in aliens:
        for bullet in alien.bullets.sprites():
            bullet.draw_bullet()
    player.current_ship.blitme()
    for alien in aliens:
        alien.blitme()

    screen.blit(player.lifes_text, (settings.screen_width - 325, settings.screen_height - 65))
    # Hace visible la pantalla mas reciente
    pygame.display.flip()

def update_bullets(bullets, ship, aliens, settings, player):
    """
    Actualiza la posicion de los proyectiles y se deshace
    de los proyectiles viejos (se salen de la pantalla)
    """
    # Actualizamos los proyectiles de la nave del jugador
    bullets.update()
    # Nos desacemos de los proyectiles que esten fuera de la pantalla
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0 or bullet.rect.top >= settings.screen_height \
            or bullet.rect.right <= 0 or bullet.rect.left >= settings.screen_width:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    for alien in collisions.values():
        alien[0].hit(ship, aliens)

    # Actualizamos los proyectiles de los aliens
    for alien in aliens:
        alien.bullets.update()
        for bullet in alien.bullets.copy():
            # Nos desacemos de los proyectiles que esten fuera de la pantalla
            if bullet.rect.bottom <= 0 or bullet.rect.top >= settings.screen_height \
                or bullet.rect.right <= 0 or bullet.rect.left >= settings.screen_width:
                alien.bullets.remove(bullet)

        collisions = pygame.sprite.spritecollide(ship, alien.bullets, True)
        for collition in collisions:
            ship.hit(collition, player)

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
        if ship.position == 0:
            new_bullet = Bullet(settings, screen, ship.position,
                                ship.rect.centerx, ship.rect.top, ship.bullet_damage)
        elif ship.position == 1:
            new_bullet = Bullet(settings, screen, ship.position,
                                ship.rect.left, ship.rect.centery, ship.bullet_damage)
        elif ship.position == 2:
            new_bullet = Bullet(settings, screen, ship.position,
                                ship.rect.centerx, ship.rect.bottom, ship.bullet_damage)
        elif ship.position == 3:
            new_bullet = Bullet(settings, screen, ship.position,
                                ship.rect.right, ship.rect.centery, ship.bullet_damage)

        bullets.add(new_bullet)
