from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# было на лекции!!!!
# @dp.message_handler()
# async  def all_messages(message):
#     print('Мы получили сообщение')

# @dp.message_handler(text= ['urban', 'ff'])
# async def urban_message(message):
#     print('Urban message')
#
# @dp.message_handler(commands=['start'])
# async def start_message(message):
#     print('Start message')
# homework
# К коду из подготовительного видео напишите две асинхронные функции:
# start(message) - печатает строку в консоли 'Привет! Я бот помогающий твоему здоровью.' . Запускается только когда
# написана команда '/start' в чате с ботом. (используйте соответствующий декоратор)
# all_massages(message) - печатает строку в консоли 'Введите команду /start, чтобы начать общение.'.
# Запускается при любом обращении не описанном ранее. (используйте соответствующий декоратор)
@dp.message_handler(commands=['start'])
async def start(message):
    print('Привет! Я бот помогающий твоему здоровью.')
@dp.message_handler()
async def all_massages(message):
    print('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)