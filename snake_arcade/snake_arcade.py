#!/usr/bin/env python3

"""Snake Arcade - A 2D snake game by Nigel Maher."""

import os
import random

import arcade

import colours
import food
import game_over_screen
import level_screen
import main_menu_screen
import settings
import snake
import states

# Change working directory to the font directory.
fonts_dir = os.path.join(os.path.split(
    os.path.dirname(os.path.abspath(__file__)))[0], 'fonts')
os.chdir(fonts_dir)


class Game(arcade.Window):
    """Main application."""

    def __init__(self, width, height, title, fullscreen=True):
        """
        Initialize the application.

        Call the parent constructor & override default arcade
        properties where required.

        Define the game state, difficulty & theme defaults.
        """
        super().__init__(width, height, title)
        super().set_update_rate(1 / settings.FPS)
        super().set_mouse_visible(False)
        self.game_state = states.GAME_STATES['main_menu']
        self.mode = states.GAME_MODES['normal']
        self.score = None
        self.themes = colours.themes
        self.theme = colours.jungle
        arcade.set_background_color(self.theme['bg'])

    def setup_screens(self):
        """Set up the game screens."""
        self.level = level_screen.LevelScreen(self.theme)
        self.main_menu = main_menu_screen.MainMenuScreen(self.theme)
        self.start_title_loop = False
        self.pause_title_loop = False
        self.game_over_screen = game_over_screen.GameOverScreen(self.theme)
        # Instantiate snake & food objects in position for the main menu.
        self.snake_p1 = snake.Snake(self.theme, size=settings.CELL,
                                    speed=12, head_pos=[12, 27],
                                    direction='')
        self.food = food.Food(self.theme, settings.CELL,
                              self.snake_p1, pos=[6, 27])

    def setup_game(self):
        """Set up the game."""
        # Instantiate snake & food objects in random positions for gameplay.
        self.snake_p1 = snake.Snake(
            self.theme, size=settings.CELL, speed=6,
            head_pos=[self.get_random_board_coords(pad_left=2,
                                                   pad_right=2)[0],
                      self.get_random_board_coords(pad_bottom=5,
                                                   pad_top=14)[1]]
            )
        self.spawn_food_randomly(self.snake_p1, self.food)
        # Instantiate the appropriate scoring system.
        if self.mode == states.GAME_MODES['easy']:
            self.score = Score(50, None)
        elif self.mode == states.GAME_MODES['normal']:
            self.score = Score(100, 500)
        elif self.mode == states.GAME_MODES['hard']:
            self.score = Score(200, 600)

    def menu_mode(self, delta_time):
        """
        Logic for running the main menu.

        Features a snake that loops around the title text.
        """
        # Pause the snake before starting to loop around the title text.
        if self.snake_p1.direction == '' and not self.start_title_loop:
            self.main_menu.timer += 1
            if self.main_menu.timer == 60:
                # Reset the timer & start the snake loop.
                self.main_menu.timer = 0
                self.start_title_loop = True
                self.snake_p1.direction = 'LEFT'
        # Pause on theme change.
        if self.snake_p1.direction == '' and self.start_title_loop:
            self.pause_title_loop = True
            self.main_menu.timer += 1
            if self.main_menu.timer == 30:
                # Reset the timer & continue the snake loop.
                self.main_menu.timer = 0
                self.pause_title_loop = False
                self.snake_p1.direction = self.snake_p1.last_direction
        # Check for collisions with food.
        self.check_food_collisions(self.snake_p1, self.food.position)
        # Grow the snake when food is eaten.
        if self.snake_p1.eating and len(self.snake_p1.body_segment_list) <= 16:
            self.snake_p1.grow_body()
            self.snake_p1.eating = False
            # Spawn food ahead of the snake as it loops around the title text.
            self.food.position = self.place_food_along_track(
                self.snake_p1,
                self.main_menu.snake_track,
                6
                )
            self.food.shape_list = self.food.create_food()
        elif self.snake_p1.eating and \
                len(self.snake_p1.body_segment_list) > 16:
            self.snake_p1.eating = False
            self.food.position = self.place_food_along_track(
                self.snake_p1,
                self.main_menu.snake_track,
                6
                )
            self.food.shape_list = self.food.create_food()
        self.snake_p1.loop(
            self.main_menu.snake_track[0],
            self.main_menu.snake_track[1],
            self.main_menu.snake_track[2],
            self.main_menu.snake_track[3],
        )
        self.snake_p1.move(delta_time)

    def normal_mode(self, delta_time):
        """
        Logic for a gameplay mode aimed at intermediate players.

        Features a snake that speeds up once it reaches a milestone score.
        """
        # Check for collisions with food & border walls.
        self.check_food_collisions(self.snake_p1, self.food.position)
        self.check_wall_collisions(self.snake_p1)
        # Check for a collision with the snake's own body.
        self.snake_p1.check_body_collisions()
        # Grow the snake & advance the game state when food is eaten.
        if self.snake_p1.eating:
            self.snake_p1.grow_body()
            self.food.food_eaten += 1
            self.snake_p1.eating = False
            # Spawn food.
            self.spawn_food_randomly(self.snake_p1, self.food)
            # Update the score & score display string.
            self.score.add_food_points()
            self.score.get_padded_str()
            # Increase snake speed (if below max) if a milestone is reached.
            if self.score.check_milestone():
                # if self.snake_p1.speed < self.snake_p1.max_speed:
                self.snake_p1.increase_speed(1)
                self.snake_p1.raise_min_speed(1)
        # Flash the snake body when dead.
        if self.snake_p1.dead:
            self.snake_p1.flash_body(30, self.theme)
            self.game_state = states.GAME_STATES['game_over']
        self.snake_p1.move(delta_time)

    def get_next_theme(self):
        """Cycle through application colour themes."""
        theme_index = self.themes.index(self.theme)
        theme_index += 1
        if theme_index == len(self.themes):
            theme_index = 0
        next_theme = self.themes[theme_index]
        return next_theme

    def get_random_theme(self):
        """Choose a random theme which is not in use."""
        random_theme = random.choice(self.themes)
        while random_theme == self.theme:
            random_theme = random.choice(self.themes)
        return random_theme

    def switch_theme(self, theme):
        """Change object colours to match the current application theme."""
        self.theme = theme
        self.main_menu.update_theme(theme)
        self.level.update_theme(theme)
        self.snake_p1.update_theme(theme)
        self.food.update_theme(theme)
        self.game_over_screen.update_theme(theme)

    def get_random_board_coords(self, pad_left=0, pad_right=0,
                                pad_bottom=0, pad_top=0):
        """
        Get random coordinates on the game board.

        Allow for padding from the game board edges.
        """
        x = random.randint((settings.BOARD_LEFT + pad_left),
                           (settings.BOARD_RIGHT - pad_right))
        y = random.randint((settings.BOARD_BOTTOM + pad_bottom),
                           (settings.BOARD_TOP - pad_top))
        return x, y

    def spawn_food_randomly(self, snake, food):
        """
        Spawn a food object on the game board in a random position.

        Respawn if food is placed inside the snake.
        """
        new_pos_xy = [self.get_random_board_coords()[0],
                      self.get_random_board_coords()[1]]
        food.position = new_pos_xy
        # Respawn if food position is inside of the snake.
        while food.position in snake.body_segment_list:
            self.spawn_food_randomly(snake, food)
        food.shape_list = food.create_food()
        food.food_spawned += 1
        return new_pos_xy

    def place_food_along_track(self, p1_snake, track, distance):
        """
        Place food ahead of the snake as it loops clockwise around a "track".

        Track coordinates (four rectangular points) are required as a
        tuple containing four (x, y) tuples.

        Placement distance in game grid "cells".
        """
        global new_pos_x
        global new_pos_y
        top_l = (track[0])
        top_r = (track[1])
        bot_r = (track[2])
        bot_l = (track[3])
        if p1_snake.direction == 'LEFT':
            # Place food ahead of the snake along the axis it travels.
            new_pos_x = p1_snake.head_pos[0] - distance
            new_pos_y = p1_snake.head_pos[1]
            # If the new postion is past the bottom left corner point.
            if new_pos_x < bot_l[0]:
                # Get the amount of overshoot.
                overshoot = abs(new_pos_x - bot_l[0])
                # Turn the corner by going up along the y-axis.
                new_pos_y = bot_l[1] + overshoot
                # Limit travel along the x-axis to the course corner point.
                new_pos_x = bot_l[0] - 1
        elif p1_snake.direction == 'RIGHT':
            new_pos_x = p1_snake.head_pos[0] + distance
            new_pos_y = p1_snake.head_pos[1]
            if new_pos_x > top_r[0]:
                overshoot = abs(new_pos_x - top_r[0])
                new_pos_y = top_r[1] - overshoot
                new_pos_x = top_r[0] + 1
        elif p1_snake.direction == 'UP':
            new_pos_y = p1_snake.head_pos[1] + distance
            new_pos_x = p1_snake.head_pos[0]
            if new_pos_y > top_l[1]:
                overshoot = abs(new_pos_y - top_l[1])
                new_pos_x = top_l[0] + overshoot
                new_pos_y = top_l[1] + 1
        elif p1_snake.direction == 'DOWN':
            new_pos_y = p1_snake.head_pos[1] - distance
            new_pos_x = p1_snake.head_pos[0]
            if new_pos_y < bot_r[1]:
                overshoot = abs(new_pos_y - bot_r[1])
                new_pos_x = bot_r[0] - overshoot
                new_pos_y = bot_r[1] - 1
        new_food_pos = [new_pos_x, new_pos_y]
        return new_food_pos

    def check_food_collisions(self, snake, food):
        """Check if the snake has collided with a piece of food."""
        if snake.head_pos[0] == food[0] and \
                snake.head_pos[1] == food[1]:
            snake.eating = True

    def check_wall_collisions(self, snake):
        """Check if the snake has collided with a wall."""
        if snake.head_pos[0] < settings.BOARD_LEFT:
            snake.dead = True
        elif snake.head_pos[0] > settings.BOARD_RIGHT:
            snake.dead = True
        elif snake.head_pos[1] > settings.BOARD_TOP:
            snake.dead = True
        elif snake.head_pos[1] < settings.BOARD_BOTTOM:
            snake.dead = True

    def draw_game(self):
        """Draw all in game objects."""
        arcade.set_background_color(self.theme['bg'])
        self.level.draw(self.score.get_padded_str())
        self.snake_p1.shape_list.draw()
        self.food.shape_list.draw()

    def draw_main_menu(self):
        """Draw all main menu objects."""
        arcade.set_background_color(self.theme['bg'])
        self.main_menu.draw()
        self.snake_p1.shape_list.draw()
        self.food.shape_list.draw()

    def draw_game_over_screen(self):
        """Draw game over objects as an overlay on top of gameplay."""
        self.draw_game()
        self.game_over_screen.draw()

    def on_draw(self):
        """Python Arcade Library method to render the screen."""
        arcade.start_render()

        # Draw the main menu screen.
        if self.game_state == 'main_menu':
            self.draw_main_menu()
        # Draw the game.
        elif self.game_state == 'running':
            self.draw_game()
        # Draw the game when paused.
        elif self.game_state == 'paused':
            self.draw_game()
        # Draw the game over overlay on top of the game.
        elif self.game_state == 'game_over':
            self.draw_game_over_screen()

    def update(self, delta_time):
        """Python Arcade Library method to handle game logic."""
        if self.game_state == 'main_menu':
            self.menu_mode(delta_time)
        elif self.game_state == 'running':
            if self.mode == 'normal':
                self.normal_mode(delta_time)
        elif self.game_state == 'paused':
            if self.mode == 'normal':
                self.normal_mode(delta_time)
        elif self.game_state == 'game_over':
            if self.mode == 'normal':
                self.normal_mode(delta_time)

    def handle_main_menu_input(self, key):
        """Handle input when the main menu is running."""
        if key == arcade.key.ENTER:
            self.setup_game()
            self.game_state = states.GAME_STATES['running']
        elif key == arcade.key.T and not self.pause_title_loop:
            self.snake_p1.last_direction = self.snake_p1.direction
            self.snake_p1.direction = ''
            self.switch_theme(self.get_next_theme())
        elif key == arcade.key.T and self.pause_title_loop:
            self.switch_theme(self.get_next_theme())
        elif key == arcade.key.S:
            self.snake_p1.increase_speed(1)
        elif key == arcade.key.D:
            self.snake_p1.decrease_speed(1)

    def handle_gameplay_input(self, key):
        """Handle input when the game is running."""
        # Get player's desired direction:
        if key == arcade.key.UP:
            self.snake_p1.change_direction = 'UP'
        elif key == arcade.key.DOWN:
            self.snake_p1.change_direction = 'DOWN'
        elif key == arcade.key.LEFT:
            self.snake_p1.change_direction = 'LEFT'
        elif key == arcade.key.RIGHT:
            self.snake_p1.change_direction = 'RIGHT'
        elif key == arcade.key.S:
            self.snake_p1.increase_speed(1)
        elif key == arcade.key.D:
            self.snake_p1.decrease_speed(1)
        # Pause the game.
        elif key == arcade.key.P:
            # Store the current direction.
            self.snake_p1.last_direction = self.snake_p1.direction
            # Stop the snake moving.
            self.snake_p1.direction = ''
            self.game_state = 'paused'
        elif key == arcade.key.T:
            self.switch_theme(self.get_next_theme())

    def handle_pause_input(self, key):
        """Handle input when the game is paused."""
        if key == arcade.key.P:
            # Continue the snake moving in the current direction.
            self.snake_p1.direction = self.snake_p1.last_direction
            self.game_state = states.GAME_STATES['running']
        elif key == arcade.key.T:
            self.switch_theme(self.get_next_theme())

    def handle_game_over_input(self, key):
        """Handle input when the game is over."""
        if key == arcade.key.Y:
            # Restart the game.
            self.setup_game()
            self.game_state = states.GAME_STATES['running']
        elif key == arcade.key.N:
            self.setup_screens()
            self.game_state = states.GAME_STATES['main_menu']
        elif key == arcade.key.T:
            self.switch_theme(self.get_next_theme())

    def on_key_press(self, key, key_modifiers):
        """Python Arcade Library method to handle keyboard input."""
        if self.game_state == 'main_menu':
            self.handle_main_menu_input(key)
        elif self.game_state == 'running':
            self.handle_gameplay_input(key)
        elif self.game_state == 'paused':
            self.handle_pause_input(key)
        elif self.game_state == 'game_over':
            self.handle_game_over_input(key)


class Score():
    """Custom scoring system."""

    def __init__(self, food_points, milestone_amount, score=0):
        """Initialize the scoring system."""
        self.score = score
        self.food_points = food_points
        self.milestone_amount = milestone_amount
        self.milestone_checkpoint = 0

    def add_food_points(self):
        """Add the value of one food item to the score."""
        self.score += self.food_points

    def check_milestone(self):
        """
        Check if a milestone score has been reached.

        Once reached, update the milestone total so that the next check
        can be made accurately.

        Return a Boolean value.
        """
        if self.milestone_amount is not None:
            if self.score - self.milestone_amount == self.milestone_checkpoint:
                self.milestone_checkpoint += self.milestone_amount
                return True
            else:
                return False

    def get_padded_str(self):
        """Get a string for the score padded with leading zeros."""
        padded_score_str = str(self.score).zfill(6)
        return padded_score_str


def main():
    """Run the application."""
    game = Game(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT,
                settings.WINDOW_TITLE)
    game.setup_screens()
    arcade.run()


if __name__ == "__main__":
    main()
