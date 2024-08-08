from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from dexterapp.models import Person
from dexterapp.views.utils import get_url_with_query_params
from dexterapp.views.base_view import BaseView
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)
from dexterapp.service.address import service as AddressService
from dexterapp.service.connection import service as ConnectionService
from dexterapp.service.email import service as EmailService
from dexterapp.service.network import service as NetworkService
from dexterapp.service.person import service as PersonService
from dexterapp.service.phone import service as PhoneNumberService
from dexterapp.service.relationship import service as RelationshipService
from dexterapp.service.tag import service as TagService


class PeopleView(BaseView):
    def get(self, request):
        error_message = request.GET.get("error_message")
        people = PersonService.get_people_for_user(user=request.user)
        context = {
            "people": people,
            "error_message": error_message
        }
        return render(request, "persons/index.html", context)


@login_required
def create_person(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")

    try:
        person = PersonService.create_person(user=request.user,
                                             first_name=first_name,
                                             last_name=last_name)
    except GeneratorExit as e:
        context = {
            "error_message": f"Could not create person {first_name} {last_name}: {e}"
        }
        return render(request, "networks/index.html", context)

    return redirect("person_profile", person.id)


@login_required
def delete_person(request):
    person_id = request.POST.get("person_id")
    PersonService.delete_person(user=request.user,
                                person_id=person_id)

    return redirect("people")


class UpdatePersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["image", "first_name", "last_name", "birthday", "pronouns", "gender", "notes"]
        widgets = {
            "birthday": forms.widgets.DateInput(attrs={"class": "form-control",
                                                       "placeholder": "Birthday",
                                                       "type": "date"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get("image").widget.attrs.update({"class": "form-control"})
        self.fields.get("first_name").widget.attrs.update({"class": "form-control",
                                                           "placeholder": "Enter first name"})
        self.fields.get("last_name").widget.attrs.update({"class": "form-control",
                                                          "placeholder": "Enter last name"})
        self.fields.get("pronouns").widget.attrs.update({"class": "form-control",
                                                         "placeholder": "Enter pronouns"})
        self.fields.get("gender").widget.attrs.update({"class": "form-control",
                                                       "placeholder": "Enter gender"})
        self.fields.get("notes").widget.attrs.update({"class": "form-control-plaintext",
                                                      "placeholder": "Enter notes"})


class PersonProfileView(BaseView):
    def get(self, request, person_id):
        error_message = request.GET.get("error_message")
        try:
            person = PersonService.get_person(user=request.user,
                                              person_id=person_id)
        except DoesNotValidate as e:
            return redirect(get_url_with_query_params("people",
                                                      {"error_message": f"Could not retrieve person {person_id}: {e}"}))

        connections = ConnectionService.get_all_connections_for_person(user=request.user,
                                                                       person_id=person_id)
        relationships = RelationshipService.get_relationships_for_user(user=request.user)
        people = PersonService.get_people_for_user(user=request.user)
        networks = NetworkService.get_networks_for_user(user=request.user)

        context = {
            "person": person,
            "valid_email_labels": ["Work", "Home"],
            "valid_phone_labels": ["Work", "Home"],
            "upload_image_form": UpdatePersonForm(instance=person),
            "connections": connections,
            "relationships": relationships,
            "people": people,
            "networks": networks,
            "user_tags": TagService.get_tags_for_user(user=request.user),
            "tags_on_person": [pt.tag.id for pt in person.persontag_set.all()],
            "error_message": error_message
        }

        return render(request, "persons/profile.html", context)

    def post(self, request, person_id):
        person = PersonService.get_person(user=request.user,
                                          person_id=person_id)
        form = UpdatePersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            return redirect("person_profile", person.id)


@login_required
def update_image_for_person(request, person_id):
    if request.method == "POST":
        person = PersonService.get_person(user=request.user,
                                          person_id=person_id)
        form = UpdatePersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            return redirect("person_profile", person.id)


@login_required
def add_email_to_person(request, person_id):
    label = request.POST.get("email_label")
    email = request.POST.get("email")

    try:
        EmailService.create_email_for_person(person_id=person_id,
                                             label=label,
                                             email=email,
                                             user=request.user)
    except DoesNotValidate as e:
        return redirect(get_url_with_query_params("person_profile",
                                                  {"error_message": f"Could not add email {email} to person {person_id}: {e}"},
                                                  person_id))

    return redirect("person_profile", person_id)


@login_required
def update_email_for_person(request, person_id, email_address_id):
    EmailService.update_email_for_person(user=request.user,
                                         email_id=email_address_id,
                                         person_id=person_id,
                                         label=request.POST.get(f"update_email_label_{email_address_id}"),
                                         email=request.POST.get(f"update_email_{email_address_id}"))

    return redirect("person_profile", person_id)


@login_required
def delete_email_for_person(request, person_id, email_address_id):
    EmailService.delete_email_for_person(user=request.user,
                                         email_id=email_address_id,
                                         person_id=person_id)

    return redirect("person_profile", person_id)


@login_required
def add_phone_number_to_person(request, person_id):
    label = request.POST.get("phone_label")
    number = request.POST.get("phone_number")
    try:
        PhoneNumberService.create_phone_number_for_person(user=request.user,
                                                          person_id=person_id,
                                                          label=label,
                                                          number=number)
    except DoesNotValidate as e:
        return redirect(get_url_with_query_params("person_profile",
                                                  {"error_message": f"Could not add phone {number} to person {person_id}: {e}"},
                                                  person_id))

    return redirect("person_profile", person_id)


@login_required
def update_phone_number_for_person(request, person_id, phone_number_id):
    label = request.POST.get(f"update_phone_label_{phone_number_id}")
    number = request.POST.get(f"update_phone_number_{phone_number_id}")

    try:
        PhoneNumberService.update_phone_number_for_person(user=request.user,
                                                          person_id=person_id,
                                                          label=label,
                                                          number=number)
    except DoesNotValidate as e:
        return redirect(get_url_with_query_params("person_profile",
                                                  {"error_message": f"Could not update phone {number} for person {person_id}: {e}"},
                                                  person_id))

    return redirect("person_profile", person_id)


@login_required
def delete_phone_number_for_person(request, person_id, phone_number_id):
    PhoneNumberService.delete_phone_number_for_person(user=request.user,
                                                      phone_number_id=phone_number_id,
                                                      person_id=person_id)

    return redirect("person_profile", person_id)


@login_required
def add_address_to_person(request, person_id):
    label = request.POST.get("address_name")
    street1 = request.POST.get("street1")
    street2 = request.POST.get("street2")
    city = request.POST.get("city")
    state = request.POST.get("state")
    postal_code = request.POST.get("postal_code")
    country = request.POST.get("country")

    try:
        AddressService.create_address_for_person(person_id=person_id,
                                                 label=label,
                                                 street1=street1,
                                                 street2=street2,
                                                 city=city,
                                                 state=state,
                                                 postal_code=postal_code,
                                                 country=country,
                                                 user=request.user)
    except DoesNotValidate as e:
        return redirect(get_url_with_query_params("person_profile",
                                                  {"error_message": f"Could not create address {street1} for person {person_id}: {e}"},
                                                  person_id))

    return redirect("person_profile", person_id)


@login_required
def update_address_for_person(request, person_id, address_id):
    label = request.POST.get(f"address_name_{address_id}")
    street1 = request.POST.get(f"street1_{address_id}")
    street2 = request.POST.get(f"street2_{address_id}")
    city = request.POST.get(f"city_{address_id}")
    state = request.POST.get(f"state_{address_id}")
    postal_code = request.POST.get(f"postal_code_{address_id}")
    country = request.POST.get(f"country_{address_id}")

    try:
        AddressService.update_address_for_person(person_id=person_id,
                                                 address_id=address_id,
                                                 label=label,
                                                 street1=street1,
                                                 street2=street2,
                                                 city=city,
                                                 state=state,
                                                 postal_code=postal_code,
                                                 country=country,
                                                 user=request.user)
    except DoesNotValidate as e:
        return redirect(get_url_with_query_params("person_profile",
                                                  {"error_message": f"Could not update address {address_id} for person {person_id}: {e}"},
                                                  person_id))

    return redirect("person_profile", person_id)


@login_required
def delete_address_for_person(request, person_id, address_id):
    AddressService.delete_address_for_person(user=request.user,
                                             address_id=address_id,
                                             person_id=person_id)

    return redirect("person_profile", person_id)


@login_required
def add_connection_to_person(request, person_id):
    to_person_id = request.POST.get("to_person_id")
    to_relationship_id = request.POST.get("to_relationship_id")
    from_relationship_id = request.POST.get("from_relationship_id")

    try:
        ConnectionService.add_connection_to_person(user=request.user,
                                                   from_person_id=person_id,
                                                   to_person_id=to_person_id,
                                                   from_relationship_id=from_relationship_id,
                                                   to_relationship_id=to_relationship_id)
    except DoesNotValidate as e:
        return redirect(get_url_with_query_params("person_profile",
                                                  {"error_message": f"Could not add relationship from person {person_id} to {to_person_id}: {e}"},
                                                  person_id))

    return redirect("person_profile", person_id)


@login_required
def delete_connection_for_person(request, person_id, connection_id):
    try:
        ConnectionService.delete_connection(user=request.user,
                                            connection_id=connection_id)
    except Exception as e:
        return redirect(get_url_with_query_params("person_profile",
                                                  {"error_message": f"Could not delete connection {connection_id}: {e}"},
                                                  person_id))

    return redirect("person_profile", person_id)


@login_required
def set_tags_on_person(request, person_id):
    active_tags = []
    for key, value in request.POST.items():
        if key.startswith("tag_"):
            active_tags.append(value)

    try:
        TagService.set_tags_on_person(user=request.user,
                                      person_id=person_id,
                                      tag_ids=active_tags)
    except DoesNotValidate as e:
        return redirect(get_url_with_query_params("person_profile",
                                                  {"error_message": f"Could not add tags for person {person_id}: {e}"},
                                                  person_id))

    return redirect("person_profile", person_id)
