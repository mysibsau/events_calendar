from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone

from events.models import Event


def verify_event(event_id: int, user: AbstractBaseUser):
    Event.objects.filter(id=event_id).update(
        verified=user,
        verified_date=timezone.now(),
    )


def cancel_event_verification(event_id: int):
    Event.objects.filter(id=event_id).update(
        verified=None,
        verified_date=None,
    )
