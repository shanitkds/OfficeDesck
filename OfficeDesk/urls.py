"""
URL configuration for OfficeDesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/organisation/',include('organizations.urls')),
    path('api/account/',include('account.urls')),
    path('api/org_admin/',include('org_admin.urls')),
    path('api/team_lead/',include('teamlead.urls')),
    path('api/tasks/',include('tasks.urls')),
    path("api/attendance/", include("attendance.urls")),
    path("api/acccountent/", include("accountant.urls")),
    path("api/chat/", include("chat.urls")),
    path("api/encryptfile/", include("secure_files.urls")),
    path("api/performance/", include("performance.urls")),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )