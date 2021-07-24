from django.conf import settings
from django.db.models import QuerySet, Count, Avg
from django.db.models.functions import Coalesce

from .models import Event

User = settings.AUTH_USER_MODEL


def gey_my_events(user: User) -> QuerySet[Event]:
    """
    Получает все мероприятия пользователя

    Если это автор, возвращает все мероприятия, которые он создал
    Если это участник, возвращает все мероприятия, на которые он зарегистрирован

    :param user: текущий авторизованный пользователь
    :return: QuerySet всех мероприятий
    """
    query = None
    if user.type == 0:
        query = Event.objects.select_related().filter(request__user=user).distinct()
    elif user.type == 1:
        query = Event.objects.filter(user=user)

    if query:
        return query.annotate(
            num_participants=Count('request', distinct=True),
            avg_rate=Coalesce(Avg('feedback__rating'), 0.0)
        )

    return Event.objects.none()
