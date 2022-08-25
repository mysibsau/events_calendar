from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone

from apps.events.models import Event


def verify_event(event_id: int, user: AbstractBaseUser):
    Event.objects.filter(id=event_id).update(
        status=3,
        verified=user,
        verified_date=timezone.now(),
    )


def cancel_event_verification(event_id: int):
    Event.objects.filter(id=event_id).update(
        status=1,
        verified=None,
        verified_date=None,
    )
