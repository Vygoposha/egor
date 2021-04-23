from django.forms import ModelForm, TextInput, Textarea, Select, SelectMultiple
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from django.http import request


from .models import Post


# Создаём модельную форму
class NewsForm(ModelForm):
    # в класс мета как обычно надо написать модель по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['post_type', 'post_category', 'post_title', 'post_content']

        widgets = {
            'post_type': Select(attrs={
                'class': 'custom-select',
                'option selected': 'Выбрать...'
            }),
            'post_category': SelectMultiple(attrs={
                'multiple class': 'form-control',
            }),
            'post_title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи или новости'
            }),
            'post_content': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...'
            }),
        }


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

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
            'email': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e-mail'
            }),
        }
