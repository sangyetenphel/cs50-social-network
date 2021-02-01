from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.core import serializers

from .models import User, Post, Profile
from .forms import PostForm

import json


def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.cleaned_data['post']
            new_post = Post(user=request.user, post=post)
            new_post.save()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = PostForm()
        # To get the most recent posts first
        posts_queryset = Post.objects.order_by('date_added').reverse()
        # Display 3 posts on each page
        posts_to_display = Paginator(posts_queryset, 3)
        posts = posts_to_display.page(1)
        if request.GET.get('page'):
            page = int(request.GET.get('page'))
            posts = posts_to_display.page(page)

    return render(request, "network/index.html", {'form': form, 'posts': posts})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        btn_value = data['btn_value']
        user_id = data['user_id']
        user = User.objects.get(id=user_id)
        if btn_value == 'unfollow':
            Profile.objects.filter(follower=request.user, following=user).delete()
        else:
            new_profile = Profile(follower=request.user, following=user)
            new_profile.save()
        return JsonResponse(f'{btn_value}ed {user} successfully!', safe=False)
    else:
        user = request.user
        # Getting the count of followers and following
        following = Profile.objects.filter(follower=user).count()
        follower = Profile.objects.filter(following=user).count()
        follower_list = [person.following for person in Profile.objects.filter(follower=user)]
        # Get the most recent posts first
        posts = Post.objects.order_by('date_added').reverse()
        context = {'follower': follower, 'following': following, 'posts': posts, 'follower_list': follower_list}
        return render(request, "network/profile.html", context)


def following(request):
    # List of all user objects that the request user(current user) follows
    user_following = []
    # Queryset of Profile class of user following
    user_following_profile = request.user.following.all()
    # Extracting the user object from the Profle queryset of user following
    for user in user_following_profile:
        user_following.append(user.following)

    posts = []
    # Getting all the Post objects from the users that the current user follows
    for user in user_following:
        posts.extend(Post.objects.filter(user=user).order_by('date_added').reverse())
    
    return render(request, "network/following.html", {'posts': posts})


def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method != 'POST':
        # Pre filling post form
        form = PostForm(initial={'post': post.post})
        return render(request, 'network/edit.html', {'form': form})
    else:
        form = PostForm(request.POST)
        if form.is_valid():
            post.post = form.cleaned_data['post']
            post.save()
        return HttpResponseRedirect(reverse('index'))


def like(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data['post_id']
        heart = data['heart']
        post = Post.objects.get(id=post_id)
        # if the heart was red then user is unliking the post 
        if 'red' in heart:
            post.liked_users.remove(request.user)
        else:
            post.liked_users.add(request.user)
        return JsonResponse({'likes': post.liked_users.count(), 'post_id': post_id})

