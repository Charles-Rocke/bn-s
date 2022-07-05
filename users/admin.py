from django.contrib import admin
from .models import Users, UserCredential

# Register your models here.
admin.site.register(Users)
admin.site.register(UserCredential)