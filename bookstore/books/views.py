from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from books.models import Book, Author, StoringInformation
from drf_yasg.utils import swagger_auto_schema
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from rest_framework import status
import re
from books.serializers import BookSerializer, AuthorSerializer, BookReadSerializer, HistoryReadSerializer, LeftOverSerializer,BulkImportSerializer

class BooksViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['barcode']

    def get_serializer_class(self):
        if self.request.method=="GET":
            return BookReadSerializer
        return super().get_serializer_class()

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AddLeftOversAPIView(APIView):
    # @csrf_exempt
    @swagger_auto_schema(operation_description="description")
    def post(self, request, *args, **kwargs):
        request.data["action"] = "+"
        serializer = LeftOverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"massage":"Quantity updated"})
        return Response(serializer.errors)

class RemoveLeftOversAPIView(APIView):
    # @csrf_exempt
    @swagger_auto_schema(operation_description="description")
    def post(self, request, *args, **kwargs):
        request.data["action"] = "-"
        serializer = LeftOverSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"massage":"Quantity updated"})
        return Response(serializer.errors)

class HistoryView(APIView):
    def get(self, request, id,*args, **kwargs):
        book = get_object_or_404(Book, pk=id)
        serializer = HistoryReadSerializer(book, context={"request":request})
        data = serializer.data
        addition = sum(map(lambda x: x['quantity'],filter(lambda x:x['action']=='+',data['history'])))
        data["start_balance"] = addition
        data["end_balance"] = addition - sum(map(lambda x: x['quantity'],filter(lambda x:x['action']=='-',data['history'])))
        return Response(data)
    
class BulkImportView(APIView):
    def post(self, request,*args, **kwargs):
        serializer = BulkImportSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES.get("upload_file")
            if file.name.endswith('.xlsx'):
                print(file.name.endswith('.xlsx'))
                return self.handle_excel(file)
            elif file.name.endswith('.txt'):
                return self.handle_text(file)
            else:
                return Response({"error": "Unsupported file format"})
        return Response(serializer.errors)
    
    def handle_excel(self, file):
        df = pd.read_excel(file)  
        print(df)
        try:
            for index, row in df.iterrows():
                barcode = row['barcode']
                available_quantity = int(row['available_quantity'])
                action = '+' if available_quantity>0 else  '-'
                available_quantity = abs( available_quantity)
                data = {'barcode':str(barcode), 'quantity':available_quantity, 'action' : action}
                print(data)                   
                serializer = LeftOverSerializer(data = data)
                if serializer.is_valid(raise_exception = True):
                    serializer.save()                   
                    return Response({"message": "Data uploaded successfully"},status= status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Exception occurred: {e}")
            return Response({"message":"Please check your file"}, status= status.HTTP_422_UNPROCESSABLE_ENTITY)

    def handle_text(self, file): 
        try:      
            for line in file:
                    # Use regular expression to extract alphabets (barcode) and integers (quantity)
                    line_str = line.decode('utf-8').strip()
                    match = re.match(r'([A-Za-z]+)([0-9-]+)', line_str)                
                    if match:
                        barcode = match.group(1)
                        quantity = int(match.group(2))
                        action = '+' if quantity > 0 else '-'
                        quantity = abs(quantity)
                        data = {'barcode': barcode, 'quantity': quantity, 'action': action}
                        print(data)
                        serializer = LeftOverSerializer(data = data)
                        if serializer.is_valid(raise_exception = True):
                            serializer.save()  
            return Response({"message": "Data uploaded successfully"},status= status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Exception occurred: {e}")
            return Response({"message": "Please check your file"}, status=422)
                
   