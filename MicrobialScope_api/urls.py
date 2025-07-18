"""
URL configuration for MicrobialScope_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/microbe/', include('microbe_database.urls')),
    path('api/archaea/', include('archaea_database.urls')),
    path('api/bacteria/', include('bacteria_database.urls')),
    path('api/fungi/', include('fungi_database.urls')),
    path('api/viruses/', include('viruses_database.urls')),
    path('api/largetable/', include('large_table_api.urls')),
    path('api/analysis/', include('analysis.urls'))
]
