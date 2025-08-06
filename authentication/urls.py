from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView, TokenObtainPairView, TokenVerifyView
from . import views
from .views import register, activate_user, login, logout, delete_user, reset_password, forgot_password
# protected_example, public_example

urlpatterns = [
    # Register a new user and send activation email
    path('register/', register, name='register'),
    # Activate user account via token (from email)
    path('activate/<str:token>/', activate_user, name='activate'),
    # Log in with email/username and password, return JWT
    path('login/', login, name='login'),
    # Blacklist a refresh token (used for logout)
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    # path('logout/', logout, name='logout'),

    # Send reset link to user's email
    # path('reset_password/', reset_password, name='reset_password'),
    # Reset password using the link token
    # path('reset_password/<str:token>/', password_reset_confirm, name='password_reset_confirm'),
    path("reset-password/<str:token>/", reset_password, name="reset_password"),
     # Authenticated user changes password manually
    # path('password-change/', change_password, name='password_change'),
    path("forgot-password/", forgot_password, name="forgot_password"),
    # Refresh access token using refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Verify a given access or refresh token is valid
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("user/delete/", views.delete_user, name="delete-user"),
    path('user/', views.get_user_details, name='user-details'),  # ✅ New endpoint
    #path('reset-password-confirm/<uidb64>/<token>/', reset_password_confirm, name='reset-password-confirm'),
    # path('protected/', protected_example, name='protected_example'),
    # path('public/', public_example, name='public_example'),
    
    
] 
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

# path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair')
#    # Use built-in JWT views
#     path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Login
#     path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
#     path("logout/", TokenBlacklistView.as_view(), name="token_blacklist"),