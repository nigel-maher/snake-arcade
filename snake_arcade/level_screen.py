"""Snake Arcade level screen."""

import arcade

import settings


class LevelScreen():
    """
    Snake arcade level screen.

    Where the gameplay takes place. A basic screen layout which other
    game screens can build upon.
    """

    def __init__(self, theme):
        """Initialize the level screen."""
        # Colours.
        self.bg_col = theme['bg']
        self.fg_col = theme['fg']
        self.board_col = theme['board']
        self.scoreboard_col = theme['scoreboard']
        self.score_text_col = theme['score_text']
        self.score_num_col = theme['score_num']
        # Font.
        self.font = 'prolamina_2_update'
        # Level elements for drawing.
        self.shape_list = self.create_shapes()

    def update_theme(self, theme):
        """
        Load a colour theme.

        Rebuild all required objects.
        """
        self.bg_col = theme['bg']
        self.fg_col = theme['fg']
        self.board_col = theme['board']
        self.scoreboard_col = theme['scoreboard']
        self.score_text_col = theme['score_text']
        self.score_num_col = theme['score_num']
        self.shape_list = self.create_shapes()

    def create_border_wall(self, colour):
        """
        Create a border wall around the game board & scoreboard.

        Return an object that can be rendered to the screen efficiently.
        """
        border_wall = arcade.create_rectangle_outline(
            settings.WINDOW_WIDTH / 2,
            settings.WINDOW_HEIGHT / 2,
            settings.WINDOW_WIDTH - (settings.CELL * 2),
            settings.WINDOW_HEIGHT - (settings.CELL * 2),
            colour,
            8
            )
        return border_wall

    def create_scoreboard_backing(self, colour):
        """
        Create a coloured rectangle for the scoreboard backing.

        Return an object that can be rendered to the screen efficiently.
        """
        scoreboard_backing = arcade.create_rectangle_filled(
            settings.WINDOW_WIDTH / 2,
            (settings.WINDOW_HEIGHT - settings.CELL * 4)
            + settings.CELL / 2,
            settings.WINDOW_WIDTH - (settings.CELL * 1.875),
            settings.CELL * 5.125,
            colour
            )
        return scoreboard_backing

    def create_scoreboard_overlay(self, colour):
        """
        Create a coloured rectangle with transparency.

        Return an object that can be rendered to the screen efficiently.
        """
        scoreboard_overlay = arcade.create_rectangle_filled(
            settings.WINDOW_WIDTH / 2,
            (settings.WINDOW_HEIGHT - settings.CELL * 4)
            + settings.CELL / 2,
            settings.WINDOW_WIDTH - (settings.CELL * 1.75),
            settings.CELL * 5.125,
            self.get_overlay_values(colour, 50)
            )
        return scoreboard_overlay

    def create_divider(self, colour):
        """
        Create a dividing line between the game board & scoreboard.

        Return an object that can be rendered to the screen efficiently.
        """
        divider = arcade.create_line(
             settings.CELL - (settings.CELL / 8),
             settings.WINDOW_HEIGHT - (settings.CELL * 6),
             settings.WINDOW_WIDTH - (settings.CELL - (settings.CELL / 8)),
             settings.WINDOW_HEIGHT - (settings.CELL * 6),
             colour,
             8)
        return divider

    def create_game_board(self, colour):
        """
        Create a coloured rectangle to represent the game board.

        Return an object that can be rendered to the screen efficiently.
        """
        game_board = arcade.create_rectangle_filled(
            settings.WINDOW_WIDTH / 2,
            ((settings.WINDOW_HEIGHT / 2) - (settings.CELL * 3))
            + settings.CELL / 2,
            settings.WINDOW_WIDTH - (settings.CELL * 2),
            settings.WINDOW_HEIGHT - (settings.CELL * 7),
            colour
            )
        return game_board

    def create_game_board_outline(self, colour):
        """
        Create a small outline around the game board.

        Keep a visual gap between snake objects & the border wall.

        Return an object that can be rendered to the screen efficiently.
        """
        game_board_outline = arcade.create_rectangle_outline(
            settings.WINDOW_WIDTH / 2,
            ((settings.WINDOW_HEIGHT / 2) - (settings.CELL * 3))
            + settings.CELL / 2,
            settings.WINDOW_WIDTH - (settings.CELL * 2),
            settings.WINDOW_HEIGHT - (settings.CELL * 7),
            colour,
            2
            )
        return game_board_outline

    def get_overlay_values(self, input_colour, alpha):
        """
        Add an alpha channel to an input colour & returns the result.

        The input colour must be a tuple RGB value, e.g (255. 0, 0).

        The output colour will be a tuple RGBa value e,g (255, 0, 0, 75).
        """
        start_colour = list(input_colour)
        start_colour.append(alpha)
        output_colour = tuple(start_colour)
        return output_colour

    def create_shapes(self):
        """
        Create buffered shapes for the level objects.

        Return a ShapeElementList containing the level objects to
        be drawn in stacking order.
        """
        # Redefine the shape list to clear unneeded entries.
        shape_list = arcade.ShapeElementList()
        # Some objects are deliberately drawn to slightly cover others.
        border_wall = self.create_border_wall(self.fg_col)
        scoreboard_backing = self.create_scoreboard_backing(
            self.scoreboard_col)
        scoreboard_overlay = self.create_scoreboard_overlay(self.fg_col)
        divider = self.create_divider(self.fg_col)
        game_board = self.create_game_board(self.bg_col)
        game_board_outline = self.create_game_board_outline(self.bg_col)
        # Populate the shape list.
        shape_list.append(border_wall)
        shape_list.append(scoreboard_backing)
        shape_list.append(scoreboard_overlay)
        shape_list.append(divider)
        shape_list.append(game_board)
        shape_list.append(game_board_outline)
        return shape_list

    def draw_score_text(self, colour):
        """Draw text for the score label."""
        arcade.draw_text('SCORE:', 49.6, 564, colour,
                         58, font_name=self.font)

    def draw_score_num(self, score, colour):
        """Draw text for the score."""
        arcade.draw_text(score, 200, 564, colour,
                         58, font_name=self.font)

    def draw(self, score):
        """Draw all the level objects."""
        self.shape_list.draw()
        self.draw_score_text(self.score_text_col)
        self.draw_score_num(score, self.score_num_col)
