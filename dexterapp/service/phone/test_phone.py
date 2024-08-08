from django.contrib.auth import get_user_model
from django.test import TestCase

from . import service as PhoneService
from dexterapp.models import (
    PhoneNumber,
    Person
)
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


class TestPhoneNumberService(TestCase):
    def setUp(self):
        self.user = get_user_model()(
            username="asdf",
            first_name="First",
            last_name="Last",
            email="test@example.com"
        )
        self.user.save()

        self.person = Person(user=self.user,
                             first_name="Test",
                             last_name="Person")
        self.person.save()

    def test_create_phone_number_for_person(self):
        phone = PhoneService.create_phone_number_for_person(user=self.user,
                                                            person_id=self.person.id,
                                                            label="Work",
                                                            number="2125555555")
        self.assertEqual(phone.user, self.user)
        self.assertEqual(phone.person, self.person)
        self.assertEqual(phone.label, "Work")
        self.assertEqual(phone.number, "2125555555")

    def test_create_phone_number_for_person_invalid_person(self):
        with self.assertRaises(DoesNotValidate):
            PhoneService.create_phone_number_for_person(user=self.user,
                                                        person_id=self.user.id,
                                                        label="Work",
                                                        number="2125555555")

    def test_create_phone_number_for_person_duplicate(self):
        PhoneNumber(user=self.user,
                    person=self.person,
                    label="Work",
                    number="2125555555").save()
        with self.assertRaises(DoesNotValidate):
            PhoneService.create_phone_number_for_person(user=self.user,
                                                        person_id=self.person.id,
                                                        label="Work",
                                                        number="2125555555")

    def test_update_phone_number_for_person(self):
        phone = PhoneNumber(user=self.user,
                            person=self.person,
                            label="Work",
                            number="2125555555")
        phone.save()

        PhoneService.update_phone_number_for_person(user=self.user,
                                                    phone_number_id=phone.id,
                                                    person_id=self.person.id,
                                                    label="Home",
                                                    number="1234567890")

        phone.refresh_from_db()
        self.assertEqual(phone.label, "Home")
        self.assertEqual(phone.number, "1234567890")

    def test_update_phone_number_for_person_invalid_phone(self):
        with self.assertRaises(DoesNotValidate):
            PhoneService.update_phone_number_for_person(user=self.user,
                                                        phone_number_id=self.user.id,
                                                        person_id=self.person.id,
                                                        label="Home",
                                                        number="1234567890")

    def test_delete_phone_number_for_person(self):
        phone = PhoneNumber(user=self.user,
                            person=self.person,
                            label="Work",
                            number="2125555555")
        phone.save()

        PhoneService.delete_phone_number_for_person(user=self.user,
                                                    phone_number_id=phone.id,
                                                    person_id=self.person.id)

        with self.assertRaises(PhoneNumber.DoesNotExist):
            phone.refresh_from_db()
