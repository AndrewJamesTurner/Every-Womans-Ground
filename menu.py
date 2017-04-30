
import sys
import ezpygame
from Box2D import b2World, b2PolygonShape

import shapes
from game import *


class MenuScene(ezpygame.Scene):

    class MenuOption:
        def __init__(self, callback, image, y_pos, selectable):
            self.callback = callback
            self.image = image
            self.y_pos = y_pos
            self.selectable = selectable

        def activate(self):
            if self.callback is not None:
                self.callback()

    def __init__(self):
        # Called once per game, when game starts
        pass


    def on_enter(self, previous_scene):
        # Called every time the game switches to this scene

        self.options = []
        self.next_y = 0.4 * SCREEN_HEIGHT
        self.selected_idx = 0

        def new_game():
            self.application.change_scene(get_space_scene())

        self.add_option("New Game", new_game, 48)
        self.add_option("Exit", sys.exit, 48)

        title_font = pygame.font.Font("assets/Courgette-Regular.ttf", 56)
        self.title_image = title_font.render("Every Woman's Ground", True, (255, 255, 255))

        self.left_indicator_icon = pygame.image.load("assets/spaceship-side.png")
        scale_down = 0.4
        indicator_rect = self.left_indicator_icon.get_rect()
        self.left_indicator_icon = pygame.transform.smoothscale(self.left_indicator_icon, (int(indicator_rect.width * scale_down), int(indicator_rect.height * scale_down)))

    def add_option(self, text, callback, font_size, selectable=True):
        font = pygame.font.Font("assets/TitilliumWeb-Regular.ttf", font_size)
        label = font.render(text, True, (255, 255, 255))
        self.options.append(self.MenuOption(callback, label, self.next_y, selectable))

        self.next_y += font_size*1.2
        self.next_y += SCREEN_HEIGHT * 0.04

    def handle_event(self, event):
        # Called every time a pygame event is fired

        # Processing keyboard input here gives one event per key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER\
                    or event.key == pygame.K_SPACE:
                self.options[self.selected_idx].activate()

            adjustment = 0
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                adjustment = -1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                adjustment = 1

            self.selected_idx += adjustment
            self.selected_idx %= len(self.options)
            while not self.options[self.selected_idx].selectable:
                self.selected_idx += adjustment
                self.selected_idx %= len(self.options)

    def draw(self, screen):
        # Called once per frame, to draw to the screen

        screen.fill(black)

        screen.blit(self.title_image, (SCREEN_WIDTH / 2 - self.title_image.get_rect().width / 2, 100))

        for menu_option in self.options:
            x = 0.5 * SCREEN_WIDTH
            x -= menu_option.image.get_width() * 0.5
            screen.blit(menu_option.image, (x, menu_option.y_pos))

        selected_option = self.options[self.selected_idx]
        option_y = selected_option.y_pos
        option_y += selected_option.image.get_height() * 0.5
        option_y -= self.left_indicator_icon.get_height() * 0.5

        option_x = SCREEN_WIDTH * 0.5
        option_x -= selected_option.image.get_width() * 0.5
        option_x -= SCREEN_WIDTH * 0.05
        option_x -= self.left_indicator_icon.get_width()

        screen.blit(self.left_indicator_icon, (option_x, option_y))

    def update(self, dt):
        # Called once per frame, to update the state of the game
        pass

        # # Box2d physics step
        # self.world.Step(DT_SCALE * dt, VELOCITY_ITERATIONS, POSITION_ITERATIONS)
        # self.world.ClearForces()

if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(MenuScene())
