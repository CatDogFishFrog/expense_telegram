from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os
from table_in_terminal import Table

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

'''****************************КЛИЕНТСКАЯ ЧАСТЬ*****************************'''

@dp.message_handler(commands=['start', 'help'])
async def command_start(message:types.Message):
    await bot.send_message(message.from_user.id, 'Команда "start" либл "help"')
    



@dp.message_handler(commands=['print'])
async def command_start(message:types.Message):
    table = Table.table_from_database(for_telegram=True, colomns_to_print=['Дата', 'Ціна', 'Назва'], sort_key='Дата')
    await bot.send_message(message.from_user.id, table, parse_mode="HTML")
    bot.send_message()



@dp.message_handler()
async def send_message(message:types.Message):
    await message.answer('Сколько будет 2 + 2?')
    if message.text == '4':
        await message.answer('Правильно')
    else:
        await message.answer('Не правильно')
        

    


'''*****************************АДМИНСКАЯ ЧАСТЬ*****************************'''

'''******************************ОБЩАЯ ЧАСТЬ********************************'''

executor.start_polling(dp, skip_updates=True)