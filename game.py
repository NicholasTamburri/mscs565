"""
Nicholas Tamburri
Version 0.0.1

Game code for Bust-a-Move clone.

Play by shooting bubbles at other bubbles.
"""

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

    LENGTH = 50
    WIDTH = 8

    BASE_IMAGE = pygame.Surface([WIDTH + 1, LENGTH])

    def __init__(self):
        super().__init__()
        self.image = Arrow.BASE_IMAGE
        self.image.fill(WHITE)
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
        self.rect.x = 300
        self.rect.y = 300

        self.angle = 0

    def update(self):
        self.image = pygame.transform.rotate(Arrow.BASE_IMAGE, self.angle)
        self.angle = (self.angle + 1) % 360


class Bubble(pygame.sprite.Sprite):
    """ This class represents a simple block the player collects. """

    def __init__(self):
        """ Constructor, create the image of the block. """
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, BLACK, [10, 10], 10)
        self.rect = self.image.get_rect()
        self.radius = 10

    def reset_pos(self):
        """ Called when the block is 'collected' or falls off
            the screen. """
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(SCREEN_WIDTH)

    def update(self):
        """ Automatically called when we need to move the block. """
        self.rect.y += 1

        if self.rect.y > SCREEN_HEIGHT + self.rect.height:
            self.reset_pos()


class Player(pygame.sprite.Sprite):
    """ This class represents the player. """

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 20])
        self.image.fill(WHITE)
        pygame.draw.circle(self.image, RED, [10, 10], 10)
        self.rect = self.image.get_rect()
        self.radius = 10

    def update(self):
        """ Update the player location. """
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """

        self.score = 0
        self.game_over = False

        # Create sprite lists
        self.block_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        # Create the block sprites
        for i in range(50):
            block = Bubble()

            block.rect.x = random.randrange(SCREEN_WIDTH)
            block.rect.y = random.randrange(-300, SCREEN_HEIGHT)

            self.block_list.add(block)
            self.all_sprites_list.add(block)

        # Create the player
        self.player = Player()
        self.all_sprites_list.add(self.player)

        # Create the arrow
        self.arrow = Arrow()
        self.all_sprites_list.add(self.arrow)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_over:
                    self.__init__()

        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over:
            # Move all the sprites
            self.all_sprites_list.update()

            # See if the player block has collided with anything.
            blocks_hit_list = pygame.sprite.spritecollide(
                self.player,
                self.block_list,
                True,
                pygame.sprite.collide_circle
            )

            # Check the list of collisions.
            for block in blocks_hit_list:
                self.score += 1
                print(self.score)
                # You can do something with "block" here.

            if len(self.block_list) == 0:
                self.game_over = True

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
    pygame.mouse.set_visible(False)

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