from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_author = Post.objects.filter(author=self.id)
        print(type(posts_author))

        posts_author_total_rating = 0
        for post in posts_author:
            posts_author_total_rating += post.post_rating * 3

        comments_author_total_rating = 0
        for comments in Comment.objects.filter(user=self.author):
            comments_author_total_rating += comments.comment_rating

        comments_posts_total_rating = 0
        for comments in Comment.objects.filter(post__in=posts_author):
            comments_posts_total_rating += comments.comment_rating

        self.author_rating = posts_author_total_rating + \
                             comments_author_total_rating + \
                             comments_posts_total_rating
        self.save()

    def __str__(self):
        return self.author.username



class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    news = 'Новость'
    article = 'Статья'
    Posts = [(news, 'Новость'), (article, 'Статья'), ('select', 'Выбрать')]
    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                               verbose_name='Автор', blank=True,
                               null=True)
    post_type = models.CharField(max_length=30, choices=Posts,
                                 default='select', verbose_name='Тип')
    post_datetime = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=255)
    post_content = models.TextField()
    post_rating = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.post_title

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.post_title.title()}: {self.post_content[:20]}'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    comment_datetime = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return self.comment_text
