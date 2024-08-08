from typing import List

from dexterapp.models import Person, PersonTag, Tag, User
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


def get_tags_for_user(user: User) -> List[Tag]:
    return Tag.objects.filter(user=user)


def get_tags_in_list(user: User,
                     tag_ids: List[str]) -> List[Tag]:
    return Tag.objects.filter(user=user,
                              id__in=tag_ids)


def get_people_with_tags(user: User,
                         tag_ids: List[str]) -> List[PersonTag]:
    return PersonTag.objects.filter(user=user,
                                    tag_id__in=tag_ids)


def create_tag(user: User, name: str) -> Tag:
    if not name:
        raise DoesNotValidate("Tag name must not be bank")

    tags = Tag.objects.filter(user=user, name=name)
    if tags:
        raise DoesNotValidate(f'Tag "{name}" already exists')

    tag = user.tag_set.create(name=name)
    if not tag:
        raise GenericError(f"Could not create tag {name}")

    return tag


def update_tag(user: User, tag_id: str, name: str) -> Tag:
    if not name:
        raise DoesNotValidate(f"Tag name must not be blank")
    elif not tag_id:
        raise DoesNotValidate(f"Tag ID must not be blank")

    try:
        tag = Tag.objects.get(id=tag_id,
                              user=user)
        tag.name = name
        tag.save()
    except Tag.DoesNotExist:
        raise DoesNotValidate(f"Tag {tag_id} does not exist")

    return tag


def delete_tag(user: User, tag_id: str):
    try:
        tag = Tag.objects.get(id=tag_id,
                              user=user)
        tag.delete()
    except Tag.DoesNotExist:
        # TODO: Log
        pass


def set_tags_on_person(user: User, person_id: str, tag_ids: List[str]):
    try:
        person = Person.objects.get(id=person_id,
                                    user=user)
        for pt in person.persontag_set.all():
            pt.delete()
    except Person.DoesNotExist:
        raise DoesNotValidate(f"Could not find Person {person_id}")

    tags = Tag.objects.filter(id__in=tag_ids,
                              user=user)

    for tag in tags:
        person_tag = PersonTag.objects.create(user=user,
                                              person=person,
                                              tag=tag)
        person_tag.save()
