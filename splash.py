import pygame

from constants import *


def display_splash_screen(screen):

    # Display game title
    font = pygame.font.SysFont("sans", 72)
    text = font.render("BUST-A-PUZZLE", True, BLACK)
    x = SCREEN_WIDTH // 2 - text.get_width() // 2
    y = 60
    screen.blit(text, [x, y])

    # Author
    y += text.get_height() + 4
    font = pygame.font.SysFont("sans", 24)
    text = font.render("by Nicholas Tamburri", True, BLACK)
    x = SCREEN_WIDTH // 2 - text.get_width() // 2
    y += 4
    screen.blit(text, [x, y])
