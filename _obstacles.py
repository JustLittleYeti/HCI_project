from random import randint

import pygame

class Obstacles:
    def __init__(self):
        self._x = 800
        self._y = 300
        self._minWidth, self._maxWidth = 20, 70
        self._minHeight, self._maxHeight = 30, 60
        self._minSpace, self.maxSpace = 40, 70
        self._space = 50
        self._current_space = 0
        self._counter = 0
        self.objects = []

    def _create(self):
        width = randint(self._minWidth,self._maxWidth)
        height = randint(self._minHeight,self._maxHeight)
        level = 100 if not randint(0,5) else 0
        y = self._y - height - level
        self.objects.append([self._x, y, width, height])

    def manage(self):
        self._current_space += 1
        if self._current_space > self._space:
            self._create()
            self._current_space = 0
            self._space = randint(self._minSpace,self.maxSpace)
        if self.objects:
            if self.objects[0][0] + self.objects[0][2] < 0:
                del self.objects[0]
                self._counter += 1  
        for obj in self.objects:
            obj[0] -= 5

    def draw(self, window):
        for obj in self.objects:
            pygame.draw.rect(window, (150,90,50), (
                obj[0],obj[1],obj[2],obj[3]))

    def getCounter(self):
        return self._counter