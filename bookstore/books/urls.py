from django.urls import path, include
from rest_framework.routers import DefaultRouter
from books import views

router = DefaultRouter()
router.register('book', views.BooksViewSet, basename="book")
router.register('author', views.AuthorViewSet, basename="author")
router.register('leftover', views.StoringInformationViewSet, basename="StoringInformation")


urlpatterns = [
    path('', include(router.urls)),
    path("history/<int:id>/", views.HistoryView.as_view(), name="history"),
]