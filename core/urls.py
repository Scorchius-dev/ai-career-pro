"""
URL configuration for core project.

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
from django.urls import path, include
# Step 1: Add cv_update and cv_delete to your imports
from builder.views import (
    index, signup, cv_create, dashboard, cv_update, cv_delete
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),

    # Create
    path('cv/new/', cv_create, name='cv_create'),

    # Read
    path('dashboard/', dashboard, name='dashboard'),

    # Update (The <int:pk> captures the ID of the CV you want to edit)
    path('cv/<int:pk>/edit/', cv_update, name='cv_update'),

    # Delete
    path('cv/<int:pk>/delete/', cv_delete, name='cv_delete'),

    path('', index, name='index'),
]
