from typing import List

from dexterapp.models import EmailAddress, Person, User
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


def create_email_for_person(user: User,
                            person_id: Person,
                            label: str,
                            email: str) -> EmailAddress:
    try:
        person = Person.objects.get(id=person_id,
                                    user=user)
    except Person.DoesNotExist:
        raise DoesNotValidate(f"Could not retrieve Person {person_id}")

    email_address = EmailAddress.objects.filter(email=email,
                                                person_id=person.id,
                                                user=user)
    if email_address:
        raise DoesNotValidate(f"Email {email} already exists for person {person_id}")

    email = person.emailaddress_set.create(label=label,
                                           email=email,
                                           user=user)

    return email


def update_email_for_person(user: User,
                            email_id: str,
                            person_id: Person,
                            label: str,
                            email: str) -> EmailAddress:
    email_address = EmailAddress.objects.filter(id=email_id,
                                                person_id=person_id,
                                                user=user)
    if not email_address:
        raise DoesNotValidate(f"Could not retrieve email {email_id} for person {person_id}")

    email_address = email_address[0]
    email_address.label = label
    email_address.email = email
    email_address.save()

    return email_address


def delete_email_for_person(user: User,
                            email_id: str,
                            person_id: Person):
    try:
        email_address = EmailAddress.objects.get(id=email_id,
                                                 person_id=person_id,
                                                 user=user)
        email_address.delete()
    except EmailAddress.DoesNotExist:
        # TODO: Log
        pass
