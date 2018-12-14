from constants import *


# Bubbles are in the format (row, column, color)

STAGES = (
    # Stage 0 is nonexistent
    (),

    # Stage 1
    (
        (-1, 0, NODE), (-1, 1, NODE), (-1, 2, NODE), (-1, 3, NODE),
        (-1, 4, NODE), (-1, 5, NODE), (-1, 6, NODE),

        (0, 0, RED), (0, 1, RED), (0, 2, RED), (0, 3, RED),
        (0, 4, RED), (0, 5, RED), (0, 6, RED), (0, 7, RED),

        (1, 0, ORANGE), (1, 1, ORANGE), (1, 2, ORANGE), (1, 3, BLUE),
        (1, 4, ORANGE), (1, 5, ORANGE), (1, 6, ORANGE),

        (2, 1, YELLOW), (2, 2, YELLOW), (2, 3, BLUE),
        (2, 4, BLUE), (2, 5, YELLOW), (2, 6, YELLOW),

        (3, 1, GREEN), (3, 5, GREEN),
    ),

    # Stage 2
    (
        (0, 1, NODE), (0, 2, NODE),

        (1, 0, NODE), (1, 1, BLUE), (1, 2, NODE),

        (2, 1, NODE), (2, 2, BLUE), (2, 5, NODE), (2, 6, NODE),

        (3, 4, BLUE), (3, 5, BLUE), (3, 6, NODE),

        (4, 5, NODE), (4, 6, NODE),

        (5, 1, NODE), (5, 2, BLUE),

        (6, 1, NODE), (6, 2, BLUE), (6, 3, NODE),

        (7, 1, NODE), (7, 2, NODE),
    ),

    # Stage 3
    (
        (-1, 0, NODE), (-1, 1, NODE), (-1, 2, NODE), (-1, 3, NODE),
        (-1, 4, NODE), (-1, 5, NODE), (-1, 6, NODE),

        (0, 0, ORANGE), (0, 1, YELLOW), (0, 2, RED), (0, 3, ORANGE),
        (0, 4, YELLOW), (0, 5, RED), (0, 6, ORANGE), (0, 7, YELLOW),

        (1, 0, RED), (1, 1, ORANGE), (1, 2, YELLOW), (1, 3, RED),
        (1, 4, ORANGE), (1, 5, YELLOW), (1, 6, RED),

        (2, 0, ORANGE), (2, 1, YELLOW), (2, 2, RED), (2, 3, ORANGE),
        (2, 4, YELLOW), (2, 5, RED), (2, 6, ORANGE), (2, 7, YELLOW),

        (3, 0, RED), (3, 1, ORANGE), (3, 2, YELLOW), (3, 3, RED),
        (3, 4, ORANGE), (3, 5, YELLOW), (3, 6, RED),

        (4, 0, ORANGE), (4, 1, YELLOW), (4, 2, RED), (4, 3, ORANGE),
        (4, 4, YELLOW), (4, 5, RED), (4, 6, ORANGE), (4, 7, YELLOW),
    ),
)
