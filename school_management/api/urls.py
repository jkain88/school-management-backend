from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
  path('account/', include('school_management.account.urls')),
  path('token', TokenObtainPairView.as_view(), name='token_obtain')
]
