import pygame

from _player import Player
from _obstacles import Obstacles

class Game:
    def __init__(self):
        pygame.init()
        self._window = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("Game")
        self._background = pygame.image.load('_background.jpg').convert()
        self._smallFont = pygame.font.SysFont('calibri',30)
        self._bigFont = pygame.font.SysFont('calibri', 80)

    def _drawBackground(self):
        self._window.blit(self._background,(0,0))

    def _drawScore(self):
        text = self._smallFont.render(
            "SCORE: %d"%self.obstacles.getCounter(), 
            True,(200,200,200))
        self._window.blit(text,(50,360))

    def _drawLostScreen(self):
        header = self._bigFont.render("YOU HAVE LOST",True,(200,200,200))
        body = self._smallFont.render("JUMP TO START NEW GAME",True,(200,200,200))
        self._window.blit(header,(150,100))
        self._window.blit(body,(230,200))

    def newGame(self):
        self.player = Player()
        self.obstacles = Obstacles()
        self.run = True

    def move(self):
        self.player.jump()

    def manageEvents(self):
        self.player.run()
        self.obstacles.manage()
        if self.obstacles.objects:
            if self.player.collision(self.obstacles.objects[0]):
                self.lose()

    def renderFrame(self):
        self._drawBackground()
        self.player.draw(self._window)
        self.obstacles.draw(self._window)
        if not self.run:
            s = pygame.Surface((800,400))
            s.set_alpha(128)
            s.fill((0,0,0))
            self._window.blit(s, (0,0))
            self._drawLostScreen()
        self._drawScore()
        pygame.display.update()

    def lose(self):
        self.run = False