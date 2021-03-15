from django.views.generic import ListView, DetailView  # импортируем класс получения деталей объекта
from .models import Post


class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет
    # лежать html, в котором будут все инструкции о том, как именно
    # пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать
    # все объекты, его надо указать, чтобы обратиться к самому списку
    # объектов через html-шаблон
    queryset = Post.objects.order_by('-post_datetime')


class NewsDetail(DetailView):
    model = Post # модель всё та же, но мы хотим получать детали конкретно
    # отдельного товара
    template_name = 'news_id.html'  # название шаблона будет product.html
    context_object_name = 'news_id'  # название объекта. в нём будет