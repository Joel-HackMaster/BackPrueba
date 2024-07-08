"""
URL configuration for BackPrueba project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.users.api.views.views import LoginAPIView, TestingLogueo, LogoutApiView
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login', LoginAPIView.as_view(), name='login'),
    path('api/logout', LogoutApiView.as_view(), name='logout'),
    path('api/test', TestingLogueo.as_view(), name='test'),
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.api.routers'), name='users_api'),
    path('docs/', include_docs_urls(title="Task API"))
]
