from django.core.management.base import BaseCommand, CommandError
from NewsPaperApp.models import Post, Category


class Command(BaseCommand):
    help = 'Подсказка вашей команды'  # показывает подсказку при вводе "python manage.py <ваша команда> --help"
    requires_migrations_checks = True  # напоминать ли о миграциях. Если тру — то будет напоминание о том, что не сделаны все миграции (если такие есть)

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('--category', type=str, help='Имя категории, посты в которой будут удалены', )

    def handle(self, *args, **kwargs):
        # здесь можете писать любой код, который выполнется при вызове вашей команды
        category = kwargs['category']

        if category:
            if category in list(Category.objects.all().values_list('category_name', flat=True)):
                self.stdout.write(f"Вы действительно хотите удалить все посты в категории {category}?")
                answer = input()  # считываем подтверждение
                if answer == 'yes':
                    # Post.objects.filter(post_category__category_name=category).delete()
                    self.stdout.write(self.style.SUCCESS(f'Посты в категории <{category}> успешно удалены'))
                    return
                else:
                    self.stdout.write(self.style.ERROR('Команда отменена'))
            else:
                self.stdout.write(f"Категории <{category}> не существует, попробуйте еще раз")
        else:
            self.stdout.write("Вы действительно хотите удалить все посты?")
            answer = input()  # считываем подтверждение
            if answer == 'yes':
                # Post.objects.filter(post_category__category_name=category).delete()
                self.stdout.write(self.style.SUCCESS(f'Все посты успешно удалены'))
                return
            else:
                self.stdout.write(self.style.ERROR('Команда отменена'))
