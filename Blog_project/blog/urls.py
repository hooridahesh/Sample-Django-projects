from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="starting_page"),
    path("post", views.post, name="post_page"),
    path("post/<slug:slug>", views.single_post, name="post_detail")
]
