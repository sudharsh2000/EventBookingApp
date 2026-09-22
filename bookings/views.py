from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from bookings import services
from bookings.models import Booking
from bookings.serializers import BookingCreateSerializer, BookingSerializer


class BookingViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = BookingSerializer

    def get_queryset(self):
        qs = Booking.objects.all()
        return qs if self.request.user.is_staff else qs.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        s = BookingCreateSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        booking = services.create_booking(user=request.user, **s.validated_data)
        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        booking = services.cancel_booking(user=request.user, booking_id=pk)
        return Response(BookingSerializer(booking).data)

