from django.urls import path
from .views import ArticleCreateView, BlogListView, ArticleDetailView, ArticleUpdateView, ArticleDeleteView
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='create'),
    path('', cache_page(60*60)(BlogListView.as_view()), name='list'),
    path('read/<slug:slug>/', ArticleDetailView.as_view(), name='view'),
    path('edit/<slug:slug>/', ArticleUpdateView.as_view(), name='update'),
    path('delete/<slug:slug>/', ArticleDeleteView.as_view(), name='delete'),
]
