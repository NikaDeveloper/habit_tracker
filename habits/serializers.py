from rest_framework import serializers
from .models import Habit
from .validators import (
    RewardRelationValidator,
    ExecutionTimeValidator,
    RelatedHabitIsPleasantValidator,
    PleasantHabitValidator,
    PeriodicityValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        validators = [
            RewardRelationValidator(field1="reward", field2="related_habit"),
            ExecutionTimeValidator(field="time_to_complete"),
            RelatedHabitIsPleasantValidator(field="related_habit"),
            PleasantHabitValidator(
                is_pleasant_field="is_pleasant",
                reward_field="reward",
                related_habit_field="related_habit",
            ),
            PeriodicityValidator(field="periodicity"),
        ]
