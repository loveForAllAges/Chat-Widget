from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def landing(request):
    return render(request, 'landing.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('dialogs/', include('chat.urls')),
    path('accounts/', include('account.urls')),
    path('', landing, name='landing'),
]
