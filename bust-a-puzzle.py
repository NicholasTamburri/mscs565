"""
Nicholas Tamburri
Bust-a-Puzzle Version 0.0.1

A board of bubbles is generated. The player controls the arrow
at the bottom of the board, which aims and fires bubbles.
Fired bubbles stick to the bubbles on the board.
Game ends when a board bubble is below the kill line at the bottom.
Neither removing board bubbles nor shifting them down have been implemented yet.

Play by aiming the arrow using (fittingly) the arrow keys
and using the space bar to fire the bubble.
"""

import math
import pygame
import random

# --- Global constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 127, 0)

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


class Board(object):
    """ This class represents the game board. """

    def __init__(self):
        self.bubble_list = pygame.sprite.Group()


class Bubble(pygame.sprite.Sprite):
    """ This class represents a bubble. """
    RADIUS = 20
    DIAMETER = RADIUS * 2

    COLORS = (RED, ORANGE, YELLOW, GREEN, BLUE)

    def __init__(self, centerx, centery, color):
        """ Constructor, create the image of the block. """
        super().__init__()
        self.image = pygame.Surface([Bubble.DIAMETER, Bubble.DIAMETER])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        self.color = color

        pygame.draw.circle(self.image, color, [Bubble.RADIUS, Bubble.RADIUS], Bubble.RADIUS)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.radius = self.rect.width / 2

        self.float_centerx = float(self.rect.centerx)
        self.float_centery = float(self.rect.centery)

        self.x_change = 0
        self.y_change = 0


class PlayerBubble(Bubble):
    """ This class represents the bubble that the player shoots. """
    # def __init__(self, centerx, centery):
    #     super().__init__(centerx, centery)

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


class BoardBubble(Bubble):
    """ This class represents bubbles on the board. """

    def __init__(self, centerx, centery, color, board, fired=False):
        super().__init__(centerx, centery, color)
        self.fired = fired

        self.adjacent_bubble_list = pygame.sprite.spritecollide(
            self, board.bubble_list, False
        )
        board.bubble_list.add(self)
        self.connected_bubble_list = pygame.sprite.Group()
        self.connected_same_color_bubble_list = pygame.sprite.Group()

        for bubble in self.adjacent_bubble_list:
            self.connected_bubble_list.add(bubble.connected_bubble_list.sprites())

        for bubble in self.connected_bubble_list:
            if self.color == bubble.color:
                self.connected_same_color_bubble_list.add(bubble)


class Ceiling(pygame.sprite.Sprite):
    """ Top border of the play field. """
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([8 * Bubble.DIAMETER, 1])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH / 2 - 4 * Bubble.DIAMETER
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


class KillLine(pygame.sprite.Sprite):
    """ Game over when board bubbles cross this line. """
    def __init__(self, y):
        super().__init__()

        self.image = pygame.Surface([8 * Bubble.DIAMETER, 1])
        self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH / 2 - 4 * Bubble.DIAMETER
        self.rect.y = y


class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
    # Some math to find vertical spacing of the bubbles
    Y_SPACE = math.sqrt(4 / 5 * (
            math.sqrt(Bubble.RADIUS ** 2 + Bubble.DIAMETER ** 2)\
            - Bubble.DIAMETER\
        ) ** 2)\
        + math.sqrt(Bubble.RADIUS ** 2 + Bubble.DIAMETER ** 2)\
            - Bubble.DIAMETER
    # For reference, here is the math:
    # distance = math.sqrt(Bubble.RADIUS ** 2 + Bubble.DIAMETER ** 2)
    # space = distance - Bubble.DIAMETER
    # y_space = math.sqrt(4 / 5 * space ** 2)

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """

        self.score = 0
        self.game_over = False

        self.k_left_is_pressed = False
        self.k_up_is_pressed = False
        self.k_right_is_pressed = False

        # Create game board
        self.board = Board()

        # Create sprite lists
        # self.board_bubble_list = pygame.sprite.Group()
        self.bubble_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        # Create play field borders
        self.ceiling = Ceiling()
        self.left_wall = Wall(SCREEN_WIDTH / 2 - 4 * Bubble.DIAMETER)
        self.right_wall = Wall(SCREEN_WIDTH / 2 + 4 * Bubble.DIAMETER)
        self.all_sprites_list.add(self.ceiling)
        self.all_sprites_list.add(self.left_wall)
        self.all_sprites_list.add(self.right_wall)

        # Create the arrow
        self.arrow = Arrow()
        self.all_sprites_list.add(self.arrow)

        # Create some board bubbles
        y_pos = 0
        for column in range(8):
            x_pos = self.left_wall.rect.right + Bubble.RADIUS \
                    + column * Bubble.DIAMETER
            for row in range(11):
                y_pos = self.ceiling.rect.bottom + Bubble.RADIUS \
                        + row * (Bubble.DIAMETER - Game.Y_SPACE)
                if row % 2 == 1:
                    x_pos += Bubble.RADIUS
                elif row > 0:
                    x_pos -= Bubble.RADIUS
                if column != 7 or row % 2 == 0:
                    # These lines represent the board pattern
                    if row == 0:
                        # Add the bubble
                        bubble = BoardBubble(x_pos, y_pos, RED, self.board)
                        self.board.bubble_list.add(bubble)
                        self.bubble_list.add(bubble)
                        self.all_sprites_list.add(bubble)
                    if row == 1:
                        if column != 3:
                            # Add the bubble
                            bubble = BoardBubble(x_pos, y_pos, ORANGE, self.board)
                            self.board.bubble_list.add(bubble)
                            self.bubble_list.add(bubble)
                            self.all_sprites_list.add(bubble)
                    if row == 2:
                        if column == 1\
                                or column == 2\
                                or column == 5\
                                or column == 6:
                            # Add the bubble
                            bubble = BoardBubble(x_pos, y_pos, YELLOW, self.board)
                            self.board.bubble_list.add(bubble)
                            self.bubble_list.add(bubble)
                            self.all_sprites_list.add(bubble)
                    if row == 3:
                        if column == 1\
                                or column == 5:
                            # Add the bubble
                            bubble = BoardBubble(x_pos, y_pos, GREEN, self.board)
                            self.board.bubble_list.add(bubble)
                            self.bubble_list.add(bubble)
                            self.all_sprites_list.add(bubble)

        # Create the kill line
        self.kill_line = KillLine(y_pos + Bubble.RADIUS)
        self.all_sprites_list.add(self.kill_line)

        # Create the player's bubble
        self.bubble = PlayerBubble(self.arrow.rect.centerx,
                                   self.arrow.rect.centery,
                                   BLUE)
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
                speed = 8
                angle = math.radians(self.arrow.angle - 90)
                self.bubble.x_change = -math.cos(angle) * speed
                self.bubble.y_change = math.sin(angle) * speed

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
            elif self.arrow.angle < 0: # Pointing right
                self.arrow.change_angle = 1 # Rotate left
            else: # Pointing straight up
                self.arrow.change_angle = 0 # Do not rotate
        elif self.k_left_is_pressed == self.k_right_is_pressed:
            self.arrow.change_angle = 0
        elif self.k_left_is_pressed:
            self.arrow.change_angle = 1
        elif self.k_right_is_pressed:
            self.arrow.change_angle = -1

        # Handle collision with board bubble
        bubble_hit = pygame.sprite.spritecollideany(
            self.bubble, self.board.bubble_list, pygame.sprite.collide_circle
        )
        if bubble_hit:# and bubble_hit.color != self.bubble.color:
            x_diff = self.bubble.rect.centerx - bubble_hit.rect.centerx
            y_diff = self.bubble.rect.centery - bubble_hit.rect.centery

            new_y = 0
            if abs(y_diff) < Bubble.RADIUS:
                new_y = bubble_hit.rect.centery
            elif y_diff < 0:
                new_y = bubble_hit.rect.centery - Bubble.DIAMETER + Game.Y_SPACE
            else:
                new_y = bubble_hit.rect.centery + Bubble.DIAMETER - Game.Y_SPACE

            new_x = 0
            if new_y == bubble_hit.rect.centery:
                if x_diff > 0:
                    new_x = bubble_hit.rect.centerx + Bubble.DIAMETER
                else:
                    new_x = bubble_hit.rect.centerx - Bubble.DIAMETER
            else:
                if x_diff > 0:
                    new_x = bubble_hit.rect.centerx + Bubble.RADIUS
                else:
                    new_x = bubble_hit.rect.centerx - Bubble.RADIUS

            # Add a new bubble, based on the shot bubble, to the board
            new_bubble = BoardBubble(new_x, new_y, self.bubble.color, self.board)
            self.board.bubble_list.add(new_bubble)
            self.bubble_list.add(new_bubble)
            self.all_sprites_list.add(new_bubble)

            # Ready another bubble to be fired
            self.bubble.reset_pos()

            # End game if the new bubble is below the kill line
            if new_bubble.rect.centery > self.kill_line.rect.y:
                self.game_over = True
        # if bubble_hit and bubble_hit.color == self.bubble.color:
        #     bubble_hit.kill()
        #     self.bubble.reset_pos()


    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(WHITE)

        # if not self.game_over:
        self.all_sprites_list.draw(screen)

        if self.game_over:
            # font = pygame.font.Font("Serif", 25)
            font = pygame.font.SysFont("serif", 25)
            text = font.render("Game Over, click to restart", True, BLACK)
            center_x = (SCREEN_WIDTH // 2) - (text.get_width() // 2)
            center_y = (SCREEN_HEIGHT // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        pygame.display.flip()


def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Bust-a-Puzzle v0.0.1")

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
