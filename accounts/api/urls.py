from django.urls import path
from accounts.api.views import (
    RegisterAPI,
    UserListAPI,
    LoginAPI,
    AccountMeAPI,
    AdminDeleteUserAPI,
    LogoutAPI,
    PasswordChangeAPI,
    CheckoutAPI,
    ConfirmOrderAPI,
    ProfileAPI
)

app_name = "accounts_api"
urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="register"),
    path("users/", UserListAPI.as_view(), name="users"),
    path("login/", LoginAPI.as_view(), name="login"),
    path("accounts/me/", AccountMeAPI.as_view(), name="accounts_delete"),
    path("accounts/<int:id>/", AdminDeleteUserAPI.as_view(),
         name="accounts-delete-admin"),
    path("logout/", LogoutAPI.as_view(), name="logout"),
    path("accounts/change-password/", PasswordChangeAPI.as_view(),
         name="change_password"),
    path("accounts/checkout/", CheckoutAPI.as_view(),
         name="checkout"),
    path("accounts/confirm-order/", ConfirmOrderAPI.as_view(),
         name="confimorder"),
    path("profile/", ProfileAPI.as_view(), name="profile"),
]