from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class BaseView(LoginRequiredMixin, View):
    login_url = "/dexter/accounts/login"
    redirect_field_name = "next"
