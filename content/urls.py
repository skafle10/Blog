
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from . import views


urlpatterns = [
    
    path("", views.home_page, name = "home_page"),
    path("write-for-us/", views.write_blog, name= "write_content"),
    path("signup/",views.signup_users, name= "signup"),
    path("login/", views.login_users, name = "login"),
    path("logout/",views.logout_user, name="logout"),
    path("editpost/<slug:post_slug>/",views.edit_post,name= "post_edit"),
    path("deletepost/<slug:post_slug>/",views.delete_post,name="post_delete"),
    path("about/", views.about, name= "about_page"),
    path("archive/",views.archives,name="archive"),
    path("read/<slug:post_slug>/",views.read_post,name="post_detail"),

]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)