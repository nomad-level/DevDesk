from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'email', 'date_created']
    list_filter = ['category', 'status', 'date_created']
    search_fields = ['title', 'description', 'email']
    list_editable = ['status']
    date_hierarchy = 'date_created'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'body_preview', 'date_created']
    list_filter = ['date_created']
    search_fields = ['name', 'body', 'post__title']
    date_hierarchy = 'date_created'
    
    def body_preview(self, obj):
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body
    body_preview.short_description = 'Comment'

