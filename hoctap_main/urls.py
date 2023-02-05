from django.urls import path 
from . import views

urlpatterns = [
    path('', views.indexView),
    path('posts/', views.PostListView),
    path('post/search', views.searchPostView),
    path('post/create', views.createNewPostPageView),
    path('posts/<slug:post_id>/', views.PostDetailView),
    path('posts/<slug:post_id>/change', views.PostChangeView),
    path('posts/<slug:post_id>/delete', views.PostDeleteView),
    path('posts/<slug:post_id>/hoidap/', views.PostQnAListView),
    path('posts/<slug:post_id>/hoidap/all-questions-author', views.PostQnASeeQuestions_forAuthor),
    path('posts/<slug:post_id>/hoidap/all-questions-questioner', views.PostQnASeeQuestions_forQuestioner),
    path('posts/<slug:post_id>/hoidap/send-question', views.PostQnACreateQuestion),
    path('posts/<slug:post_id>/hoidap/<str:idQnA>/answer', views.PostQnA_Answer),
    path('posts/<slug:post_id>/hoidap/<str:idQnA>/', views.PostQnAInfo),

    path('test/', views.TestListView),
    path('test/search', views.searchTestView),
    path('test/create', views.createNewTestPageView),
    path('tests/<slug:test_id>/', views.TestDetailView),
    path('tests/<slug:test_id>/topscore', views.TestTopScoreView),
    # path('tests/<slug:test_id>/change', views.TestChangeView),
    # path('tests/<slug:test_id>/delete', views.TestDeleteView),
    
    # path('tests/<slug:test_id>/hoidap/', views.TestQnAListView),
    # path('tests/<slug:test_id>/hoidap/all-questions-author', views.TestQnASeeQuestions_forAuthor),
    # path('tests/<slug:test_id>/hoidap/all-questions-questioner', views.TestQnASeeQuestions_forQuestioner),
    # path('tests/<slug:test_id>/hoidap/send-question', views.TestQnACreateQuestion),
    # path('tests/<slug:test_id>/hoidap/<str:idQnA>/answer', views.TestQnA_Answer),
    # path('tests/<slug:post_id>/hoidap/<str:idQnA>/', views.TestQnAInfo),
]
