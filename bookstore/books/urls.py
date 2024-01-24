from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt

from books import views

router = DefaultRouter()
router.register('book', views.BooksViewSet, basename="book")
router.register('author', views.AuthorViewSet, basename="author")


urlpatterns = [
    path('', include(router.urls)),
    path("history/<int:id>/", views.HistoryView.as_view(), name="history"),
    path('leftover/add/', views.AddLeftOversAPIView.as_view(), name="left_over_add"),
    # path('leftover/bulk/', views.StoringInformationViewSet, basename="StoringInformation"),
    path('leftover/remove/', views.RemoveLeftOversAPIView.as_view(), name="left_over_remove"),
    path('bulkimport/',views.BulkImportView.as_view(),name="bulkimport"),    
]