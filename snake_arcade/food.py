"""Snake Arcade food object."""

import arcade

import settings


class Food():
    """Square food object for the snake to eat."""

    food_spawned = 0
    food_eaten = 0

    def __init__(self, theme, size, snake, pos=[0, 0]):
        """
        Initialize the food object.

        Define the physical & positional defaults.
        """
        # Physical attributes.
        self.size = size
        self.fill_colour = theme['food']
        self.border_colour = theme['food_border']
        # Position. Coordinates/units are in game grid "cells".
        self.position = pos
        # Offset amount required to align food objects to the game grid.
        self.offset = settings.CELL / 2
        # Prepare food for drawing.
        self.shape_list = self.create_food()

    def update_theme(self, theme):
        """
        Load a colour theme.

        Rebuild all required objects.
        """
        self.fill_colour = theme['food']
        self.border_colour = theme['food_border']
        self.shape_list = self.create_food()

    def get_grid_coords(self):
        """
        Get cartesian coordinates for a piece of food in pixels.

        Use an offset to account for the way arcade creates rectangles,
        so that each rectangular object is centered within the rows &
        columns of the game grid.
        """
        x = (self.position[0] * self.size) - self.offset
        y = (self.position[1] * self.size) - self.offset
        grid_coords = (x, y)
        return grid_coords

    # *** BUFFERED DRAWING METHODS *** #

    def get_food_points(self, position, width=settings.CELL,
                        height=settings.CELL):
        """Get a list of four vertices for a piece of food."""
        food_points = arcade.get_rectangle_points(
            position[0],
            position[1],
            width,
            height,
            )
        return food_points

    def create_food_border(self, position, colour, width=settings.CELL,
                           height=settings.CELL):
        """Create the colour border for a piece of food."""
        food_border = arcade.create_rectangle_outline(
            position[0],
            position[1],
            width,
            height,
            colour,
            2
            )
        return food_border

    def create_food_fill(self):
        """
        Create the square fill for a piece of food.

        Return a vertex buffer object (VBO) that can be rendered to the
        screen efficiently.
        """
        food_point_list = []
        food_colour_list = []
        # Add the food shape points & colour.
        food_points = self.get_food_points(self.get_grid_coords())
        for point in food_points:
            food_point_list.append(point)
            food_colour_list.append(self.fill_colour)
        # Create the food fill VBO.
        food_fill = arcade.create_rectangles_filled_with_colors(
            food_point_list,
            food_colour_list
            )
        return food_fill

    def create_food(self):
        """
        Create buffered shapes for the food objects.

        Return a ShapeElementList list containing the food object to
        be drawn.
        """
        # Redefine the shape list to clear unneeded entries.
        shape_list = arcade.ShapeElementList()
        # Get the food object components.
        food_fill = self.create_food_fill()
        food_border = self.create_food_border(self.get_grid_coords(),
                                              self.border_colour)
        # Populate the shape list.
        shape_list.append(food_fill)
        shape_list.append(food_border)
        return shape_list
