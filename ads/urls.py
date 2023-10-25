from django.urls import path
from . import views

app_name = 'ads'
urlpatterns = [
    path('list', views.AdListView.as_view(), name='ad_list'),
]
