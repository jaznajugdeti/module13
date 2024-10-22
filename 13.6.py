from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Необходимо дополнить код предыдущей задачи, чтобы при нажатии на кнопку 'Рассчитать' присылалась Inline-клавиатруа.
# Создайте клавиатуру InlineKeyboardMarkup с 2 кнопками InlineKeyboardButton:
# С текстом 'Рассчитать норму калорий' и callback_data='calories'
# С текстом 'Формулы расчёта' и callback_data='formulas'
api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
Inline_kb = InlineKeyboardMarkup(resize_keyboard=True)
Inline_button = InlineKeyboardButton(text= 'Рассчитать норму калорий', callback_data='calories')
Inline_button2 = InlineKeyboardButton(text= 'Формулы расчёта', callback_data='formulas' )
Inline_kb.add(Inline_button)
Inline_kb.add(Inline_button2)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button2 = KeyboardButton(text= 'Информация')
button = KeyboardButton(text= 'Рассчитать')
kb.add(button2)
kb.add(button)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Информация о боте!')

    # Создайте новую функцию main_menu(message), которая:
    # Будет обёрнута в декоратор message_handler, срабатывающий при передаче текста 'Рассчитать'.
    # Сама функция будет присылать ранее созданное Inline меню и текст 'Выберите опцию:'
@dp.message_handler(text= 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup = Inline_kb)
# Создайте новую функцию get_formulas(call), которая:
# Будет обёрнута в декоратор callback_query_handler, который будет реагировать на текст 'formulas'.
# Будет присылать сообщение с формулой Миффлина-Сан Жеора.
@dp.callback_query_handler(text= 'formulas')
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора для мужчин:\n'
                            '10 х вес(кг) + 6.25 х рост(см) - 5 х возраст + 5\n'
                              'Формула Миффлина-Сан Жеора для женщин:\n'
                              '10 х вес(кг) + 6.25 х рост(см) - 5 х возраст -161')
    await call.answer()
# Измените функцию set_age и декоратор для неё:
# Декоратор смените на callback_query_handler, который будет реагировать на текст 'calories'.
# Теперь функция принимает не message, а call. Доступ к сообщению будет следующим - call.message.
@dp.callback_query_handler(text= 'calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state= UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state= UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = float(data['age'])
    growth = float(data['growth'])
    weight = float(data['weight'])

    man = 10 * weight + 6.25 * growth - 5 * age + 5
    woman = 10 * weight + 6.25 * growth - 5 * age - 161

    await UserState.weight.set()
    await message.answer(f"Норма калорий для мужчин: {man}")
    await message.answer(f"Норма калорий для женщин: {woman}")

    await state.finish()

    # По итогу получится следующий алгоритм:
    # Вводится команда /start
    # На эту команду присылается обычное меню: 'Рассчитать' и 'Информация'.
    # В ответ на кнопку 'Рассчитать' присылается Inline меню: 'Рассчитать норму калорий' и 'Формулы расчёта'
    # По Inline кнопке 'Формулы расчёта' присылается сообщение с формулой.
    # По Inline кнопке 'Рассчитать норму калорий' начинает работать машина состояний по цепочке.
    # Необходимо дополнить код предыдущей задачи,
    # чтобы вопросы о параметрах тела для расчёта калорий выдавались по нажатию кнопки.
    # Измените massage_handler для функции set_age.

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)