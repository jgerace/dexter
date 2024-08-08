import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.
class Connection(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    from_person = models.ForeignKey("Person", on_delete=models.DO_NOTHING, related_name="+")
    from_relationship = models.ForeignKey("Relationship", related_name="+", on_delete=models.DO_NOTHING)
    to_person = models.ForeignKey("Person", on_delete=models.DO_NOTHING, related_name="+")
    to_relationship = models.ForeignKey("Relationship", related_name="+", on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)


class Network(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True, upload_to="network/", default="/network/default.jpg")
    people = models.ManyToManyField("Person")
    created_at = models.DateTimeField(default=timezone.now)


class PersonTag(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey("Person", on_delete=models.DO_NOTHING)
    tag = models.ForeignKey("Tag", on_delete=models.DO_NOTHING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)


class Relationship(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)


class Tag(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)


class User(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    birthday = models.DateField(default=None, null=True)
    image = models.ImageField(null=True, upload_to="user/", default="/user/default.jpg")
    created_at = models.DateTimeField(default=timezone.now)


class Person(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    birthday = models.DateField(default=None, blank=True, null=True)
    pronouns = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    image = models.ImageField(null=True, upload_to="person/", default="/person/default.jpg")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)


class EmailAddress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    person = models.ForeignKey("Person", on_delete=models.DO_NOTHING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)


class PhoneNumber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=20)
    number = models.CharField(max_length=20)
    person = models.ForeignKey("Person", on_delete=models.DO_NOTHING)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(max_length=20)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    street1 = models.CharField(max_length=100)
    street2 = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True)
