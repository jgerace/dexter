import arrow
from typing import List

from dexterapp.models import Person, User
from dexterapp.service.exceptions import (
    DoesNotValidate,
    GenericError
)


def get_people_for_user(user: User):
    return Person.objects.filter(user=user)


def get_person(user: User, person_id: str) -> Person:
    try:
        person = Person.objects.get(user=user,
                                    id=person_id)
    except Person.DoesNotExist:
        raise DoesNotValidate(f"Could not retrieve {person_id}")

    return person


def get_people_with_birthdays_in_range(user: User,
                                       start_date: arrow.Arrow,
                                       end_date: arrow.Arrow) -> List[Person]:
    """
    :param user:
    :param start_date: YYYY-MM-DD format
    :param end_date: YYYY-MM-DD format
    :return:
    """
    result = Person.objects.filter(user=user,
                                   birthday__month__gte=start_date.format("MM"),
                                   birthday__month__lte=end_date.format("MM"),
                                   birthday__day__lte=end_date.format("DD"))
    return result


def create_person(user: User,
                  first_name: str,
                  last_name: str,
                  birthday=None,
                  pronouns: str = "",
                  gender: str = "",
                  notes: str = "") -> Person:
    if not first_name:
        raise DoesNotValidate("First name must not be bank")
    elif not last_name:
        raise DoesNotValidate("Last name must not be bank")

    person = user.person_set.create(first_name=first_name,
                                    last_name=last_name,
                                    birthday=birthday,
                                    pronouns=pronouns,
                                    gender=gender,
                                    notes=notes,
                                    user=user)
    if not person:
        raise GenericError(f"Could not create person {first_name} {last_name}")

    return person


def update_person(user: User,
                  person_id: str,
                  first_name: str,
                  last_name: str,
                  birthday=None,
                  pronouns: str = "",
                  gender: str = "",
                  notes: str = "") -> Person:
    if not first_name:
        raise DoesNotValidate("First name must not be bank")

    try:
        person = Person.objects.get(id=person_id,
                                    user=user)
    except Person.DoesNotExist:
        raise DoesNotValidate(f"Could not retrieve Person {person_id}")

    person.first_name = first_name
    person.last_name = last_name
    person.birthday = birthday
    person.pronouns = pronouns
    person.gender = gender
    person.notes = notes

    person.save()

    return person


def delete_person(user: User, person_id: str):
    try:
        person = Person.objects.get(id=person_id,
                                    user=user)
        person.delete()
    except Person.DoesNotExist:
        # TODO: Log
        pass
