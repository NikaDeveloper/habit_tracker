from django.db import models
from django.conf import settings


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель",
        related_name="habits",
        null=True,
        blank=True,
    )
    place = models.CharField(max_length=100, verbose_name="Место")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=200, verbose_name="Действие")

    is_pleasant = models.BooleanField(
        default=False, verbose_name="признак приятной привычки"
    )

    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная привычка",
        null=True,
        blank=True,
    )

    periodicity = models.PositiveIntegerField(
        default=1, verbose_name="Периодичность (в днях)"
    )

    reward = models.CharField(
        max_length=200, verbose_name="Вознаграждение", null=True, blank=True
    )
    time_to_complete = models.PositiveIntegerField(
        verbose_name="Время на выполнение (сек)"
    )
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["id"]
