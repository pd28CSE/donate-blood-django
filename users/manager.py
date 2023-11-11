from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, name, email, date_of_birth, mobile_number, address,blood_group, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not name:
            raise ValueError("Users must have name")
        if not email:
            raise ValueError("Users must have an email address")
        if not mobile_number:
            raise ValueError("Users must have a mobile number")
        if not address:
            raise ValueError("Users must have an address")
        if not date_of_birth:
            raise ValueError("Date of birth must be needed")
        if not blood_group:
            raise ValueError("Users must have a blood group")
        
        user = self.model(
            name=name.title(),
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            mobile_number=mobile_number,
            address=address,
            blood_group=blood_group,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, date_of_birth, mobile_number, address, blood_group, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            name=name,
            email=email,
            date_of_birth=date_of_birth,
            mobile_number=mobile_number,
            blood_group=blood_group,
            address=address,
            password=password,
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

