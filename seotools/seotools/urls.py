"""seotools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from seotools.grades.views import grades
from seotools.grades.views import cssvalidation
from seotools.grades.views import imageanalysis
from seotools.grades.views import keyworddensity
from seotools.grades.views import hostgator
from seotools.grades.views import ourocred
from seotools.grades.views import adv
from seotools.grades.views import ole

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('grades/', grades),
    path('cssvalidation/', cssvalidation),
    path('imageanalysis/', imageanalysis),
    path('keyworddensity/', keyworddensity),
    path('hostgator/', hostgator),
    path('ourocred/', ourocred),
    path('adv/', adv),
    path('ole/', ole),
]

urlpatterns += staticfiles_urlpatterns()
