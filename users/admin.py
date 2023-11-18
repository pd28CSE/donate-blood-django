from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html

from .models import MyUser, UserBloodDonate, BloodNeeded
from .forms import UserChangeForm, UserCreationForm


# Register your models here.


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    def profile_picture(self, obj):
        if not obj.image:
            return format_html('<img src="" alt="No Image" width="50%" />')
        return format_html(
            '<img src="{}" width="50%" />'.format(obj.image.url),
        )

    # rename the profile_picture column name on admin panel
    profile_picture.short_description = "Profile Picture View"

    def get_name(self, obj):
        return obj.name.title()

    get_name.short_description = "Name"

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = [
        "email",
        "name",
        "mobile_number",
        "age",
        "date_of_birth",
        "address",
        "blood_group",
        "is_active",
        "is_admin",
        "is_superuser",
        "preview_image",
    ]
    list_filter = [
        "address",
        "blood_group",
    ]
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "email",
                    "password",
                ]
            },
        ),
        (
            "Personal Information",
            {
                "classes": [
                    "collapse"
                ],  # for show and hide the "Personal info" section
                "fields": [
                    "name",
                    "mobile_number",
                    "blood_group",
                    "height",
                    "weight",
                    "bmi",
                    "gender",
                    "is_ready_to_donate",
                    "date_of_birth",
                    "max_age",
                    "address",
                    "image",
                    "profile_picture",
                ],
            },
        ),
        (
            "Permissions",
            {
                "fields": [
                    "is_active",
                    (
                        "is_admin",
                        "is_superuser",
                    ),  # is_admin and is_superuser is in the same row.
                ]
            },
        ),
        (
            "Important Dates",
            {
                "fields": [
                    "last_login",
                    "next_donation_remaining_days",
                ],
            },
        ),
    ]
    readonly_fields = [
        "profile_picture",
        "next_donation_remaining_days",
    ]
    """
    add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    overrides get_fieldsets to use this attribute when creating
    a user using admin panel.
    """
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],  # for css
                "fields": [
                    "name",
                    "email",
                    "password1",
                    "password2",
                ],
            },
        ),
        (
            "Personal info",
            {
                "classes": ["wide"],  # for css
                "fields": [
                    "mobile_number",
                    "blood_group",
                    "date_of_birth",
                    "address",
                    "image",
                ],
            },
        ),
    ]
    search_fields = [
        "email",
        "address",
        "blood_group",
    ]
    ordering = [
        "email",
    ]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


@admin.register(UserBloodDonate)
class UserBloodDonateAdmin(admin.ModelAdmin):
    list_display = [
        "blood_donner",
        "blood_recipients",
        "place",
    ]
    fields = [
        "blood_donner",
        "blood_recipients",
        "place",
    ]
    list_filter = [
        "blood_donner",
        "blood_recipients",
    ]
    search_fields = [
        "blood_donner",
    ]


# admin.site.register(UserBloodDonate, UserBloodDonateAdmin)

admin.site.register(BloodNeeded)
