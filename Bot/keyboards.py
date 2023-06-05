import math
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_keyboard(channels, page=1):
    """
    Function that creates an inline keyboard with paginated channel buttons
    """
    # Creating a keyboard
    keyboard = InlineKeyboardMarkup(row_width=3)
    items_per_page = 10
    n_pages = math.ceil(len(channels) / items_per_page)

    # Extract channels of current page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    page_channels = channels[start_index:end_index]

    # Creating buttons for the channel list
    for channel in page_channels:
        channel_button = InlineKeyboardButton(text=channel['name'], url=f'https://t.me/{channel["username"][1:]}')
        keyboard.add(channel_button)

    # Creating navigation buttons for page switching
    if page > 1:
        prev_page_button = InlineKeyboardButton(text='⬅️️', callback_data=f'page:{page-1}')
    else:
        prev_page_button = InlineKeyboardButton(text='️️', callback_data='none')
    page_button = InlineKeyboardButton(text=f'{page} / {n_pages}', callback_data='none')
    if page < n_pages:
        next_page_button = InlineKeyboardButton(text='➡️', callback_data=f'page:{page+1}')
    else:
        next_page_button = InlineKeyboardButton(text='️️', callback_data='none')
    keyboard.add(prev_page_button, page_button, next_page_button)

    return keyboard
