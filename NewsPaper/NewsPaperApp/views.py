from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # импортируем класс получения деталей объекта
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect
from django.http import HttpRequest

from .models import Post
from .filters import PostFilter
from .forms import NewsForm, UserForm


class NewsList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news.html'  # указываем имя шаблона, в котором будет
    # лежать html, в котором будут все инструкции о том, как именно
    # пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать
    # все объекты, его надо указать, чтобы обратиться к самому списку
    # объектов через html-шаблон
    queryset = Post.objects.order_by('-post_datetime')
    paginate_by = 10


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_id.html'
    context_object_name = 'news_id'


class NewsSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-post_datetime')

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class NewsCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'news_add.html'
    form_class = NewsForm
    permission_required = ('NewsPaperApp.add_post',
                           'NewsPaperApp.change_post',
                           'NewsPaperApp.delete_post',
                           )


class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'news_add.html'
    form_class = NewsForm
    permission_required = ('NewsPaperApp.add_post',
                           'NewsPaperApp.change_post',
                           'NewsPaperApp.delete_post',
                           )
    permission_denied_message = 'Чтобы редактировать посты, необходимо стать автором'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name= 'authors').exists()
        return context


class NewsDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'news_delete.html'
    context_object_name = 'news_id'
    queryset = Post.objects.all()
    success_url = '/news/'

    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect(f'/profile/{request.user.id}')


class UserUpdateView(UpdateView):
    template_name = 'user_profile.html'
    form_class = UserForm
    success_url = f'/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return User.objects.get(pk=id)
