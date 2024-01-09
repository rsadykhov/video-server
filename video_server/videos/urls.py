from django.urls import path
from . import views



app_name = "videos"

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("videos/<int:pk>/", views.VideosDetailView.as_view(), name="videos_detail"),
    path("tags/", views.tags_list_view, name="tags_list"),
    path("tags/<int:pk>/", views.tags_detail_view, name="tags_detail"),
    path("categories/", views.categories_list_view, name="categories_list"),
    path("categories/<int:pk>/", views.categories_detail_view, name="categories_detail"),
]