from django.views.generic import ListView, DetailView
from chat.views import StaffOnly
from .models import User


class AccountListView(StaffOnly, ListView):
    model = User
    template_name = 'account_list.html'

class AccountDetailView(StaffOnly, DetailView):
    model = User
    template_name = 'account_detail.html'