from django.contrib import admin
from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from first_part import views

# URL configuration for the API endpoints
urlpatterns = [
    path('admin/', admin.site.urls),

    # Get latest plane data by call sign
    path('api/plane/<str:callsign>/', views.PlaneDetailView.as_view()),

    # User registration
    path('api/register/', views.RegisterView.as_view(), name='register'),

    # JWT login (token generation)
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # JWT token refresh
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Get previous plane positions within last 5 minutes
    path('api/previousePositions/<str:call_sign>/', views.PreviousePositionsView.as_view(), name='previouse_positions'),

    # User account info (GET/PUT/DELETE)
    path('api/account/', views.AccountInfoView.as_view(), name='account-info'),
]

# Include Django Debug Toolbar URLs
urlpatterns += debug_toolbar_urls()
