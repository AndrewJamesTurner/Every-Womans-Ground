
import sys
from game import *

from menu import MenuScene


class WinScene(MenuScene):

    def on_enter(self, previous_scene):
        super(WinScene, self).on_enter(previous_scene)
        
        message_font = pygame.font.Font("assets/Courgette-Regular.ttf", 72)
        self.title_image = message_font.render("You Win", True, (255, 255, 255))

        def new_game():
            self.application.change_scene(get_space_scene())

        self.add_option("Restart Game", new_game, 48)
        self.add_option("Quit", sys.exit, 48)

    def draw(self, screen):
        screen.fill((50, 100, 255))

        self.draw_menu_options(screen)

        screen.blit(self.title_image, (SCREEN_WIDTH / 2 - self.title_image.get_rect().width / 2, 100))

if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(WinScene())
