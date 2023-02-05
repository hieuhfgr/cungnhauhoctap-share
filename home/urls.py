from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.indexView),
    path('register/', views.registerView),
    path('login/', auth_views.LoginView.as_view(template_name= 'login/login.html')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/')),
    path('about/', views.aboutView),
    path('about/team/', views.teamView),
    path('about/faq/', views.faqsView),
    path('about/support/', views.supportView),
    path('announcement/', views.AnnouncementListView),
    path('announcement/<str:id>', views.AnnouncementDetailView),
]