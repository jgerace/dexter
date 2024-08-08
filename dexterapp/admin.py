from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import *

admin.site.register(Connection)
admin.site.register(Network)
admin.site.register(PersonTag)
admin.site.register(Relationship)
admin.site.register(Tag)
admin.site.register(User, UserAdmin)
admin.site.register(Person)
admin.site.register(EmailAddress)
admin.site.register(PhoneNumber)
admin.site.register(Address)
