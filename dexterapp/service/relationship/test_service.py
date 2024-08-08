import arrow
from django.contrib.auth import get_user_model
from django.test import TestCase

from . import service as RelationshipService
from dexterapp.models import (
    Person,
    Relationship
)
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


class TestRelationshipService(TestCase):
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

    def test_get_relationships_for_user(self):
        Relationship(user=self.user, name="parent").save()
        Relationship(user=self.user, name="child").save()

        relationships = RelationshipService.get_relationships_for_user(user=self.user)

        self.assertEqual(len(relationships), 2)

    def test_create_relationship(self):
        relationship = RelationshipService.create_relationship(user=self.user,
                                                               name="relationship")
        self.assertEqual(relationship.name, "relationship")

    def test_create_relationship_invalid_name(self):
        with self.assertRaises(DoesNotValidate):
            RelationshipService.create_relationship(user=self.user, name="")

    def test_update_relationship(self):
        relationship = Relationship(user=self.user,
                                    name="relationship")
        relationship.save()
        self.assertEqual(relationship.name, "relationship")

        RelationshipService.update_relationship(user=self.user,
                                                relationship_id=relationship.id,
                                                name="parent")

        relationship.refresh_from_db()
        self.assertEqual(relationship.name, "parent")

    def test_update_relationship_invalid_name(self):
        relationship = Relationship(user=self.user,
                                    name="relationship")
        relationship.save()
        self.assertEqual(relationship.name, "relationship")

        with self.assertRaises(DoesNotValidate):
            RelationshipService.update_relationship(user=self.user,
                                                    relationship_id=relationship.id,
                                                    name="")

    def test_update_relationship_invalid_relationship(self):
        with self.assertRaises(DoesNotValidate):
            RelationshipService.update_relationship(user=self.user,
                                                    relationship_id=self.user.id,
                                                    name="name")

    def test_delete_relationship(self):
        relationship = Relationship(user=self.user,
                                    name="relationship")
        relationship.save()

        RelationshipService.delete_relationship(user=self.user,
                                                relationship_id=relationship.id)
        with self.assertRaises(Relationship.DoesNotExist):
            relationship.refresh_from_db()
