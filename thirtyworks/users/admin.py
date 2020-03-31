from django.contrib import admin
from .models import UserProfile
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
import csv
from django.http import HttpResponse


# Register your models here.
# admin.site.register(UserProfile)

class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ['blocked',         ('date_blocked', DropdownFilter),]

    list_display = ['user', 'get_email']

    actions = ['export_as_csv']

    def get_email(self, obj):
        return obj.user.email

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names+['email'])
        for obj in queryset:
            userprofile = obj
            user = userprofile.user
            email_address = user.email
            print('email = {}'.format(email_address))
            row = writer.writerow([getattr(obj, field) for field in field_names] + [email_address])

        return response

    export_as_csv.short_description = "Export Selected"


admin.site.register(UserProfile, UserProfileAdmin)