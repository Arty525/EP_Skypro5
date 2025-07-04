from rest_framework import serializers
from .models import User, Payments


class UserSerializer(serializers.ModelSerializer):
    payment_history = serializers.SerializerMethodField()

    def get_payment_history(self, instance):
        payment_history = instance.payments_set.all()
        return PaymentSerializer(payment_history, many=True).data

    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"
