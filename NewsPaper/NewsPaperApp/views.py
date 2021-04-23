from datetime import datetime, timedelta, date

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView  # импортируем класс получения деталей объекта
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect, render
from django.core.cache import cache  # импортируем наш кэш


from django.http import HttpResponse, HttpRequest
from django.views import View

from .tasks import news_create_notify, news_weekly_notify
from .models import Post, Category, Author
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_count'] = len(Post.objects.all())

        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_id.html'
    context_object_name = 'news_id'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно
        obj = cache.get(f'news-{self.kwargs["pk"]}',None)  # кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object()
            cache.set(f'news-{self.kwargs["pk"]}', obj)
            print('Set obj to cash')
        else:
            print('Get obj from cash')

        return obj


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

    def form_valid(self, form):
        author = Author.objects.get(author=self.request.user)
        form.instance.author = author

        form.save()
        subscribers_set = set(form.instance.post_category.all().values_list('subscribers', flat=True))
        subscribers_list = list(subscribers_set)
        news_create_notify.delay(users_id=subscribers_list, news_id=form.instance.id)

        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        author = Author.objects.get(author=self.request.user)
        news_day_limit = 3

        if len(Post.objects.filter(author=author, post_datetime__date=date.today())) >= news_day_limit:
            return redirect('/news/day_limit')

        return super().get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     author = request.POST.get('user')
    #     post_type = request.POST['post_type']
    #     post_category = request.POST['post_category']
    #     post_title = request.POST['post_title']
    #     post_content = request.POST['post_content']
    #
    #     news = Post(author=author,
    #                 post_type=post_type,
    #                 post_title=post_title,
    #                 post_content=post_content,
    #                 )
    #     news.save()
    #     news.post_category.add(post_category)
    #
    #     print('----------------')
    #     print(news.post_category.all())
    #
    #     for user_id in list(news.post_category.all().values_list('subscribers', flat=True)):
    #         user = User.objects.get(id=user_id)
    #         html_content = render_to_string('news_create_notify.html',
    #                                         {'news': news,
    #                                          'username': user.username,
    #                                          }
    #                                         )
    #         msg = EmailMultiAlternatives(
    #             subject=f'{news.post_title}',
    #             # body=news.post_content,  # это то же, что и message
    #             from_email='epanisimov@yandex.ru',
    #             to=[user.email],  # это то же, что и recipients_list
    #             )
    #         msg.attach_alternative(html_content, "text/html")  # добавляем html
    #         msg.send()
    #
    #     return redirect('/news/')


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
    if not Author.objects.filter(author=request.user).exists():
        Author.objects.create(author=request.user).save()
    return redirect(f'/profile/{request.user.id}')


class UserUpdateView(UpdateView):
    template_name = 'user_profile.html'
    form_class = UserForm
    success_url = f'/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return User.objects.get(pk=id)


@login_required
def subscribe(request, pk):
    category = Category.objects.get(id=request.POST.get('category_id'))

    if category.subscribers.filter(id=request.user.id).exists():
        category.subscribers.remove(request.user)
    else:
        category.subscribers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))


# вьюшка для тестирования celery
class IndexView(View):
    def get(self, request):
        news_weekly_notify.delay()
        return HttpResponse('Hello!')


#вьющка для вывода постов по категориям
class NewsCategory(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news_category.html'  # указываем имя шаблона, в котором будет
    # лежать html, в котором будут все инструкции о том, как именно
    # пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать
    # все объекты, его надо указать, чтобы обратиться к самому списку
    # объектов через html-шаблон
    queryset = Post.objects.order_by('-post_datetime')
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        category_id = self.kwargs['pk']

        return qs.filter(post_category__id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        context['post_count'] = len(Post.objects.filter(post_category__id=category_id))
        context['category'] = Category.objects.get(id=category_id)

        return context

