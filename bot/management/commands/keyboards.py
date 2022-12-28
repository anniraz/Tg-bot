from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot_pagination import InlineKeyboardPaginator
paginator = InlineKeyboardPaginator(
        10,
        current_page=1,
        data_pattern='elements#{page}'
    )
from bot.models import Post

def menu():
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='Create post', callback_data='create_post'),
        # InlineKeyboardButton(text='Update post', callback_data='update_post'),
        # InlineKeyboardButton(text='Delete post', callback_data='delete_post'),
        InlineKeyboardButton(text='My posts', callback_data='my_posts'),
        )
    return keyboard


def my_posts(user,page=1):
    posts = Post.objects.filter(user=user)
    paginator = InlineKeyboardPaginator(
        len(posts),
        current_page=page,
        data_pattern='character#{page}'
    )
    for i in posts:
        paginator.add_before(
            InlineKeyboardButton(text=i.title, callback_data=i.id)
            )

    
    return paginator.markup

def delete_post(id):
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='Delete post', callback_data=f'delete {id}'),
    )
    return keyboard