from django.db import models


class BloodGroups(models.TextChoices):
    AP = ("A+", "A RhD Positive")
    AN = ("A-", "A RhD Negative")
    BP = ("B+", "B RhD Positive")
    BN = ("B-", "B RhD Negative")
    OP = ("O+", "O RhD Positive")
    ON = ("O-", "O RhD Negative")
    ABP = ("AB+", "AB RhD Positive")
    ABN = ("AB-", "AB RhD Negative")
