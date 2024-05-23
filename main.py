import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.filters import Command

from env_var import TOKEN
from env_var import test_balance
from env_var import channel_id
from database import init_db, add_or_update_user, get_user_balance



dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    is_premium = message.from_user.is_premium
    add_or_update_user(user_id, is_premium)
    await message.answer(
        f"""congratulations, you are one of those who believed.\nfor your interest you received 200 coins.\ntelegram premium users receive +100 to the base reward.
there is no referral program here.\n27,500,000 coins have been allocated for this distribution.\ncoins that are not collected in time will be burned.\n{html.bold('glhf')}
        """
        )

@dp.message(Command("balance"))
async def echo_balance(message: Message) -> None:
    user_id = message.from_user.id
    user_balance = get_user_balance(user_id)
    await message.answer(f"your balance: {user_balance} $FTK")

@dp.message(Command("premium"))
async def check_premium(message: Message) -> None:
    user_id = message.from_user.id
    is_premium = message.from_user.is_premium
    add_or_update_user(user_id, is_premium)
    if message.from_user.is_premium:
        await message.answer(f"+100. that's fun.")
    else:
        await message.answer(f"oh, i'm sorry. +0")



#################################
from aiogram.exceptions import TelegramBadRequest

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

async def check_subscription(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except TelegramBadRequest:
        return False

@dp.message(Command(commands=['subscription']))
async def subscription(message: Message):
    user_id = message.from_user.id
    is_subscribed = await check_subscription(user_id)
    if is_subscribed:
        await message.answer('yap. get ur tokens')
    else:
        await message.answer('oh, u r not our member:\nt.me/funticketowners')



# @dp.message()
# async def echo_handler(message: Message) -> None:
#     try:
#         # Send a copy of the received message
#         await message.send_copy(chat_id=message.chat.id)
#     except TypeError:
#         # But not all the types is supported to be copied so need to handle it
#         await message.answer("Nice try!")


async def main() -> None:
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())