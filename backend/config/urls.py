from django.urls import path
from catalogue import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/health/", views.health, name="health"),
    path("api/products/", views.products, name="products"),
    path("api/enquiry/", views.enquiry, name="enquiry"),
]
