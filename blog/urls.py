from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.posts_list, name="post-list"),
    path('<int:id>/', views.post_detail, name="post-detail"),
    path('cards/', views.post_cards, name="post-list-cards"),
    path('<int:post_id>/rate', views.rate_post, name="rate-post"),

    path('tag/create/', views.create_tag, name="create-tag"),
    path('tag/<int:pk>/edit', views.edit_tag, name="edit-tag"),
    path('tag/<int:pk>/delete', views.delete_tag, name="delete-tag"),
]
