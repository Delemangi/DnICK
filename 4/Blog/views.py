from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from .models import Post, Block, BlogUser
from .forms import PostForm, BlockForm


def posts(request: WSGIRequest):
    blocked_users = Block.objects.filter(blocker__user=request.user).values_list("blocked__user", flat=True)
    visible_posts = Post.objects.get_queryset().exclude(user__user__in=blocked_users)

    return render(request, "index.html", {"posts": visible_posts})


def profile(request: WSGIRequest):
    user = BlogUser.objects.get(user=request.user)
    visible_posts = Post.objects.filter(user=user)

    return render(request, "profile.html", {"user": user, "posts": visible_posts})


def add(request: WSGIRequest):
    if request.method == "POST":
        form_data = PostForm(data=request.POST, files=request.FILES)

        if form_data.is_valid():
            post = form_data.save(commit=False)
            post.user = BlogUser.objects.get(user=request.user)
            post.save()

            return redirect("posts")

    return render(request, "add.html", {"form": PostForm})


def blocked(request: WSGIRequest):
    if request.method == "POST":
        form_data = BlockForm(data=request.POST, files=request.FILES)

        if form_data.is_valid():
            block = form_data.save(commit=False)
            block.blocker = BlogUser.objects.get(user=request.user)
            block.save()

            return redirect("blocked")

    blocks = Block.objects.filter(blocker__user=request.user)
    blocked_users = BlogUser.objects.filter(user__in=blocks.values_list("blocked__user", flat=True))

    return render(request, "blocked.html", {"form": BlockForm, "users": blocked_users})
