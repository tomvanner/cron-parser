class ValidationError(Exception):
    pass


class InvalidCronExpressionError(ValidationError):
    pass


class InvalidCronValueError(ValidationError):
    pass