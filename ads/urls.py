from django.urls import path
from . import views

app_name = 'ads'
urlpatterns = [
    path('list', views.AdListView.as_view(), name='ad_list'),
    path('create', views.AdCreateView.as_view(), name='ad_create'),
    path('detail/<int:pk>', views.AdDetailView.as_view(), name='ad_detail'),
    path('search', views.AdSearchView.as_view(), name='ad_search'),
]
