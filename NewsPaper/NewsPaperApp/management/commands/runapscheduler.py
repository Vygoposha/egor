import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import datetime, timedelta
import pytz


from NewsPaperApp.models import Post, Category

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
def my_job():
    #  Your job processing logic here...

    post_datetime_filter = datetime.now(pytz.timezone('Europe/Moscow')) - timedelta(days=7)

    notify_dict = {}
    for category in Category.objects.all():
        for subscriber in category.subscribers.all():
            if subscriber not in notify_dict.keys():
                notify_dict.update({subscriber: Post.objects.filter(post_category=category,
                                                                    post_datetime__gte=post_datetime_filter)})
            else:
                                notify_dict[subscriber] = notify_dict[subscriber].union(Post.objects.filter(post_category=category,
                                                                                            post_datetime__gte=post_datetime_filter)).order_by('post_datetime')

    subject = 'Подборка новостей за неделю'
    for user, news in notify_dict.items():
        html_content = render_to_string('news_weekly_notify.html',
                                        {'news': list(news),
                                         'username': user.username,
                                         }
                                        )
        msg = EmailMultiAlternatives(
            subject=subject,
            # body=news.post_content,  # это то же, что и message
            from_email='epanisimov@yandex.ru',
            to=[user.email],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        msg.send()


# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            # trigger=CronTrigger(second="*/10"),
            trigger=CronTrigger(day_of_week="sun", hour="10", minute="00"),
            # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
