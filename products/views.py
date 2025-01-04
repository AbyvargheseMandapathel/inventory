from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from users.permissions import *
from .models import Product, Category, StockTransaction
from .serializers import ProductSerializer, CategorySerializer, StockTransactionSerializer
from users.models import User  # Ensure the User model is imported
import csv
import io
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Product, Category
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
import csv
from io import StringIO
from .models import Product, Category
from django.http import HttpResponse
from rest_framework.decorators import permission_classes


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        # Admin can create/update/delete products, Manager can only view/edit products
        if self.action in ['create', 'update', 'destroy']:
            self.permission_classes = [IsAdmin]
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsManager]  # Manager and Admin can view products
        return super().get_permissions()


# Stock Transaction ViewSet: Staff can create transactions; Manager and Admin can manage
class StockTransactionViewSet(ModelViewSet):
    queryset = StockTransaction.objects.all()
    serializer_class = StockTransactionSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            self.permission_classes = [IsManager | IsStaff]  # Staff and Manager can perform stock transactions
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [IsStaff]  # Staff and Admin can view transactions
        return super().get_permissions()


# Export Products as CSV
@permission_classes([IsAdminUser])  # Only Admin can access this view
class ProductExportView(APIView):
    def get(self, request, *args, **kwargs):
        # Query the products and related categories
        products = Product.objects.select_related('product_category').all()
        
        # Prepare CSV data
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Product Name', 'Description', 'Category', 'Model Number', 
            'Serial Number', 'Stock Level', 'Reorder Point', 
            'Supplier Name', 'Supplier Email', 'Supplier Contact', 
            'Order Date', 'Quantity', 'Order Status'
        ])
        
        for product in products:
            writer.writerow([
                product.product_name, product.description, product.product_category.name if product.product_category else '',
                product.model_number, product.serial_number, product.stock_level, product.reorder_point, 
                product.supplier_name, product.supplier_email, product.supplier_contact, 
                product.order_date, product.quantity, product.order_status
            ])
        
        return response


class ProductImportView(APIView):
    permission_classes = [IsAdminUser]  # Only Admin can access this view
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file', None)
        if not file:
            return Response({'detail': 'No file provided'}, status=400)

        # Read the CSV file data
        file_data = file.read().decode("utf-8")
        csv_reader = csv.reader(StringIO(file_data))
        next(csv_reader)  # Skip header row

        for row in csv_reader:
            product_name, description, category_name, model_number, serial_number, stock_level, reorder_point, supplier_name, supplier_email, supplier_contact, order_date, quantity, order_status = row
            
            # Create or get the category
            category, created = Category.objects.get_or_create(name=category_name)
            
            # Create the Product
            Product.objects.create(
                product_name=product_name,
                description=description,
                product_category=category,
                model_number=model_number,
                serial_number=serial_number,
                stock_level=int(stock_level),
                reorder_point=int(reorder_point),
                supplier_name=supplier_name,
                supplier_email=supplier_email,
                supplier_contact=supplier_contact,
                order_date=order_date,
                quantity=int(quantity),
                order_status=order_status
            )

        return Response({'detail': 'Products imported successfully'}, status=201)


