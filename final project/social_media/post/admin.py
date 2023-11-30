from django.contrib import admin
from .models import Post, LikePost, Comment
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'title')
    search_fields = ('user', 'title', 'body')
    list_filter = ('user', 'title', 'body', 'created')
    raw_id_fields = ('user',)
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)

admin.site.register(LikePost)
admin.site.register(Comment)
