from django.contrib.auth import get_user_model
from django.test import TestCase

from . import service as EmailService
from dexterapp.models import (
    EmailAddress,
    Person
)
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


class TestEmailService(TestCase):
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

        self.email = EmailAddress(user=self.user,
                                  person=self.person,
                                  label="label",
                                  email="test@test.com")
        self.email.save()

    def test_create_email_for_person(self):
        email = EmailService.create_email_for_person(user=self.user,
                                                     person_id=self.person.id,
                                                     label="label",
                                                     email="admin@example.com")
        self.assertEqual(email.user, self.user)
        self.assertEqual(email.person, self.person)
        self.assertEqual(email.label, "label")
        self.assertEqual(email.email, "admin@example.com")

    def test_create_email_for_person_duplicate(self):
        with self.assertRaises(DoesNotValidate):
            EmailService.create_email_for_person(user=self.user,
                                                 person_id=self.person.id,
                                                 label="label",
                                                 email="test@test.com")

    def test_update_email_for_person(self):
        email = EmailService.update_email_for_person(user=self.user,
                                                     email_id=self.email.id,
                                                     person_id=self.person.id,
                                                     label="label2",
                                                     email="test@example.com")
        self.assertEqual(email.user, self.user)
        self.assertEqual(email.person, self.person)
        self.assertEqual(email.label, "label2")
        self.assertEqual(email.email, "test@example.com")

    def test_delete_email_for_person(self):
        email = EmailAddress.objects.get(id=self.email.id)
        self.assertEqual(email.id, self.email.id)

        EmailService.delete_email_for_person(user=self.user,
                                             email_id=self.email.id,
                                             person_id=self.person.id)

        with self.assertRaises(EmailAddress.DoesNotExist):
            EmailAddress.objects.get(id=self.email.id)
