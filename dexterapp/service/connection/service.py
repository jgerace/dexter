from typing import List

from dexterapp.models import Connection, Person, Relationship, User
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


def get_all_connections_for_person(user: User,
                                   person_id: str) -> List:
    from_connections = get_connections_from_person(user=user,
                                                   from_person_id=person_id)
    to_connections = get_connections_to_person(user=user,
                                               to_person_id=person_id)
    result = [(c.id, c.to_person, c.to_relationship) for c in from_connections]
    result.extend((c.id, c.from_person, c.from_relationship) for c in to_connections)

    return result


def get_connections_from_person(user: User,
                                from_person_id: str) -> List[Connection]:
    connections = Connection.objects.filter(user=user,
                                            from_person_id=from_person_id)
    return connections


def get_connections_to_person(user: User,
                              to_person_id: str) -> List[Connection]:
    connections = Connection.objects.filter(user=user,
                                            to_person_id=to_person_id)
    return connections


def add_connection_to_person(user: User,
                             from_person_id: str,
                             to_person_id: str,
                             from_relationship_id: str,
                             to_relationship_id: str) -> Connection:
    try:
        from_person = Person.objects.get(id=from_person_id,
                                         user=user)
    except Person.DoesNotExist:
        raise DoesNotValidate(f"Person {from_person_id} does not exist")

    try:
        to_person = Person.objects.get(id=to_person_id,
                                       user=user)
    except Person.DoesNotExist:
        raise DoesNotValidate(f"Person {to_person_id} does not exist")

    # Not gonna stop the user if they're adding another connection between the same people

    try:
        from_relationship = Relationship.objects.get(id=from_relationship_id)
        to_relationship = Relationship.objects.get(id=to_relationship_id)
    except Relationship.DoesNotExist as e:
        raise DoesNotValidate(f"Relationship does not exist {e}")

    connection = Connection(user=user,
                            from_person=from_person,
                            to_person=to_person,
                            from_relationship=from_relationship,
                            to_relationship=to_relationship)
    connection.save()

    return connection


def delete_connection(user: User,
                      connection_id: str):
    try:
        connection = Connection.objects.get(user=user,
                                            id=connection_id)
        connection.delete()
    except Connection.DoesNotExist:
        # TODO: Log
        pass
