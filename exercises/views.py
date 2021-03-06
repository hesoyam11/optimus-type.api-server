from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, viewsets, permissions, filters

from .models import Exercise, Attempt, FastestAttempt, LayoutStatistics
from .serializers import (
    ExerciseSerializer,
    AttemptListItemSerializer,
    AttemptDetailSerializer,
    FastestAttemptSerializer,
    LayoutStatisticsSerializer
)
from .permissions import IsCreatorOrReadOnly


@method_decorator(
    name='create', decorator=swagger_auto_schema(tags=['exercises'])
)
@method_decorator(
    name='list', decorator=swagger_auto_schema(tags=['exercises'])
)
@method_decorator(
    name='retrieve', decorator=swagger_auto_schema(tags=['exercises'])
)
@method_decorator(
    name='destroy', decorator=swagger_auto_schema(tags=['exercises'])
)
class ExerciseViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Exercise.objects.select_related('creator').filter(
        creator__is_active=True, is_banned=False, is_removed=False
    )
    serializer_class = ExerciseSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly
    )
    filter_backends = (
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter
    )
    filterset_fields = ('creator', 'locale')
    search_fields = ('title',)
    ordering_fields = ('created_at', 'title', 'attempt_counter')

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_destroy(self, instance: Exercise):
        instance.is_removed = True
        instance.save()


@method_decorator(
    name='create', decorator=swagger_auto_schema(tags=['attempts'])
)
@method_decorator(
    name='list', decorator=swagger_auto_schema(tags=['attempts'])
)
@method_decorator(
    name='retrieve', decorator=swagger_auto_schema(tags=['attempts'])
)
class AttemptViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Attempt.objects.select_related('creator', 'exercise').filter(
        creator__is_active=True,
        exercise__is_banned=False, exercise__is_removed=False
    )
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly
    )
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('creator', 'exercise', 'layout')
    ordering_fields = ('created_at', 'time_spent')

    def get_serializer_class(self):
        if self.action == 'list':
            return AttemptListItemSerializer
        return AttemptDetailSerializer

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


@method_decorator(
    name='list', decorator=swagger_auto_schema(tags=['attempts'])
)
@method_decorator(
    name='retrieve', decorator=swagger_auto_schema(tags=['attempts'])
)
class FastestAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FastestAttempt.objects.select_related('creator').filter(
        creator__is_active=True
    )
    serializer_class = FastestAttemptSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('exercise',)
    ordering_fields = ('time_spent',)


@method_decorator(
    name='list', decorator=swagger_auto_schema(tags=['statistics'])
)
@method_decorator(
    name='retrieve', decorator=swagger_auto_schema(tags=['statistics'])
)
class LayoutStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LayoutStatistics.objects.all()
    serializer_class = LayoutStatisticsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('user',)
    ordering_fields = ('layout',)
