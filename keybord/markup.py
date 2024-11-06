from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


meny = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Заявка на канцелярию'),
            KeyboardButton(text='Заявка на ПО')
        ],
        [
            KeyboardButton(text='Заявка на любую тему'),
            KeyboardButton(text='Сбор инициатив')
        ],
        [
            KeyboardButton(text='История заявок'),
        ]
    ], resize_keyboard=True
)

admin_meny = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Заявка на канцелярию'),
            KeyboardButton(text='Заявка на ПО')
        ],
        [
            KeyboardButton(text='Заявка на любую тему'),
            KeyboardButton(text='Сбор инициатив')
        ],
        [
            KeyboardButton(text='История заявок'),
            KeyboardButton(text='admin menu')
        ]
    ], resize_keyboard=True
)


admin_meny_all = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Заменить почту'),
            KeyboardButton(text='Найти заявку по тикету')
        ],
        [
            KeyboardButton(text='Просмотр незавершенных заявок'),
            KeyboardButton(text='Просмотр последних 30 заявок')
        ],
        [
            KeyboardButton(text='Главное меню')
        ]
    ], resize_keyboard=True
)

replace_email = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Канцелярия'),
            KeyboardButton(text='ПО')
        ],
        [
            KeyboardButton(text='Любая тема'),
            KeyboardButton(text='Приходящая почта')
        ],
        [
            KeyboardButton(text='Главное меню')
        ]
    ], resize_keyboard=True
)
