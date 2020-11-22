from django.conf.urls import url
from django.urls import path
from . import views
from .views import ArticleView

# app_name = "articles"
urlpatterns = [
    url(r'^send_command$', views.download, name='download'),
    path('articles/', ArticleView.as_view()),
    path('articles/<int:pk>', ArticleView.as_view()),
    path('', views.index, name='index'),

]


