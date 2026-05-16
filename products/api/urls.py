from django.urls import path
from .views import (
     ProductListAPI,
     ProductDetailAPI,
     ProductSearchAPI,
     RecommendationProductAPI
)

app_name = "products_api"
urlpatterns = [
    path("products-list/", ProductListAPI.as_view(), name="product_list"),

    path("recommendation/", RecommendationProductAPI.as_view(),
         name="Recommendation_Product"),

    path("products-detail/<slug:slug>/", ProductDetailAPI.as_view(),
         name="product_detail"),

    path("search/", ProductSearchAPI.as_view(), name="produt_search"),

]