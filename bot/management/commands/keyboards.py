from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
# from telegram_bot_pagination import InlineKeyboardPaginator

from bot.models import Post

def menu():
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='Create post', callback_data='create_post'),
        InlineKeyboardButton(text='My posts', callback_data='my_posts'),
        )
    return keyboard


def my_posts(user,page,count,o):
    posts = Post.objects.filter(user=user)
    keyboard = InlineKeyboardMarkup()
    for i in posts[o:page]:
        keyboard.add(
            InlineKeyboardButton(text=i.title, callback_data=i.id)
        )
    if page <=1:
        keyboard.add(
            InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
            InlineKeyboardButton(text='next --->', callback_data='next_page'),
        )
    elif page >1 and page<count:
        keyboard.add(
            InlineKeyboardButton(text='<--- back', callback_data='back_page'),
            InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
            InlineKeyboardButton(text='next --->', callback_data='next_page'),
        )
    elif page>=count:
        keyboard.add(
            InlineKeyboardButton(text='<--- back', callback_data='back_page'),
            InlineKeyboardButton(text=f'{page}/{count}', callback_data=f' '),
        ) 
    return keyboard





def delete_post(id):
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(text='Delete post', callback_data=f'delete {id}'),
    )
    return keyboard



    # def my_posts(user,page=1):
    # posts = Post.objects.filter(user=user)
    # paginator = InlineKeyboardPaginator(
    #     len(posts),
    #     current_page=page,
    #     data_pattern='character#{page}'
    # )
    # for i in posts:
    #     paginator.add_before(
    #         InlineKeyboardButton(text=i.title, callback_data=i.id)
    #         )

    
    # return paginator.markup