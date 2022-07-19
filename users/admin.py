from django.contrib import admin
from .models import User, UserCredential

# Register your models here.
admin.site.register(User)
admin.site.register(UserCredential)