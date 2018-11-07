import pygame, math

from constants import *


class Arrow(pygame.sprite.Sprite):
    """ The player-controlled arrow that shoots bubbles. """

    LENGTH = 100
    WIDTH = 12

    HOME_Y = SCREEN_HEIGHT - 51

    BASE_IMAGE = pygame.Surface([WIDTH + 1, LENGTH])

    def __init__(self, centerx):
        super().__init__()
        self.image = Arrow.BASE_IMAGE
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        self.centerx = centerx

        pygame.draw.line(self.image, BLACK,
                         [Arrow.WIDTH / 2, 0],
                         [Arrow.WIDTH / 2, Arrow.LENGTH - Arrow.WIDTH * 3 / 2])
        pygame.draw.line(self.image, BLACK,
                         [Arrow.WIDTH / 2, Arrow.LENGTH - Arrow.WIDTH * 3 / 2],
                         [1, Arrow.LENGTH])
        pygame.draw.line(self.image, BLACK,
                         [Arrow.WIDTH / 2, Arrow.LENGTH - Arrow.WIDTH * 3 / 2],
                         [Arrow.WIDTH - 1, Arrow.LENGTH])
        pygame.draw.polygon(self.image, BLACK, [
            [Arrow.WIDTH / 2, 0],
            [0, Arrow.WIDTH * 2],
            [Arrow.WIDTH, Arrow.WIDTH * 2]
        ])
        self.rect = self.image.get_rect()
        self.rect.centerx = self.centerx
        self.rect.centery = Arrow.HOME_Y

        # Angle is in degrees.
        # 0 is straight up, positive is left, negative is right
        self.angle = 0 # degrees
        self.change_angle = 0

    def update(self):
        self.angle += self.change_angle
        if self.angle >= 86:
            self.angle = 85
        if self.angle <= -86:
            self.angle = -85

        self.image = pygame.transform.rotate(Arrow.BASE_IMAGE, self.angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.centerx
        self.rect.centery = Arrow.HOME_Y


class Ceiling(pygame.sprite.Sprite):
    """ Top border of the play field. """
    def __init__(self, board):
        super().__init__()

        self.image = pygame.Surface([board.width + 2, 1])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = board.x
        self.rect.y = board.y


class Wall(pygame.sprite.Sprite):
    """ Left and right borders of the play field. """
    def __init__(self, x, board):
        super().__init__()

        self.image = pygame.Surface([1, SCREEN_HEIGHT])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = board.y


class KillLine(pygame.sprite.Sprite):
    """ Game over when board bubbles cross this line. """
    def __init__(self, y, board):
        super().__init__()

        self.image = pygame.Surface([board.width + 2, 1])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = board.x
        self.rect.y = y


class Board(object):
    """ This class represents the game board. """
    BUBBLE_RADIUS = 20
    BUBBLE_DIAMETER = BUBBLE_RADIUS * 2

    COLUMNS = 8
    ROWS = 11

    WIDTH = COLUMNS * BUBBLE_DIAMETER

    # Some math to find vertical spacing of the bubbles
    Y_SPACE = math.sqrt(4 / 5 * (
            math.sqrt(BUBBLE_RADIUS ** 2 + BUBBLE_DIAMETER ** 2) \
            - BUBBLE_DIAMETER \
        ) ** 2) \
              + math.sqrt(BUBBLE_RADIUS ** 2 + BUBBLE_DIAMETER ** 2) \
              - BUBBLE_DIAMETER
    # For reference, here is the math:
    # distance = math.sqrt(Bubble.RADIUS ** 2 + Bubble.DIAMETER ** 2)
    # space = distance - Bubble.DIAMETER
    # y_space = math.sqrt(4 / 5 * space ** 2)

    def __init__(self):
        super().__init__()

        self.bubble_radius = Board.BUBBLE_RADIUS
        self.bubble_diameter = Board.BUBBLE_DIAMETER

        self.width = Board.WIDTH
        self.x = SCREEN_WIDTH / 2 - self.width / 2
        self.y = 50

        self.columns = Board.COLUMNS
        self.rows = Board.ROWS
        self.y_space = Board.Y_SPACE

        self.arrow = Arrow(self.x + self.width / 2 + 2)
        self.bubble_list = pygame.sprite.Group()

        self.ceiling = Ceiling(self)
        self.left_wall = Wall(self.x, self)
        self.right_wall = Wall(self.x + self.width + 1, self)

        kill_line_y = self.y + self.rows * (self.bubble_diameter - self.y_space) + self.y_space
        self.kill_line = KillLine(kill_line_y, self)