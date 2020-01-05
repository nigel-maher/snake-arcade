"""Snake Arcade colours (RGB) & themes."""

# CMYK theme colours.
black = (0, 0, 0)
cyan = (0, 174, 239)
magenta = (236, 0, 140)
yellow = (255, 242, 0)
white = (255, 255, 255)

# Glamour theme colours.
glamour_highlight = (254, 246, 248)
glamour_lowlight = (254, 150, 183)
glamour_pale = (255, 200, 212)
glamour_pink_light = (253, 0, 97)
glamour_pink_mid = (219, 0, 84)
glamour_pink_dark = (184, 0, 71)

# Greyscale theme colours.
greyscale_25 = (191, 191, 191)
greyscale_50 = (128, 128, 128)
greyscale_75 = (64, 64, 64)

# Jungle theme colours.
jungle_green_1 = (0, 255, 145)
jungle_green_2 = (160, 255, 145)
jungle_green_3 = (215, 255, 145)
jungle_purple = (34, 4, 70)
jungle_purple_tint = (89, 67, 116)

# Medals theme colours.
medals_bronze = (238, 96, 52)
medals_gold = (255, 194, 40)
medals_grey = (31, 31, 31)
medals_grey_tint = (87, 87, 87)
medals_silver = (198, 202, 214)

# Mobile theme colours.
mobile_army = (38, 50, 4)
mobile_lime = (167, 204, 0)

# Scuba theme colours.
scuba_blue = (3, 3, 56)
scuba_blue_tint = (66, 66, 106)
scuba_coral_aqua = (0, 213, 198)
scuba_coral_pink = (255, 118, 195)
scuba_coral_orange = (255, 166, 93)

# Colour themes.
cmyk = {'board': black,
        'bg': black,
        'fg': greyscale_75,
        'head': cyan,
        'eye': cyan,
        'pupil': black,
        'snake_body_1': magenta,
        'snake_body_2': yellow,
        'snake_body_3': cyan,
        'snake_border': black,
        'food': white,
        'food_border': black,
        'scoreboard': black,
        'score_text': cyan,
        'score_num': white,
        'game_over': cyan,
        'small_text': white,
        'arcade': white,
        'S': cyan,
        'N': magenta,
        'A': yellow,
        'K': magenta,
        'E': cyan}

glamour = {'board': glamour_pale,
           'bg': glamour_pale,
           'fg': glamour_lowlight,
           'head': glamour_pink_light,
           'eye': glamour_pink_light,
           'pupil': glamour_pale,
           'snake_body_1': glamour_pink_mid,
           'snake_body_2': glamour_pink_dark,
           'snake_body_3': glamour_pink_light,
           'snake_border': glamour_pale,
           'food': glamour_highlight,
           'food_border': glamour_pale,
           'scoreboard': glamour_pale,
           'score_text': glamour_pink_light,
           'score_num': glamour_highlight,
           'game_over': glamour_pink_light,
           'small_text': glamour_pink_dark,
           'arcade': glamour_highlight,
           'S': glamour_pink_light,
           'N': glamour_pink_mid,
           'A': glamour_pink_dark,
           'K': glamour_pink_mid,
           'E': glamour_pink_light}

greyscale = {'board': black,
             'bg': black,
             'fg': greyscale_75,
             'head': white,
             'eye': white,
             'pupil': black,
             'snake_body_1': greyscale_25,
             'snake_body_2': greyscale_50,
             'snake_body_3': white,
             'snake_border': black,
             'food': white,
             'food_border': black,
             'scoreboard': black,
             'score_text': greyscale_25,
             'score_num': white,
             'game_over': greyscale_25,
             'small_text': white,
             'arcade': white,
             'S': white,
             'N': greyscale_25,
             'A': greyscale_50,
             'K': greyscale_25,
             'E': white}

jungle = {'board': jungle_purple,
          'bg': jungle_purple,
          'fg': jungle_purple_tint,
          'head': jungle_green_1,
          'eye': jungle_green_1,
          'pupil': jungle_purple,
          'snake_body_1': jungle_green_2,
          'snake_body_2': jungle_green_3,
          'snake_body_3': jungle_green_1,
          'snake_border': jungle_purple,
          'food': white,
          'food_border': jungle_purple,
          'scoreboard': jungle_purple,
          'score_text': jungle_green_1,
          'score_num': white,
          'game_over': jungle_green_1,
          'small_text': white,
          'arcade': white,
          'S': jungle_green_1,
          'N': jungle_green_2,
          'A': jungle_green_3,
          'K': jungle_green_2,
          'E': jungle_green_1}

medals = {'board': medals_grey,
          'bg': medals_grey,
          'fg': medals_grey_tint,
          'head': medals_gold,
          'eye': medals_gold,
          'pupil': medals_grey,
          'snake_body_1': medals_silver,
          'snake_body_2': medals_bronze,
          'snake_body_3': medals_gold,
          'snake_border': medals_grey,
          'food': white,
          'food_border': medals_grey,
          'scoreboard': medals_grey,
          'score_text': medals_gold,
          'score_num': white,
          'game_over': medals_gold,
          'small_text': white,
          'arcade': white,
          'S': medals_gold,
          'N': medals_silver,
          'A': medals_bronze,
          'K': medals_silver,
          'E': medals_gold}

mobile = {'board': mobile_lime,
          'bg': mobile_lime,
          'fg': mobile_army,
          'head': mobile_army,
          'eye': mobile_army,
          'pupil': mobile_lime,
          'snake_body_1': mobile_army,
          'snake_body_2': mobile_army,
          'snake_body_3': mobile_army,
          'snake_border': mobile_lime,
          'food': mobile_army,
          'food_border': mobile_lime,
          'scoreboard': mobile_army,
          'score_text': mobile_lime,
          'score_num': mobile_lime,
          'game_over': mobile_army,
          'small_text': mobile_army,
          'arcade': mobile_army,
          'S': mobile_army,
          'N': mobile_army,
          'A': mobile_army,
          'K': mobile_army,
          'E': mobile_army}

scuba = {'board': scuba_blue,
         'bg': scuba_blue,
         'fg': scuba_blue_tint,
         'head': scuba_coral_aqua,
         'eye': scuba_coral_aqua,
         'pupil': scuba_blue,
         'snake_body_1': scuba_coral_orange,
         'snake_body_2': scuba_coral_pink,
         'snake_body_3': scuba_coral_aqua,
         'snake_border': scuba_blue,
         'food': white,
         'food_border': scuba_blue,
         'scoreboard': scuba_blue,
         'score_text': scuba_coral_aqua,
         'score_num': white,
         'game_over': scuba_coral_aqua,
         'small_text': white,
         'arcade': white,
         'S': scuba_coral_aqua,
         'N': scuba_coral_orange,
         'A': scuba_coral_pink,
         'K': scuba_coral_orange,
         'E': scuba_coral_aqua}

# List of colour themes, ordered for selection in application.
themes = [jungle, scuba, medals, cmyk, greyscale, glamour, mobile]
