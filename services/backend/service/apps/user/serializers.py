from rest_framework import serializers

from django.db import transaction


from apps.models import User


class RegistrationSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = (
            'role',
        )

    @transaction.atomic()
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            surname=validated_data['surname'],
            password=validated_data['password'],
        )
        return user


class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'name', 'surname', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = (
            'email',
            'role',
        )

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)
