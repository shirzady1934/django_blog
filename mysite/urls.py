from . import views
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('blog/api/', include('blog.api.urls')),
    path('', views.blog),
]