from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('cards/', views.post_list_cards, name='post_list_cards'),
    path('<int:id>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('tag/create/', views.create_tag, name='create-tag'),
    path('tag/edit/<int:pk>/', views.edit_tag, name='edit-tag'),
    path('tag/delete/<int:pk>/', views.delete_tag, name='delete-tag'),
    path('tags/<slug:slug>/', views.tags, name='post-tags'),
]
