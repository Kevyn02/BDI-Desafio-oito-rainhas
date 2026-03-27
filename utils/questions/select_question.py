from utils.stylize_text import stylize_text, Styles, TextColors, BackgroundColors
from typing import Iterable


def select_question(
    content: str,
    allowed_values: Iterable[str | int] | None = None,
    default_value: str | int | None = None,
    invalid_message: str | None = None,
):
    info_message = stylize_text(content, Styles.UNDERLINE, TextColors.CYAN)
    danger_message = stylize_text(
        "" if invalid_message is None or invalid_message == "" else invalid_message,
        Styles.UNDERLINE,
        TextColors.RED,
    )
    value = input(f"{info_message} ").strip().lower()

    while True:
        if value is None or value == "":
            return default_value

        if allowed_values is None:
            return value

        if value in [str(allowed_value).lower() for allowed_value in allowed_values]:
            return value

        value = input(f"{danger_message} {info_message} ").strip().lower()
