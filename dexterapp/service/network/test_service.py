from django.contrib.auth import get_user_model
from django.test import TestCase

from . import service as NetworkService
from dexterapp.models import (
    Network,
    Person
)
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


class TestNetworkService(TestCase):
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

        self.person2 = Person(user=self.user,
                             first_name="Test2",
                             last_name="Person2")
        self.person2.save()

        self.network = Network(user=self.user,
                               name="Super Team Awesome")
        self.network.save()

    def test_create_network(self):
        network = NetworkService.create_network(user=self.user,
                                                name="Network")
        self.assertEqual(network.user, self.user)
        self.assertEqual(network.name, "Network")

    def test_get_networks_for_user(self):
        user2 = get_user_model()(
            username="ghjkl",
            first_name="TEST",
            last_name="TEST",
            email="TEST@TEST.com"
        )
        user2.save()

        person = Person(user=user2,
                        first_name="User2",
                        last_name="User2Person")
        person.save()

        network2 = Network(user=user2,
                           name="My Secret Family")

        networks = NetworkService.get_networks_for_user(user=self.user)

        self.assertEqual(len(networks), 1)
        network = networks[0]
        self.assertEqual(network.user, self.user)
        self.assertEqual(network.name, self.network.name)

    def test_get_network(self):
        network = NetworkService.get_network(user=self.user,
                                             network_id=self.network.id)
        self.assertEqual(network.id, self.network.id)
        self.assertEqual(network.name, self.network.name)

    def test_get_invalid_network(self):
        unsaved_network = Network(user=self.user,
                                  name="name")
        with self.assertRaises(DoesNotValidate):
            NetworkService.get_network(user=self.user,
                                       network_id=unsaved_network.id)

    def test_delete_network(self):
        Network.objects.get(id=self.network.id)

        NetworkService.delete_network(user=self.user,
                                      network_id=self.network.id)

        with self.assertRaises(Network.DoesNotExist):
            Network.objects.get(id=self.network.id)

    def test_add_person(self):
        self.assertEqual(len(self.network.people.all()), 0)

        NetworkService.add_person(user=self.user,
                                  network_id=self.network.id,
                                  person_id=self.person.id)

        self.network.refresh_from_db()
        self.assertEqual(len(self.network.people.all()), 1)

    def test_add_person_invalid_network(self):
        unsaved_network = Network(user=self.user,
                                  name="Blargh")

        with self.assertRaises(DoesNotValidate):
            NetworkService.add_person(user=self.user,
                                      network_id=unsaved_network.id,
                                      person_id=self.person.id)

    def test_add_person_invalid_person(self):
        unsaved_person = Person(user=self.user,
                                first_name="ASDF",
                                last_name="QWER")

        with self.assertRaises(DoesNotValidate):
            NetworkService.add_person(user=self.user,
                                      network_id=self.network.id,
                                      person_id=unsaved_person.id)

    def test_delete_person(self):
        self.assertEqual(len(self.network.people.all()), 0)

        NetworkService.add_person(user=self.user,
                                  network_id=self.network.id,
                                  person_id=self.person.id)

        self.network.refresh_from_db()
        self.assertEqual(len(self.network.people.all()), 1)

        NetworkService.delete_person(user=self.user,
                                     network_id=self.network.id,
                                     person_id=self.person.id)

        self.network.refresh_from_db()
        self.assertEqual(len(self.network.people.all()), 0)

    def test_delete_invalid_person(self):
        self.assertEqual(len(self.network.people.all()), 0)

        NetworkService.add_person(user=self.user,
                                  network_id=self.network.id,
                                  person_id=self.person.id)

        self.network.refresh_from_db()
        self.assertEqual(len(self.network.people.all()), 1)

        unsaved_person = Person(user=self.user,
                                first_name="ASDF",
                                last_name="QWER")
        with self.assertRaises(DoesNotValidate):
            NetworkService.delete_person(user=self.user,
                                         network_id=self.network.id,
                                         person_id=unsaved_person.id)

    def test_delete_person_invalid_network(self):
        self.assertEqual(len(self.network.people.all()), 0)

        NetworkService.add_person(user=self.user,
                                  network_id=self.network.id,
                                  person_id=self.person.id)

        self.network.refresh_from_db()
        self.assertEqual(len(self.network.people.all()), 1)

        unsaved_network = Network(user=self.user,
                                  name="Blargh")
        with self.assertRaises(DoesNotValidate):
            NetworkService.delete_person(user=self.user,
                                         network_id=unsaved_network.id,
                                         person_id=self.person.id)
