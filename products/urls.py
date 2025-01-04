from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductExportView, ProductImportView, ProductViewSet, StockTransactionViewSet
from . import views


router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'stock-transactions', StockTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('products/export/', ProductExportView.as_view(), name='product-export'),
    path('products/import/', ProductImportView.as_view(), name='product-import'),
]
