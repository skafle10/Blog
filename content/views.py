from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Permission,Group,User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import permission_required,login_required
from content.models import BlogPost
from content.forms import BlogForm
import random

# Create your views here.

def home_page(request):
    query_set = BlogPost.objects.all()
    highlighted_posts = query_set.order_by('?')[:6]
    latest_posts = query_set.order_by("-uploaded_at")[:2]
    return render(request, "home.html",{"highlighted_posts":highlighted_posts, "posts":latest_posts})
    

def read_post(request,post_slug):
    query_set = BlogPost.objects.get(slug= post_slug)
    return render(request,"read_blog.html",{"post":query_set})


@permission_required("content.change_blogpost",raise_exception=True)
def edit_post(request,post_slug):
    original_post = get_object_or_404(BlogPost,slug = post_slug)
    
    if request.method == "POST":
        form = BlogForm(request.POST,request.FILES,instance=original_post)
        if form.is_valid():
            updated_post = form.save(commit=False)
            updated_post.save()
            form.save_m2m()
            messages.success(request, "Post updated")
            return redirect("home_page")
    else:
        form = BlogForm(instance=original_post)  

    return render(request, "write_blogs.html",{"form":form})




@permission_required("content.delete_blogpost", raise_exception=True)
def delete_post(request,post_slug):

    if request.user.is_authenticated:
        post_to_be_deleted = BlogPost.objects.get(slug=post_slug)
        post_to_be_deleted.delete()

        messages.success(request,"Post deleted")
        return redirect("home_page")

        
    else:
        return HttpResponse("Permission not allowed")


def signup_users(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect("home_page")
    else:
        form = UserCreationForm()
    return render (request, "signup.html")



def login_users(request):

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            next_url = request.POST.get("next")
            if next_url:
                return redirect(next_url)
            
            return redirect("home_page")

        else:
            return HttpResponse("Invalid username or password")
        
    return render(request,"login_page.html")


def logout_user(request):
    logout(request)

    return redirect ("home_page")


@login_required(login_url='login')
def write_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
      
            new_blog=form.save(commit=False)
            new_blog.user_id = request.user.pk
            new_blog.save()
            form.save_m2m()

            messages.success(request,"Your blog is published")
            authors_group,created = Group.objects.get_or_create("Authors")
            writer = User.objects.get(username= request.user.username)
            writer.groups.add(authors_group)
            return redirect("home_page")
        

    else:
        form = BlogForm()
    return render(request, "write_blogs.html",{"form":form})
    



def archives(request):
    all_posts = BlogPost.objects.all()
    return render(request, "archives.html",{"all_posts":all_posts})


def about(request):

    return render(request,"about.html")



