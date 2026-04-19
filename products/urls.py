from django.urls import path
from .views import ProductDetailView, ProductSearchView, ProductPageView

app_name = 'products'

urlpatterns = [
    path("search/", ProductSearchView.as_view(), name="product_search"),

    path("products/<slug:slug>/", ProductPageView.as_view(), 
         name="product_page"),

    path("<slug:slug>/", ProductDetailView.as_view(), name="detail"),

]
