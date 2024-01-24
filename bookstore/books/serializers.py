from rest_framework import serializers
from books.models import Book, Author, StoringInformation
from datetime import date
from django.shortcuts import get_object_or_404
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

    def validate_birth_date(self, value):
        if value <= date(1990,1,1):
            raise serializers.ValidationError("Birth Date Must Be Grater than 01/01/1900")
        return value


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"

    def validate_publish_year(self, value):
        if value <= 1900:
            raise serializers.ValidationError("Publish Year Must Be Grater than 1900")
        return value


class BookReadSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    class Meta:
        model = Book
        fields = "__all__"
    
    
class LeftOverSerializer(serializers.Serializer):
    barcode = serializers.CharField(max_length=100)
    action = serializers.CharField(max_length=10)
    quantity = serializers.IntegerField()

    def validate(self, obj):
        book = get_object_or_404(Book, barcode=obj["barcode"])
        self.context["book"] = book
        if obj['quantity'] <=0:
            raise serializers.ValidationError("Please enter valid quantity")
        if obj["action"] == "-" and book.available_quantity - obj['quantity'] < 0:
            raise serializers.ValidationError("books can not be set to negative")
        return obj

    def create(self,validated_data):
        book = self.context["book"]
        StoringInformation.objects.create(book=book, quantity=validated_data["quantity"], action="+")
        if validated_data["action"] == "-":
            book.available_quantity -= validated_data["quantity"]
        else:
            book.available_quantity += validated_data["quantity"]
        book.save()
        return book


class HistoryBookReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title"]

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoringInformation
        fields = ['created_at','quantity', "action"]

class HistoryReadSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    history = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['book','history']

    def get_book(self, obj):
        return HistoryBookReadSerializer(obj).data

    def get_history(self, obj):
        request = self.context["request"]
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        qs = obj.storinginformation_set.all().order_by('-created_at')
        if start_date and end_date:
            qs.filter(created_at__gte=start_date, created_at__lte=end_date)
        elif start_date and not end_date:
            qs.filter(created_at__gte=start_date)
            return HistorySerializer(qs, many=True).data
        elif end_date and not start_date:
            qs.filter(created_at__lte=end_date)
        return HistorySerializer(qs, many=True).data
    
class BulkImportSerializer(serializers.Serializer):
    upload_file = serializers.FileField(required = True)