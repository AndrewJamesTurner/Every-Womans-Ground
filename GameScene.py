
import pygame
import ezpygame

from game import *

FUEL_MESSAGE_COLOUR = (50, 150, 150)
FUEL_MESSAGE_TOP = 10
FUEL_MESSAGE_LEFT = 20
FUEL_BAR_BACKGROUND_COLOUR = (50, 50, 50)
FUEL_BAR_FOREGROUND_COLOUR = FUEL_MESSAGE_COLOUR
FUEL_BAR_BORDER_COLOUR = (200, 200, 200)
FUEL_BAR_LENGTH = 100
FUEL_BAR_WIDTH = 20
FUEL_BAR_PADDING = 10
FUEL_BAR_BORDER_WIDTH = 3


class GameScene(ezpygame.Scene):
    """
    Common base class for all the scenes that are part of the game.
    Used to draw common overlays such as the fuel bar.
    """

    def __init__(self):
        font = pygame.font.Font("assets/TitilliumWeb-Regular.ttf", 30)
        self.fuel_text = font.render("Fuel", True, FUEL_MESSAGE_COLOUR)
        self.fuel_text_rect = self.fuel_text.get_rect()

    def draw_overlays(self, screen):
        screen.blit(self.fuel_text, (FUEL_MESSAGE_LEFT, FUEL_MESSAGE_TOP))
        fuel_bar_left = FUEL_MESSAGE_LEFT + self.fuel_text_rect.width + FUEL_BAR_PADDING
        fuel_bar_top = FUEL_MESSAGE_TOP + self.fuel_text_rect.height / 2 - FUEL_BAR_WIDTH / 2
        fuel_bar_fill_length = get_shared_values().fuel / get_shared_values().MAX_FUEL * FUEL_BAR_LENGTH

        pygame.draw.rect(screen, FUEL_BAR_BACKGROUND_COLOUR,
                         (fuel_bar_left, fuel_bar_top, FUEL_BAR_LENGTH, FUEL_BAR_WIDTH), 0)
        pygame.draw.rect(screen, FUEL_BAR_FOREGROUND_COLOUR,
                         (fuel_bar_left, fuel_bar_top, fuel_bar_fill_length, FUEL_BAR_WIDTH), 0)
        pygame.draw.rect(screen, FUEL_BAR_BORDER_COLOUR,
                         (fuel_bar_left, fuel_bar_top, FUEL_BAR_LENGTH, FUEL_BAR_WIDTH), FUEL_BAR_BORDER_WIDTH)

        # print(get_shared_values().MAX_FUEL / get_shared_values().fuel)
        # print(get_shared_values().fuel)
