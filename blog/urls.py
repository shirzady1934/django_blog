from django.urls import path
from . import views
urlpatterns = [
        path('<int:post_id>/', views.post_show, name = 'post_show'),
        path('submit_post', views.submit_post, name = 'submit_post'),
        path('delete_post', views.delete_post, name = 'delete_post'),
        path('posts/<str:p_user>/<int:p_id>/', views.user_post, name = 'posts'),
        path('posts/<str:username>/', views.user, name = 'posts_user'),
        path('publish', views.publish, name = 'publish'),
        path('', views.new_post, name = 'new_post'),     
        path('login', views.login, name='login'),
        path('logout', views.logout, name='logout'),
        path('home', views.home, name='home'),
]

