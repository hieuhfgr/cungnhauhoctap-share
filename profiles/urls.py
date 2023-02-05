from django.urls import path 
from . import views

urlpatterns = [
    path('detail/<username>/', views.profileView),
    path('detail/<username>/change', views.profileChangeView),
    path('search/', views.searchView),
    path('topusers/', views.topUserListView),
    path('detail/<username>/claimrank/', views.claimRankView),
]