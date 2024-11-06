from aiogram import F, types, Router, Bot
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import os

# ================================
from keybord import ilane
from states import state_
from database import db
# --------------------------------

load_dotenv()
bot = Bot(token=os.getenv('TOKEN_API'))
GROUP_ID = int(os.getenv("GROUP_ID"))


router_group = Router()


async def message_group(user_id, text, topic, ticket):
    inline_group = ilane.create_inline_group(ticket)
    sent_message = await bot.send_message(
        GROUP_ID,
        f"Тема: {topic}\nЗаявка: {text}\nТикет: `{ticket}`\nID юзера: `{user_id}`",
        reply_markup=inline_group,
        parse_mode='Markdown'
    )
    return sent_message.message_id


@router_group.callback_query(F.data.startswith("approve:"))
async def true(callback: types.CallbackQuery):
    ticket = callback.data.split(":")[1]
    original_message_id = callback.message.message_id
    await db.true_application("положительно", ticket)
    await bot.send_message(
        GROUP_ID,
        f"Одобрено",
        reply_to_message_id=original_message_id
    )
    user_id = await db.ticket_user_id(ticket)
    await bot.send_message(user_id, "Ваша заявка была одобрена!")
    await callback.message.edit_reply_markup(reply_markup=None)


@router_group.callback_query(F.data.startswith("reject:"))
async def false(callback: types.CallbackQuery, state: FSMContext):
    ticket = callback.data.split(":")[1]
    original_message_id = callback.message.message_id
    await bot.send_message(GROUP_ID, "Укажите комментарий", reply_to_message_id=original_message_id)
    await state.set_state(state_.false.text)
    await state.update_data(ticket_user_id=ticket)
    await db.true_application("Отрицательно", ticket)
    await callback.message.edit_reply_markup(reply_markup=None)


@router_group.message(state_.false.text)
async def comment(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    text = data['text']
    ticket = data['ticket_user_id']
    user_id = await db.ticket_user_id(ticket)
    await bot.send_message(user_id, f"Ваша заявка была отклонена.\n\nКомментарий: {text}")
    try:
        await bot.send_message(GROUP_ID, "Готово!")
        await state.clear()
    finally:
        pass


@router_group.message(Command('duplicate'))
async def duplicate_ticket(state: FSMContext):
    await bot.send_message(GROUP_ID, "Видите тикет")
    await state.set_state(state_.duplicate_by_ticket.duplicate_by_ticket)


@router_group.message(state_.duplicate_by_ticket.duplicate_by_ticket)
async def process_ticket(message: types.Message, state: FSMContext):
    await state.update_data(duplicate_by_ticket=message.text)
    data = await state.get_data()
    ticket = data['duplicate_by_ticket']
    result = await db.duplicate_ticket(ticket)
    if result:
        pass
    else:
        await bot.send_message(GROUP_ID, f"Тикет {ticket} не найден или не удалось дублировать.")
    await state.clear()
