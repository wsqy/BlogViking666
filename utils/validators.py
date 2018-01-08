
from django.core import validators

def IntValidators(min=1, max=100):
    validatorsList = []
    if isinstance(min, int):
        validatorsList.append(validators.MinValueValidator(min, message=('不能小于%(limit_value)s.')))
    if isinstance(max, int):
        validatorsList.append(validators.MaxValueValidator(max, message=('不能大于%(limit_value)s.')))

    return validatorsList
