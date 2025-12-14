from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Habit
from .serializers import HabitSerializer
from .paginators import CustomPaginator
from .permissions import IsOwner


class HabitViewSet(viewsets.ModelViewSet):
    """ CRUD для привычек. Показывает только личные привычки """
    serializer_class = HabitSerializer
    pagination_class = CustomPaginator
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicHabitListAPIView(generics.ListAPIView):
    """ Список публичных привычек. Доступен всем, но без редактирования """
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = HabitSerializer
    pagination_class = CustomPaginator
    permission_classes = [IsAuthenticated]
