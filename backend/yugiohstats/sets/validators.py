from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
from helpers.validators import get_valid_set_codes


def validate_set_code(value):
    if str(value).upper() not in get_valid_set_codes:
        raise serializers.ValidationError(f'{value} is not a valid set code (eg: \'RA01\')')
    return str(value).upper()

# unique_set_link = UniqueValidator(queryset=Set.objects.all())