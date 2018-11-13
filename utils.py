import pygame
import random

from constants import RED


def sprite_at(position, sprite_list):
    point = pygame.sprite.Sprite()
    point.image = pygame.Surface([1, 1])
    point.rect = point.image.get_rect()
    point.rect.x = position[0]
    point.rect.y = position[1]
    return pygame.sprite.spritecollideany(point, sprite_list)


def determine_next(board):
    colors = []
    for bubble in board.bubble_list:
        if bubble.color not in colors and bubble.color in board.BUBBLE_COLORS:
            colors.append(bubble.color)
    if len(colors) == 0:
        return RED
    return colors[random.randrange(len(colors))]


def is_board_cleared(board):
    colors = []
    for bubble in board.bubble_list:
        if bubble.color not in colors and bubble.color in board.BUBBLE_COLORS:
            colors.append(bubble.color)
    return len(colors) == 0
