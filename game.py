"""
Nicholas Tamburri
Version 0.0.1

Game code for Bust-a-Move clone.

Play by shooting bubbles at other bubbles.
"""

import math
import pygame
import random

# --- Global constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500


# --- Classes ---


class Arrow(pygame.sprite.Sprite):
    """ The player-controlled arrow that shoots bubbles. """

    LENGTH = 100
    WIDTH = 12

    HOME_X = SCREEN_WIDTH / 2 - 1
    HOME_Y = SCREEN_HEIGHT - 51

    BASE_IMAGE = pygame.Surface([WIDTH + 1, LENGTH])

    def __init__(self):
        super().__init__()
        self.image = Arrow.BASE_IMAGE
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

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
        self.rect.centerx = Arrow.HOME_X
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
        self.rect.centerx = Arrow.HOME_X
        self.rect.centery = Arrow.HOME_Y


class Bubble(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """

    def __init__(self, centerx, centery):
        """ Constructor, create the image of the block. """
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        pygame.draw.circle(self.image, BLACK, [10, 10], 10)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.radius = 10

        self.float_centerx = float(self.rect.centerx)
        self.float_centery = float(self.rect.centery)

        self.x_change = 0
        self.y_change = 0

    def reset_pos(self):
        """ Called when the bubble falls off the screen. """
        self.x_change = 0
        self.y_change = 0

        self.rect.centerx = Arrow.HOME_X
        self.rect.centery = Arrow.HOME_Y

        self.float_centerx = float(self.rect.centerx)
        self.float_centery = float(self.rect.centery)

    def update(self):
        """ Automatically called when we need to move the block. """
        self.float_centerx += self.x_change
        self.float_centery += self.y_change

        self.rect.centerx = int(self.float_centerx)
        self.rect.centery = int(self.float_centery)

        # Ricochet off borders
        if self.rect.left < 0 or self.rect.right >= SCREEN_WIDTH:
            self.x_change *= -1
        if self.rect.top < 0:
            self.y_change *= -1

        if self.rect.centery > SCREEN_HEIGHT + self.rect.height:
            self.reset_pos()


class Ceiling(pygame.sprite.Sprite):
    """ Top border of the play field. """
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([400, 1])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = 150
        self.rect.y = 50


class Wall(pygame.sprite.Sprite):
    """ Left and right borders of the play field. """
    def __init__(self, x):
        super().__init__()

        self.image = pygame.Surface([1, SCREEN_HEIGHT])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 50


class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """

        self.score = 0
        self.game_over = False

        self.k_left_is_pressed = False
        self.k_up_is_pressed = False
        self.k_right_is_pressed = False

        # Create sprite lists
        self.bubble_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        # Create play field borders
        self.ceiling = Ceiling()
        self.left_wall = Wall(150)
        self.right_wall = Wall(550)
        self.all_sprites_list.add(self.ceiling)
        self.all_sprites_list.add(self.left_wall)
        self.all_sprites_list.add(self.right_wall)

        # Create the arrow
        self.arrow = Arrow()
        self.all_sprites_list.add(self.arrow)

        # Create the bubble
        self.bubble = Bubble(self.arrow.rect.centerx, self.arrow.rect.centery)
        self.bubble_list.add(self.bubble)
        self.all_sprites_list.add(self.bubble)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.k_left_is_pressed = True
                if event.key == pygame.K_UP:
                    self.k_up_is_pressed = True
                if event.key == pygame.K_RIGHT:
                    self.k_right_is_pressed = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.k_left_is_pressed = False
                if event.key == pygame.K_UP:
                    self.k_up_is_pressed = False
                if event.key == pygame.K_RIGHT:
                    self.k_right_is_pressed = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE\
                    and self.bubble.x_change == 0 and self.bubble.y_change == 0:
                speed = 5
                self.bubble.x_change = -math.cos(math.radians(self.arrow.angle - 90)) * speed
                self.bubble.y_change = math.sin(math.radians(self.arrow.angle - 90)) * speed

        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over:
            # Move all the sprites
            self.all_sprites_list.update()

        # Bubble ricochets off walls and ceiling
        if pygame.sprite.collide_rect(self.left_wall, self.bubble)\
                or pygame.sprite.collide_rect(self.bubble, self.right_wall):
            self.bubble.x_change *= -1
        if pygame.sprite.collide_rect(self.ceiling, self.bubble):
            self.bubble.y_change *= -1

        # Handle arrow aiming
        if self.k_up_is_pressed:
            if self.arrow.angle > 0: # Pointing left
                self.arrow.change_angle = -1 # Rotate right
            if self.arrow.angle < 0: # Pointing right
                self.arrow.change_angle = 1 # Rotate left
            if self.arrow.angle == 0: # Pointing straight up
                self.arrow.change_angle = 0
        else:
            if self.k_left_is_pressed == self.k_right_is_pressed:
                self.arrow.change_angle = 0
            elif self.k_left_is_pressed:
                self.arrow.change_angle = 1
            elif self.k_right_is_pressed:
                self.arrow.change_angle = -1


    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(WHITE)

        if self.game_over:
            # font = pygame.font.Font("Serif", 25)
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        if not self.game_over:
            self.all_sprites_list.draw(screen)

        pygame.display.flip()


def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")

    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()

    # Create an instance of the Game class
    game = Game()

    # Main game loop
    while not done:
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()

        # Update object positions, check for collisions
        game.run_logic()

        # Draw the current frame
        game.display_frame(screen)

        # Pause for the next frame
        clock.tick(60)

    # Close window and exit
    pygame.quit()


# Call the main function, start up the game
if __name__ == "__main__":
    main()
