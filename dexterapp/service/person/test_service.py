import arrow
from django.contrib.auth import get_user_model
from django.test import TestCase

from . import service as PersonService
from dexterapp.models import (
    Person
)
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


class TestPersonService(TestCase):
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
                             last_name="Person",
                             birthday=arrow.utcnow().shift(days=3).date())
        self.person.save()

        self.person2 = Person(user=self.user,
                              first_name="Test2",
                              last_name="Person2",
                              birthday=arrow.utcnow().shift(days=12).date())
        self.person2.save()

    def test_get_people_for_user(self):
        people = PersonService.get_people_for_user(user=self.user)

        self.assertEqual(len(people), 2)

    def test_get_person(self):
        person = PersonService.get_person(user=self.user,
                                          person_id=self.person.id)
        self.assertEqual(person.id, self.person.id)

    def test_get_person_invalid(self):
        with self.assertRaises(DoesNotValidate):
            PersonService.get_person(user=self.user,
                                     person_id=self.user.id)

    def test_get_people_with_birthdays_in_range(self):
        people = PersonService.get_people_with_birthdays_in_range(user=self.user,
                                                                  start_date=arrow.utcnow(),
                                                                  end_date=arrow.utcnow().shift(days=7))
        self.assertEqual(len(people), 1)
        self.assertEqual(people[0].id, self.person.id)

    def test_create_person(self):
        birthday = arrow.utcnow().date()
        person = PersonService.create_person(user=self.user,
                                             first_name="New",
                                             last_name="Person",
                                             birthday=birthday,
                                             pronouns="ASDF",
                                             gender="QWER",
                                             notes="NOTES")
        self.assertEqual(person.user, self.user)
        self.assertEqual(person.first_name, "New")
        self.assertEqual(person.last_name, "Person")
        self.assertEqual(person.birthday, birthday)
        self.assertEqual(person.pronouns, "ASDF")
        self.assertEqual(person.gender, "QWER")
        self.assertEqual(person.notes, "NOTES")

    def test_create_person_invalid_first_name(self):
        birthday = arrow.utcnow().date()
        with self.assertRaises(DoesNotValidate):
            PersonService.create_person(user=self.user,
                                        first_name="",
                                        last_name="Person",
                                        birthday=birthday,
                                        pronouns="ASDF",
                                        gender="QWER",
                                        notes="NOTES")

    def test_create_person_invalid_last_name(self):
        birthday = arrow.utcnow().date()
        with self.assertRaises(DoesNotValidate):
            PersonService.create_person(user=self.user,
                                        first_name="New",
                                        last_name="",
                                        birthday=birthday,
                                        pronouns="ASDF",
                                        gender="QWER",
                                        notes="NOTES")

    def test_update_person(self):
        birthday = arrow.utcnow().date()
        PersonService.update_person(user=self.user,
                                    person_id=self.person.id,
                                    first_name="NewFirst",
                                    last_name="NewLast",
                                    birthday=birthday,
                                    pronouns="New",
                                    gender="New",
                                    notes="New")

        self.person.refresh_from_db()
        self.assertEqual(self.person.first_name, "NewFirst")
        self.assertEqual(self.person.last_name, "NewLast")
        self.assertEqual(self.person.birthday, birthday)
        self.assertEqual(self.person.pronouns, "New")
        self.assertEqual(self.person.gender, "New")
        self.assertEqual(self.person.notes, "New")

    def test_update_person_invalid_first_name(self):
        birthday = arrow.utcnow().date()

        with self.assertRaises(DoesNotValidate):
            PersonService.update_person(user=self.user,
                                        person_id=self.person.id,
                                        first_name="",
                                        last_name="NewLast",
                                        birthday=birthday,
                                        pronouns="New",
                                        gender="New",
                                        notes="New")

    def test_update_person_invalid_person(self):
        birthday = arrow.utcnow().date()

        with self.assertRaises(DoesNotValidate):
            PersonService.update_person(user=self.user,
                                        person_id=self.user.id,
                                        first_name="NewFirst",
                                        last_name="NewLast",
                                        birthday=birthday,
                                        pronouns="New",
                                        gender="New",
                                        notes="New")

    def test_delete_person(self):
        PersonService.delete_person(user=self.user,
                                    person_id=self.person.id)

        with self.assertRaises(Person.DoesNotExist):
            self.person.refresh_from_db()
