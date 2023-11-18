from rest_framework import serializers
from datetime import timedelta

from ..models import MyUser, BloodNeeded, UserBloodDonate


class MyUserModelSerializer(serializers.ModelSerializer):
    height = serializers.FloatField(required=True)
    weight = serializers.FloatField(required=True)

    class Meta:
        model = MyUser
        fields = [
            "email",
            "name",
            "age",
            "gender",
            "blood_group",
            "height",
            "weight",
            "bmi",
            "mobile_number",
            "address",
            "is_ready_to_donate",
            "image",
            "date_of_birth",
            "password",
        ]
        # exclude = [
        #     "groups",
        #     "user_permissions",
        #     "last_login",
        #     "is_active",
        #     "is_admin",
        #     "is_superuser",
        # ]
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
            "bmi": {
                "read_only": True,
            },
            "is_ready_to_donate": {
                "read_only": True,
            },
        }

    def foot_to_meter(self, height):
        """
        convert foot to meters.
        1 foot = 0.3048 meters
        """
        return height * 0.3048

    def calculate_bmi(self, height, width) -> float:
        """
        calculate BMI
        BMI = weight_in_Kg/pow((height_in_meters), 2)
        """
        return width / (height * height)

    def get_age_limit(self, date_of_birth):
        donate_age_limit = date_of_birth + timedelta(days=60 * 365)
        return donate_age_limit.year

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.max_age = self.get_age_limit(validated_data.get("date_of_birth"))
        height = validated_data.get("height")  # foot.inch
        height_meters = self.foot_to_meter(height)
        user.bmi = self.calculate_bmi(
            height_meters,
            validated_data.get("weight"),
        )
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.name = validated_data.get("name", instance.name)

        instance.blood_group = validated_data.get(
            "blood_group",
            instance.blood_group,
        )
        instance.gender = validated_data.get("gender", instance.gender)
        instance.height = validated_data.get("height", instance.height)
        instance.weight = validated_data.get("weight", instance.weight)
        instance.bmi = self.calculate_bmi(
            self.foot_to_meter(instance.height), instance.weight
        )
        instance.mobile_number = validated_data.get(
            "mobile_number", instance.mobile_number
        )
        instance.address = validated_data.get("address", instance.address)
        instance.image = validated_data.get("image", instance.image)
        instance.date_of_birth = validated_data.get(
            "date_of_birth", instance.date_of_birth
        )
        instance.max_age = self.get_age_limit(instance.date_of_birth)

        password = validated_data.get("password", None)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class BloodNeededModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodNeeded
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["blood_recipients"] = MyUserModelSerializer(
            instance=instance.blood_recipients
        ).data
        return representation


class UserBloodDonateAddSerializer(serializers.ModelSerializer):
    blood_donner = serializers.EmailField(read_only=True)

    class Meta:
        model = UserBloodDonate
        fields = "__all__"


class UserBloodDonateSerializer(serializers.ModelSerializer):
    blood_donner = serializers.EmailField(read_only=True)
    blood_recipients = MyUserModelSerializer()

    class Meta:
        model = UserBloodDonate
        fields = "__all__"
