"""
Este modilo contiene las funciones que permiten
a Alien Invasion funcionar, y para que sea mas
facil de modificar
"""
import sys
import pygame

from bullet import Bullet

def check_events(settings, screen, ship, bullets, shop, round_ended, player):
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_mouse_button_down_events(shop, round_ended, ship, player)

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

def check_mouse_button_down_events(shop, round_ended, ship, player):
    """
    Responder ante eventos de raton
    """
    mouse_position = pygame.mouse.get_pos()
    aux = pygame.Rect(0, 0, 1, 1)
    aux.centerx = mouse_position[0]
    aux.centery = mouse_position[1]
    if round_ended:
        if aux.colliderect(shop.shop_icon_rect):
            shop.shop_open = True
            return
        if shop.shop_open:
            if aux.colliderect(shop.exit_icon_rect):
                shop.shop_open = False
                return
            if aux.colliderect(shop.shop_items_rects[0][shop.shop_progress[0]]):
                shop.upgrade("repair", ship, player)
                return
            elif aux.colliderect(shop.shop_items_rects[1][shop.shop_progress[1]]):
                shop.upgrade("speed", ship, player)
                return
            elif aux.colliderect(shop.shop_items_rects[2][shop.shop_progress[2]]):
                shop.upgrade("health", ship, player)
                return
            elif aux.colliderect(shop.shop_items_rects[3][shop.shop_progress[3]]):
                shop.upgrade("damage", ship, player)
                return
            elif aux.colliderect(shop.shop_items_rects[4][shop.shop_progress[4]]):
                shop.upgrade("bpm", ship, player)
                return
            elif aux.colliderect(shop.shop_items_rects[5][shop.shop_progress[5]]):
                shop.upgrade("life", ship, player)
                return

def update_screen(settings, screen, player, aliens, bullets, round_number,
                  round_ended, timer, round_end_time, shop):
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
    
    # Escribimos en pantalla el numero de ronda
    round_text = settings.my_font.render("Round " + str(round_number), False, (255, 255, 255))
    screen.blit(round_text, (10, 10))

    # Si la ronda ha terminado, imprimimos el tiempo restante para que empiece la siguiente
    if round_ended:
        next_round_text =\
            settings.my_font.render("Next round: " +
                                    str(round_end_time - int((pygame.time.get_ticks() - timer) / 1000))
                                                  + " s", False, (255, 255, 255))
        screen.blit(next_round_text, (settings.screen_width - 300, 10))
        screen.blit(shop.shop_icon, shop.shop_icon_rect)
        
        # Notificamos durante 5 segundos el final de la ronda al jugador (en medio de la pantalla)
        if pygame.time.get_ticks() - timer <= 5000:
            round_end_text = settings.my_font.render("Round " + str(round_number) + " ended. " +
                                                     "You can now open the shop",
                                                     False, (255, 255, 255))
            screen.blit(round_end_text, (settings.screen_width/2 - 300, settings.screen_height/2))
        shop.blitme()
    # Escribimos en pantala las vidas del jugador
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
                                ship.rect.centerx, ship.rect.top, ship.bullet_damage,
                                ship.bullet_speed_factor)
        elif ship.position == 1:
            new_bullet = Bullet(settings, screen, ship.position,
                                ship.rect.left, ship.rect.centery, ship.bullet_damage,
                                ship.bullet_speed_factor)
        elif ship.position == 2:
            new_bullet = Bullet(settings, screen, ship.position,
                                ship.rect.centerx, ship.rect.bottom, ship.bullet_damage,
                                ship.bullet_speed_factor)
        elif ship.position == 3:
            new_bullet = Bullet(settings, screen, ship.position,
                                ship.rect.right, ship.rect.centery, ship.bullet_damage,
                                ship.bullet_speed_factor)

        bullets.add(new_bullet)
