import  logging
from aiogram import  types
from aiogram.utils.executor import  start_webhook
from config import  bot, dp, WEBHOOK_URL,  WEBHOOK_PATH, WEBHOOK_HOST, WEBAPP_PORT
from db import  database

async def on_startup(dispatcher):
    await database.connect()
    await bot.set_webhook(WEBHOOK_URL, brop_pending_updares=True)


async def on_shutdown(dispatcher):
    await database.disconnect()
    await bot.delete_webhook()


async def save(user_id, text):
    await database.execute(f"INSER INTO messager(telegram_id, text) "
                           f"VALUES (:telegram_id, :text)", values={'tegram_id': user_id, 'text': text})
                           
                           
async def read(user_id):
    results = await database.fetch_all('SELECT text '
                                        'FROM mrssages '
                                        'Where telegram_id = :telegram_id ',
                                        values={'telegram_id': user_id})
    return [next(result.values()) for result in results]
    
   
@dp.message_handler()
async def echo(message: types.Message):
    await save(message.from_user.id, message.text)
    messages = await read(message.from_user.id)
    await message.answer(messages)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBHOOK_HOST,
        port=WEBAPP_PORT,
    )