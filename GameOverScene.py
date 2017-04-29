
from game import *


class GameOverScene(ezpygame.Scene):

    def __init__(self):
        message_font = pygame.font.Font("assets/Courgette-Regular.ttf", 72)
        self.message_image = message_font.render("Game Over", True, (255, 255, 255))

    def on_enter(self, previous_scene):
        pass

    def handle_event(self, event):
        pass

    def draw(self, screen):
        screen.fill(black)

        screen.blit(self.message_image, (SCREEN_WIDTH / 2 - self.message_image.get_rect().width / 2, 200))

    def update(self, dt):
        pass

if __name__ == '__main__':
    app = ezpygame.Application(title='The Game', resolution=(SCREEN_WIDTH, SCREEN_HEIGHT), update_rate=FPS)
    app.run(GameOverScene())
