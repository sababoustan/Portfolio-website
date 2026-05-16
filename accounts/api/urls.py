from django.urls import path
from rest_framework_simplejwt.views import (
     TokenObtainPairView, TokenRefreshView)
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
     path('token/', TokenObtainPairView.as_view(),
          name='token_obtain_pair'),
     path('token/refresh/', TokenRefreshView.as_view(),
          name='token_refresh'),
     path("register/", RegisterAPI.as_view(), name="register"),
     path("users/", UserListAPI.as_view(), name="users"),
     path("login/", LoginAPI.as_view(), name="login"),
     path("accounts/me/", AccountMeAPI.as_view(), name="accounts_delete"),
     path("accounts/<int:id>/", AdminDeleteUserAPI.as_view(),
          name="accounts-delete-admin"),
     path("logout/", LogoutAPI.as_view(), name="logout"),
     path("accounts/change-password/", PasswordChangeAPI.as_view(),
          name="change_password"),
     path("checkout/", CheckoutAPI.as_view(),
          name="checkout"),
     path("confirm-order/", ConfirmOrderAPI.as_view(),
          name="confimorder"),
     path("profile/", ProfileAPI.as_view(), name="profile"),
]