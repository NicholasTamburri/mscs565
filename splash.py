import pygame

from constants import *


def display_splash_screen(screen, image1, image2, image3):

    # Display game title
    font = pygame.font.SysFont("sans", 72)
    text = font.render("BUST-A-PUZZLE", True, BLACK)
    x = SCREEN_WIDTH // 2 - text.get_width() // 2
    y = 10
    screen.blit(text, [x, y])

    # Author
    y += text.get_height() + 4
    font = pygame.font.SysFont("sans", 24)
    text = font.render("by Nicholas Tamburri", True, BLACK)
    x = SCREEN_WIDTH // 2 - text.get_width() // 2
    screen.blit(text, [x, y])

    # How to play
    y += text.get_height() + 24
    text = font.render("Clear the bubbles by shooting same-colored groups.",
                       True, BLACK)
    x = SCREEN_WIDTH // 2 - text.get_width() // 2
    screen.blit(text, [x, y])

    y += text.get_height() + 8
    font = pygame.font.SysFont("sans", 24, bold=True)
    text = font.render("Use the arrow keys to aim and the space bar to fire.",
                       True, BLACK, True)
    x = SCREEN_WIDTH // 2 - text.get_width() // 2
    screen.blit(text, [x, y])

    # Game images
    y += text.get_height() + 30
    width1 = image1.get_rect().width
    width2 = image2.get_rect().width
    width3 = image3.get_rect().width
    space = (SCREEN_WIDTH - width1 - width2 - width3) // 4
    x = space
    screen.blit(image1, [x, y])

    x += width1 + space
    screen.blit(image2, [x, y])

    x += width2 + space
    screen.blit(image3, [x, y])

    # Click to begin
    y = SCREEN_HEIGHT - 50
    text = font.render("Press the Return key or click the screen to begin.",
                       True, BLACK)
    x = SCREEN_WIDTH // 2 - text.get_width() // 2
    screen.blit(text, [x, y])
