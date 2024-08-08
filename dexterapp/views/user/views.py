import arrow
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.views import View
from dexterapp.service.network import service as NetworkService
from dexterapp.service.person import service as PersonService
from dexterapp.views.base_view import BaseView


class HomePageView(BaseView):
    
    def get(self, request):
        today = arrow.utcnow()
        end_date = today.shift(days=7)
        people = PersonService.get_people_with_birthdays_in_range(user=request.user,
                                                                  start_date=today,
                                                                  end_date=end_date)
        context = {
            "birthdays": people,
            "networks": NetworkService.get_networks_for_user(user=request.user)
        }
        return render(request, "home/index.html", context)


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")


class RegistrationView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        context = {
            "form": form
        }
        return render(request, "registration/create_user.html", context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            context = {
                "form": form
            }
            return render(request, "registration/create_user.html", context)


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["image", "first_name", "last_name", "username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get("image").widget.attrs.update({"class": "form-control"})
        self.fields.get("first_name").widget.attrs.update({"class": "form-control",
                                                           "placeholder": "Enter first name"})
        self.fields.get("last_name").widget.attrs.update({"class": "form-control",
                                                          "placeholder": "Enter last name"})
        self.fields.get("username").widget.attrs.update({"class": "form-control",
                                                         "placeholder": "Enter username"})
        self.fields.get("email").widget.attrs.update({"class": "form-control",
                                                       "placeholder": "Enter email address"})
        print(self.fields)


class UserProfileView(BaseView):
    def get(self, request):
        context = {
            "profile_update_form": UpdateUserForm(instance=request.user)
        }
        return render(request, "user/index.html", context)

    def post(self, request):
        form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # TODO: Will this validate uniqueness for email/username in this operation?
            form.save()
            return redirect("profile")


@login_required
def user_profile(request):
    context = {
    }
    return render(request, "user/index.html", context)
