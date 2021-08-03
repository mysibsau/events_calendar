from user.models import User


def __user_builder(user_id: int, **kwargs) -> bool:
    users = User.objects.filter(id=user_id)
    if len(users) != 1:
        return False

    users.update(**kwargs)
    return True


def confirm_user(user_id: int) -> bool:
    return __user_builder(
        user_id,
        confirmed=True,
        is_active=True,
    )


def ban_user(user_id: int) -> bool:
    return __user_builder(
        user_id,
        confirmed=False,
        is_active=False,
        is_staff=False,
    )


def make_user_staff(user_id: int) -> bool:
    return __user_builder(
        user_id,
        confirmed=True,
        is_active=True,
        is_staff=True,
    )
