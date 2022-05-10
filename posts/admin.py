from django.contrib import admin
from .models import Post, Comment        #,Category,Subscribe,Tag,Notification


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display=['name','slug']
#     prepopulated_fields={'slug':('name',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'post', 'name','email', 'status', 'created']

    class Meta:
        model = Comment


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = ['__str__', 'category','author']
#     search_fields = ['content', 'author__username', 'author__email']
#     prepopulated_fields={'slug':('title',)}

#     class Meta:
#         model = Post


# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     prepopulated_fields={'slug':('name',)}

#     class Meta:
#         model = Tag


# admin.site.register(Notification)
# admin.site.register(Subscribe)
