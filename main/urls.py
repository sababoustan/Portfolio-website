from django.urls import path
from .views import HomeView, dashboard_view

app_name = 'main'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
