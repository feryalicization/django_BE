from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.urls import path
from .views import *




schema_view = get_schema_view(
    openapi.Info(
        title="PT Qtasnim Digital Teknologi",
        default_version='v1',
        description="API for PT Qtasnim Digital Teknologi Test",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [

    path('api/token/', CustomObtainAuthToken.as_view(), name='api_token'),
    path('api/register/', UserRegistrationView.as_view(), name='user_register'),

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]