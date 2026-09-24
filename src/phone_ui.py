import pygame


class PhoneUI:

    def __init__(self):

        self.width = 600
        self.height = 750

        pygame.init()

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption(
            "Classic Button Phone - Snake"
        )

        self.font = pygame.font.SysFont(
            "Arial",
            26,
            bold=True
        )

        self.title_font = pygame.font.SysFont(
            "Arial",
            30,
            bold=True
        )

        self.small_font = pygame.font.SysFont(
            "Arial",
            18
        )

        # -------------------------
        # LCD SCREEN
        # -------------------------

        self.screen_rect = pygame.Rect(
            100,
            70,
            400,
            330
        )

        # -------------------------
        # NAVIGATION BUTTONS
        # -------------------------

        self.up_button = pygame.Rect(
            255,
            470,
            90,
            55
        )

        self.left_button = pygame.Rect(
            155,
            530,
            90,
            55
        )

        self.center_button = pygame.Rect(
            255,
            530,
            90,
            55
        )

        self.right_button = pygame.Rect(
            355,
            530,
            90,
            55
        )

        self.down_button = pygame.Rect(
            255,
            590,
            90,
            55
        )

    def draw_phone(self):

        # Background
        self.screen.fill((30, 30, 30))

        # -------------------------
        # PHONE BODY
        # -------------------------

        pygame.draw.rect(
            self.screen,
            (80, 80, 80),
            (50, 20, 500, 700),
            border_radius=35
        )

        # -------------------------
        # TITLE
        # -------------------------

        title = self.title_font.render(
            "SNAKE",
            True,
            (230, 230, 230)
        )

        self.screen.blit(
            title,
            (
                self.width // 2 - title.get_width() // 2,
                30
            )
        )

        # -------------------------
        # LCD SCREEN
        # -------------------------

        pygame.draw.rect(
            self.screen,
            (180, 200, 150),
            self.screen_rect,
            border_radius=8
        )

        pygame.draw.rect(
            self.screen,
            (20, 20, 20),
            self.screen_rect,
            4,
            border_radius=8
        )

        # -------------------------
        # NAVIGATION BUTTONS
        # -------------------------

        buttons = [
            (self.up_button, "▲"),
            (self.left_button, "◀"),
            (self.center_button, "OK"),
            (self.right_button, "▶"),
            (self.down_button, "▼")
        ]

        for rect, text in buttons:

            pygame.draw.rect(
                self.screen,
                (25, 25, 25),
                rect,
                border_radius=12
            )

            pygame.draw.rect(
                self.screen,
                (160, 160, 160),
                rect,
                2,
                border_radius=12
            )

            label = self.font.render(
                text,
                True,
                (240, 240, 240)
            )

            self.screen.blit(
                label,
                (
                    rect.centerx - label.get_width() // 2,
                    rect.centery - label.get_height() // 2
                )
            )

    def get_button_direction(self, position):

        if self.up_button.collidepoint(position):
            return (0, -1)

        if self.left_button.collidepoint(position):
            return (-1, 0)

        if self.right_button.collidepoint(position):
            return (1, 0)

        if self.down_button.collidepoint(position):
            return (0, 1)

        return None