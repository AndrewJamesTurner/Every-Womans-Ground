
import sys
from game import *

from menu import MenuScene


class MessageScene(MenuScene):

    def on_enter(self, previous_scene):
        # Called every time the game switches to this scene

        super(MessageScene, self).on_enter(previous_scene)

        def new_game():
            self.application.change_scene(get_space_scene())

        self.next_y += 200
        self.add_option("Search for a new home", new_game, 48)

        messages = [
'Earth is fast becoming uninhabitable. ',
'Womankind must search for a new planet to call home. ',
'',
'Captain your spaceship to new planets, successfully land',
'and discover whether it can sustain life.',
'Don’t run out of fuel, oxygen or take too much damage',
'or it’s game over!',
'',
'The future of womankind is in your hands. ',
'',
'Can you find the new Earth that will become',
'"Every Woman\'s Ground"?',
]

        message_font = pygame.font.Font("assets/Courgette-Regular.ttf", 30)
        self.message_images = []
        for message in messages:
            self.message_images.append(message_font.render(message, True, (255, 255, 255)))

        self.backdrop = pygame.image.load("assets/backdrop1.jpg").convert()
        scale_down = 1
        backdrop_rect = self.backdrop.get_rect()
        self.backdrop = pygame.transform.smoothscale(self.backdrop, (int(backdrop_rect.width * scale_down), int(backdrop_rect.height * scale_down)))

    def draw(self, screen):
        screen.fill(black)

        screen.blit(self.backdrop, (0, 0))

        self.draw_menu_options(screen)

        y_pos = 50
        for message_image in self.message_images:
            screen.blit(message_image, (80, y_pos))
            y_pos += 30

if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(MessageScene())
