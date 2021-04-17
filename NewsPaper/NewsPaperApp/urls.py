from django.urls import path
from django.views.generic import TemplateView
from .views import NewsList, NewsDetail, NewsSearch, NewsCreateView, \
    NewsUpdateView, NewsDeleteView, subscribe

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас
    # останется пустым, позже станет ясно почему
    path('', NewsList.as_view()),
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде
    # view. Для этого вызываем метод as_view
    path('<int:pk>', NewsDetail.as_view(), name='news'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('add/', NewsCreateView.as_view(), name='news_add'),
    path('<int:pk>/edit', NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete', NewsDeleteView.as_view(), name='news_delete'),
    path('subscribe/<int:pk>', subscribe, name='subscribe'),
    path('day_limit/', TemplateView.as_view(template_name='news_day_limit.html')),
]
