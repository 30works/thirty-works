from django.contrib import admin
from .models import Post, Day
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter

# Register your models here.
# admin.site.register(Post)
admin.site.register(Day)


class PostAdmin(admin.ModelAdmin):
    list_filter = (
        # for ordinary fields
        ('day__number', DropdownFilter),
        ('author__username', DropdownFilter),
        # # for choice fields
        # ('a_choicefield', ChoiceDropdownFilter),
        # # for related fields
        # ('a_foreignkey_field', RelatedDropdownFilter),
    )

    list_display = ['title', 'author', 'day', 'anything_else']

admin.site.register(Post, PostAdmin)