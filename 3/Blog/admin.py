from django.contrib import admin
from .models import *


class BlogUserAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return obj is not None and request.user == obj.user

    def has_delete_permission(self, request, obj=None):
        return obj is not None and request.user == obj.user

    def has_add_permission(self, request):
        return request.user.is_superuser


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "user"]
    search_fields = ["title", "content"]
    list_filter = ["creation_date"]

    def has_view_permission(self, request, obj=None):
        if obj is None:
            return True

        blocked = Block.objects.filter(blocker=obj.user,
                                       blocked=BlogUser.objects.filter(user=request.user).first()).first()

        return blocked is None

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or (obj is not None and request.user == obj.user)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser or (obj is not None and request.user == obj.user)

    def has_add_permission(self, request):
        return True


class CommentAdmin(admin.ModelAdmin):
    list_display = ["content", "creation_date"]

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or (obj is not None and request.user == obj.user)

    def has_delete_permission(self, request, obj=None):
        return (
                request.user.is_superuser or
                obj.post.user == request.user or
                (obj is not None and request.user == obj.user)
        )

    def has_add_permission(self, request):
        return True


class BlockedAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return obj is not None and obj.blocker == request.user

    def has_delete_permission(self, request, obj=None):
        return obj is not None and obj.blocker == request.user

    def has_add_permission(self, request):
        return True


admin.site.register(BlogUser, BlogUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Block, BlockedAdmin)
