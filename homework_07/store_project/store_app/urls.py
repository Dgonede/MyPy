
from django.urls import path

from .views import ProductsIndexView
app_name ="store_app"

urlpatterns = [
    path("", ProductsIndexView.as_view(), name="products_index"),
    
]

