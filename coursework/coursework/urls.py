"""
URL configuration for coursework project.

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
from django.urls import path, include, re_path
from flashcall_auth.views import *
from custom_auth.views import *
from groups.views import *
from lessons.views import *
from results.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/user/get_token', Flashcall_get.as_view()),
    path('api/v1/auth/user/check_token', Flashcall_check.as_view()),
    path('api/v1/auth/user/send_update_password_code', Flashcall_get_reset_password.as_view()),
    path('api/v1/auth/user/check_update_password_code', Flashcall_check_reset_password.as_view()),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/auth/user/',UserView.as_view()),
    path('api/v1/groups/',GroupAPIView.as_view()),
    path('api/v1/groups/<int:pk>/',GroupAPIView.as_view()),
    path('api/v1/lessons/',LessonAPIView.as_view()),
    path('api/v1/lessons/<int:pk>/',LessonAPIView.as_view()),
    path('api/v1/results/', ResultAPIView.as_view()),
    path('api/v1/results/<int:pk>/', ResultAPIView.as_view()),
    path('api/v1/lessons_to_results/', ResultsToGetAPIView.as_view()),
]


admin.site.site_header = 'Панель администрирования "Расписание-мобайл"'
admin.site.index_title = 'Расписание'