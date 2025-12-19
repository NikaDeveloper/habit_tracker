from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User
from habits.models import Habit


class HabitTestCase(APITestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create(
            email="test@example.com", is_staff=False, is_superuser=False
        )
        self.user.set_password("testpass")
        self.user.save()

        # Получаем токен и авторизуемся
        self.client.force_authenticate(user=self.user)

        # URL для списка привычек
        self.list_url = reverse("habits:habits-list")

        # Создаем одну приятную привычку (для тестов связывания)
        self.pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дома",
            time="10:00:00",
            action="Лежать на диване",
            is_pleasant=True,
            time_to_complete=60,
            periodicity=1,
        )

        # Данные для правильной полезной привычки
        self.habit_data = {
            "place": "Спортзал",
            "time": "12:00:00",
            "action": "Приседания",
            "periodicity": 1,
            "reward": "Вкусный обед",
            "time_to_complete": 60,
            "is_public": True,
        }

    def test_create_habit(self):
        """Тест успешного создания привычки"""
        response = self.client.post(self.list_url, self.habit_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_list_habits(self):
        """Тест просмотра списка"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Должны видеть 1 созданную в setUp привычку
        self.assertEqual(len(response.data["results"]), 1)

    def test_validator_time_limit(self):
        """Тест валидатора времени выполнения > 120 сек"""
        data = self.habit_data.copy()
        data["time_to_complete"] = 150  # Ошибка
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Время выполнения должно быть не больше 120 секунд", str(response.data)
        )

    def test_validator_reward_and_related(self):
        """Тест валидатора: нельзя и вознаграждение и связанную привычку"""
        data = self.habit_data.copy()
        data["related_habit"] = self.pleasant_habit.id  # Добавляем связанную
        # reward уже есть в self.habit_data
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Нельзя одновременно выбрать связанную привычку и вознаграждение",
            str(response.data),
        )

    def test_validator_related_is_pleasant(self):
        """Тест валидатора: связанная привычка должна быть приятной"""
        # Создаем обычную (не приятную) привычку
        useful_habit = Habit.objects.create(
            user=self.user,
            place="Работа",
            time="09:00:00",
            action="Работа",
            is_pleasant=False,
            time_to_complete=60,
        )
        data = self.habit_data.copy()
        del data["reward"]  # Убираем награду, чтобы не сработал предыдущий валидатор
        data["related_habit"] = (
            useful_habit.id
        )  # Пытаемся привязать полезную, а не приятную

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Связанная привычка должна быть приятной", str(response.data))

    def test_public_habits(self):
        """Тест списка публичных привычек"""
        # Создаем публичную привычку
        Habit.objects.create(
            user=self.user,
            place="Улица",
            time="15:00:00",
            action="Бег",
            is_pleasant=False,
            time_to_complete=60,
            is_public=True,
        )
        url = reverse("habits:public-habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Должна быть минимум 1 публичная привычка
        self.assertGreaterEqual(len(response.data["results"]), 1)
