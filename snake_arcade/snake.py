"""Snake Arcade playable character."""

import arcade

import settings


class Snake():
    """
    The hero character.

    Snake objects grow in length after eating food & die after
    colliding with a wall or their own body.

    Snake objects can speed up/down to a maximum/minimum amount.
    """

    def __init__(self, theme, size=settings.CELL, speed=8, head_pos=[0, 0],
                 direction='UP', change_direction=''):
        """
        Initialize the snake character.

        Define the physical, directional, positional, movement & status
        defaults.
        """
        # Physical attributes.
        self.size = size
        self.head_colour = theme['head']
        self.body_colour_1 = theme['snake_body_1']
        self.body_colour_2 = theme['snake_body_2']
        self.body_colour_3 = theme['snake_body_3']
        self.border_colour = theme['snake_border']
        self.eye_colour = theme['eye']
        self.pupil_colour = theme['pupil']
        # Direction.
        self.direction = direction
        self.change_direction = change_direction
        self.last_direction = ''
        # Position. Coordinates/units are in game grid "cells".
        self.head_pos = head_pos
        # Position used to get distance travelled by head between each 'move'.
        self.previous_pos = [self.head_pos[0], self.head_pos[1]]
        # List of body segment positions.
        self.body_segment_list = self.align()
        # Offset amount required to align snake objects to the game grid.
        self.offset = settings.CELL / 2
        # Movement (in game "cells" per second).
        self.speed = speed
        self.min_speed = 6
        self.max_speed = 16
        # Health status.
        self.eating = False
        self.dead = False
        self.time_dead = 0
        # Prepare snake for drawing.
        self.shape_list = self.create_snake()

    def update_theme(self, theme):
        """
        Load a colour theme.

        Rebuild all required objects.
        """
        self.head_colour = theme['head']
        self.body_colour_1 = theme['snake_body_1']
        self.body_colour_2 = theme['snake_body_2']
        self.body_colour_3 = theme['snake_body_3']
        self.border_colour = theme['snake_border']
        self.eye_colour = theme['eye']
        self.pupil_colour = theme['pupil']
        # Rebuild snake (although called in update_body()) to avoid glitches.
        self.shape_list = self.create_snake()

    def set_direction(self):
        """
        Set the snake direction to the player's desired direction.

        Disable opposing movements so that the snake cannot collide
        with itself.
        """
        if self.change_direction == 'UP' and \
           self.direction != 'DOWN':
            self.direction = 'UP'
        elif self.change_direction == 'DOWN' \
                and self.direction != 'UP':
            self.direction = 'DOWN'
        elif self.change_direction == 'LEFT' \
                and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif self.change_direction == 'RIGHT' \
                and self.direction != 'LEFT':
            self.direction = 'RIGHT'

    def align(self):
        """
        Align the snake along the axis it will travel.

        Set the body to follow the direction of the head.
        """
        # '' indicates the snake is stationary.
        if self.direction == 'LEFT' or self.direction == '':
            aligned_snake = [[self.head_pos[0], self.head_pos[1]],
                             [self.head_pos[0] + 1, self.head_pos[1]],
                             [self.head_pos[0] + 2, self.head_pos[1]]]
        elif self.direction == 'RIGHT':
            aligned_snake = [[self.head_pos[0], self.head_pos[1]],
                             [self.head_pos[0] - 1, self.head_pos[1]],
                             [self.head_pos[0] - 2, self.head_pos[1]]]
        elif self.direction == 'UP':
            aligned_snake = [[self.head_pos[0], self.head_pos[1]],
                             [self.head_pos[0], self.head_pos[1] - 1],
                             [self.head_pos[0], self.head_pos[1] - 2]]
        elif self.direction == 'DOWN':
            aligned_snake = [[self.head_pos[0], self.head_pos[1]],
                             [self.head_pos[0], self.head_pos[1] + 1],
                             [self.head_pos[0], self.head_pos[1] + 2]]
        return aligned_snake

    def move(self, dt):
        """
        Move the snake head cell around the board.

        Take delta time into account & make movements in game grid
        "cell" sized increments.
        """
        if not self.dead:
            if self.direction == 'UP':
                self.head_pos[1] += (self.speed * dt)
                if self.get_distance_travelled()[1] >= 1:
                    self.head_pos[1] = int(self.head_pos[1])
                    self.previous_pos[1] += 1
                    self.update_body()
                    self.set_direction()
            elif self.direction == 'DOWN':
                self.head_pos[1] -= (self.speed * dt)
                if self.get_distance_travelled()[1] >= 1:
                    # Account for int() rounding down.
                    self.head_pos[1] = int(self.head_pos[1] + 1)
                    self.previous_pos[1] -= 1
                    self.update_body()
                    self.set_direction()
            elif self.direction == 'LEFT':
                self.head_pos[0] -= (self.speed * dt)
                if self.get_distance_travelled()[0] >= 1:
                    # Account for int() rounding down.
                    self.head_pos[0] = int(self.head_pos[0] + 1)
                    self.previous_pos[0] -= 1
                    self.update_body()
                    self.set_direction()
            elif self.direction == 'RIGHT':
                self.head_pos[0] += (self.speed * dt)
                if self.get_distance_travelled()[0] >= 1:
                    self.head_pos[0] = int(self.head_pos[0])
                    self.previous_pos[0] += 1
                    self.update_body()
                    self.set_direction()

    def get_distance_travelled(self):
        """Measure the amount the snake has moved from the last position."""
        x_dist = abs(self.previous_pos[0] - self.head_pos[0])
        y_dist = abs(self.previous_pos[1] - self.head_pos[1])
        return x_dist, y_dist

    def increase_speed(self, increment):
        """Increase the speed of the snake up to a maximum."""
        if self.speed < self.max_speed:
            if not self.speed + increment > self.max_speed:
                self.speed = self.speed + increment
            elif self.speed + increment > self.max_speed:
                self.speed = self.max_speed

    def decrease_speed(self, increment):
        """Decrease the speed of the snake down to a minimum."""
        if self.speed > self.min_speed:
            if not self.speed - increment < self.min_speed:
                self.speed = self.speed - increment
            elif self.speed - increment < self.min_speed:
                self.speed = self.min_speed

    def raise_min_speed(self, increment):
        """Raise the minimum speed of the snake."""
        if self.min_speed < self.max_speed:
            if not self.min_speed + increment > self.max_speed:
                self.min_speed += increment

    def loop(self, top_l, top_r, bot_r, bot_l):
        """
        Loop the snake clockwise around four rectangular coordinates.

        Coordinates, or corner points of the "track", are required in
        (x, y) format.
        """
        if self.head_pos[0] == bot_l[0] and self.head_pos[1] == bot_l[1]:
            self.change_direction = 'UP'
        elif self.head_pos[0] == top_l[0] and self.head_pos[1] == top_l[1]:
            self.change_direction = 'RIGHT'
        elif self.head_pos[0] == top_r[0] and self.head_pos[1] == top_r[1]:
            self.change_direction = 'DOWN'
        elif self.head_pos[0] == bot_r[0] and self.head_pos[1] == bot_r[1]:
            self.change_direction = 'LEFT'

    def check_body_collisions(self):
        """Check if the snake has collided with itself."""
        if self.head_pos in self.body_segment_list[1:-1]:
            self.dead = True

    def grow_body(self):
        """
        Increase the snake length by one "cell".

        Insert the "head" as the first segment to achieve growth.
        """
        self.body_segment_list.insert(0, list(self.head_pos))

    def update_body(self):
        """
        Update the snake body.

        Grow the body when required.
        """
        if self.eating:
            self.grow_body()
        else:
            self.body_segment_list.insert(0, list(self.head_pos))
            # Stop growth by removing the last body segment (the "tail").
            self.body_segment_list.pop()
            self.shape_list = self.create_snake()

    def flash_body(self, interval, theme):
        """
        Repeatedly flash the visibility of the snake.

        Change body part colour to match the background to achieve a
        flash effect.
        """
        # Start the counter.
        self.time_dead += 1
        # Load the theme background colour into the snake body parts.
        if self.time_dead > 5 and self.time_dead <= interval:
            self.head_colour = theme['bg']
            self.body_colour_1 = theme['bg']
            self.body_colour_2 = theme['bg']
            self.body_colour_3 = theme['bg']
            self.border_colour = theme['bg']
            self.eye_colour = theme['bg']
            self.pupil_colour = theme['bg']
            self.shape_list = self.create_snake()
        # Reload the snake colours into the snake body parts.
        elif self.time_dead > interval:
            # Reset the counter.
            self.time_dead = 0
            self.head_colour = theme['head']
            self.body_colour_1 = theme['snake_body_1']
            self.body_colour_2 = theme['snake_body_2']
            self.body_colour_3 = theme['snake_body_3']
            self.border_colour = theme['snake_border']
            self.eye_colour = theme['eye']
            self.pupil_colour = theme['pupil']
            self.shape_list = self.create_snake()

    def get_grid_coords(self):
        """
        Get cartesian coordinates for the snake in pixels.

        Use an offset to account for the way arcade creates rectangles,
        so that each rectangular object is centered within the rows &
        columns of the game grid.
        """
        grid_coords = []
        for position in self.body_segment_list:
            x = (position[0] * self.size) - self.offset
            y = (position[1] * self.size) - self.offset
            offset_coords = (x, y)
            grid_coords.append(offset_coords)
        return grid_coords

    # *** BUFFERED DRAWING METHODS *** #

    def get_segment_points(self, position, width=settings.CELL,
                           height=settings.CELL):
        """Get a list of four vertices for one segment of the snake."""
        segment_points = arcade.get_rectangle_points(
            position[0],
            position[1],
            width,
            height,
            )
        return segment_points

    def create_segment_border(self, position, colour, width=settings.CELL,
                              height=settings.CELL):
        """Create the colour border for one segment of the snake."""
        segment_border = arcade.create_rectangle_outline(
            position[0],
            position[1],
            width,
            height,
            colour,
            2
            )
        return segment_border

    def create_body_segment_fills(self, body_segments):
        """
        Create the snake body segments (including head/tail).

        Return a list of vertex buffer objects (VBOs) that can be
        rendered to the screen efficiently.
        """
        body_segment_point_list = []
        body_segment_colour_list = []
        # Add the head shape points & the head colour.
        for segment_xy in body_segments[:1]:
            segment_points = self.get_segment_points(segment_xy)
            for point in segment_points:
                body_segment_point_list.append(point)
                body_segment_colour_list.append(self.head_colour)
        # Add body segment shape points & the first body segment colour.
        for segment_xy in body_segments[1::3]:
            segment_points = self.get_segment_points(segment_xy)
            for point in segment_points:
                body_segment_point_list.append(point)
                body_segment_colour_list.append(self.body_colour_1)
        # Add body segment shape points & the second body segment colour.
        for segment_xy in body_segments[2::3]:
            segment_points = self.get_segment_points(segment_xy)
            for point in segment_points:
                body_segment_point_list.append(point)
                body_segment_colour_list.append(self.body_colour_2)
        # Add body segment shape points & the third body segment colour.
        for segment_xy in body_segments[3::3]:
            segment_points = self.get_segment_points(segment_xy)
            for point in segment_points:
                body_segment_point_list.append(point)
                body_segment_colour_list.append(self.body_colour_3)
        # Create the entire body VBO.
        body_segment_fills = arcade.create_rectangles_filled_with_colors(
            body_segment_point_list,
            body_segment_colour_list
            )
        return body_segment_fills

    def create_body_segment_borders(self, body_segments):
        """
        Create the snake body segments borders (including head/tail).

        Return a list of objects that can be rendered to the screen
        efficiently.
        """
        body_segments_border_list = []
        for segment in body_segments:
            body_segments_border_list.append(
                self.create_segment_border(segment, self.border_colour))
        return body_segments_border_list

    def get_eye_points(self):
        """
        Get a list of eight vertices for two rectangular eye objects.

        Return points for eyes facing in any direction the snake can travel.
        """
        eye_point_list = []
        # Create the eyes, even when direction not set e.g. game is paused.
        if self.direction == 'UP' or self.direction == '':
            left_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                - self.size / 3,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                + self.size / 12,
                width=self.size / 4,
                height=self.size / 3,
                 )
            right_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                + self.size / 3,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                + self.size / 12,
                width=self.size / 4,
                height=self.size / 3
                 )
        elif self.direction == 'DOWN':
            left_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                - self.size / 3,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                - self.size / 12,
                width=self.size / 4,
                height=self.size / 3
                 )
            right_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                + self.size / 3,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                - self.size / 12,
                width=self.size / 4,
                height=self.size / 3
                 )
        elif self.direction == 'LEFT':
            left_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                - self.size / 10,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                + self.size / 3,
                width=self.size / 3,
                height=self.size / 4
                 )
            right_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                - self.size / 10,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                - self.size / 3,
                width=self.size / 3,
                height=self.size / 4
                 )
        elif self.direction == 'RIGHT':
            left_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                + self.size / 10,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                + self.size / 3,
                width=self.size / 3,
                height=self.size / 4
                 )
            right_eye_fill = arcade.get_rectangle_points(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                + self.size / 10,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                - self.size / 3,
                width=self.size / 3,
                height=self.size / 4
                 )
        for point in left_eye_fill:
            eye_point_list.append(point)
        for point in right_eye_fill:
            eye_point_list.append(point)
        return eye_point_list

    def create_eye_borders(self, colour):
        """
        Create the snake eye borders.

        Return a list of objects that can be rendered to the screen
        efficiently.
        """
        eye_borders_list = []
        # Create eye borders, even when direction not set e.g. game is paused.
        if self.direction == 'UP' or self.direction == '':
            left_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                - self.size / 3,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                + self.size / 12,
                self.size / 4, self.size / 3, colour,
                1
                 )
            right_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                + self.size / 3,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                + self.size / 12,
                self.size / 4, self.size / 3, colour,
                1
                 )
        elif self.direction == 'DOWN':
            left_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                - self.size / 3,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                - self.size / 12,
                self.size / 4, self.size / 3, colour,
                1
                 )
            right_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                + self.size / 3,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                - self.size / 12,
                self.size / 4, self.size / 3, colour,
                1
                 )
        elif self.direction == 'LEFT':
            left_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                - self.size / 10,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                + self.size / 3,
                self.size / 3, self.size / 4, colour,
                1
                 )
            right_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                - self.size / 10,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                - self.size / 3,
                self.size / 3, self.size / 4, colour,
                1
                 )
        elif self.direction == 'RIGHT':
            left_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                + self.size / 10,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                + self.size / 3,
                self.size / 3, self.size / 4, colour,
                1
                 )
            right_eye_border = arcade.create_rectangle_outline(
                ((self.body_segment_list[0][0] * settings.CELL) - self.offset)
                + self.size / 10,
                ((self.body_segment_list[0][1] * settings.CELL) - self.offset)
                - self.size / 3,
                self.size / 3, self.size / 4, colour,
                1
                 )
        eye_borders_list.append(left_eye_border)
        eye_borders_list.append(right_eye_border)
        return eye_borders_list

    def create_eye_fills(self, eye_point_list, colour):
        """
        Create the snake body segments (including head/tail).

        Return a list of vertex buffer objects (VBOs) that can be
        rendered to the screen efficiently.
        """
        eye_fill_point_list = []
        eye_fill_colour_list = []
        for point in eye_point_list:
            eye_fill_point_list.append(point)
            eye_fill_colour_list.append(colour)
        # Create the eye group VBO.
        eye_fills = arcade.create_rectangles_filled_with_colors(
            eye_fill_point_list,
            eye_fill_colour_list
        )
        return eye_fills

    def create_snake(self):
        """
        Create buffered shapes for the snake object.

        Return a ShapeElementList list containing the each part of the
        snake object to be drawn.
        """
        # Redefine the shape list to clear unneeded entries.
        shape_list = arcade.ShapeElementList()
        # Get all the snake objects.
        body_fills = self.create_body_segment_fills(self.get_grid_coords())
        body_borders = self.create_body_segment_borders(self.get_grid_coords())
        eyes = self.create_eye_fills(self.get_eye_points(),
                                     self.pupil_colour)
        eye_borders = self.create_eye_borders(self.eye_colour)
        # Populate the shape list.
        shape_list.append(body_fills)
        for border in body_borders:
            shape_list.append(border)
        shape_list.append(eyes)
        for border in eye_borders:
            shape_list.append(border)
        return shape_list
