from typing import List

from dexterapp.models import Network, Person, User
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


def create_network(user: User, name: str) -> Network:
    network = user.network_set.create(name=name)
    if not network:
        # TODO: Logging
        raise GenericError(f"Could not create network {name}")

    return network


def get_networks_for_user(user: User) -> List[Network]:
    return Network.objects.filter(user=user)


def get_network(user: User, network_id: str) -> Network:
    try:
        network = Network.objects.get(user=user,
                                      id=network_id)
    except Network.DoesNotExist:
        raise DoesNotValidate(f"Network {network_id} does not exist")

    return network


def delete_network(user: User, network_id: str):
    try:
        network = Network.objects.get(id=network_id,
                                      user=user)
        network.delete()
    except Network.DoesNotExist:
        pass


def add_person(user: User, network_id: str, person_id: str):
    try:
        network = Network.objects.get(id=network_id,
                                      user=user)
    except Network.DoesNotExist:
        raise DoesNotValidate(f"Network {network_id} does not exist")

    try:
        person = Person.objects.get(id=person_id,
                                    user=user)
    except Person.DoesNotExist:
        raise DoesNotValidate(f"Person {person_id} does not exist")

    network.people.add(person)


def delete_person(user: User, network_id: str, person_id: str):
    try:
        person = Person.objects.get(id=person_id,
                                    user=user)
    except Person.DoesNotExist:
        raise DoesNotValidate(f"Person {person_id} does not exist")

    try:
        network = Network.objects.get(id=network_id,
                                      user=user)
    except Network.DoesNotExist:
        raise DoesNotValidate(f"Network {network_id} does not exist")

    network.people.remove(person)
