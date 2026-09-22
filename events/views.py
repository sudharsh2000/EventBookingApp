import django_filters as filters
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from core.permissions import IsStaff
from events.models import Event
from events.serializers import EventSerializer


class EventFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Event
        fields = ["city", "category", "min_price", "max_price"]


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    filterset_class = EventFilter
    search_fields = ["title", "venue", "city"]

    def get_queryset(self):
        qs = Event.objects.all()
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return qs
        return qs.filter(status="published")

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsStaff()]