import pygame

from constants import *


class Score(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.width = SCREEN_WIDTH
        self.height = 96

        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = 1
        self.rect.y = 1

        self.value = 0

    def bubbles_popped(self, count):
        self.value += count * 10

    def bubbles_dropped(self, count):
        points = 0
        if count > 0:
            # Limit drop bonus to 17 bubbles, i.e. 1310720 points
            if count > 17:
                count = 17
            points = (2 ** count) * 10
            self.value += points
        return points

    def time_bonus(self, seconds):
        self.value += max(0, 500000 - 10000 * max(0, seconds - 15))

    def update(self):
        # Clear previous score
        self.image.fill(WHITE)

        font = pygame.font.SysFont("sans", 48)
        text = font.render("Score", True, BLACK)
        self.image.blit(text, [0, 0])

        y = text.get_height()
        text = font.render(str(self.value), True, BLACK)
        self.image.blit(text, [0, y])


class DropScore(pygame.sprite.Sprite):
    """ This number pops up to let the player know how many points were earned
        from a drop. """

    def __init__(self, points):
        super().__init__()

        font = pygame.font.SysFont("sans", 36)
        self.text = font.render(str(points), True, BLACK)

        self.image = pygame.Surface([self.text.get_width(),
                                     self.text.get_height()])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT // 2 + 10

        self.frame = 0

    def update(self):
        self.frame += 1

        if self.frame > 120:  # Two seconds, at 60 fps
            self.kill()

        elif self.frame < 30 and self.frame % 3 == 0:
            self.rect.centery -= 1

        self.image.blit(self.text, [0, 0])
