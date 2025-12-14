from rest_framework.exceptions import ValidationError


class RewardRelationValidator:
    """Исключает одновременный выбор связанной привычки и вознаграждения"""

    def __init__(self, field1, field2):
        self.field1 = field1  # reward
        self.field2 = field2  # related_habit

    def __call__(self, value):
        reward = value.get(self.field1)
        related_habit = value.get(self.field2)

        if reward and related_habit:
            raise ValidationError(
                "Нельзя одновременно выбрать связанную привычку и вознаграждение"
            )


class ExecutionTimeValidator:
    """Чтобы время выполнения не превышало 120 секунд"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        exec_time = value.get(self.field)
        if exec_time and exec_time > 120:
            raise ValidationError("Время выполнения должно быть не больше 120 секунд")


class RelatedHabitIsPleasantValidator:
    """В связанные привычки могут попадать только с признаком приятной привычки"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        related_habit = value.get(self.field)
        if related_habit and not related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной")


class PleasantHabitValidator:
    """Чтобы у приятной привычки не было вознаграждения или связанной привычки"""

    def __init__(self, is_pleasant_field, reward_field, related_habit_field):
        self.is_pleasant_field = is_pleasant_field
        self.reward_field = reward_field
        self.related_habit_field = related_habit_field

    def __call__(self, value):
        is_pleasant = value.get(self.is_pleasant_field)
        reward = value.get(self.reward_field)
        related_habit = value.get(self.related_habit_field)
        if is_pleasant and (reward and related_habit):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки "
            )


class PeriodicityValidator:
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        periodicity = value.get(self.field)
        if periodicity and (periodicity > 7 or periodicity < 1):
            raise ValidationError("Периодичность должна быть от 1 до 7 дней")
