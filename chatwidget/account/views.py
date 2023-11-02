from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from chat.views import StaffOnly
from .models import User
from django.db.models import Q


class AccountListView(StaffOnly, ListView):
    model = User
    template_name = 'account_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        return User.objects.filter(~Q(pk=self.request.user.pk) & Q(is_active=True))


class AccountDetailView(StaffOnly, DetailView):
    model = User
    template_name = 'account_detail.html'