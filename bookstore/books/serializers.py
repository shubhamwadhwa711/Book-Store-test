from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField, Serializer, ListField
from books.models import Book, Author, StoringInformation
from datetime import date

class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def validate_birth_date(self, value):
        if value <= date(1990,1,1):
            raise ValidationError("Birth Date Must Be Grater than 01/01/1900")
        return value


class BookSerializer(ModelSerializer):
    # author = AuthorSerializer()
    class Meta:
        model = Book
        fields = "__all__"

    def validate_publish_year(self, value):
        if value <= 1990:
            raise ValidationError("Publish Year Must Be Grater than 1900")
        return value


class BookReadSerializer(ModelSerializer):
    author = AuthorSerializer()
    quantity = SerializerMethodField()
    class Meta:
        model = Book
        fields = "__all__"
    
    def get_quantity(self, obj):
        return obj.quantity

    
class StoringInformationSerializer(ModelSerializer):
    class Meta:
        model = StoringInformation
        fields = "__all__"

class HistoryBookReadSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title"]

class HistorySerializer(ModelSerializer):
    class Meta:
        model = StoringInformation
        fields = ['created_at','quantity']

class HistoryReadSerializer(ModelSerializer):
    book = SerializerMethodField()
    history = SerializerMethodField()

    class Meta:
        model = Book
        fields = ['book', 'history']

    def get_book(self, obj):
        return HistoryBookReadSerializer(obj).data

    def get_history(self, obj):
        return HistorySerializer(obj.storinginformation_set.all().order_by('-created_at'), many=True).data