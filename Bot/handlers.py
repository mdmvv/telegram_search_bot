from aiogram import types
from loader import bot
from loader import dp
from scraping import search
from keyboards import create_keyboard


search_data = []  # Array that contains the data of all searches for the current session


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    Handler for the '/start' and '/help' commands
    """
    await bot.send_message(message.chat.id, "Привіт! Я бот, який допоможе знайти канали із заданою назвою. Надішліть мені назву, і я знайду відповідні канали.")


@dp.message_handler()
async def send_channel_list(message: types.Message):
    """
    Handler for processing user messages
    """
    # Search channels based on user message and sending the channel list
    channels = search(message.text)
    keyboard = create_keyboard(channels)
    sent_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Список каналів за вашим запитом:",
        reply_to_message_id=message.message_id,
        reply_markup=keyboard
    )

    # Save search
    current_search = {'chat_id': message.chat.id, 'message_id': sent_message.message_id, 'channels': channels}
    search_data.append(current_search)


@dp.callback_query_handler(lambda query: query.data.startswith('page:'))
async def handle_page(callback_query: types.CallbackQuery):
    """
    Handler for processing pagination button clicks
    """
    chat_id = callback_query.message.chat.id
    message_id = callback_query.message.message_id

    # Selecting the corresponding channels in search_data based on chat_id and message_id
    channels = []
    for item in search_data:
        if item['chat_id'] == chat_id and item['message_id'] == message_id:
            channels = item['channels']
            break

    # Creating updated keyboard with the new page
    page = int(callback_query.data.split(':')[1])
    keyboard = create_keyboard(channels, page)

    # Sending the updated channel list to the user
    await bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=keyboard
    )
