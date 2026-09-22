from rest_framework.views import exception_handler as drf_handler
from rest_framework.response import Response


class DomainError(Exception):
    status_code = 400
    def __init__(self, message):
        self.message = message


class InvalidReferralCode(DomainError):
    pass


class NotEnoughSeats(DomainError):
    status_code = 409


class EventNotBookable(DomainError):
    pass


class BookingNotCancellable(DomainError):
    pass


def custom_exception_handler(exc, context):
    if isinstance(exc, DomainError):
        return Response({"error": exc.message}, status=exc.status_code)
    return drf_handler(exc, context)