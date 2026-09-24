import os
import time

import pygame
import cv2

from snake import SnakeGame
from hand_tracker import HandTracker


# ============================================================
# PYGAME + SOUND
# ============================================================

pygame.mixer.pre_init(
    44100,
    -16,
    2,
    512
)

pygame.init()

pygame.mixer.init()


# ============================================================
# WINDOW SIZE
# ============================================================

GAME_WIDTH = 700
GAME_HEIGHT = 700

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 760


screen = pygame.display.set_mode(
    (
        WINDOW_WIDTH,
        WINDOW_HEIGHT
    )
)

pygame.display.set_caption(
    "AI Hand Controlled Snake"
)


# ============================================================
# COLORS
# ============================================================

BLACK = (15, 15, 15)

WHITE = (255, 255, 255)

GREEN = (40, 200, 80)

DARK_GREEN = (20, 120, 50)

RED = (220, 40, 40)

YELLOW = (255, 220, 50)

BLUE = (40, 150, 255)

GRAY = (100, 100, 100)


# ============================================================
# FONTS
# ============================================================

title_font = pygame.font.SysFont(
    "arial",
    28,
    bold=True
)

info_font = pygame.font.SysFont(
    "arial",
    22
)

game_over_font = pygame.font.SysFont(
    "arial",
    55,
    bold=True
)


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ============================================================
# SOUND PATH
# ============================================================

eat_path = os.path.join(
    BASE_DIR,
    "sounds",
    "eat.wav"
)

game_over_path = os.path.join(
    BASE_DIR,
    "sounds",
    "game_over.wav"
)


# ============================================================
# LOAD SOUND
# ============================================================

eat_sound = None

game_over_sound = None


if os.path.exists(eat_path):

    eat_sound = pygame.mixer.Sound(
        eat_path
    )

    eat_sound.set_volume(1.0)


if os.path.exists(game_over_path):

    game_over_sound = pygame.mixer.Sound(
        game_over_path
    )

    game_over_sound.set_volume(1.0)


# ============================================================
# CREATE GAME
# ============================================================

game = SnakeGame(
    width=GAME_WIDTH,
    height=GAME_HEIGHT,
    cell_size=35
)


# ============================================================
# HAND TRACKER
# ============================================================

tracker = HandTracker()


# ============================================================
# SNAKE SPEED
# ============================================================

MOVE_DELAY = 0.16

last_move_time = time.time()


# ============================================================
# GAME OVER SOUND
# ============================================================

previous_game_over = False


# ============================================================
# MAIN LOOP
# ============================================================

running = True


while running:

    # ========================================================
    # EVENTS
    # ========================================================

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == pygame.KEYDOWN:

            # Quit
            if event.key == pygame.K_q:

                running = False

            # Restart
            if event.key == pygame.K_r:

                game.reset()

                previous_game_over = False

                last_move_time = time.time()


    # ========================================================
    # GET HAND + CAMERA
    # ========================================================

    direction, camera_frame = (
        tracker.get_direction()
    )


    # ========================================================
    # CHANGE SNAKE DIRECTION
    # ========================================================

    if direction == "UP":

        game.change_direction(
            (0, -1)
        )

    elif direction == "DOWN":

        game.change_direction(
            (0, 1)
        )

    elif direction == "LEFT":

        game.change_direction(
            (-1, 0)
        )

    elif direction == "RIGHT":

        game.change_direction(
            (1, 0)
        )


    # ========================================================
    # CONTINUOUS MOVEMENT
    # ========================================================

    current_time = time.time()

    if (
        current_time - last_move_time
        >= MOVE_DELAY
    ):

        ate_food = game.update()

        last_move_time = current_time

        # ----------------------------------------------------
        # APPLE SOUND
        # ----------------------------------------------------

        if ate_food:

            print(
                "APPLE EATEN - NEW APPLE CREATED"
            )

            if eat_sound:

                eat_sound.play()


    # ========================================================
    # GAME OVER SOUND
    # ========================================================

    if (
        game.game_over
        and not previous_game_over
    ):

        print("GAME OVER")

        if game_over_sound:

            game_over_sound.play()


    previous_game_over = game.game_over


    # ========================================================
    # BACKGROUND
    # ========================================================

    screen.fill(
        BLACK
    )


    # ========================================================
    # TITLE
    # ========================================================

    title = title_font.render(
        "AI HAND CONTROLLED SNAKE",
        True,
        WHITE
    )

    screen.blit(
        title,
        (
            25,
            15
        )
    )


    # ========================================================
    # GAME POSITION
    # ========================================================

    game_x = 20
    game_y = 55


    # ========================================================
    # GAME BORDER
    # ========================================================

    pygame.draw.rect(
        screen,
        (50, 50, 50),
        (
            game_x - 3,
            game_y - 3,
            GAME_WIDTH + 6,
            GAME_HEIGHT + 6
        )
    )


    # ========================================================
    # GAME BACKGROUND
    # ========================================================

    pygame.draw.rect(
        screen,
        (25, 25, 25),
        (
            game_x,
            game_y,
            GAME_WIDTH,
            GAME_HEIGHT
        )
    )


    # ========================================================
    # GRID
    # ========================================================

    for x in range(
        0,
        GAME_WIDTH,
        game.cell_size
    ):

        pygame.draw.line(
            screen,
            (35, 35, 35),
            (
                game_x + x,
                game_y
            ),
            (
                game_x + x,
                game_y + GAME_HEIGHT
            )
        )


    for y in range(
        0,
        GAME_HEIGHT,
        game.cell_size
    ):

        pygame.draw.line(
            screen,
            (35, 35, 35),
            (
                game_x,
                game_y + y
            ),
            (
                game_x + GAME_WIDTH,
                game_y + y
            )
        )


    # ========================================================
    # DRAW SNAKE
    # ========================================================

    for index, segment in enumerate(
        game.snake
    ):

        x, y = segment

        px = (
            game_x
            + x * game.cell_size
        )

        py = (
            game_y
            + y * game.cell_size
        )

        rect = pygame.Rect(
            px + 3,
            py + 3,
            game.cell_size - 6,
            game.cell_size - 6
        )


        # ----------------------------------------------------
        # HEAD
        # ----------------------------------------------------

        if index == 0:

            pygame.draw.rect(
                screen,
                GREEN,
                rect,
                border_radius=10
            )

            # Eyes

            pygame.draw.circle(
                screen,
                WHITE,
                (
                    px + 10,
                    py + 10
                ),
                5
            )

            pygame.draw.circle(
                screen,
                WHITE,
                (
                    px + 25,
                    py + 10
                ),
                5
            )

            # Pupils

            pygame.draw.circle(
                screen,
                BLACK,
                (
                    px + 10,
                    py + 10
                ),
                2
            )

            pygame.draw.circle(
                screen,
                BLACK,
                (
                    px + 25,
                    py + 10
                ),
                2
            )


        # ----------------------------------------------------
        # BODY
        # ----------------------------------------------------

        else:

            pygame.draw.rect(
                screen,
                DARK_GREEN,
                rect,
                border_radius=8
            )


    # ========================================================
    # DRAW APPLE
    # ========================================================

    if game.food is not None:

        fx, fy = game.food

        apple_x = (
            game_x
            + fx * game.cell_size
            + game.cell_size // 2
        )

        apple_y = (
            game_y
            + fy * game.cell_size
            + game.cell_size // 2
        )


        # Apple body

        pygame.draw.circle(
            screen,
            RED,
            (
                apple_x,
                apple_y
            ),
            14
        )


        # Apple highlight

        pygame.draw.circle(
            screen,
            (255, 120, 120),
            (
                apple_x - 5,
                apple_y - 5
            ),
            4
        )


        # Stem

        pygame.draw.line(
            screen,
            (100, 60, 20),
            (
                apple_x,
                apple_y - 10
            ),
            (
                apple_x + 3,
                apple_y - 18
            ),
            3
        )


        # Leaf

        pygame.draw.ellipse(
            screen,
            GREEN,
            (
                apple_x + 2,
                apple_y - 20,
                12,
                6
            )
        )


    # ========================================================
    # CAMERA PANEL
    # ========================================================

    camera_x = 740

    camera_y = 80


    # Camera title

    camera_title = title_font.render(
        "HAND CONTROL CAMERA",
        True,
        WHITE
    )

    screen.blit(
        camera_title,
        (
            camera_x,
            35
        )
    )


    # Camera border

    pygame.draw.rect(
        screen,
        (60, 60, 60),
        (
            camera_x - 5,
            camera_y - 5,
            CAMERA_WIDTH + 10,
            CAMERA_HEIGHT + 10
        )
    )


    # ========================================================
    # CAMERA IMAGE
    # ========================================================

    if camera_frame is not None:

        camera_frame = cv2.resize(
            camera_frame,
            (
                CAMERA_WIDTH,
                CAMERA_HEIGHT
            )
        )

        camera_rgb = cv2.cvtColor(
            camera_frame,
            cv2.COLOR_BGR2RGB
        )

        camera_surface = (
            pygame.surfarray.make_surface(
                camera_rgb.swapaxes(0, 1)
            )
        )

        screen.blit(
            camera_surface,
            (
                camera_x,
                camera_y
            )
        )


    # ========================================================
    # CAMERA INFORMATION
    # ========================================================

    instruction = info_font.render(
        "Move your palm around the virtual joystick",
        True,
        WHITE
    )

    screen.blit(
        instruction,
        (
            camera_x,
            camera_y + CAMERA_HEIGHT + 20
        )
    )


    # ========================================================
    # SCORE
    # ========================================================

    score_text = info_font.render(
        f"Score: {game.score}",
        True,
        WHITE
    )

    screen.blit(
        score_text,
        (
            25,
            720
        )
    )


    # ========================================================
    # LENGTH
    # ========================================================

    length_text = info_font.render(
        f"Length: {len(game.snake)}",
        True,
        WHITE
    )

    screen.blit(
        length_text,
        (
            180,
            720
        )
    )


    # ========================================================
    # CONTROLS
    # ========================================================

    controls_text = info_font.render(
        "R = Restart     Q = Quit",
        True,
        WHITE
    )

    screen.blit(
        controls_text,
        (
            400,
            720
        )
    )


    # ========================================================
    # GAME OVER
    # ========================================================

    if game.game_over:

        overlay = pygame.Surface(
            (
                GAME_WIDTH,
                GAME_HEIGHT
            ),
            pygame.SRCALPHA
        )

        overlay.fill(
            (
                0,
                0,
                0,
                190
            )
        )

        screen.blit(
            overlay,
            (
                game_x,
                game_y
            )
        )


        # Game over text

        game_over_text = game_over_font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(
            game_over_text,
            (
                game_x + 180,
                game_y + 280
            )
        )


        # Restart text

        restart_text = info_font.render(
            "Press R to Restart",
            True,
            WHITE
        )

        screen.blit(
            restart_text,
            (
                game_x + 250,
                game_y + 350
            )
        )


    # ========================================================
    # UPDATE DISPLAY
    # ========================================================

    pygame.display.flip()


# ============================================================
# CLEANUP
# ============================================================

tracker.release()

pygame.quit()
