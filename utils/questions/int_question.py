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
    info_message = stylize_text(content, Styles.UNDERLINE, TextColors.CYAN)
    danger_message = stylize_text(
        "" if invalid_message is None or invalid_message == "" else invalid_message,
        Styles.UNDERLINE,
        TextColors.RED,
    )
    value = input(f"{info_message} ")

    while True:
        if value is None or value == "":
            return default_value

        if allowed_values is None:
            return int(value)

        if isinstance(allowed_values, dict):
            try:
                num = float(value)
            except ValueError:
                value = input(f"{danger_message} {info_message} ")
                continue

            min_v = allowed_values.get("min")
            max_v = allowed_values.get("max")

            is_the_value_lower_than_min = min_v is not None and num < min_v
            is_the_value_greater_than_max = max_v is not None and num > max_v

            if is_the_value_lower_than_min or is_the_value_greater_than_max:
                value = input(f"{danger_message} {info_message} ")
                continue

            return int(num)

        if value in allowed_values:
            return int(value)

        value = input(f"{danger_message} {info_message} ")
