import functools

from aiogram import Bot, Dispatcher, executor, types
import time

token = '1920835884:AAHW8pRl3AhVs7x3mJYue_HhpDvmGVNAQ2c'
bot = Bot(token)
dp = Dispatcher(bot)
password = '1234567890'


class User:
    stage = 0
    chat_id = 0
    user_password = 0
    message = []

    def __init__(self):
        self.stage = 0
        self.chat_id = 0
        self.user_password = 0


class Users:
    users = {}

    def get(self, message: types.Message):
        if not message.from_user.id in self.users.keys():
            self.users[message.from_user.id] = User()
        return self.users[message.from_user.id]


users = Users()


async def check(func):
    async def decorator(message: types.Message):
        if message.chat.id != message.from_user.id:
            return
        return await func(message)
    return decorator


@dp.message_handler(commands=['start'])
async def say_hi(message: types.Message):
    user = users.get(message)
    user.stage = 1
    user.chat_id = message.chat.id
    await bot.send_message(chat_id=message.from_user.id, text='це бот для спаму в чаті)')


@check
@dp.message_handler(commands=['try'])
async def try_pass(message: types.Message):
    user = users.get(message)
    if user.stage != 1:
        return
    user.user_password = message.text[message.text.find(' ') + 1:]
    text = 'Доступ відкрито' if user.user_password == password else 'ні'
    if user.user_password == password:
        user.stage = 2
    await bot.send_message(text=text, chat_id=message.chat.id)


@dp.message_handler(content_types=[types.ContentType.STICKER])
async def set_info(message: types.Message):
    user = users.get(message)
    if user.stage != 2:
        return
    func = functools.partial(bot.send_sticker, user.chat_id, message.sticker.file_id)
    user.message.append(func)


@dp.message_handler(content_types=[types.ContentType.ANIMATION])
async def set_ino(message: types.Message):
    user = users.get(message)
    print(message)
    if user.stage != 2:
        return
    func = functools.partial(bot.send_animation, user.chat_id, message.animation.file_id)
    user.message.append(func)


@check
@dp.message_handler(commands=['spam_start'])
async def start_spam(message: types.Message):
    user = users.get(message)
    if user.stage != 2:
        return
    print(user.message)
    user.stage = 3
    for i in range(10000):
        for j in user.message:
            time.sleep(3)
            try:
                await j()
            except Exception:
                pass


if __name__ == '__main__':
    executor.start_polling(dp)