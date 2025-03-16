from django.urls import path
from equity_eye import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='testAPI'),
    path('search/', views.search),
    path('articles/', views.ArticleView.as_view()),
    path('articles/<int:id>', views.ArticleView.as_view()),
    path('articles/<slug:range>', views.ArticleView.as_view()),
    path('articles/<path:url>', views.ArticleView.as_view()),
    path('assets/<str:ticker>', views.AssetView.as_view()),
    path('assets/', views.AssetView.as_view()),
    path('prices/<str:id>', views.StockPriceView.as_view()),
    path('prices/', views.StockPriceView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
