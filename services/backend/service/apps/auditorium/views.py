from datetime import datetime, time

from apps.perm import IsAdmin
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Auditorium, Order
from .serializers import AuditoriumSerializer, OrderSerializer


class AuditoriumList(generics.ListAPIView):
    queryset = Auditorium.objects.all()
    serializer_class = AuditoriumSerializer


class AuditoriumCreate(generics.CreateAPIView):
    queryset = Auditorium.objects.all()
    serializer_class = AuditoriumSerializer
    permission_classes = [IsAdmin, permissions.IsAuthenticated]


class AuditoriumDetail(generics.RetrieveAPIView):
    queryset = Auditorium.objects.all()
    serializer_class = AuditoriumSerializer


class AuditoriumUpdate(generics.UpdateAPIView):
    queryset = Auditorium.objects.all()
    serializer_class = AuditoriumSerializer
    permission_classes = [IsAdmin, permissions.IsAuthenticated]


class AuditoriumDestroy(generics.DestroyAPIView):
    queryset = Auditorium.objects.all()
    serializer_class = AuditoriumSerializer
    permission_classes = [IsAdmin, permissions.IsAuthenticated]


class OrderCreate(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def create(self, request, *args, **kwargs):
        # Отримуємо дані з запиту
        user = request.data.get('user')
        auditorium = request.data.get('auditorium')
        reservation_date = request.data.get('reservation_date')
        start_datetime = request.data.get('start_datetime')
        end_datetime = request.data.get('end_datetime')

        # Перевіряємо, чи значення start_datetime та end_datetime є null
        if start_datetime is None and end_datetime is None:
            # Якщо так, встановлюємо значення start_datetime та end_datetime на початок та кінець дня відповідно
            start_datetime = time(0, 0, 0)
            end_datetime = time(23, 59, 59)
        else:
            # Якщо значення start_datetime та end_datetime є рядками, то переводимо їх у час
            if isinstance(start_datetime, str):
                start_datetime = datetime.strptime(start_datetime, '%H:%M:%S').time()
            if isinstance(end_datetime, str):
                end_datetime = datetime.strptime(end_datetime, '%H:%M:%S').time()

        # Перевіряємо, чи існує вже замовлення з такою ж датою та часом
        conflicts = Order.objects.filter(
            Q(
                reservation_date=reservation_date,
                start_datetime__lte=start_datetime,
                end_datetime__gt=start_datetime
            ) |
            Q(
                reservation_date=reservation_date,
                start_datetime__lt=end_datetime,
                end_datetime__gte=end_datetime
            )
        )

        # Якщо конфліктів не має, створюємо нове замовлення
        if not conflicts:
            order = Order.objects.create(
                user_id=user,
                auditorium_id=auditorium,
                reservation_date=reservation_date,
                start_datetime=start_datetime,
                end_datetime=end_datetime
            )
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'message': 'Order conflicts with an existing reservation'},
                status=status.HTTP_409_CONFLICT
            )


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()

    def put(self, request, *args, **kwargs):
        # Отримуємо об'єкт Order за id
        order = self.get_object()

        # Отримуємо дані з запиту
        user = request.data.get('user', order.user_id)
        auditorium = request.data.get('auditorium', order.auditorium_id)
        reservation_date = request.data.get('reservation_date', order.reservation_date)
        start_datetime = request.data.get('start_datetime', order.start_datetime)
        end_datetime = request.data.get('end_datetime', order.end_datetime)

        # Перевіряємо, чи значення start_datetime та end_datetime є null
        if start_datetime is None and end_datetime is None:
            # Якщо так, встановлюємо значення start_datetime та end_datetime на початок та кінець дня відповідно
            start_datetime = time(0, 0, 0)
            end_datetime = time(23, 59, 59)
        else:
            # Якщо значення start_datetime та end_datetime є рядками, то переводимо їх у час
            if isinstance(start_datetime, str):
                start_datetime = datetime.strptime(start_datetime, '%H:%M:%S').time()
            if isinstance(end_datetime, str):
                end_datetime = datetime.strptime(end_datetime, '%H:%M:%S').time()

        # Перевіряємо, чи існує вже замовлення з такою ж датою та часом, окрім поточного замовлення
        conflicts = Order.objects.filter(
            ~Q(pk=order.pk),
            Q(reservation_date=reservation_date,
              start_datetime__lte=start_datetime,
              end_datetime__gt=start_datetime) |
            Q(reservation_date=reservation_date,
              start_datetime__lt=end_datetime,
              end_datetime__gte=end_datetime)
        )

        # Якщо конфліктів не має, зберігаємо зміни
        if not conflicts:
            order.user_id = user
            order.auditorium_id = auditorium
            order.reservation_date = reservation_date
            order.start_datetime = start_datetime
            order.end_datetime = end_datetime
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'message': 'Order conflicts with an existing reservation'},
                status=status.HTTP_409_CONFLICT
            )
