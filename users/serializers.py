from rest_framework import serializers
from .models import User, Payments
from .permissions import IsCurrentUser

class UserSerializer(serializers.ModelSerializer):
    payment_history = serializers.SerializerMethodField()

    def get_payment_history(self, instance):
        payment_history = instance.payments_set.all()
        return PaymentSerializer(payment_history, many=True).data

    class Meta:
        model = User
        fields = "__all__"


class FullUserSerializer(serializers.ModelSerializer):
    payment_history = serializers.SerializerMethodField()

    def get_payment_history(self, instance):
        payment_history = instance.payments_set.all()
        return PaymentSerializer(payment_history, many=True).data

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "city", "phone_number", "avatar", "payment_history"]

class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "city"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"
