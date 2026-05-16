from django.urls import path
from .views import ProductCommentAPI

app_name = "comments_api"
urlpatterns = [
    path("<slug:slug>/", ProductCommentAPI.as_view(),
         name="product_comments"),
]