from typing import List

from dexterapp.models import Relationship, User
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


def get_relationships_for_user(user: User) -> List[Relationship]:
    return Relationship.objects.filter(user=user)


def create_relationship(user: User, name: str) -> Relationship:
    if not name:
        raise DoesNotValidate("Tag name must not be bank")

    relationship = user.relationship_set.create(name=name)
    if not relationship:
        raise GenericError(f"Could not create relationship {name}")

    return relationship


def update_relationship(user: User, relationship_id: str, name: str) -> Relationship:
    if not name:
        raise DoesNotValidate("Relationship name must not be blank")
    elif not relationship_id:
        raise DoesNotValidate("Relationship ID must not be blank")

    try:
        relationship = Relationship.objects.get(id=relationship_id,
                                                user=user)
        relationship.name = name
        relationship.save()
    except Relationship.DoesNotExist:
        raise DoesNotValidate(f"Relationship {relationship_id} does not exist")

    return relationship


def delete_relationship(user: User, relationship_id: str):
    try:
        relationship = Relationship.objects.get(id=relationship_id,
                                                user=user)
        relationship.delete()
    except Relationship.DoesNotExist:
        # TODO: Log
        pass
