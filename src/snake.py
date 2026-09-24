import random


class SnakeGame:

    def __init__(self, width=700, height=700, cell_size=35):

        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.cols = width // cell_size
        self.rows = height // cell_size

        self.reset()

    def reset(self):

        center_x = self.cols // 2
        center_y = self.rows // 2

        self.snake = [
            (center_x, center_y),
            (center_x - 1, center_y),
            (center_x - 2, center_y),
            (center_x - 3, center_y),
            (center_x - 4, center_y)
        ]

        # Start moving right
        self.direction = (1, 0)

        self.next_direction = (1, 0)

        self.score = 0

        self.game_over = False

        # Create first apple
        self.food = self.create_food()

    # --------------------------------------------------------
    # CREATE APPLE
    # --------------------------------------------------------

    def create_food(self):

        available = []

        for x in range(self.cols):

            for y in range(self.rows):

                if (x, y) not in self.snake:

                    available.append((x, y))

        if available:

            return random.choice(available)

        return None

    # --------------------------------------------------------
    # CHANGE DIRECTION
    # --------------------------------------------------------

    def change_direction(self, direction):

        opposite = (
            -self.direction[0],
            -self.direction[1]
        )

        # Don't allow direct reverse
        if direction != opposite:

            self.next_direction = direction

    # --------------------------------------------------------
    # UPDATE SNAKE
    # --------------------------------------------------------

    def update(self):

        if self.game_over:

            return False

        self.direction = self.next_direction

        head_x, head_y = self.snake[0]

        dx, dy = self.direction

        new_head = (
            head_x + dx,
            head_y + dy
        )

        # ----------------------------------------------------
        # WALL COLLISION
        # ----------------------------------------------------

        if (
            new_head[0] < 0
            or new_head[0] >= self.cols
            or new_head[1] < 0
            or new_head[1] >= self.rows
        ):

            self.game_over = True

            return False

        # ----------------------------------------------------
        # SELF COLLISION
        # ----------------------------------------------------

        if new_head in self.snake:

            self.game_over = True

            return False

        # ----------------------------------------------------
        # ADD NEW HEAD
        # ----------------------------------------------------

        self.snake.insert(0, new_head)

        # ----------------------------------------------------
        # APPLE EATEN
        # ----------------------------------------------------

        if new_head == self.food:

            self.score += 10

            # Create a completely new apple
            self.food = self.create_food()

            # IMPORTANT:
            # Do NOT remove the tail.
            # Therefore snake grows.
            return True

        # ----------------------------------------------------
        # NORMAL MOVEMENT
        # ----------------------------------------------------

        self.snake.pop()

        return False
    