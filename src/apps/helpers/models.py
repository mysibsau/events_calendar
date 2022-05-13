from typing import Type

from django.db import models


def enum_max_length(text_choices: Type[models.Choices]) -> int:
    return max(len(value) for value in text_choices.values)
