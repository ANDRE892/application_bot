from aiogram import F, types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext


# ================================
from database import db
from states import state_
from keybord import markup
from hendlers.admin import admins_menu
from sending_email import sendding
# --------------------------------

router_user = Router()


@router_user.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    ADMIN_ID = [889158373, 768229612]
    if await db.exists(user_id):
        if user_id in ADMIN_ID:
            await admins_menu(user_id, message)
        else:
            await message.answer("Добро пожаловать!", reply_markup=markup.meny)
    else:
        await message.answer("Видите своё имя и фамилию")
        await state.set_state(state_.start.name_surname)


@router_user.message(state_.start.name_surname)
async def new_user(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    name_surname = message.text
    await message.answer(f"Добро пожаловать {name_surname}")
    await db.new_user(user_id, name_surname)
    await state.clear()


@router_user.message(F.text.in_(["Заявка на канцелярию", "Заявка на ПО", "Заявка на любую тему"]))
async def application(message: types.Message, state: FSMContext):

    topics = {
        "Заявка на канцелярию": "chancellery",
        "Заявка на ПО": "software",
        "Заявка на любую тему": "topic"
    }

    if message.text in topics:
        await message.answer("Напишите свою заявку")
        await state.update_data(topic=topics[message.text])
        await state.set_state(state_.application.application)


@router_user.message(state_.application.application)
async def application_state(message: types.Message, state: FSMContext):
    data = await state.get_data()
    topic = data['topic']
    application_message = message.text
    user_id = message.from_user.id
    await db.applications_save(user_id, application_message, topic)
    await sendding.sending_email(topic, application_message)
    await state.clear()
    await message.answer("Ваша заявка принята на рассмотрение")


@router_user.message(F.text.in_(["История заявок", "Сбор инициатив"]))
async def asd(message: types.Message):
    user_id = message.from_user.id

    if message.text == "История заявок":
        all_application = await db.history_bid(user_id)
        response = "История ваших 30 последних заявок:\n"
        for app in all_application:
            response += f"Заявка: {app['application']}\n" \
                        f"Статус: {app['status']}\n"\
                        f"----------------------------------------\n"
        await message.answer(response)
