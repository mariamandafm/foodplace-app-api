from rest_framework import viewsets, permissions, authentication

from core.models import (
    FoodItem,
    Order,
    )
from menu import (
    serializers,

)


class AuthenticatedForWriteMethods(permissions.BasePermission):
    """
    Custom permisson class to require authentication for write methods.
    """

    def has_permission(self, request, view):
        # Safe methods: GET and HEAD.
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated


class FoodItemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FoodItemDetailSerializer
    queryset = FoodItem.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [AuthenticatedForWriteMethods]

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.FoodItemSerializer

        return self.serializer_class


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
