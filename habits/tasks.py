from celery import shared_task
from django.utils import timezone
import pytz
from .models import Habit
from .services import send_telegram_message


@shared_task
def send_habit_reminder():
    """ Задача поиска привычек и отправки уведомлений """

    now = timezone.now()

    moscow_timezone = pytz.timezone('Europe/Moscow')
    local_time = now.astimezone(moscow_timezone)

    current_hour = local_time.hour
    current_minute = local_time.minute

    habits = Habit.objects.filter(
        time__hour=current_hour,
        time__minute=current_minute,
        user__telegram_id__isnull=False
    )

    for habit in habits:
        chat_id = habit.user.telegram_id
        message = f'Напоминание! Пора выполнить привычку: {habit.action} в {habit.place}'

        try:
            # Отправка сообщения
            send_telegram_message(chat_id, message)
            print(f'!!! УСПЕХ: Уведомление отправлено пользователю {chat_id} для привычки {habit.action}')
        except Exception as e:
            print(f'!!! ОШИБКА ОТПРАВКИ пользователю {chat_id}: {e}')
