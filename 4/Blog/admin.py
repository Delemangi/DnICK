from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest

from .models import BlogUser, Post, Comment, File, Block


class BlogUserAdmin(admin.ModelAdmin):
    def has_view_permission(self, request: HttpRequest, obj: BlogUser | None = None) -> bool:
        return True

    def has_change_permission(self, request: HttpRequest, obj: BlogUser | None = None) -> bool:
        return obj is not None and request.user == obj.user

    def has_delete_permission(self, request: HttpRequest, obj: BlogUser | None = None) -> bool:
        return obj is not None and request.user == obj.user

    def has_add_permission(self, request: HttpRequest) -> bool:
        return request.user.is_superuser


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "user"]
    search_fields = ["title", "content"]
    list_filter = ["creation_date"]
    exclude = ["user"]

    def has_view_permission(self, request: HttpRequest, obj: Post | None = None) -> bool:
        return request.user.is_superuser or (obj is not None and not Block.objects.filter(blocker__user=obj.user.user,
                                                                                          blocked__user=request.user).exists())

    def has_change_permission(self, request: HttpRequest, obj: Post | None = None) -> bool:
        return request.user.is_superuser or (obj is not None and request.user == obj.user.user)

    def has_delete_permission(self, request: HttpRequest, obj: Post | None = None) -> bool:
        return request.user.is_superuser or (obj is not None and request.user == obj.user.user)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return True

    def save_model(self, request: HttpRequest, obj: Post | None, form: ModelForm, change: bool) -> None:
        if obj is not None:
            obj.user = BlogUser.objects.get(user=request.user)

        super().save_model(request, obj, form, change)


class CommentAdmin(admin.ModelAdmin):
    list_display = ["content", "creation_date"]
    exclude = ["user"]

    def has_view_permission(self, request: HttpRequest, obj: Comment | None = None) -> bool:
        return request.user.is_superuser or (
                obj is not None and not Block.objects.filter(blocker__user=obj.post.user.user,
                                                             blocked__user=request.user).exists())

    def has_change_permission(self, request: HttpRequest, obj: Comment | None = None) -> bool:
        return request.user.is_superuser or (obj is not None and request.user == obj.user.user)

    def has_delete_permission(self, request: HttpRequest, obj: Comment | None = None) -> bool:
        return request.user.is_superuser or (
                obj is not None and (request.user == obj.post.user or request.user == obj.user.user))

    def has_add_permission(self, request: HttpRequest) -> bool:
        return True

    def save_model(self, request: HttpRequest, obj: Comment | None, form: ModelForm, change: bool) -> None:
        if obj is not None:
            obj.user = BlogUser.objects.get(user=request.user)

        super().save_model(request, obj, form, change)


class FileAdmin(admin.ModelAdmin):
    def has_view_permission(self, request: HttpRequest, obj: File | None = None) -> bool:
        return obj is not None and Block.objects.filter(blocker__user=obj.post.user.user,
                                                        blocked__user=request.user).exists()

    def has_change_permission(self, request: HttpRequest, obj: File | None = None) -> bool:
        return obj is not None and request.user == obj.post.user.user

    def has_delete_permission(self, request: HttpRequest, obj: File | None = None) -> bool:
        return obj is not None and request.user == obj.post.user.user

    def has_add_permission(self, request: HttpRequest) -> bool:
        return True


class BlockAdmin(admin.ModelAdmin):
    def has_view_permission(self, request: HttpRequest, obj: Block | None = None) -> bool:
        return True

    def has_change_permission(self, request: HttpRequest, obj: Block | None = None) -> bool:
        return obj is not None and request.user == obj.blocker.user

    def has_delete_permission(self, request: HttpRequest, obj: Block | None = None) -> bool:
        return obj is not None and request.user == obj.blocker.user

    def has_add_permission(self, request: HttpRequest) -> bool:
        return True


admin.site.register(BlogUser, BlogUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Block, BlockAdmin)
