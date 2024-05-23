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

from env_var import TOKEN, test_balance, channel_id
from database import init_db, add_or_update_user, get_user_balance, update_user_tasks_and_coins, set_initial_coins_received, has_user_received_initial_coins

dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id
    is_premium = message.from_user.is_premium
    add_or_update_user(user_id, is_premium)
    is_subscribed = await check_subscription(user_id)
    if is_subscribed:
        if not has_user_received_initial_coins(user_id):
            update_user_tasks_and_coins(user_id, 1, 200)
            set_initial_coins_received(user_id)
            await message.answer(
                f"""congratulations, you are one of those who believed.\nfor your interest you received 200 tickets\nthere is no referral program here.\n{html.bold('glhf')}"""
            )
        else:
            await message.answer("You have already received your initial 200 coins.")
    else:
        await message.answer("nah, subscribe to the channel first.\nt.me/funticketowners")
        await message.answer("when you're done, check your status:\n/subscription")

@dp.message(Command("balance"))
async def echo_balance(message: Message) -> None:
    user_id = message.from_user.id
    user_balance = get_user_balance(user_id)
    await message.answer(f"your balance: {user_balance} $FTK")

# @dp.message(Command("premium"))
# async def check_premium(message: Message) -> None:
#     user_id = message.from_user.id
#     is_premium = message.from_user.is_premium
#     add_or_update_user(user_id, is_premium)
#     if message.from_user.is_premium:
#         await message.answer(f"+100. that's fun.")
#     else:
#         await message.answer(f"oh, i'm sorry. +0")

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
        if not has_user_received_initial_coins(user_id):
            update_user_tasks_and_coins(user_id, 1, 200)
            set_initial_coins_received(user_id)
            await message.answer('yap. get ur tokens')
        else:
            await message.answer("You have already received your initial 200 coins.")
    else:
        await message.answer('oh, u r not our member:\nt.me/funticketowners')

async def main() -> None:
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
