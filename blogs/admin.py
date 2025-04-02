from django.contrib import admin
from .models import Category, BlogPost, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

from django.contrib import admin
from .models import BlogPost

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_approved', 'is_published', 'created_at')
    list_filter = ('is_approved', 'is_published', 'created_at')
    search_fields = ('title', 'content', 'author__username')

    actions = ['approve_blog_posts', 'publish_blog_posts']

    def approve_blog_posts(self, request, queryset):
        queryset.update(is_approved=True)
    approve_blog_posts.short_description = "Approve selected blog posts"

    def publish_blog_posts(self, request, queryset):
        queryset.update(is_published=True)
    publish_blog_posts.short_description = "Publish selected blog posts"

admin.site.register(BlogPost, BlogPostAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('post__title', 'author__username', 'content')
    ordering = ('created_at',)


