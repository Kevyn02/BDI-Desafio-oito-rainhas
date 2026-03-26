from utils.stylize_text import stylize_text, Styles, TextColors, BackgroundColors
from typing import Iterable, TypedDict


class Range(TypedDict, total=False):
    min: int
    max: int


def int_question(
    content: str,
    allowed_values: Iterable[str | int] | Range | None = None,
    default_value: int | None = None,
    invalid_message: str | None = None,
):
    message = stylize_text(content, Styles.UNDERLINE, TextColors.CYAN)
    value = input(f"{message} ")

    while True:
        if value is None or value == "":
            return default_value

        if allowed_values is None:
            return int(value)

        if isinstance(allowed_values, dict):
            try:
                num = float(value)
            except ValueError:
                value = input(
                    f"{stylize_text(invalid_message, Styles.UNDERLINE, TextColors.RED)} "
                )
                continue

            min_v = allowed_values.get("min")
            max_v = allowed_values.get("max")

            if min_v is not None and num < min_v:
                value = input(
                    f"{stylize_text(invalid_message, Styles.UNDERLINE, TextColors.RED)} "
                )
                continue

            if max_v is not None and num > max_v:
                value = input(
                    f"{stylize_text(invalid_message, Styles.UNDERLINE, TextColors.RED)} "
                )
                continue

            return int(num)

        if value in allowed_values:
            return int(value)

        value = stylize_text(invalid_message, Styles.UNDERLINE, TextColors.RED)
