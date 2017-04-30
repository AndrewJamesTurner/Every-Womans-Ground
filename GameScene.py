
import pygame
import ezpygame

from game import *
import constants



class FillBar:

    def __init__(self, font, font_size, text, colour):
        font = pygame.font.Font(font, font_size)
        self.text_surface = font.render(text, True, colour)
        self.text_rect = self.text_surface.get_rect()

    def draw(self, screen, text_left, text_top, text_bar_padding, bar_width, bar_length,
             bar_border_width, bar_background_colour, bar_foreground_colour, bar_border_colour,
             bar_value, bar_max_value):
        screen.blit(self.text_surface, (text_left, text_top))
        fuel_bar_left = text_left + self.text_rect.width + text_bar_padding
        fuel_bar_top = text_top + self.text_rect.height / 2 - bar_width / 2
        fuel_bar_fill_length = bar_value / bar_max_value * bar_length

        pygame.draw.rect(screen, bar_background_colour,
                         (fuel_bar_left, fuel_bar_top, bar_length, bar_width), 0)
        pygame.draw.rect(screen, bar_foreground_colour,
                         (fuel_bar_left, fuel_bar_top, fuel_bar_fill_length, bar_width), 0)
        pygame.draw.rect(screen, bar_border_colour,
                         (fuel_bar_left, fuel_bar_top, bar_length, bar_width), bar_border_width)






class TextBox:

    def __init__(self, font, font_size, text, colour):
        font = pygame.font.Font(font, font_size)
        self.text_surface = font.render(text, True, colour)
        self.text_rect = self.text_surface.get_rect()

    def draw(self, screen, text_left, text_top, text_bar_padding, bar_width, bar_length,
             bar_border_width, bar_background_colour, bar_foreground_colour, bar_border_colour,
             bar_value, bar_max_value):
        screen.blit(self.text_surface, (text_left, text_top))
        fuel_bar_left = text_left + self.text_rect.width + text_bar_padding
        fuel_bar_top = text_top + self.text_rect.height / 2 - bar_width / 2
        fuel_bar_fill_length = bar_value / bar_max_value * bar_length

        pygame.draw.rect(screen, bar_background_colour,
                         (fuel_bar_left, fuel_bar_top, bar_length, bar_width), 0)
        pygame.draw.rect(screen, bar_foreground_colour,
                         (fuel_bar_left, fuel_bar_top, fuel_bar_fill_length, bar_width), 0)
        pygame.draw.rect(screen, bar_border_colour,
                         (fuel_bar_left, fuel_bar_top, bar_length, bar_width), bar_border_width)



class GameScene(ezpygame.Scene):
    """
    Common base class for all the scenes that are part of the game.
    Used to draw common overlays such as the fuel bar.
    """

    def __init__(self):
        self.fuel_bar = FillBar(font="assets/TitilliumWeb-Regular.ttf", font_size=25,
                                text="Fuel", colour=(200, 200, 0))
        self.health_bar = FillBar(font="assets/TitilliumWeb-Regular.ttf", font_size=25,
                                  text="Health", colour=(150, 50, 50))
        self.oxygen_bar = FillBar(font="assets/TitilliumWeb-Regular.ttf", font_size=25,
                                  text="Oxygen", colour=(50, 150, 150))




    def check_game_over(self):

        shared_values = get_shared_values()

        if shared_values.fuel <= 0 or shared_values.health <= 0 or shared_values.oxygen <= 0:
            self.application.change_scene(get_game_over_scene())


    def check_shared_values(self):

        shared_values = get_shared_values()

        if shared_values.health > MAX_HEALTH:
            shared_values.health = MAX_HEALTH

        if shared_values.fuel > MAX_FUEL:
            shared_values.fuel = MAX_FUEL


    def draw_overlays(self, screen):

        self.fuel_bar.draw(screen, text_left=20, text_top=10, text_bar_padding=10,
                           bar_width=20, bar_length=100, bar_border_width=3,
                           bar_background_colour=(50, 50, 50), bar_foreground_colour=(200, 200, 0),
                           bar_border_colour=(200, 200, 200),
                           bar_value=get_shared_values().fuel, bar_max_value=constants.MAX_FUEL)

        self.health_bar.draw(screen, text_left=205, text_top=10, text_bar_padding=10,
                             bar_width=20, bar_length=100, bar_border_width=3,
                             bar_background_colour=(50, 50, 50), bar_foreground_colour=(150, 50, 50),
                             bar_border_colour=(200, 200, 200),
                             bar_value=get_shared_values().health, bar_max_value=constants.MAX_HEALTH)

        self.oxygen_bar.draw(screen, text_left=420, text_top=10, text_bar_padding=10,
                             bar_width=20, bar_length=100, bar_border_width=3,
                             bar_background_colour=(50, 50, 50), bar_foreground_colour=(50, 150, 150),
                             bar_border_colour=(200, 200, 200),
                             bar_value=get_shared_values().oxygen, bar_max_value=constants.MAX_OXYGEN)




