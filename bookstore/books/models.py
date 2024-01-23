from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
from django.urls import reverse

class Author(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    birth_date = models.DateField(_("Birth Date"))    

    class Meta:
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("author-detail", kwargs={"pk": self.pk})



class Book(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    publish_year = models.IntegerField(_("Publish Year"))
    author = models.ForeignKey("books.Author", on_delete=models.CASCADE)
    barcode = models.CharField(_("Barcode"), max_length=100, null=True, blank=True)
    available_quantity = models.PositiveIntegerField(_("Available Quantity"), default=0)
    

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"pk": self.pk})


class StoringInformation(models.Model):
    ACTION_CHOICES = (("+", "Add"),("-", "Remove"))
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("Quantity"))
    action = models.CharField(_("Action"), choices=ACTION_CHOICES, max_length=10)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("StoringInformation")
        verbose_name_plural = _("StoringInformations")

    def __str__(self):
        return self.book.title

    def get_absolute_url(self):
        return reverse("StoringInformation-detail", kwargs={"pk": self.pk})
