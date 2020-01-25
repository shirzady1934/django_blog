from django.urls import path
from . import views
urlpatterns = [
        path('submit_post', views.submit_post, name = 'submit_post'),
        path('delete_post', views.delete_post, name = 'delete_post'),
        path('signup/', views.sign_up, name='signup'),
        path('submit_comment/', views.submit_comment, name='submit_comment'),
        path('profile/<str:username>/<int:id>/', views.user_post, name = 'posts'),
        path('profile/<str:username>/', views.user_show, name = 'user_show'),
        path('publish', views.publish, name = 'publish'),
        path('', views.new_post, name = 'new_post'),     
        path('login', views.login, name='login'),
        path('logout', views.logout, name='logout'),
        path('home', views.home, name='home'),
]

