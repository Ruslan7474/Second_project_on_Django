from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from apps.news.views import (
    homepage, news_detail, category_detail, news_search,
    register, user_login, user_logout
)


urlpatterns = [
    path('', homepage, name='homepage'),
    path('category/<slug:slug>/', category_detail, name='category_detail'),
    path('news/<slug:slug>/', news_detail, name='news_detail'),
    path('search/', news_search, name='news_search'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
