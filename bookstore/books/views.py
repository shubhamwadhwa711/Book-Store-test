from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from books.models import Book, Author, StoringInformation
from drf_yasg.utils import swagger_auto_schema
from django.views.decorators.csrf import csrf_exempt
from books.serializers import BookSerializer, AuthorSerializer, BookReadSerializer, HistoryReadSerializer, LeftOverSerializer

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