from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import EmailMultiAlternatives, mail_managers
from django.template.loader import render_to_string


from .models import Post, User


# def notify_post_create(sender, instance, **kwargs):
#     subject = f'Новый пост в категории {instance.post_category}'
#     print(instance.post_category.all().values('category_name'))
#
#     for user_id in list(instance.post_category.all().values_list('subscribers', flat=True)):
#         user = User.objects.get(id=user_id)
#         html_content = render_to_string('news_create_notify.html',
#                                         {'news': instance,
#                                          'username': user.username,
#                                          }
#                                         )
#         print(user.email)
#         msg = EmailMultiAlternatives(
#             subject=subject,
#             # body=news.post_content,  # это то же, что и message
#             from_email='epanisimov@yandex.ru',
#             to=[user.email],  # это то же, что и recipients_list
#         )
#         msg.attach_alternative(html_content, "text/html")  # добавляем html
#         msg.send()
#
#
# m2m_changed.connect(notify_post_create, sender=Post.post_category.through)
