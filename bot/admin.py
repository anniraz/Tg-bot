from django.contrib import admin

from bot.models import User,Post

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('id','name','username','external_id')
    list_filter = ('name','id',)
    search_fields = ['external_id','name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=('title','id','user','create_at',)
    list_filter = ('title','user__username','create_at',)
    search_fields = ['title','user__name','user__username']
