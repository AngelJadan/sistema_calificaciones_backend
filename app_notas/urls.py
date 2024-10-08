"""
URL configuration for app_notas project.

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
from django.urls import path, re_path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from persona import views as views_persona

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path(
        "openapi/",
        get_schema_view(
            title="School Service",
            description="API developers hpoing to use our service",
            version="1.0.0",
        ),
        name="openapi-schema",
    ),
    path(
        "documentation/",
        TemplateView.as_view(
            template_name="documentation_api.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="documentation",
    ),
    path("obtener_token/", views_persona.obtener_token),
    path("log_out/", views_persona.Logout.as_view()),
    path("persona/", include("persona.urls")),
    path("calificacion/", include("calificacion.urls")),
    path("curso/", include("curso.urls")),
]
