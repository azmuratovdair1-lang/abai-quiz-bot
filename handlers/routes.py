from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile
)
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from handlers.database import save_user_score, get_top_users

router = Router()


def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мероприятия"), KeyboardButton(text="Рейтинг")],
            [KeyboardButton(text="Список учеников 11 а класса"), KeyboardButton(text="Список учеников 11 ае класса")]
        ],
        resize_keyboard=True
    )

    return keyboard


@router.message(Command("start"))
async def start(message:Message):
    photo = FSInputFile("photo6.jpeg")

    await message.answer_photo(photo=photo)
    await message.answer("Привет! Гимназист, я бот для тебя\n\nНапиши /help для помощи")


@router.message(F.text.lower() == "список учеников 11 ае класса")
async def show_students_11ae(message:Message):
    students_text = (
        "📋список учинеков 11 ае класса\n"
        "1.Ажмуратов Даир\n"
        "2.Хамидолла Жандос\n"
        "3.Серікқали Ералы\n"
        "4.Ғұбайдолла Ерасыл\n"
        "5.Данияр Ақбота\n"
        "6.Жұмағали Амир\n"
        "7.Ерланұлы Иманай\n"
        "8.Мұрат Құралай\n"
        "9.Закария Айзере\n"
        "10.Бақтыгерей Ерасыл\n"
        "11.Хабен Камшат\n"
        "12.Қалимат Қарақат\n"
    )
    await message.answer(students_text)


@router.message(Command("help"))
async def help(message:Message):
    await message.answer("Команды:\n/start - запустить бот\n/help - список команд\n/about - про нас", reply_markup=get_main_reply_keyboard())


@router.message(F.text.lower() == "список учеников 11 а класса")
async def show_students_11a(message: Message):
    students_text = (
        "📋список учинеков 11 а класса\n"
        "1.Салық Еркебұлан\n"
        "2.Базарбай Нұрдаулет\n"
        "3.Базарбай Ердаулет\n"
        "4.Өмірғали Нұркен\n"
        "5.Джумагазиев Темирлан\n"
        "6.Амидуллаева Динара\n"
        "7.Асылбекқызы Мөлдір\n"
        "8.Зинеш Құндыз\n"
        "9.Қадырғали Жансая\n"
        "10.Қайрат Айару\n"
        "11.Қанат Арайлым\n"
        "12.Мұрат Айназым\n"
        "13.Орынбасар Гүлім\n"
        "14.Өрес Айнара\n"
        "15.Саин Гүлжайна\n"
        "16.Тлекова Дильназ\n"
        "17.Тілекбай Нұрсила\n"
    )
    await message.answer(students_text)


@router.message(Command("about"))
async def about(message: Message):
    await message.answer("Это информация о нашем боте🤖:\n"
                         "💻Наш Telegram-бот разработан с использованием языка программирования Python и библиотеки Aiogram.\n"
                         "🎯Главная цель проекта — помочь ученикам школы-гимназии получать необходимую информацию, быть в курсе школьных мероприятий, олимпиад и других важных событий.\n"
                         "👁️Бот предназначен не только для учащихся, но и для учителей, а также всех, кто связан с нашей школой-гимназией.\n"
                         "🎣Мы стремимся сделать школьную жизнь удобнее, интереснее и доступнее для каждого! 🎓\n\n\n"
                         "Создатель:🧑‍💻Ажмуратов Даир ученик 11 ае класса\n"
                         "Автор идеи:👩‍🏫Алипова Гульмаржан зауч по воспитанию"
                         )


@router.message(F.text.lower() == "мероприятия")
async def show_quiz(message: Message, state: FSMContext):
    await state.update_data(score=0)
    await state.update_data(score=0)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="Да ✅(+10)", callback_data="q1_yes"),
            InlineKeyboardButton(text="Нет ❌(0)", callback_data="q1_no")
            ]
        ]
    )

    await message.answer("Участвовал ли ты в Тоғызқұмалақтан сайыс?", reply_markup=keyboard)
    await state.set_state(QuizStates.question_1)




class QuizStates(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    question_8 = State()
    question_9 = State()
    question_10 = State()

@router.callback_query(QuizStates.question_1, F.data.startswith("q1_"))
async def proccess_question_1(callback: CallbackQuery, state: FSMContext):
    if callback.data == "q1_yes":
        data = await state.get_data()
        current_score = data.get("score", 0)
        await state.update_data(score=current_score + 10)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Да ✅(+10)", callback_data="q2_yes"),
                    InlineKeyboardButton(text="Нет ❌(0)", callback_data="q2_no")
                ]
            ]
        )

        await callback.message.edit_text(
            "Участвовал ли ты в Күзгі асар жәрмеңкесі?",
            reply_markup=keyboard
        )

        await state.set_state(QuizStates.question_2)
        await callback.answer()

@router.callback_query(QuizStates.question_10, F.data.startswith("q10"))
async def proccess_question_final_question  (callback: CallbackQuery, state: FSMContext):
    if callback.data == "q10_yes":
        data = await state.get_data()
        await state.update_data(score=data.get("score", 0)+10)

    final_data = await state.get_data()
    total_score = final_data.get("score", 0)
    user_id = callback.from_user.id
    full_name = callback.from_user.full_name or "ученик"
    save_user_score(user_id, full_name, total_score)

    await callback.message.answer(
        f"Опрос успешно завершен!🥳🥳🥳\n\n"
        f"Твой итоговый результат: {total_score} баллов💯\n"
        f"Твои посещаемые мероприятия записаны и добавлен в общий рейтинг!📈"
    )

    await state.clear()
    await callback.answer()


@router.callback_query(F.data.startswith("q"))
async def proccess_any_question(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    if "_yes" in callback.data:
        data = await state.get_data()
        await state.update_data(score=data.get("score", 0)+10)

    next_steps = {
        QuizStates.question_1.state: (QuizStates.question_2, "Участвовал ли ты в Күзгі асар жәрмеңкесі?", "q2"),
        QuizStates.question_2.state: (QuizStates.question_3, "Участвовал ли ты в Қыздар арасында 'Былғары доп'?", "q3"),
        QuizStates.question_3.state: (QuizStates.question_4, "Участвовал ли ты в 'Адал азамат' эссе жазу?", "q4"),
        QuizStates.question_4.state: (QuizStates.question_5, "Участвовал ли ты в 'Күзгі демалыс кітаппен'?", "q5"),
        QuizStates.question_5.state: (QuizStates.question_6, "Участвовал ли ты в 'Республикам-мақтанышым'?", "q6"),
        QuizStates.question_6.state: (QuizStates.question_7, "Участвовал ли ты в Мектеп Президентін сайлау?", "q7"),
        QuizStates.question_7.state: (QuizStates.question_8, "Участвовал ли ты в 'Таза Қазақстан'?", "q8"),
        QuizStates.question_8.state: (QuizStates.question_9, "Участвовал ли ты в 'Менің Отаным-Қазақстан'сурет көрмесі?", "q9"),
        QuizStates.question_9.state: (QuizStates.question_10, "Участвовал ли ты в Шахматтан сайыс?", "q10"),
    }

    if current_state in next_steps:
        next_state, next_text, q_prefix = next_steps[current_state]

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Да ✅(+10)", callback_data=f"{q_prefix}_yes"),
                    InlineKeyboardButton(text="Нет ❌(0)", callback_data=f"{q_prefix}_no"),
                ]
            ]
        )

        await callback.message.edit_text(next_text, reply_markup=keyboard)
        await state.set_state(next_state)

    await callback.answer()


@router.message(F.text.lower() == "рейтинг" )
async def show_rating(message: Message):
    top_users = get_top_users()

    if not top_users:
        await message.answer("Пока еще никто не прошел опрос,будь первым")
        return

    text = "Общий рейтинг гимназистов:\n\n"
    for index, (name, score) in enumerate(top_users, start=1):
        medal = "🥇" if index == 1 else "🥈" if index == 2 else "🥉" if index == 3 else f"{index}"
        text += f"{medal} {name} - {score} баллов\n"

    await message.answer(text)
