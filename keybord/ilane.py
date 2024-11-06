from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_inline_group(ticket):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Одобрить",
                    callback_data=f"approve:{ticket}"
                ),
                InlineKeyboardButton(
                    text="Отказать",
                    callback_data=f"reject:{ticket}"
                )
            ]
        ]
    )
