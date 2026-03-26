from utils.stylize_text import stylize_text, Styles, TextColors, BackgroundColors


def str_question(
    content: str,
):
    message = stylize_text(content, Styles.UNDERLINE, TextColors.CYAN)
    return input(f"{message} ")
