from typing import List

from dexterapp.models import Address, Person, User
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


def create_address_for_person(user: User,
                              person_id: Person,
                              label: str,
                              street1: str,
                              street2: str,
                              city: str,
                              state: str,
                              postal_code: str,
                              country: str) -> Address:
    try:
        person = Person.objects.get(id=person_id,
                                    user=user)
    except Person.DoesNotExist:
        raise DoesNotValidate(f"Could not retrieve Person {person_id}")

    address = person.address_set.create(user=user,
                                        label=label,
                                        street1=street1,
                                        street2=street2,
                                        city=city,
                                        state=state,
                                        postal_code=postal_code,
                                        country=country)

    if not address:
        raise GenericError(f"Could not create address {street1} for {person_id}")

    return address


def update_address_for_person(user: User,
                              person_id: Person,
                              address_id: str,
                              label: str,
                              street1: str,
                              street2: str,
                              city: str,
                              state: str,
                              postal_code: str,
                              country: str) -> Address:
    address = Address.objects.filter(id=address_id,
                                     person_id=person_id,
                                     user=user)
    if not address:
        raise DoesNotValidate(f"Could not retrieve address {address_id} for person {person_id}")

    address = address[0]
    address.label = label
    address.street1 = street1
    address.street2 = street2
    address.city = city
    address.state = state
    address.postal_code = postal_code
    address.country = country
    address.save()

    return address


def delete_address_for_person(user: User,
                              address_id: str,
                              person_id: Person):
    try:
        address = Address.objects.get(id=address_id,
                                      person_id=person_id,
                                      user=user)
        address.delete()
    except Address.DoesNotExist:
        # TODO: Log
        pass
