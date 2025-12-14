from celery import shared_task
from django.utils import timezone
from .models import Habit
from .services import send_telegram_message


@shared_task
def send_habit_reminder():
    """ задача поиска привычек и отправки уведомлений """
    now = timezone.now().localtime()
    current_time = now.strftime("%H:%M:00")

    habits = Habit.objects.filter(time=current_time, user__telegram_id__isnull=False)

    for habit in habits:
        chat_id = habit.user.telegram_id
        message = f'Напоминание! Пора выполнить привычку: {habit.action} в {habit.place}'

        try:
            send_telegram_message(chat_id, message)
            print(f'Уведомление отправлено пользователю {chat_id} для привычки {habit.action}')
        except Exception as e:
            print(f'Ошибка отправки пользователю {chat_id}: {e}')
