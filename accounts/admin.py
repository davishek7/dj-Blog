from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']

    class Meta:
        model = Profile

admin.site.register(Profile,ProfileAdmin)
