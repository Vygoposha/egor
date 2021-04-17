from NewsPaper.NewsPaperApp.models import Author, Category, Post, Comment
from django.contrib.auth.models import User


# Создать двух пользователей (с помощью метода User.objects.create_user).
user1 = User.objects.create_user(username='User1', email='user1@user1',
                                 password='user1password')
user2 = User.objects.create_user(username='User2', email='user2@user2',
                                 password='user2password')

# Создать два объекта модели Author, связанные с пользователями.
author1 = Author.objects.create(author=user1)
author2 = Author.objects.create(author=user2)

# Добавить 4 категории в модель Category.
category1 = Category.objects.create(category_name='Спорт')
category2 = Category.objects.create(category_name='Политика')
category3 = Category.objects.create(category_name='Наука')
category4 = Category.objects.create(category_name='Криминал')

# Добавить 2 статьи и 1 новость.
article1 = Post.objects.create(author=author1,
                               post_type=Post.article,
                               post_title='Заголовок слово1 статьи 1',  # слово1 - цензурируемое
                               post_content='Текст статьи 1',
                               )
article2 = Post.objects.create(author=author1,
                               post_type=Post.article,
                               post_title='Заголовок статьи 2',
                               post_content='Текст статьи 2. Пример '
                                            'цензурируемого слова в тексте '
                                            'статьи - СЛОВО2!',  # слово2 - цензурируемое
                               )
news1 = Post.objects.create(author=author2,
                            post_type=Post.news,
                            post_title='Заголовок новости 1',
                            post_content='Текст новости 1',
                            )
news2 = Post.objects.create(author=author1,
                            post_type=Post.news,
                            post_title='Заголовок новости 2',
                            post_content='Текст новости 2',
                            )


# Присвоить им категории (как минимум в одной статье/новости должно быть не
# меньше 2 категорий).
article1.post_category.add(category1)
article1.post_category.add(category2)
article2.post_category.add(category3)
news1.post_category.add(category4)
news2.post_category.add(category3)

# Создать как минимум 4 комментария к разным объектам модели Post (в каждом
# объекте должен быть как минимум один комментарий).
comment1 = Comment.objects.create(post=article1,
                                  user=user1,
                                  comment_text='Текст комментария 1')
comment2 = Comment.objects.create(post=article1,
                                  user=user2,
                                  comment_text='Текст комментария 2')
comment3 = Comment.objects.create(post=article2,
                                  user=user1,
                                  comment_text='Текст комментария 3')
comment4 = Comment.objects.create(post=news1,
                                  user=user2,
                                  comment_text='Текст комментария 4')

# Применяя функции like() и dislike() к статьям/новостям и комментариям,
# скорректировать рейтинги этих объектов.
comment1.like()
comment2.like()
comment3.like()
comment4.like()
comment1.like()
comment2.like()
comment3.like()
comment1.like()
comment2.like()
comment1.like()
comment1.dislike()
comment4.dislike()
comment3.dislike()
comment1.dislike()
article1.like()
article1.like()
article1.like()
article1.like()
article1.like()
article2.like()
article2.like()
article2.like()
news1.dislike()
news1.like()
news1.like()
news1.like()
news1.like()
news1.like()

# Обновить рейтинги пользователей.
author1.update_rating()
author2.update_rating()

# Вывести username и рейтинг лучшего пользователя (применяя сортировку и
# возвращая поля первого объекта).
top_author = Author.objects.all().order_by('-author_rating')
print(top_author.values('author__username', 'author_rating')[0])

# Вывести дату добавления, username автора, рейтинг, заголовок и превью
# лучшей статьи, основываясь на лайках/дислайках к этой статье.
top_post = Post.objects.all().order_by('-post_rating')
print(top_post.values('post_datetime',
                       'author__author__username',
                       'post_rating',
                       'post_title',
                       'post_content')[0])

# Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
Comment.objects.filter(post=top_post[0]).values('comment_datetime',
                                                'user',
                                                'comment_rating',
                                                'comment_text')


# Переопределение переменных в случае перезапуска Shell
from NewsPaperApp.models import Author, Category, Post, Comment, User
from django.contrib.auth.models import User

user1 = User.objects.get(id=1)
user2 = User.objects.get(id=2)
author1 = Author.objects.get(id=1)
author2 = Author.objects.get(id=2)
category1 = Category.objects.get(id=1)
category2 = Category.objects.get(id=2)
category3 = Category.objects.get(id=3)
category4 = Category.objects.get(id=4)
article1 = Post.objects.get(id=1)
article2 = Post.objects.get(id=2)
news1 = Post.objects.get(id=3)
news2 = Post.objects.get(id=4)
comment1 = Comment.objects.get(id=1)
comment2 = Comment.objects.get(id=2)
comment3 = Comment.objects.get(id=3)
comment4 = Comment.objects.get(id=3)

category2.subscribers.all().values_list('username', flat=True)

for category in article1.post_category.all():
    category.subscribers.all()

article1.post_category.all().values_list('subscribers__username', flat=True)

article1.post_category.all().values('subscribers')

article1.post_category.all().values_list('subscribers__username', flat=True)
list(article1.post_category.all().values_list('subscribers', flat=True))


user1.email = 'user1@user1.com'
user2.email = 'user2@user2.com'


# article1.post_title = 'Заголовок слово1 статьи 1'
# article1.save()
# article2.post_content = 'Текст статьи 2. Пример цензурируемого слова в тексте статьи - СЛОВО2!'
# article2.save()

Author.objects.all()
Author.objects.filter(author_id=8).exists()

Author.objects.create(author_id=8).save()

User.objects.filter(username='Egorza').values('id')