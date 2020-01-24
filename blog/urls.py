from django.urls import path
from . import views
urlpatterns = [
        path('submit_post', views.submit_post, name = 'submit_post'),
        path('delete_post', views.delete_post, name = 'delete_post'),
        path('signup/', views.sign_up, name='signup'),
        path('<str:username>/<int:id>/', views.user_post, name = 'posts'),
        path('<str:username>/', views.user_show, name = 'use_showr'),
        path('publish', views.publish, name = 'publish'),
        path('', views.new_post, name = 'new_post'),     
        path('login', views.login, name='login'),
        path('logout', views.logout, name='logout'),
        path('home', views.home, name='home'),
]

