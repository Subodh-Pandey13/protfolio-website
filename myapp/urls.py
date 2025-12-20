from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("cv/", views.cv, name= "cv"),
    path("research/", views.research, name = "research"),
    path("teaching/", views.teaching, name = "teaching"),
    path("blog/", views.blog, name = "blog"),
    path("contact/", views.contact, name = "contact"),

]