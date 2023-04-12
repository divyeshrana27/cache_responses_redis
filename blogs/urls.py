from django.urls import path
from . import views
urlpatterns = [
    path("blogs/", views.get_blogs),
    path("blog/", views.get_blog),
    path("blog/create/", views.create_blog)
]
