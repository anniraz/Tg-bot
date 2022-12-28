from django.contrib import admin

from bot.models import User,Post

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=('id','name','username','external_id')

admin.site.register(Post)