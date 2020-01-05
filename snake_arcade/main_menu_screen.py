"""Snake Arcade main menu screen."""

import arcade

import level_screen
import settings


class MainMenuScreen(level_screen.LevelScreen):
    """
    Snake Arcade main menu screen.

    Consists of text & objects designed to be drawn on top of a level
    screen instance.
    """

    def __init__(self, theme):
        """Initialize the main menu screen."""
        super().__init__(theme)
        # Rectangular coords offset around title (top_l, top_r, bot_r, bot_l).
        self.snake_track = ((4, 36), (21, 37), (22, 28), (5, 27))
        # Colours.
        self.letter_s_col = theme['S']
        self.letter_n_col = theme['N']
        self.letter_a_col = theme['A']
        self.letter_k_col = theme['K']
        self.letter_e_col = theme['E']
        self.arcade = theme['arcade']
        self.small_text_col = theme['small_text']
        # Timer.
        self.timer = 0

    def update_theme(self, theme):
        """
        Load a colour theme.

        Rebuild all required objects.
        """
        self.bg_col = theme['bg']
        self.fg_col = theme['fg']
        self.letter_s_col = theme['S']
        self.letter_n_col = theme['N']
        self.letter_a_col = theme['A']
        self.letter_k_col = theme['K']
        self.letter_e_col = theme['E']
        self.arcade = theme['arcade']
        self.small_text_col = theme['small_text']
        self.shape_list = self.create_shapes()

    def create_menu_board(self, colour):
        """
        Create a coloured rectangle for the menu board.

        Return an object that can be rendered to the screen efficiently.
        """
        menu_board = arcade.create_rectangle_filled(
            settings.WINDOW_WIDTH / 2,
            settings.WINDOW_HEIGHT / 2,
            settings.WINDOW_WIDTH - (settings.CELL * 2),
            settings.WINDOW_HEIGHT - (settings.CELL * 2),
            colour
            )
        return menu_board

    def create_menu_board_outline(self, colour):
        """
        Create a small outline around the menu board.

        Keep a visual gap between snake objects & the border wall.

        Return an object that can be rendered to the screen efficiently.
        """
        menu_board_outline = arcade.create_rectangle_outline(
            settings.WINDOW_WIDTH / 2,
            settings.WINDOW_HEIGHT / 2,
            settings.WINDOW_WIDTH - (settings.CELL * 2),
            settings.WINDOW_HEIGHT - (settings.CELL * 2),
            colour,
            2
            )
        return menu_board_outline

    def create_shapes(self):
        """
        Create buffered shapes for the main menu objects.

        Return a ShapeElementList containing the main menu objects to
        be drawn in stacking order.
        """
        # Redefine the shape list to clear unneeded entries.
        shape_list = arcade.ShapeElementList()
        # Some objects are deliberately drawn to slightly cover others.
        border_wall = self.create_border_wall(self.fg_col)
        menu_board = self.create_menu_board(self.bg_col)
        menu_board_outline = self.create_menu_board_outline(self.bg_col)
        # Populate the shape list.
        shape_list.append(border_wall)
        shape_list.append(menu_board)
        shape_list.append(menu_board_outline)
        return shape_list

    def draw_title(self, col_s, col_n, col_a, col_k, col_e, col_arc):
        """Draw text for the game title."""
        arcade.draw_text('S', 76, 487, col_s,
                         108, font_name=self.font)
        arcade.draw_text('N', 126, 487, col_n,
                         108, font_name=self.font)
        arcade.draw_text('A', 176, 487, col_a,
                         108, font_name=self.font)
        arcade.draw_text('K', 226, 487, col_k,
                         108, font_name=self.font)
        arcade.draw_text('E', 276, 487, col_e,
                         108, font_name=self.font)
        arcade.draw_text('arcade', 108, 443, col_arc,
                         70, font_name=self.font)

    def draw_instructions(self, colour):
        """Draw text for the game instructions."""
        arcade.draw_text('Eat the food!', 123, 335, colour,
                         32, font_name=self.font)

    def draw_controls(self, colour):
        """Draw text for the game controls."""
        arcade.draw_text('[ENTER] Start', 139, 265, colour,
                         24, font_name=self.font)
        arcade.draw_text('[ARROWS] Turn', 131, 235, colour,
                         24, font_name=self.font)
        arcade.draw_text('[S] Speed Up', 140, 205, colour,
                         24, font_name=self.font)
        arcade.draw_text('[D] Speed Down', 128, 175, colour,
                         24, font_name=self.font)
        arcade.draw_text('[T] Theme', 152, 145, colour,
                         24, font_name=self.font)

    def draw_version_num(self, colour):
        """Draw text for the game version number."""
        arcade.draw_text(settings.VERSION, 178, 65, colour,
                         18, font_name=self.font)

    def draw(self):
        """Draw all the main menu objects."""
        self.shape_list.draw()
        self.draw_title(self.letter_s_col, self.letter_n_col,
                        self.letter_a_col, self.letter_k_col,
                        self.letter_e_col, self.arcade)
        self.draw_instructions(self.letter_s_col)
        self.draw_controls(self.small_text_col)
        self.draw_version_num(self.small_text_col)
