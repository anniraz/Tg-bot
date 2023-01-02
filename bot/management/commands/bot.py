from django.core.management.base import BaseCommand
from django.conf import settings
from telebot import TeleBot

from bot.models import User,Post
from bot.management.commands.keyboards import menu,my_posts,delete_post
from bot.management.commands.text import my_post_text


bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


class Command(BaseCommand):
    help = "Zarina's Telegram Bot"

    def handle(self, *args, **kwargs):
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()							
        bot.infinity_polling()	




@bot.message_handler(commands=['start'])
def start(message): 
    # create user or get user
    User.objects.get_or_create(
        external_id=message.chat.id,
        username=message.from_user.username,
        name=message.from_user.first_name,
    )
    bot.send_message(message.chat.id,'hi  (^-^)/',reply_markup=menu())

# for pagination
page=1  #for how many posts will show there
count=0 #posts count
o=0 #auxiliary variable

@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    global count
    global page
    global o

    count=len(Post.objects.filter(user=User.objects.get(external_id=call.message.chat.id)))
    chat_id = call.message.chat.id

    #for  create posts
    if call.data == 'create_post':
        bot.send_message(call.message.chat.id, "write your post's title:")
        bot.register_next_step_handler(call.message, get_title)


    if call.data == 'my_posts':
        # List of your posts
        bot.send_message(chat_id=chat_id, text='<b>My Posts</b>',
                               reply_markup=my_posts(user=User.objects.get(external_id=call.message.chat.id),count=count,page=page,o=o), parse_mode='HTML')
    
    # for pagination
    if call.data == 'next_page':
        if page < count:
            o=page
            page = page + 1
            bot.delete_message(call.message.chat.id, call.message.message_id)
            call.data='my_posts'
            return callbacks(call)


    if call.data == 'back_page':
        if page > 1:
            page=o
            o = page - 1
            bot.delete_message(call.message.chat.id, call.message.message_id)
            call.data='my_posts'
            return callbacks(call)
    # # # #

    if call.data in [str(i.id) for i in Post.objects.filter(user=User.objects.get(external_id=call.message.chat.id))]:

        # for a detailed view of the post

        post=Post.objects.get(id=call.data)
        text=my_post_text.format(post.title,post.text)
        if not post.image :
            bot.send_message(call.message.chat.id, text, parse_mode='HTML',reply_markup=delete_post(post.id))
        else:
            bot.send_photo(chat_id=chat_id,photo=open(f'media/{post.image}', 'rb'),caption=text, parse_mode='HTML',reply_markup=delete_post(post.id))
            


    if call.data in [f'delete {i.id}' for i in Post.objects.filter(user=User.objects.get(external_id=call.message.chat.id))]:
        # to delete a post
        id=call.data.split(' ')[-1]
        try:
            post=Post.objects.get(id=id)
            post.delete()
            bot.send_message(call.message.chat.id, 'DELETED')
        except:
            bot.send_message(call.message.chat.id, 'NOT REMOVED')



############## for creating post############################################################
title = ''
text = ''
photo=''

def get_title(message):
    global title
    title=message.text
    bot.send_message(message.from_user.id, "photo:")
    bot.register_next_step_handler(message, get_photo)

def get_photo(message):
    global photo
    try:    
        fileID = message.photo[-1].file_id   
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f"media/posts/img{file_info.file_unique_id}.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.from_user.id, "write your post's text:")
        photo=f"posts/img{file_info.file_unique_id}.jpg"
    except:
        bot.send_message(message.from_user.id, "it's not a photo!")
        bot.send_message(message.from_user.id, "write your post's text:")
    bot.register_next_step_handler(message, get_text)

def get_text(message):
    global text
    text=message.text
    bot.send_message(message.from_user.id, 'post title: '+title+'\ntext: '+text+'\nkeep? (yes/no)')
    bot.register_next_step_handler(message, create_post)

def create_post(message):
    u= User.objects.get(external_id=message.chat.id)
    if message.text=='yes':
        try:
            Post.objects.create(
                user=u,
                image=photo,
                title=title,
                text=text
            )
            bot.send_message(message.from_user.id, 'CREATED')
        except Exception as ex:
            bot.send_message(message.from_user.id, f'FAILED {ex}')
    else:
        bot.send_message(message.from_user.id, 'refused to save')

# ######################################################################################



@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id,'привет (^-^)/  \nнажми на /start')
