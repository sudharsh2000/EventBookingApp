from rest_framework import serializers
from events.models import Category, Event


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "vendor", "category", "title", "description", "venue", "city",
                  "start_time", "end_time", "total_seats", "available_seats", "price", "status"]
        read_only_fields = ["available_seats"]