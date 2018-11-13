from constants import *


# Bubbles are in the format (row, column, color)

STAGES = [
    # Stage 1
    [
        (-1, 0, GRAY), (-1, 1, GRAY), (-1, 2, GRAY), (-1, 3, GRAY),
        (-1, 4, GRAY), (-1, 5, GRAY), (-1, 6, GRAY),

        (0, 0, RED), (0, 1, RED), (0, 2, RED), (0, 3, RED),
        (0, 4, RED), (0, 5, RED), (0, 6, RED), (0, 7, RED),

        (1, 0, ORANGE), (1, 1, ORANGE), (1, 2, ORANGE),
        (1, 4, ORANGE), (1, 5, ORANGE), (1, 6, ORANGE),

        (2, 1, YELLOW), (2, 2, YELLOW), (2, 5, YELLOW), (2, 6, YELLOW),

        (3, 1, GREEN), (3, 5, GREEN)
    ]
]


# Coordinates are in the form (row, column)
STAGE_COORDINATES = (
    (
        (-1, 0), (-1, 1), (-1, 2), (-1, 3),
        (-1, 4, GRAY), (-1, 5, GRAY), (-1, 6, GRAY),

        (0, 0, RED), (0, 1, RED), (0, 2, RED), (0, 3, RED),
        (0, 4, RED), (0, 5, RED), (0, 6, RED), (0, 7, RED),

        (1, 0, ORANGE), (1, 1, ORANGE), (1, 2, ORANGE),
        (1, 4, ORANGE), (1, 5, ORANGE), (1, 6, ORANGE),

        (2, 1, YELLOW), (2, 2, YELLOW), (2, 5, YELLOW), (2, 6, YELLOW),

        (3, 1, GREEN), (3, 5, GREEN)
    )
)