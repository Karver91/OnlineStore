from django.urls import path, include
from rest_framework import routers

from api.views import InventoryModelViewSet, CartModelViewSet

app_name = 'OnlineStore_api'

router = routers.DefaultRouter()
router.register(r'products', InventoryModelViewSet)
router.register(r'cart', CartModelViewSet)


urlpatterns = [
    path('', include(router.urls))
]
