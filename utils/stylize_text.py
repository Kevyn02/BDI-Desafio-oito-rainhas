# \033[style;text_color;back_color+m
# \033[0;30;40m

# Styles              Text colors       Background colors
# 0 -> Default        30 -> white       40 -> white
# 1 -> Bold           31 -> red         41 -> red
# 4 -> Underline      32 -> green       42 -> green
# 7 -> Negative       33 -> yellow      43 -> yellow
#                     34 -> blue        44 -> blue
#                     35 -> purple      45 -> purple
#                     36 -> cyan        46 -> cyan
#                     37 -> gray        47 -> gray
from enum import Enum


class Styles(Enum):
    NONE = 0
    BOLD = 1
    UNDERLINE = 4
    NEGATIVE = 7


class TextColors(Enum):
    WHITE = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    PURPLE = 35
    CYAN = 36
    GRAY = 37


class BackgroundColors(Enum):
    WHITE = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    PURPLE = 45
    CYAN = 46
    GRAY = 47


def stylize_text(
    content: str,
    style: Styles = Styles.NONE,
    text_color: TextColors = TextColors.WHITE,
    background_color: BackgroundColors = BackgroundColors.WHITE,
) -> str:
    return f"\033[{style.value};{text_color.value};{background_color.value}m{content}\033[m"
