from textwrap import dedent
from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards.reply import number_button
from keyboards.inline import fac_buttons, applay_buttons
from config import faculties, ADMIN_ID

class Reg(StatesGroup):
    name = State()
    number = State()
    city = State()
    faculty = State()

router = Router()

nomer_reg = 0 #счетчик регестраций

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    user_first_name = message.from_user.first_name
    user_name = message.from_user.username
    text = dedent(f"""
    👋 Здравствуйте, {user_first_name}!
    
    Добро пожаловать в систему регистрации!

    Введите ваше ФИО полностью (например: Иванов Иван Иванович):

    📱 Ваш Telegram: @{user_name}
    """)
    await state.set_state(Reg.name)
    await message.answer(text=text)

@router.message(Reg.name)
async def phone_number(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.number)
    await message.answer(text=dedent(f"""
    📞 Введите свой номер телефона или нажмите на кнопку ниже ☺️
"""), reply_markup=number_button())


@router.message(Reg.number, F.text)
async def phone_number(message: Message, state: FSMContext):
    phone = message.text
    await state.update_data(number=phone)
    await state.set_state(Reg.city)
    await message.answer("Введите свой город, например: Минск", reply_markup=ReplyKeyboardRemove())


@router.message(Reg.number, F.contact)
async def phone_number(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(number=phone)
    await state.set_state(Reg.city)
    await message.answer("Введите свой город, например: Минск", reply_markup=ReplyKeyboardRemove())

@router.message(Reg.city)
async def city(message: Message, state: FSMContext):
    city = message.text
    await state.update_data(city=city)
    await state.set_state(Reg.faculty)
    await message.answer(text="🎓 Выберите факультет из списка ниже 👇", reply_markup=fac_buttons(faculties))

@router.callback_query(Reg.faculty, F.data.startswith("faculty:"))
async def faculty(callback: CallbackQuery, state: FSMContext):
    faculty_name = callback.data.split(":")[1]
    await state.update_data(faculty=faculty_name)
    await callback.answer()
    data = await state.get_data()
    await callback.message.edit_text(
        text=dedent(f"""
        Регестрация завершена!
        👤 Имя: {data.get('name')}
        📞 Номер телефона: {data.get('number')}
        🌆 Город: {data.get('city')}
        🎓 Факультет: {data.get('faculty')}
        
        ❓ Данные указанны верно?
        """),
        reply_markup=applay_buttons()
    )
@router.callback_query(F.data == "no")
async def confirm_no(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Сбрасываем данные...")
    await state.clear()
    await start(callback.message, state)



@router.callback_query(F.data == "yes")
async def confirm_yes(callback: CallbackQuery, state: FSMContext,bot: Bot, ):
    global nomer_reg
    nomer_reg +=1
    await callback.answer()
    data = await state.get_data()
    text = dedent(f"""
    Регестрация №: {nomer_reg}
    👤 Имя: {data.get('name')}
    📞 Номер телефона: {data.get('number')}
    🌆 Город: {data.get('city')}
    🎓 Факультет: {data.get('faculty')}
    🔗 Юзернейм: @{callback.from_user.username or 'нет'}
    🆔 ID: {callback.from_user.id}
    """)
    await bot.send_message(chat_id=ADMIN_ID,text=text)

    await callback.message.edit_text("🎉 Регистрация успешно завершена! Ждем тебя.")
    await state.clear()