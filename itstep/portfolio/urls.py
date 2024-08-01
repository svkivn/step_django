from django.urls import path

from .views import hello, about_me, my_skill, redirect_to_hello, home_view


urlpatterns = [
    #path('', hello, name="p-hi"),
    path('about/', about_me, name="about"),
    path('skills/<int:id>', my_skill, name="skill"),
    path('skills/', my_skill, name="skill"),
    path('re/', redirect_to_hello, name="re"),
    path('', home_view, name="home-view")
]