#!/usr/bin/env python3
import contextlib
import logging
import sys

# don't print pygame welcome
with contextlib.redirect_stdout(None):
    import pygame
    from pygame.sprite import Group, spritecollide

from cultivate import settings
from cultivate.loader import get_music
from cultivate.map import Map
from cultivate.npc import Npc
from cultivate.sprites.pickups import Lemon, WaterBucket
from cultivate.player import Player
from cultivate.tooltip import Tooltip

K_INTERACT = pygame.K_x
K_QUIT_INTERACTION = pygame.K_q


def main(argv=sys.argv[1:]):
    # configure logging
    logging_config = {"level": logging.INFO,
                      "format": "%(levelname)-8s %(asctime)15s [%(filename)s@%(lineno)-3s] %(message)s"}
    # check for debug parameter
    if "--debug" in argv:
        settings.DEBUG = True
        logging_config["level"] = logging.DEBUG
    logging.basicConfig(**logging_config)

    # init pygame
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
    clock = pygame.time.Clock()
    pygame.mixer.init()
    bgm = get_music("beeball.ogg")
    bgm.play(-1)

    # init objects
    player = Player(settings.WIDTH // 2, settings.HEIGHT // 2)
    game_map = Map(player)

    npc_sprites = Group()
    npc_sprites.add(Npc([(1000, 1000), (1000, 1200), (1200, 1200), (1200, 1000)]))

    pickups = Group()
    pickups.add(Lemon(750, 750))
    pickups.add(WaterBucket(1000, 1000))

    tooltip_entries = Group()
    tooltip_entries.add(*npc_sprites)
    tooltip_entries.add(*pickups)
    tooltip_entries.add(game_map.bed)

    tooltip_bar = Tooltip()

    # main game loop
    while True:
        # check for user exit, ignore all other events
        logging.debug("Check for events")
        for event in pygame.event.get():
            if ((event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)
                    or (event.type == pygame.QUIT)):
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and player.pickup:
                    player.pickup.x = player.x + game_map.map_view_x
                    player.pickup.y = player.y + game_map.map_view_y
                    pickups.add(player.pickup)
                    tooltip_entries.add(player.pickup)
                    player.pickup = None
                elif event.key == K_INTERACT:
                    if not player.pickup:
                        picked_up = spritecollide(player, pickups, True)
                        if picked_up:
                            tooltip_entries.remove(picked_up)
                            player.pickup = picked_up.pop()
                            continue

                    if not player.interacting_with:
                        player.start_interact()

                elif event.key == K_QUIT_INTERACTION:
                    player.stop_interact()

                elif event.key == pygame.K_c:
                    to_interact = spritecollide(player, pickups, False)
                    if to_interact:
                        item = to_interact.pop()
                        if player.pickup and player.pickup.can_combine(item):
                            new_item = player.pickup.combine(item)
                            new_item.x = item.x
                            new_item.y = item.y
                            player.pickup = None
                            pickups.remove(item)
                            tooltip_entries.remove(item)
                            pickups.add(new_item)
                            tooltip_entries.add(new_item)

                elif event.type == pygame.KEYDOWN:
                    player.key_press(event.key)

        logging.debug("Update object positions")

        game_map.update_map_view(pygame.key.get_pressed())

        npc_sprites.update(game_map.get_viewport())
        pickups.update(game_map.get_viewport())
        player.update()


        interactions = []
        tooltip_bar.clear_tooltip()
        for item in tooltip_entries:
            tooltip_rect = player.tooltip_boundary(game_map.get_viewport())
            if tooltip_rect.colliderect(item.rect):
                if player.pickup and player.pickup.can_combine(item):
                    tooltip_bar.set_tooltip("Press c to combine")
                elif not player.pickup:
                    tooltip_bar.set_tooltip(f"press x to {item.get_help_text()}")

                player.set_nearby(item)
                break
            else:
                player.set_nearby(None)

        game_map.recompute_state()
        # draw objects at their updated positions
        logging.debug("Draw to buffer")
        game_map.draw(screen)
        game_map.state.draw(screen)
        pickups.draw(screen)

        player.draw(screen, pygame.key.get_pressed())

        for npc in npc_sprites:
            npc.draw(screen)

        if not player.conversation:
            tooltip_bar.draw(screen)

        # display FPS
        if settings.DEBUG:
            fps_str = f"FPS: {clock.get_fps():.2f}"
            fps_surface = settings.SM_FONT.render(fps_str, True, pygame.Color("black"))
            screen.blit(fps_surface, (50, 50))

        # display new draws
        logging.debug("Display buffer")
        pygame.display.flip()

        logging.debug("Wait for next frame")
        clock.tick(settings.FPS)

if __name__ == "__main__":
    main()
