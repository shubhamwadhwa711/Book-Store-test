from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from books.models import Book, Author, StoringInformation
from books.serializers import BookSerializer, AuthorSerializer, StoringInformationSerializer, BookReadSerializer, HistoryReadSerializer

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

class StoringInformationViewSet(ModelViewSet):
    # http_method_names = ["POST"]
    queryset = StoringInformation.objects.all()
    serializer_class = StoringInformationSerializer

class HistoryView(APIView):
    def get(self, request, id,*args, **kwargs):
        book = get_object_or_404(Book, pk=id)
        serializer = HistoryReadSerializer(book)
        return Response(serializer.data)