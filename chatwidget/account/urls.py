from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render

urlpatterns = [
    path('', views.AccountListView.as_view(), name='account-list'),
    # path('<uuid:pk>/', views.AccountDetailView.as_view(), name='account-detail')
]
