from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.html import mark_safe
from datetime import datetime, timedelta

from . manager import MyUserManager


class MyUser(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(
        verbose_name='full name',
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
            ('A+', 'A RhD Positive'),
            ('A-', 'A RhD Negative'),
            ('B+', 'B RhD Positive'),
            ('B-', 'B RhD Negative'),
            ('O+', 'O RhD Positive'),
            ('O-', 'O RhD Negative'),
            ('AB+', 'AB RhD Positive'),
            ('AB-', 'AB RhD Negative'),
        ],
        blank=False,
        null=False,
    )
    gender = models.CharField(
        max_length=2,
        choices=[
            ('M', 'Male'),
            ('F', 'Female')
        ],
    )
    date_of_birth = models.DateField(help_text='YYYY-MM-DD formate.')
    max_age = models.IntegerField(default=0)
    height = models.FloatField(help_text='Height in Foot.Inch, For Example: 5.7', default=0.0)
    weight = models.FloatField( help_text='Weight in kilograms', default=0.0)
    bmi = models.FloatField(default=0.0)
    is_ready_to_donate = models.BooleanField(
        verbose_name= 'is interested to donate blood',
        default=False, 
        help_text='Are you interested to donate blood?'
    )
    next_donation_remaining_days = models.DateField(auto_now_add=True)
    mobile_number = models.TextField(
        verbose_name='mobile number',
        max_length=20,
        blank=False,
        null=False,
    )
    address = models.TextField(
        verbose_name='present address',
        max_length=255,
        blank=False,
        null=False,
    )
    image = models.ImageField(upload_to='profile-pictures')
    
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "mobile_number", "blood_group", "address", "date_of_birth"]

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
            return mark_safe("<img src='{}' alt='{}' width='25%'/>".format(self.image.url, self.image.name))

    @property
    def age(self):
        "calculate age based on date_of_birth"
        # need to efficient
        today = datetime.today()
        year =  today.year + (today.month + (today.day/30.0))/12.0
        # print(today.strftime("%Y-%m-%d"))
        birth =  self.date_of_birth.year + (self.date_of_birth.month + (self.date_of_birth.day/30.0))/12.0
        return f"%.1f" %(year - birth)
    
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


class UserBloodDonate(models.Model):
    bloodDoner = models.ForeignKey(MyUser, related_name="donner", on_delete=models.CASCADE)
    bloodRecipients = models.ForeignKey(MyUser, related_name="recipients", on_delete=models.CASCADE)
    place = models.CharField(max_length=200, blank=False, null=False)
    donateDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Blood Donation List'
        verbose_name_plural = "Blood Donation List"

    def __str__(self):
        return self.bloodDoner.email

