from django.urls import path
from .views import detail_post, update_post, delete_post, create_post, all_post
urlpatterns = [
	path('create', create_post, name='create-post'),
	path('update/<pk>', update_post, name='update-post'),
	path('delete/<pk>', delete_post, name='delete-post'),
	#path('', all_post, name='all-post'),	
	path('<pk>', detail_post, name='show-post'),
	path('', all_post, name='all-post')
]