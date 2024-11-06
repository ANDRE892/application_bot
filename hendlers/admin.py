from aiogram import F, types, Router
from aiogram.fsm.context import FSMContext

# ================================
from database import db
from keybord import markup
from states import state_
# --------------------------------

ADMIN_ID = [889158373, 768229612]

router_user_admin = Router()


async def admins_menu(user_id: int, message: types.Message):
    if user_id in ADMIN_ID:
        await message.answer("Добро пожаловать в панель администратора", reply_markup=markup.admin_meny)


@router_user_admin.message(F.text == "admin menu")
async def admin_menu(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMIN_ID:
        await message.answer("﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌", reply_markup=markup.admin_meny_all)


@router_user_admin.message(F.text == "Главное меню")
async def admin_menu(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMIN_ID:
        await message.answer("﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌", reply_markup=markup.admin_meny)


@router_user_admin.message(F.text == "Заменить почту")
async def replace_email(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMIN_ID:
        await message.answer("Выберите почту", reply_markup=markup.replace_email)


@router_user_admin.message(F.text.in_(["Канцелярия", "ПО", "Любая тема"]))
async def new_email_pass(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in ADMIN_ID:
        topics = {
            "Канцелярия": "chancellery",
            "ПО": "software",
            "Любая тема": "topic"
        }
        if message.text in topics:
            await message.answer("Email адрес")
            await state.update_data(topic=topics[message.text])
            await state.set_state(state_.email.email)


@router_user_admin.message(state_.email.email)
async def new_email(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in ADMIN_ID:
        await state.update_data(email=message.text)
        await message.answer("Пароль к  (приложению)")
        await state.set_state(state_.email.password)


@router_user_admin.message(state_.email.password)
async def new_pass(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in ADMIN_ID:
        await state.update_data(password=message.text)
        data = await state.get_data()
        password = data.get('password')
        email = data.get('email')
        topic = data.get('topic')
        await message.answer(f"Вы заменили {topic} на {email}")
        print(password, email, topic)
        await db.replacement_email(password, email, topic)
        await state.clear()


@router_user_admin.message(F.text == "Приходящая почта")
async def new_email_incoming(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in ADMIN_ID:
        await message.answer("Ведите приходящую почту")
        await state.set_state(state_.email_incoming.email)


@router_user_admin.message(state_.email_incoming.email)
async def email_incoming(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in ADMIN_ID:
        await state.update_data(email=message.text)
        data = await state.get_data()
        email = data.get('email')
        await message.answer(f"Вы поменяли приходящую почту на {email}")
        await db.incoming_email(email)
        await state.clear()


@router_user_admin.message(F.text == "Просмотр последних 30 заявок")
async def all_applications(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMIN_ID:
        applications = await db.thirty_application()

        if not applications:
            await message.answer("Заявок нет.")
            return

        for i in range(0, len(applications), 5):
            chunk = applications[i:i + 5]
            text = "\n\n".join(
                [
                    f"Заявка от {app['timestamp']}\n"
                    f"Тема: {app['topic']}\n"
                    f"Текст: {app['application']}\n"
                    f"Статус: {app['status']}\n"
                    f"Тикет: `{app['ticket']}`"
                    for app in chunk
                ]
            )
            await message.answer(text, parse_mode="Markdown")


@router_user_admin.message(F.text == "Найти заявку по тикету")
async def find_application(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in ADMIN_ID:
        await message.answer("Ведите тикет")
        await state.set_state(state_.ticket.ticket)


@router_user_admin.message(state_.ticket.ticket)
async def find_application_ticket(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in ADMIN_ID:
        await state.update_data(ticket=message.text)
        data = await state.get_data()
        ticket = data.get('ticket')
        results = await db.find_application(ticket)
        if results:
            for result in results:
                await message.answer(
                    f"id юзера: {result['user_id']}\n"
                    f"Заявка: {result['application']}\n"
                    f"Статус: {result['status']}\n"
                    f"Дата: {result['timestamp']}\n"
                    f"Тема: {result['topic']}"
                )
                await state.clear()
        else:
            await message.answer("Заявка с таким тикетом не найдена.")
            await state.clear()


@router_user_admin.message(F.text == "Просмотр незавершенных заявок")
async def unfinished_application(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMIN_ID:
        results = await db.unfinished_application()

        if results:
            for result in results:
                await message.answer(
                    f"id пользователя: {result['user_id']}\n"
                    f"Заявка: {result['application']}\n"
                    f"Тикет: `{result['ticket']}`\n"
                    f"Дата: {result['timestamp']}\n"
                    f"Тема: {result['topic']}",
                    parse_mode="Markdown"
                )
        else:
            await message.answer("Незавершенных заявок не найдено.")
