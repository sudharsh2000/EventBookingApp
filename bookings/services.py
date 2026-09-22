"""Seat arithmetic — locked, atomic, one place only."""
from django.db import transaction
from django.db.models import F
from bookings.models import Booking
from core.exceptions import NotEnoughSeats, EventNotBookable, BookingNotCancellable
from events.models import Event


@transaction.atomic
def create_booking(*, user, event_id, quantity):
    event = Event.objects.select_for_update().get(pk=event_id)  # lock the row

    if event.status != "published":
        raise EventNotBookable("Event is not open for booking.")
    if event.available_seats < quantity:
        raise NotEnoughSeats(f"Only {event.available_seats} seat(s) left.")

    updated = Event.objects.filter(pk=event.pk, available_seats__gte=quantity).update(available_seats=F("available_seats") - quantity)
    if updated == 0:
        raise NotEnoughSeats("Seats were just taken, try again.")

    return Booking.objects.create(user=user, event=event, quantity=quantity, total_amount=event.price * quantity)


@transaction.atomic
def cancel_booking(*, user, booking_id):
    booking = Booking.objects.select_for_update().get(pk=booking_id, user=user)
    if booking.status == "cancelled":
        raise BookingNotCancellable("Already cancelled.")

    booking.status = "cancelled"
    booking.save(update_fields=["status"])
    Event.objects.filter(pk=booking.event_id).update(available_seats=F("available_seats") + booking.quantity)
    return booking