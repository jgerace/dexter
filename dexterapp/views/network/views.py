from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from dexterapp.models import Network
from dexterapp.views.utils import get_url_with_query_params
from dexterapp.views.base_view import BaseView
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)
from dexterapp.service.network import service as NetworkService
from dexterapp.service.person import service as PersonService


class NetworksView(BaseView):
    def get(self, request):
        return render(request, "networks/index.html")


@login_required
def create_network(request):
    name = request.POST.get("name")

    try:
        network = NetworkService.create_network(user=request.user,
                                                name=name)
    except GenericError as e:
        return redirect(get_url_with_query_params("networks",
                                                  {"error_message": f"Could not create network {name}"}))
    except Exception as e:
        return redirect(get_url_with_query_params("networks",
                                                  {"error_message": f"Could not create network {name}. An unknown error occurred"}))

    return redirect("networks")


@login_required
def delete_network(request, network_id):
    NetworkService.delete_network(user=request.user,
                                  network_id=network_id)

    return redirect("networks")


class UpdateNetworkForm(forms.ModelForm):
    class Meta:
        model = Network
        fields = ["image", "name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get("image").widget.attrs.update({"class": "form-control"})
        self.fields.get("name").widget.attrs.update({"class": "form-control",
                                                     "placeholder": "Enter name"})


class NetworkProfileView(BaseView):
    def get(self, request, network_id):
        try:
            network = NetworkService.get_network(user=request.user,
                                                 network_id=network_id)
        except DoesNotValidate as e:
            return redirect(get_url_with_query_params("networks",
                                                      {"error_message": f"Invalid network {network_id}"}))
        except Exception as e:
            return redirect(get_url_with_query_params("networks",
                                                      {"error_message": f"Could not retrieve network {network_id}"}))

        people = PersonService.get_people_for_user(user=request.user)

        context = {
            "network": network,
            "people": people,
            "update_form": UpdateNetworkForm(instance=network)
        }
        return render(request, "networks/profile.html", context)

    def post(self, request, network_id):
        network = NetworkService.get_network(user=request.user,
                                             network_id=network_id)
        form = UpdateNetworkForm(request.POST, request.FILES, instance=network)
        if form.is_valid():
            form.save()
            return redirect("network_profile", network.id)


@login_required
def add_person(request, network_id):

    person_id = request.POST.get("person_id")

    try:
        NetworkService.add_person(user=request.user,
                                  network_id=network_id,
                                  person_id=person_id)
    except DoesNotValidate as e:
        return redirect(get_url_with_query_params("network_profile",
                                                  {"error_message": f"Could not add person to network: {e}"},
                                                  network_id))

    return redirect("network_profile", network_id)


@login_required
def add_person_by_person_id(request, person_id):

    network_id = request.POST.get("network_id")

    try:
        NetworkService.add_person(user=request.user,
                                  network_id=network_id,
                                  person_id=person_id)
    except Exception as e:
        return redirect(get_url_with_query_params("network_profile",
                                                  {"error_message": f"Could not add person to network: {e}"},
                                                  network_id))

    return redirect("person_profile", person_id)


@login_required
def delete_person_by_person_id(request, network_id, person_id):

    try:
        NetworkService.delete_person(user=request.user,
                                     network_id=network_id,
                                     person_id=person_id)
    except Exception as e:
        return redirect(get_url_with_query_params("network_profile",
                                                  {"error_message": f"Could not delete person from network: {e}"},
                                                  network_id))

    return redirect("network_profile", network_id)

