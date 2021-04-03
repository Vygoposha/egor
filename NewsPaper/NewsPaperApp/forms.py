from django.forms import ModelForm
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from .models import Post


# Создаём модельную форму
class NewsForm(ModelForm):
    # в класс мета как обычно надо написать модель по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['author', 'post_type', 'post_category', 'post_title', 'post_content']


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
