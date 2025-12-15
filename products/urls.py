from django.urls import path
from .views import ProductListView, ProductDetailView, ProductSearchView

app_name = 'products'

urlpatterns = [
    path("search/", ProductSearchView.as_view(), name="product_search"),
    
    path("<slug:slug>/", ProductDetailView.as_view(), name="detail"),
    
    path("", ProductListView.as_view(), name="list"),


]
