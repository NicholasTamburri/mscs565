import pygame

from constants import *


class Score(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.width = SCREEN_WIDTH
        self.height = 48

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = 1
        self.rect.y = 1

        self.value = 0

    def bubbles_popped(self, count):
        self.value += count

    def bubbles_dropped(self, count):
        if count > 0:
            self.value += 2 ** count

    def update(self):
        # Clear previous score
        self.image.fill(WHITE)

        score_str = "Score: " + str(self.value)
        font = pygame.font.SysFont("sans", 48)
        text = font.render(score_str, True, BLACK)
        self.image.blit(text, [0, 0])
