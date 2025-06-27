from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Payments, User
from .serializers import UserSerializer, PaymentSerializer
from rest_framework import viewsets, generics


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']