import arrow
from django.contrib.auth import get_user_model
from django.test import TestCase

from . import service as TagService
from dexterapp.models import (
    Person,
    PersonTag,
    Tag
)
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


class TestTagService(TestCase):
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
                              first_name="Second",
                              last_name="Person2",
                              birthday=arrow.utcnow().shift(days=3).date())
        self.person2.save()

        self.tag1 = Tag(user=self.user, name="tag 1")
        self.tag1.save()
        self.tag2 = Tag(user=self.user, name="tag 2")
        self.tag2.save()

    def test_get_tags_for_user(self):
        tags = TagService.get_tags_for_user(user=self.user)
        self.assertEqual(len(tags), 2)

    def test_get_tags_in_list(self):
        tags = TagService.get_tags_in_list(user=self.user,
                                           tag_ids=[self.tag1.id, self.tag2.id])
        self.assertEqual(len(tags), 2)
        self.assertListEqual(sorted([tag.name for tag in tags]), ["tag 1", "tag 2"])

    def test_get_people_with_tags(self):
        PersonTag(user=self.user,
                  person=self.person,
                  tag=self.tag1).save()
        PersonTag(user=self.user,
                  person=self.person2,
                  tag=self.tag2).save()
        people = TagService.get_people_with_tags(user=self.user,
                                                 tag_ids=[self.tag1.id])

        self.assertEqual(len(people), 1)

    def test_create_tag(self):
        tag = TagService.create_tag(user=self.user,
                                    name="new tag")
        tag.refresh_from_db()
        self.assertEqual(tag.name, "new tag")

    def test_create_tag_invalid_name(self):
        with self.assertRaises(DoesNotValidate):
            TagService.create_tag(user=self.user, name="")

    def test_create_tag_duplicate_name(self):
        with self.assertRaises(DoesNotValidate):
            TagService.create_tag(user=self.user, name="tag 1")

    def test_update_tag(self):
        tag = Tag(user=self.user,
                  name="new tag")
        tag.save()

        TagService.update_tag(user=self.user,
                              tag_id=tag.id,
                              name="new name")
        tag.refresh_from_db()
        self.assertEqual(tag.name, "new name")

    def test_update_tag_invalid_name(self):
        tag = Tag(user=self.user,
                  name="new tag")
        tag.save()

        with self.assertRaises(DoesNotValidate):
            TagService.update_tag(user=self.user,
                                  tag_id=tag.id,
                                  name="")

    def test_update_tag_invalid_tag(self):
        with self.assertRaises(DoesNotValidate):
            TagService.update_tag(user=self.user,
                                  tag_id=self.user.id,
                                  name="name")

    def test_delete_tag(self):
        TagService.delete_tag(user=self.user, tag_id=self.tag1.id)

        with self.assertRaises(Tag.DoesNotExist):
            self.tag1.refresh_from_db()

    def test_set_tags_on_person(self):
        TagService.set_tags_on_person(user=self.user,
                                      person_id=self.person.id,
                                      tag_ids=[self.tag1.id, self.tag2.id])

        person_tag1 = PersonTag.objects.filter(user=self.user,
                                               person_id=self.person.id,
                                               tag_id=self.tag1.id)
        person_tag2 = PersonTag.objects.filter(user=self.user,
                                               person_id=self.person.id,
                                               tag_id=self.tag2.id)

    def test_set_tags_on_person_invalid_person(self):
        with self.assertRaises(DoesNotValidate):
            TagService.set_tags_on_person(user=self.user,
                                          person_id=self.user.id,
                                          tag_ids=[self.tag1.id, self.tag2.id])

    def test_set_tags_on_person_invalid_tag(self):
        TagService.set_tags_on_person(user=self.user,
                                      person_id=self.person.id,
                                      tag_ids=[self.person.id])

        person_tags = PersonTag.objects.filter(user=self.user,
                                               person_id=self.person.id)
        self.assertEqual(len(person_tags), 0)
