from django.views.generic import ListView
from chat.views import StaffOnly
from .models import User


class AccountListView(StaffOnly, ListView):
    model = User
    template_name = 'account_list.html'