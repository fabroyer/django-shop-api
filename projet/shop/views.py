from rest_framework.viewsets import ReadOnlyModelViewSet

from shop.models import Category, Product
from shop.serializers import CategorySerializer, ProductSerializer


class CategoryViewset(ReadOnlyModelViewset):

    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()


class ProductViewset(ReadOnlyModelViewset):

    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

