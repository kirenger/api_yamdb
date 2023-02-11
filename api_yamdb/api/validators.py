import re

from rest_framework.exceptions import ValidationError

from users.models import User


def validate_username(value):
    if value == 'me':
        raise ValidationError('Недопустимое имя пользователя!')
    if User.objects.filter(username=value).exists():
        raise ValidationError(
            'Пользователь с таким именем уже зарегестрирован!'
        )
    if not re.match(r'^[\w.@+-]', value):
        raise ValidationError(
            'Username не соответствует требованиям!'
        )


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            'Пользователь с такой почтой уже зарегестрирован'
        )
