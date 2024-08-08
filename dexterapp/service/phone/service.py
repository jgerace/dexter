from typing import List

from dexterapp.models import PhoneNumber, Person, User
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


def create_phone_number_for_person(user: User,
                                   person_id: Person,
                                   label: str,
                                   number: str) -> PhoneNumber:
    try:
        person = Person.objects.get(id=person_id,
                                    user=user)
    except Person.DoesNotExist:
        raise DoesNotValidate(f"Could not retrieve Person {person_id}")

    phone_number = PhoneNumber.objects.filter(number=number,
                                              person_id=person.id,
                                              user=user)

    if phone_number:
        raise DoesNotValidate(f"Phone number {phone_number} already exists for person {person_id}")

    phone_number = person.phonenumber_set.create(label=label,
                                                 number=number,
                                                 user=user)

    return phone_number


def update_phone_number_for_person(user: User,
                                   phone_number_id: str,
                                   person_id: Person,
                                   label: str,
                                   number: str) -> PhoneNumber:
    phone_number = PhoneNumber.objects.filter(id=phone_number_id,
                                              person_id=person_id,
                                              user=user)
    if not phone_number:
        raise DoesNotValidate(f"Could not retrieve Phone number {phone_number_id} for person {person_id}")

    phone_number = phone_number[0]
    phone_number.label = label
    phone_number.number = number
    phone_number.save()

    return phone_number


def delete_phone_number_for_person(user: User,
                                   phone_number_id: str,
                                   person_id: Person):
    try:
        phone_number = PhoneNumber.objects.get(id=phone_number_id,
                                               person_id=person_id,
                                               user=user)
        phone_number.delete()
    except PhoneNumber.DoesNotExist:
        # TODO: Log
        pass
