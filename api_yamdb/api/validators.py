from rest_framework.exceptions import ValidationError
#Тут нужна моделька переопределенного юзера
from reviews.models import User
import re


def validate_username (value):
    if value == 'me':
        raise ValidationError('Недопустимое имя пользователя!')
    elif User.objects.filter(username=value).exists():
        raise ValidationError(
            'Пользователь с таким именем уже зарегестрирован!'
        )
    elif not re.match(r'^[\w.@+-]', value):
        raise ValidationError(
            'Username не соответствует требованиям!'
        )



def validate_email (value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            'Пользователь с такой почтой уже зарегестрирован'
        )