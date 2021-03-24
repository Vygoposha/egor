from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # импортируем класс получения деталей объекта

from .models import Post
from .filters import PostFilter
from .forms import NewsForm

class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет
    # лежать html, в котором будут все инструкции о том, как именно
    # пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать
    # все объекты, его надо указать, чтобы обратиться к самому списку
    # объектов через html-шаблон
    queryset = Post.objects.order_by('-post_datetime')
    paginate_by = 2


class NewsDetail(DetailView):
    model = Post # модель всё та же, но мы хотим получать детали конкретно
    # отдельного товара
    template_name = 'news_id.html'  # название шаблона будет product.html
    context_object_name = 'news_id'  # название объекта. в нём будет


class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-post_datetime')

    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class NewsCreateView(CreateView):
    template_name = 'news_add.html'
    form_class = NewsForm


class NewsUpdateView(UpdateView):
    template_name = 'news_add.html'
    form_class = NewsForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    context_object_name = 'news_id'
    queryset = Post.objects.all()
    success_url = '/news/'



