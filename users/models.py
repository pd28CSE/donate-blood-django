from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.html import mark_safe

from datetime import datetime

from .utils import fields, helper
from .manager import MyUserManager


class UserDeviceToken(models.Model):
    user = models.OneToOneField(
        "MyUser",
        unique=True,
        on_delete=models.CASCADE,
        related_name="device",
    )
    device_token = models.UUIDField(max_length=255, blank=False, null=False)

    def __str__(self):
        return self.user.email


class MyUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(
        verbose_name="full name",
        max_length=100,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    blood_group = models.CharField(
        max_length=3,
        choices=[
            ("A+", "A RhD Positive"),
            ("A-", "A RhD Negative"),
            ("B+", "B RhD Positive"),
            ("B-", "B RhD Negative"),
            ("O+", "O RhD Positive"),
            ("O-", "O RhD Negative"),
            ("AB+", "AB RhD Positive"),
            ("AB-", "AB RhD Negative"),
        ],
        blank=False,
        null=False,
    )
    gender = models.CharField(
        max_length=7,
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
        ],
    )
    date_of_birth = models.DateField(help_text="YYYY-MM-DD formate.")
    max_age = models.IntegerField(default=0)
    height = models.FloatField(
        help_text="Height in Foot.Inch, For Example: 5.7",
        default=0.0,
    )
    weight = models.FloatField(help_text="Weight in kilograms", default=0.0)
    bmi = models.FloatField(default=0.0)
    is_ready_to_donate = models.BooleanField(
        verbose_name="is interested to donate blood",
        default=False,
        help_text="Are you interested to donate blood?",
    )
    next_donation_remaining_days = models.DateField(auto_now_add=True)
    mobile_number = models.TextField(
        verbose_name="mobile number",
        max_length=20,
        blank=False,
        null=False,
    )
    address = models.TextField(
        verbose_name="present address",
        max_length=255,
        blank=False,
        null=False,
    )
    image = models.ImageField(
        upload_to="profile-pictures",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "name",
        "mobile_number",
        "blood_group",
        "address",
        "date_of_birth",
    ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @property
    def preview_image(self):
        "Show the user profile picture"
        if not self.image:
            return mark_safe("<img src='' alt='No Image' width='25%'/>")
        else:
            return mark_safe(
                "<img src='{}' alt='{}' width='25%'/>".format(
                    self.image.url, self.image.name
                )
            )

    @property
    def age(self):
        "calculate age based on date_of_birth"
        # TODO: need to efficient
        today = datetime.today()
        year = today.year + (today.month + (today.day / 30.0)) / 12.0
        # print(today.strftime("%Y-%m-%d"))
        birth = (
            self.date_of_birth.year
            + (self.date_of_birth.month + (self.date_of_birth.day / 30.0)) / 12.0
        )

        return "%.1f" % (year - birth)

    # @property
    # def next_donation_remaining_days_ab(self):
    #     # if '09-12-2023' <= datetime.today():
    #     #     # return f'{datetime.today()}';
    #     #     return '+'
    #     # else:
    #     #     # return '{}'.format(str(self.next_donation_remaining_days) - datetime.today())
    #     return datetime.today()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class BloodNeeded(models.Model):
    blood_recipients = models.ForeignKey(
        MyUser,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="blood_needs",
    )
    blood_group = models.CharField(
        choices=fields.BloodGroups.choices,
        max_length=5,
        blank=False,
        null=False,
    )
    place = models.CharField(
        max_length=255,
        blank=False,
        null=False,
    )
    coordinates = models.JSONField(
        blank=True,
        null=True,
        default=helper.get_coordinates,
    )
    date_time = models.DateTimeField(blank=False, null=False)
    hospital_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blood Needed"
        verbose_name_plural = "Blood Needs"

    def __str__(self) -> str:
        return "{} needs {}".format(
            self.blood_recipients.email,
            self.blood_group,
        )


class UserBloodDonate(models.Model):
    blood_recipients = models.ForeignKey(
        BloodNeeded,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="user_blood_donates",
    )
    blood_donner = models.ForeignKey(
        MyUser,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="user_blood_donates",
    )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blood Donation List"
        verbose_name_plural = "Blood Donation List"

    def __str__(self):
        return "{} ==> {}".format(
            self.blood_donner.email,
            self.blood_recipients.blood_recipients.email,
        )
