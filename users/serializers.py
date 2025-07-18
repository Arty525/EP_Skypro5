from rest_framework import serializers

from materials.services import session_checkout
from .models import User, Payments


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
    groups = serializers.StringRelatedField(many=True)

    def get_payment_history(self, instance):
        payment_history = instance.payments_set.all()
        for payment in payment_history:
            if payment.session_id is not None:
                payment.status = session_checkout(payment.session_id)
                payment.save()
        return PaymentSerializer(payment_history, many=True).data

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "groups",
            "first_name",
            "last_name",
            "city",
            "phone_number",
            "avatar",
            "payment_history",
        ]


class PrivateUserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ["id", "email", "groups", "first_name", "city"]


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"
