from django.urls import path
from .views import ArticleCreateView, BlogListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView


urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('', BlogListView.as_view(), name='list'),  # list of articles
    path('read/<slug:slug>/', ArticleDetailView.as_view(), name='view'),
    path('edit/<slug:slug>/', ArticleUpdateView.as_view(), name='update'),
    path('delete/<slug:slug>/', ArticleDeleteView.as_view(), name='delete'),
]