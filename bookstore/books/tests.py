from django.test import TestCase
from django.urls import reverse
from .models import Author, Book, StoringInformation

class AuthorModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author", birth_date="2000-01-01")

    def test_author_str(self):
        self.assertEqual(str(self.author), "Test Author")

    def test_author_absolute_url(self):
        url = reverse("author-detail", kwargs={"pk": self.author.pk})
        self.assertEqual(self.author.get_absolute_url(), url)


class BookModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author", birth_date="2000-01-01")
        self.book = Book.objects.create(title="Test Book", publish_year=2022, author=self.author, barcode="123")

    def test_book_str(self):
        self.assertEqual(str(self.book), "Test Book")

    def test_book_absolute_url(self):
        url = reverse("book-detail", kwargs={"pk": self.book.pk})
        self.assertEqual(self.book.get_absolute_url(), url)

    def test_book_quantity(self):
        storing_info = StoringInformation.objects.create(book=self.book, quantity=5)
        self.assertEqual(self.book.quantity, 5)


class StoringInformationModelTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author", birth_date="2000-01-01")
        self.book = Book.objects.create(title="Test Book", publish_year=2022, author=self.author, barcode="123")
        self.storing_info = StoringInformation.objects.create(book=self.book, quantity=5)

    def test_storing_info_str(self):
        self.assertEqual(str(self.storing_info), "Test Book")

    def test_storing_info_absolute_url(self):
        url = reverse("StoringInformation-detail", kwargs={"pk": self.storing_info.pk})
        self.assertEqual(self.storing_info.get_absolute_url(), url)
