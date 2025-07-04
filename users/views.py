from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Payments, User
from .permissions import IsCurrentUser
from .serializers import UserSerializer, PaymentSerializer
from rest_framework import viewsets, generics
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        queryset = User.objects.values('id', 'email', 'first_name', 'phone_number', 'city')
        return Response(queryset)

    def retrieve(self, request, pk=None):
        if self.request.user == User.objects.get(pk=pk):
            queryset = User.objects.values().get(pk=pk)
            return Response(queryset)
        else:
            queryset = User.objects.values('id', 'email', 'first_name', 'phone_number', 'city').get(pk=pk)
            return Response(queryset)

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            self.permission_classes = (IsCurrentUser,)
        return super().get_permissions()

class PaymentListAPIView(generics.ListAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']