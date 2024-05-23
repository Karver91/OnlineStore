from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from products.models import Inventory, Cart
from products.serializers import InventorySerializer, CartSerializer


class InventoryModelViewSet(ModelViewSet):
    queryset = Inventory.objects.filter(quantity__gt=0)
    serializer_class = InventorySerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'destroy'):
            self.permission_classes = (IsAdminUser, )
        return super().get_permissions()


class CartModelViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
