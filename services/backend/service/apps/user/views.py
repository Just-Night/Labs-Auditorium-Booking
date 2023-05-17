from rest_framework import generics, permissions
from apps.models import User
from apps.user import serializers
# from apps.auditorium.serializers import OrderSerializer


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = serializers.RegistrationSerializers


class UserAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserSerializers
    queryset = User.objects.all()


# class UserOrderAPIView(generics.ListAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = OrderSerializer

#     def get_queryset(self):
#         user_id = self.kwargs['pk']
#         return self.request.user.orders.filter(user_id=user_id)


class LoginAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserSerializers

    def get_object(self):
        return self.request.user
