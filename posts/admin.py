from django.contrib import admin
from .models import Post, Comment,Category

class CategoryAdmin(admin.ModelAdmin):
    list_display=['name','slug']
    prepopulated_fields={'slug':('name',)}

class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'post', 'user', 'status', 'created']

    class Meta:
        model = Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'category','author']
    search_fields = ['content', 'author__username', 'author__email']
    prepopulated_fields={'slug':('title',)}

    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category,CategoryAdmin)
