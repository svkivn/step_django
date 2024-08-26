from django.contrib import admin


from .models import Post, Category, Tag

# Register your models here.
admin.site.register(Category)
admin.site.register(Tag)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'publish', "status", "category"]
    list_filter = ['created', 'publish', "status"]
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['publish']
