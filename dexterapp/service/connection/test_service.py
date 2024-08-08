from django.contrib.auth import get_user_model
from django.test import TestCase

from . import service as ConnectionService
from dexterapp.models import (
    Connection,
    Person,
    Relationship
)
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


class TestConnectionService(TestCase):
    def setUp(self):
        self.user = get_user_model()(
            first_name="First",
            last_name="Last",
            email="test@example.com"
        )
        self.user.save()

        self.person1 = Person(user=self.user,
                             first_name="From",
                             last_name="Person")
        self.person1.save()

        self.person2 = Person(user=self.user,
                                  first_name="To",
                                  last_name="Person")
        self.person2.save()

        self.relationship1 = Relationship(user=self.user,
                                          name="relationship 1")
        self.relationship1.save()

        self.relationship2 = Relationship(user=self.user,
                                          name="relationship 2")
        self.relationship2.save()

        self.connection_1_to_2 = Connection(user=self.user,
                                            from_person=self.person1,
                                            from_relationship=self.relationship1,
                                            to_person=self.person2,
                                            to_relationship=self.relationship2)
        self.connection_1_to_2.save()

        self.connection_2_to_1 = Connection(user=self.user,
                                            from_person=self.person2,
                                            from_relationship=self.relationship2,
                                            to_person=self.person1,
                                            to_relationship=self.relationship1)
        self.connection_2_to_1.save()

    def test_get_all_connections_for_person(self):
        connections = ConnectionService.get_all_connections_for_person(user=self.user,
                                                                       person_id=self.person1.id)
        self.assertEqual(len(connections), 2)

        connection1 = connections[0]
        self.assertEqual(connection1[0], self.connection_1_to_2.id)
        self.assertEqual(connection1[1], self.person2)
        self.assertEqual(connection1[2], self.relationship2)

        connection2 = connections[1]
        self.assertEqual(connection2[0], self.connection_2_to_1.id)
        self.assertEqual(connection2[1], self.person2)
        self.assertEqual(connection2[2], self.relationship2)

    def test_get_connections_from_person(self):
        connections = ConnectionService.get_connections_from_person(user=self.user,
                                                                    from_person_id=self.person1.id)

        self.assertEqual(len(connections), 1)
        connection = connections[0]
        self.assertEqual(connection.id, self.connection_1_to_2.id)
        self.assertEqual(connection.from_person, self.person1)
        self.assertEqual(connection.to_person, self.person2)
        self.assertEqual(connection.from_relationship, self.relationship1)
        self.assertEqual(connection.to_relationship, self.relationship2)

    def test_get_connections_to_person(self):
        connections = ConnectionService.get_connections_to_person(user=self.user,
                                                                  to_person_id=self.person1.id)

        self.assertEqual(len(connections), 1)
        connection = connections[0]
        self.assertEqual(connection.id, self.connection_2_to_1.id)
        self.assertEqual(connection.from_person, self.person2)
        self.assertEqual(connection.to_person, self.person1)
        self.assertEqual(connection.from_relationship, self.relationship2)
        self.assertEqual(connection.to_relationship, self.relationship1)

    def test_add_connection_to_person(self):
        connection = ConnectionService.add_connection_to_person(user=self.user,
                                                                from_person_id=self.person1.id,
                                                                to_person_id=self.person2.id,
                                                                from_relationship_id=self.relationship1.id,
                                                                to_relationship_id=self.relationship2.id)

        self.assertEqual(connection.from_person, self.person1)
        self.assertEqual(connection.to_person, self.person2)
        self.assertEqual(connection.from_relationship, self.relationship1)
        self.assertEqual(connection.to_relationship, self.relationship2)

    def test_delete_connection(self):
        connection = Connection.objects.get(id=self.connection_1_to_2.id)
        self.assertEqual(connection.id, self.connection_1_to_2.id)

        ConnectionService.delete_connection(user=self.user,
                                            connection_id=self.connection_1_to_2.id)

        with self.assertRaises(Connection.DoesNotExist):
            Connection.objects.get(id=self.connection_1_to_2.id)
