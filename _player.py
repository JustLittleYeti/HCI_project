import pygame

class Player:
    def __init__(self):
        self._x = 100
        self._y = 230
        self._width = 35
        self._height = 70
        self._duringJump = False
        self._jumpCountPattern = 20
        self._jumpCount = self._jumpCountPattern
        self._triggerJump = False

    def jump(self):
        self._triggerJump = True

    def run(self):
        if not self._duringJump:
            if self._triggerJump:
                self._duringJump = True
        else:
            if self._jumpCount >= -self._jumpCountPattern:
                neg = 1
                if self._jumpCount < 0:
                    neg = -1
                self._y -= (self._jumpCount ** 2) * neg * 0.05
                self._jumpCount -= 1
            else:
                self._triggerJump = False
                self._duringJump = False
                self._jumpCount = self._jumpCountPattern

    def collision(self, other):
        Ax0 = self._x
        Ax1 = self._x + self._width
        Ay0 = self._y
        Ay1 = self._y + self._height
        Bx0 = other[0]
        Bx1 = other[0] + other[2]
        By0 = other[1]
        By1 = other[1] + other[3]

        if Bx1 >= Ax0 >= Bx0 or Bx1 >= Ax1 >= Bx0:
            if By1 >= Ay0 >= By0 or By1 >= Ay1 >= By0:
                return True

        if Ax1 >= Bx0 >= Ax0 or Ax1 >= Bx1 >= Ax0:
            if Ay1 >= By0 >= Ay0 or Ay1 >= By1 >= Ay0:
                return True

    def draw(self, window):
        pygame.draw.rect(window, (255,100,100), (
            self._x, int(self._y), self._width, self._height))