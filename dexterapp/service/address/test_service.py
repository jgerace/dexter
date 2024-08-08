from django.contrib.auth import get_user_model
from django.test import TestCase

from . import service as AddressService
from dexterapp.models import (
    Address,
    Person
)
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


class TestAddressService(TestCase):
    def setUp(self):
        self.user = get_user_model()(
            first_name="First",
            last_name="Last",
            email="test@example.com"
        )
        self.user.save()

        self.person = Person(user=self.user,
                             first_name="Test",
                             last_name="Person")
        self.person.save()

        self.address = AddressService.create_address_for_person(user=self.user,
                                                                person_id=self.person.id,
                                                                label="label",
                                                                street1="street1",
                                                                street2="street2",
                                                                city="city",
                                                                state="state",
                                                                postal_code="postal_code",
                                                                country="country")

    def test_create_address_for_person(self):
        address = AddressService.create_address_for_person(user=self.user,
                                                           person_id=self.person.id,
                                                           label="label",
                                                           street1="street1",
                                                           street2="street2",
                                                           city="city",
                                                           state="state",
                                                           postal_code="postal_code",
                                                           country="country")
        self.assertEqual(address.user, self.user)
        self.assertEqual(address.person, self.person)
        self.assertEqual(address.label, "label")
        self.assertEqual(address.street1, "street1")
        self.assertEqual(address.street2, "street2")
        self.assertEqual(address.city, "city")
        self.assertEqual(address.state, "state")
        self.assertEqual(address.postal_code, "postal_code")
        self.assertEqual(address.country, "country")

    def test_create_address_invalid_person(self):
        unsaved_person = Person(user=self.user,
                                first_name="Test",
                                last_name="Person")
        with self.assertRaises(DoesNotValidate):
            AddressService.create_address_for_person(user=self.user,
                                                     person_id=unsaved_person.id,
                                                     label="label",
                                                     street1="street1",
                                                     street2="street2",
                                                     city="city",
                                                     state="state",
                                                     postal_code="postal_code",
                                                     country="country")

    def test_update_address_for_person(self):
        address = AddressService.update_address_for_person(user=self.user,
                                                           person_id=self.person.id,
                                                           address_id=self.address.id,
                                                           label="label2",
                                                           street1="street3",
                                                           street2="street4",
                                                           city="city1",
                                                           state="state1",
                                                           postal_code="postal_code1",
                                                           country="country1")
        self.assertEqual(address.user, self.user)
        self.assertEqual(address.person, self.person)
        self.assertEqual(address.label, "label2")
        self.assertEqual(address.street1, "street3")
        self.assertEqual(address.street2, "street4")
        self.assertEqual(address.city, "city1")
        self.assertEqual(address.state, "state1")
        self.assertEqual(address.postal_code, "postal_code1")
        self.assertEqual(address.country, "country1")

    def test_update_address_invalid_address(self):
        unsaved_address = Address(user=self.user,
                                  person=self.person,
                                  street1="street1",)
        with self.assertRaises(DoesNotValidate):
            AddressService.update_address_for_person(user=self.user,
                                                     person_id=self.person.id,
                                                     address_id=unsaved_address.id,
                                                     label="label",
                                                     street1="street3",
                                                     street2="street4",
                                                     city="city1",
                                                     state="state1",
                                                     postal_code="postal_code1",
                                                     country="country1")

    def test_delete_address_for_person(self):
        address = Address.objects.get(id=self.address.id)
        self.assertEqual(address.id, self.address.id)

        AddressService.delete_address_for_person(user=self.user,
                                                 address_id=self.address.id,
                                                 person_id=self.person.id)

        with self.assertRaises(Address.DoesNotExist):
            Address.objects.get(id=self.address.id)
