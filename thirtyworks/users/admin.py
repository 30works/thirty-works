from django.contrib import admin
from .models import UserProfile
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter


# Register your models here.
# admin.site.register(UserProfile)

class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ['blocked']

admin.site.register(UserProfile, UserProfileAdmin)