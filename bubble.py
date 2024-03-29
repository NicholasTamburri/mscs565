from board import *
from game import Game
from utils import sprite_at


class Bubble(pygame.sprite.Sprite):
    """ This class represents a bubble. """
    RADIUS = 20
    DIAMETER = RADIUS * 2

    COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE]

    def __init__(self, centerx, centery, color):
        super().__init__()
        self.image = pygame.Surface([Bubble.DIAMETER, Bubble.DIAMETER])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        self.color = color

        r = Bubble.RADIUS

        if self.color in Bubble.COLORS:
            pygame.draw.circle(self.image, color, [r, r], r)
            pygame.draw.circle(self.image, BLACK, [r, r], r, 1)
        elif self.color == NODE:
            pygame.draw.circle(self.image, GRAY, [r, r], r)
            pygame.draw.circle(self.image, BLACK, [r, r], r, 1)
            self.shade = 125
            self.shade_increasing = True
            pygame.draw.circle(self.image, (255, self.shade, 0), [r, r], r//2)

        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.radius = self.rect.width / 2

        self.float_centerx = float(self.rect.centerx)
        self.float_centery = float(self.rect.centery)

        self.x_change = 0
        self.y_change = 0

    def update(self):
        # Redraw with new color
        r = Bubble.RADIUS
        if self.color in Bubble.COLORS:
            pygame.draw.circle(self.image, self.color, [r, r], r)
            pygame.draw.circle(self.image, BLACK, [r, r], r, 1)


class PlayerBubble(Bubble):
    """ This class represents the bubble that the player shoots. """

    def __init__(self, centerx, centery, color, board):
        super().__init__(centerx, centery, color)

        self.arrow = board.arrow

    def reset_pos(self):
        """ Called when the bubble falls off the screen. """
        self.x_change = 0
        self.y_change = 0

        self.rect.centerx = self.arrow.centerx
        self.rect.centery = Arrow.HOME_Y

        self.float_centerx = float(self.rect.centerx)
        self.float_centery = float(self.rect.centery)

    def update(self):
        self.float_centerx += self.x_change
        self.float_centery += self.y_change

        self.rect.centerx = int(self.float_centerx)
        self.rect.centery = int(self.float_centery)

        # Ricochet off borders
        if self.rect.left < 0 or self.rect.right >= SCREEN_WIDTH:
            self.x_change *= -1
        if self.rect.top < 0:
            self.y_change *= -1

        # Redraw with new color
        r = Bubble.RADIUS
        if self.color in Bubble.COLORS:
            pygame.draw.circle(self.image, self.color, [r, r], r)
            pygame.draw.circle(self.image, BLACK, [r, r], r, 1)


class BoardBubble(Bubble):
    """ This class represents bubbles on the board. """

    def initialize_bubble_lists(self):
        r = self.board.bubble_radius
        d = self.board.bubble_diameter
        for position in (
            (self.rect.centerx + d, self.rect.centery),
            (self.rect.centerx + r, self.rect.centery - self.board.y_space),
            (self.rect.centerx - r, self.rect.centery - self.board.y_space),
            (self.rect.centerx - d, self.rect.centery),
            (self.rect.centerx - r, self.rect.centery + self.board.y_space),
            (self.rect.centerx + r, self.rect.centery + self.board.y_space)
        ):
            bubble = sprite_at(position, self.board.bubble_list)
            if bubble:
                self.adjacent_bubble_list.add(bubble)
                bubble.adjacent_bubble_list.add(self)

        self.connected_bubble_list.add(self)
        for bubble in self.adjacent_bubble_list:
            self.connected_bubble_list.add(bubble.connected_bubble_list)
            bubble.connected_bubble_list.add(self.connected_bubble_list)
        for bubble in self.connected_bubble_list:
            bubble.connected_bubble_list.add(self.connected_bubble_list)

        self.connected_same_color_bubble_list.add(self)
        for bubble in self.adjacent_bubble_list:
            if bubble.color == self.color:
                self.connected_same_color_bubble_list.add(
                    bubble.connected_same_color_bubble_list)
                bubble.connected_same_color_bubble_list.add(
                    self.connected_same_color_bubble_list)
        for bubble in self.connected_same_color_bubble_list:
            bubble.connected_same_color_bubble_list.add(
                self.connected_same_color_bubble_list)

    def __init__(self, centerx, centery, color, board, fired=False):
        super().__init__(centerx, centery, color)
        self.board = board
        self.fired = fired

        self.adjacent_bubble_list = pygame.sprite.Group()
        self.connected_bubble_list = pygame.sprite.Group()
        self.connected_same_color_bubble_list = pygame.sprite.Group()

        self.initialize_bubble_lists()

        board.bubble_list.add(self)

    def update(self):
        super().update()

        r = self.board.bubble_radius

        if self.color == NODE:
            pygame.draw.circle(self.image, GRAY, [r, r], r)
            pygame.draw.circle(self.image, BLACK, [r, r], r, 1)
            if self.board.shots_fired == self.board.shift_shots - 2:
                if self.shade_increasing:
                    self.shade += 8
                    if self.shade > 255:
                        self.shade -= 8
                        self.shade_increasing = False
                else:
                    self.shade -= 8
                    if self.shade < 0:
                        self.shade += 8
                        self.shade_increasing = True
                pygame.draw.circle(self.image, (255, self.shade, 0),
                                   [r, r], r // 2)
            elif self.board.shots_fired == self.board.shift_shots - 1:
                if self.shade_increasing:
                    self.shade += 22
                    if self.shade > 255:
                        self.shade -= 22
                        self.shade_increasing = False
                else:
                    self.shade -= 22
                    if self.shade < 0:
                        self.shade += 22
                        self.shade_increasing = True
                pygame.draw.circle(self.image, (255, self.shade, 0),
                                   [r, r], r // 2)
            else:
                if self.shade_increasing:
                    self.shade += 2
                    if self.shade > 255:
                        self.shade -= 2
                        self.shade_increasing = False
                else:
                    self.shade -= 2
                    if self.shade < 100:
                        self.shade += 2
                        self.shade_increasing = True
                pygame.draw.circle(self.image, (0, max(145, self.shade), 0),
                                   [r, r], r // 2)


class PoppingBubble(Bubble):
    def __init__(self, bubble):
        super().__init__(bubble.rect.centerx, bubble.rect.centery,
                         bubble.color)

        self.frame = 0

    def update(self):
        self.frame += 1

        if self.color in Bubble.COLORS:
            if self.frame <= 12:
                self.image.fill(WHITE)
                r = Board.BUBBLE_RADIUS
                if self.frame <= 4:
                    thickness = 5
                elif self.frame <= 8:
                    thickness = 3
                else:
                    thickness = 1

                pygame.draw.line(
                    self.image,
                    self.color,
                    [r, r * 2 / 3],
                    [r, r * 1 / 3],
                    thickness
                )
                pygame.draw.line(
                    self.image,
                    self.color,
                    [r, r * 4 / 3],
                    [r, r * 5 / 3],
                    thickness
                )
                pygame.draw.line(
                    self.image,
                    self.color,
                    [r + r * math.sqrt(3) / 6, r + r / 6],
                    [r + r * math.sqrt(3) / 3, r + r / 3],
                    thickness
                )
                pygame.draw.line(
                    self.image,
                    self.color,
                    [r + r * math.sqrt(3) / 6, r - r / 6],
                    [r + r * math.sqrt(3) / 3, r - r / 3],
                    thickness
                )
                pygame.draw.line(
                    self.image,
                    self.color,
                    [r - r * math.sqrt(3) / 6, r - r / 6],
                    [r - r * math.sqrt(3) / 3, r - r / 3],
                    thickness
                )
                pygame.draw.line(
                    self.image,
                    self.color,
                    [r - r * math.sqrt(3) / 6, r + r / 6],
                    [r - r * math.sqrt(3) / 3, r + r / 3],
                    thickness
                )

            else:
                self.kill()

        elif self.color == NODE:
            if self.frame <= 20:
                r = Board.BUBBLE_RADIUS
                pygame.draw.circle(self.image, WHITE, [r, r], self.frame)

            else:
                self.kill()


class FallingBubble(Bubble):
    def __init__(self, bubble):
        super().__init__(bubble.rect.centerx, bubble.rect.centery,
                         bubble.color)

        self.y_change = 1

    def update(self):
        # Move bubble downward
        self.rect.centery += self.y_change

        # Increase falling speed
        self.y_change += 1

        # Kill bubble when it leaves the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
