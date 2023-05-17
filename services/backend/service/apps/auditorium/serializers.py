from rest_framework import serializers

from .models import Auditorium, Order


class AuditoriumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditorium
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'auditorium', 'reservation_date', 'start_datetime', 'end_datetime']
