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

from bubble import *
from score import Score


# --- Classes ---


class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    def __init__(self):
        """ Constructor. Create all our attributes and initialize
        the game. """

        self.score = 0
        self.game_started = False
        self.game_over = False

        self.k_left_is_pressed = False
        self.k_up_is_pressed = False
        self.k_right_is_pressed = False

        # Create game board, which also creates arrow
        self.board = Board()

        # Create sprite lists
        # self.board_bubble_list = pygame.sprite.Group()
        self.bubble_list = pygame.sprite.Group()
        self.all_sprites_list = pygame.sprite.Group()

        # Create play field borders
        # self.ceiling = Ceiling(self.board)
        # self.left_wall = Wall(SCREEN_WIDTH / 2 - 4 * Bubble.DIAMETER)
        # self.right_wall = Wall(SCREEN_WIDTH / 2 + 4 * Bubble.DIAMETER)
        self.all_sprites_list.add(self.board.ceiling)
        self.all_sprites_list.add(self.board.left_wall)
        self.all_sprites_list.add(self.board.right_wall)

        # Create the arrow
        # self.arrow = Arrow(self.board)
        self.all_sprites_list.add(self.board.arrow)

        # Create some board bubbles
        for column in range(8):
            x_pos = self.board.left_wall.rect.right + self.board.bubble_radius \
                    + column * self.board.bubble_diameter
            for row in range(-1, 11):
                y_pos = self.board.ceiling.rect.bottom + self.board.bubble_radius \
                        + (row) * (self.board.bubble_diameter - self.board.y_space)
                if row % 2 == 1:
                    x_pos += self.board.bubble_radius
                elif row > -1:
                    x_pos -= self.board.bubble_radius
                if column != 7 or row % 2 == 0:
                    # These lines represent the board pattern
                    if row == -1:
                        # Add node bubble
                        node = BoardBubble(x_pos, y_pos, GRAY, self.board)
                        self.board.bubble_list.add(node)
                        self.bubble_list.add(node)
                        self.all_sprites_list.add(node)
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
        # self.kill_line = KillLine(y_pos + Bubble.RADIUS, self.board)
        self.all_sprites_list.add(self.board.kill_line)

        # Create the player's bubble
        self.bubble = PlayerBubble(self.board.arrow.rect.centerx,
                                   self.board.arrow.rect.centery,
                                   YELLOW,
                                   self.board)
        self.bubble_list.add(self.bubble)
        self.all_sprites_list.add(self.bubble)

        # Create the score display
        self.score = Score()
        self.all_sprites_list.add(self.score)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.game_started = True
                if self.game_over:
                    self.__init__()
                # Debug stuff
                bubble = sprite_at(pygame.mouse.get_pos(), self.board.bubble_list)
                if bubble:
                    print("Adjacent:   ", bubble.adjacent_bubble_list)
                    print("Connected:  ", bubble.connected_bubble_list)
                    print("Color chain:", bubble.connected_same_color_bubble_list)
                    print()
                    if pygame.mouse.get_pressed()[1]:
                        for bub in bubble.connected_same_color_bubble_list:
                            bub.kill()
                    if pygame.mouse.get_pressed()[2]:
                        for bub in bubble.connected_bubble_list:
                            bub.kill()

            if self.game_started:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.k_left_is_pressed = True
                    if event.key == pygame.K_UP:
                        self.k_up_is_pressed = True
                    if event.key == pygame.K_RIGHT:
                        self.k_right_is_pressed = True

                    # Change color using Page Up and Page Down
                    if event.key == pygame.K_PAGEDOWN:
                        color_index = Bubble.COLORS.index(self.bubble.color)
                        color_index = (color_index + 1) % len(Bubble.COLORS)
                        self.bubble.color = Bubble.COLORS[color_index]
                    if event.key == pygame.K_PAGEUP:
                        color_index = Bubble.COLORS.index(self.bubble.color)
                        color_index = (color_index - 1) % len(Bubble.COLORS)
                        self.bubble.color = Bubble.COLORS[color_index]

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
                    angle = math.radians(self.board.arrow.angle - 90)
                    self.bubble.x_change = -math.cos(angle) * speed
                    self.bubble.y_change = math.sin(angle) * speed

        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over and self.game_started:
            # Move all the sprites
            self.all_sprites_list.update()

        # Bubble ricochets off walls and ceiling
        if pygame.sprite.collide_rect(self.board.left_wall, self.bubble)\
                or pygame.sprite.collide_rect(self.bubble, self.board.right_wall):
            self.bubble.x_change *= -1
        if pygame.sprite.collide_rect(self.board.ceiling, self.bubble):
            self.bubble.y_change *= -1

        # Handle arrow aiming
        if self.k_up_is_pressed:
            if self.board.arrow.angle > 0:          # Pointing left
                self.board.arrow.change_angle = -1  # Rotate right
            elif self.board.arrow.angle < 0:        # Pointing right
                self.board.arrow.change_angle = 1   # Rotate left
            else:                                   # Pointing straight up
                self.board.arrow.change_angle = 0   # Do not rotate
        elif self.k_left_is_pressed == self.k_right_is_pressed:
            self.board.arrow.change_angle = 0
        elif self.k_left_is_pressed:
            self.board.arrow.change_angle = 1
        elif self.k_right_is_pressed:
            self.board.arrow.change_angle = -1

        # Handle collision with board bubble
        bubble_hit = pygame.sprite.spritecollideany(
            self.bubble, self.board.bubble_list, pygame.sprite.collide_circle
        )
        if bubble_hit:
            x_diff = self.bubble.rect.centerx - bubble_hit.rect.centerx
            y_diff = self.bubble.rect.centery - bubble_hit.rect.centery

            if abs(y_diff) < self.board.bubble_radius:  # Same row
                new_y = bubble_hit.rect.centery
            elif y_diff < 0:                            # Above row
                new_y = bubble_hit.rect.centery - self.board.bubble_diameter + self.board.y_space
            else:                                       # Below row
                new_y = bubble_hit.rect.centery + self.board.bubble_diameter - self.board.y_space

            if new_y == bubble_hit.rect.centery:  # If same row
                if x_diff > 0:                    # Right column
                    new_x = bubble_hit.rect.centerx + self.board.bubble_diameter
                else:                             # Left column
                    new_x = bubble_hit.rect.centerx - self.board.bubble_diameter
            else:
                if x_diff > 0:                    # Right column
                    new_x = bubble_hit.rect.centerx + self.board.bubble_radius
                else:                             # Left column
                    new_x = bubble_hit.rect.centerx - self.board.bubble_radius

            # Add a new bubble, based on the shot bubble, to the board
            new_bubble = BoardBubble(new_x, new_y, self.bubble.color, self.board, True)
            # Keep bubbles in bounds
            if new_bubble.rect.left <= self.board.x - 1:
                new_bubble.rect.centerx += self.board.bubble_diameter
            elif new_bubble.rect.right >= self.board.right_wall.rect.x + 1:
                new_bubble.rect.centerx -= self.board.bubble_diameter
            self.board.bubble_list.add(new_bubble)
            self.bubble_list.add(new_bubble)
            self.all_sprites_list.add(new_bubble)

            # Fired bubble hits a cluster of bubbles that share its color
            if len(new_bubble.connected_same_color_bubble_list) > 2:
                # Pop bubbles: Kill the same-colored bubbles
                count = 0
                for bubble in new_bubble.connected_same_color_bubble_list:
                    bubble.kill()
                    count += 1
                self.score.bubbles_popped(count)

                # Recalculate all board bubbles' lists
                for bubble in self.board.bubble_list:
                    bubble.adjacent_bubble_list.empty()
                    bubble.connected_bubble_list.empty()
                    bubble.connected_same_color_bubble_list.empty()
                for bubble in self.board.bubble_list:
                    bubble.initialize_bubble_lists()

                # Drop bubbles: Kill bubbles not connected to node (gray bubble)
                count = 0
                for bubble in self.board.bubble_list:
                    colors = []
                    for connected_bubble in bubble.connected_bubble_list:
                        colors.append(connected_bubble.color)
                    if GRAY not in colors:
                        falling_bubble = FallingBubble(bubble)
                        self.bubble_list.add(falling_bubble)
                        self.all_sprites_list.add(falling_bubble)
                        bubble.kill()
                        count += 1
                if count > 0:
                    self.score.bubbles_dropped(count)

            # Kill the fired bubble and those connected to it.
            # for bubble in new_bubble.connected_bubble_list:
            #     bubble.kill()
            # new_bubble.kill()

            # Kill the fired bubble and those adjacent to it.
            # for bubble in new_bubble.adjacent_bubble_list:
            #     bubble.kill()
            # new_bubble.kill()

            # Ready another bubble to be fired
            self.bubble.reset_pos()

            # End game if the new bubble is below the kill line
            if new_bubble.rect.centery > self.board.kill_line.rect.y:
                self.game_over = True
        # if bubble_hit and bubble_hit.color == self.bubble.color:
        #     bubble_hit.kill()
        #     self.bubble.reset_pos()

    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(WHITE)

        if self.game_started:
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
