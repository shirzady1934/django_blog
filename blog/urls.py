from django.urls import path
from . import views
urlpatterns = [
        path('submit_post/', views.submit_post, name='submit_post'),
        path('delete_post/', views.delete_post, name='delete_post'),
        path('edit_post/<int:pk>/' , views.edit_post, name='edit_post'),
        path('signup/', views.sign_up, name='signup'),
        path('submit_comment/', views.submit_comment, name='submit_comment'),
        path('delete_comment/', views.delete_comment, name='delete_comment'),
        path('profile/notifications/', views.notifications, name='notifications'),
        path('profile/<str:username>/token/', views.get_token, name='get_token'),
        path('profile/<str:username>/<int:id>/', views.show_post, name = 'posts'),
        path('profile/<str:username>/', views.profile, name='profile'),
        path('', views.timeline, name='timeline'),
        path('signin/', views.signin, name='signin'),
        path('signout/', views.signout, name='signout'),
        path('home/', views.home, name='home'),
        path('isauth/', views.mss, name='mss')
]

