"""Snake Arcade game over screen."""

import arcade

import level_screen
import settings


class GameOverScreen(level_screen.LevelScreen):
    """
    Snake Arcade game over screen.

    Consists of text & objects designed to be drawn on top of a level
    screen instance.
    """

    def __init__(self, theme):
        """Initialize the game over screen."""
        super().__init__(theme)
        self.game_over_text_col = theme['game_over']
        self.small_text_col = theme['food']

    def update_theme(self, theme):
        """
        Load a colour theme.

        Rebuild all required objects.
        """
        self.bg_col = theme['bg']
        self.fg_col = theme['fg']
        self.game_over_text_col = theme['game_over']
        self.small_text_col = theme['food']
        self.shape_list = self.create_shapes()

    def create_message_box(self, colour):
        """
        Create a coloured rectangle for the message box.

        Return an object that can be rendered to the screen efficiently.
        """
        message_box = arcade.create_rectangle_filled(
            settings.WINDOW_WIDTH / 2,
            settings.WINDOW_HEIGHT / 2 + settings.CELL,
            settings.WINDOW_WIDTH - (settings.CELL * 10),
            (settings.WINDOW_HEIGHT / 2) - (settings.CELL * 7),
            colour
            )
        return message_box

    def create_message_box_overlay(self, colour):
        """
        Create a coloured rectangle with transparency for the message box.

        Return an object that can be rendered to the screen efficiently.
        """
        message_box_overlay = arcade.create_rectangle_filled(
            settings.WINDOW_WIDTH / 2,
            settings.WINDOW_HEIGHT / 2 + settings.CELL,
            settings.WINDOW_WIDTH - (settings.CELL * 10),
            (settings.WINDOW_HEIGHT / 2) - (settings.CELL * 7),
            self.get_overlay_values(colour, 50)
            )
        return message_box_overlay

    def create_message_box_outline(self, colour):
        """
        Create a small outline around the message box.

        Return an object that can be rendered to the screen efficiently.
        """
        message_box_outline = arcade.create_rectangle_outline(
            settings.WINDOW_WIDTH / 2,
            settings.WINDOW_HEIGHT / 2 + settings.CELL,
            settings.WINDOW_WIDTH - (settings.CELL * 10),
            (settings.WINDOW_HEIGHT / 2) - (settings.CELL * 7),
            colour,
            6
            )
        return message_box_outline

    def create_shapes(self):
        """
        Create buffered shapes for the game over screen objects.

        Return a ShapeElementList containing the game over screen
        objects to be drawn in stacking order.
        """
        # Redefine the shape list to clear unneeded entries.
        shape_list = arcade.ShapeElementList()
        game_board_overlay = self.create_game_board(
            self.get_overlay_values(self.bg_col, 192)
            )
        game_board_overlay_outline = self.create_game_board_outline(
            self.get_overlay_values(self.bg_col, 192)
        )
        message_box_outline = self.create_message_box_outline(self.fg_col)
        message_box = self.create_message_box(self.bg_col)
        message_box_overlay = self.create_message_box_overlay(self.fg_col)
        # Populate the shape list.
        shape_list.append(game_board_overlay)
        shape_list.append(game_board_overlay_outline)
        shape_list.append(message_box_outline)
        shape_list.append(message_box)
        shape_list.append(message_box_overlay)
        return shape_list

    def draw_game_over(self, colour):
        """Draw text for the game over message."""
        arcade.draw_text('GAME', 100, 350, colour,
                         96, font_name=self.font)
        arcade.draw_text('OVER', 111, 287, colour,
                         96, font_name=self.font)

    def draw_restart(self, colour):
        """Draw text for the restart option."""
        arcade.draw_text('RESTART Y/N?', 118, 255, colour,
                         32, font_name=self.font)

    def draw(self):
        """Draw all the game over screen objects."""
        self.shape_list.draw()
        self.draw_game_over(self.game_over_text_col)
        self.draw_restart(self.small_text_col)
