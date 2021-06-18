from django.contrib import admin
from .models import Post, Category


def nullfy_rating(modeladmin, request, queryset): # все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(post_rating=0)


nullfy_rating.short_description = 'Обнулить рейтинг' # описание для более понятного представления в админ панеле задаётся, как будто это объект


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ['post_title', 'post_type', 'post_datetime', 'author', 'post_rating']  # генерируем список имён всех полей для более красивого отображения
    list_filter = ('post_title', 'post_type', 'post_datetime', 'author', 'post_rating', 'post_category__category_name')
    search_fields = ['post_title', 'post_type', 'author__author__username', 'post_category__category_name']
    date_hierarchy = 'post_datetime'
    actions = [nullfy_rating]


# Register your models here.
admin.site.register(Category)
admin.site.register(Post, PostAdmin)

