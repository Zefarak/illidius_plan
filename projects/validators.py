from django.core.exceptions import ValidationError
from django.conf import settings


def validate_image(value):
    if value.file.size > settings.MAX_FILE_SIZE:
        raise ValidationError('Size is big than 2 mb')
