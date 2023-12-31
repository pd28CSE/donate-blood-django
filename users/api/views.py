from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from ..models import MyUser, BloodNeeded, UserBloodDonate, UserDeviceToken
from .serializers import (
    MyUserModelSerializer,
    BloodNeededModelSerializer,
    UserBloodDonateAddSerializer,
    UserBloodDonateSerializer,
    UserDeviceTokenModelSerializer,
)
from .permissions.permissions import IsOwner


class CreateUserApiView(CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserModelSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(
    #         serializer.data,
    #         status=status.HTTP_201_CREATED,
    #         headers=headers,
    #     )


class BloodDonnerListAPIView(ListAPIView):
    def get_minimum_year():
        today = datetime.today() - timedelta(days=18 * 365)
        return "{}-{}-{}".format(today.year, today.month, today.day)

    queryset = MyUser.objects.filter(
        Q(bmi__gte=17.0)
        & Q(max_age__gte=datetime.today().year)
        & Q(
            Q(gender="Male") & Q(date_of_birth__lte=get_minimum_year())
            | Q(gender="Female") & Q(date_of_birth__lte=get_minimum_year())
        )
    )
    serializer_class = MyUserModelSerializer


class UserProfileUpdateAPIView(UpdateAPIView):
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    lookup_field = "email"
    lookup_url_kwarg = "email"
    queryset = MyUser.objects.all()
    serializer_class = MyUserModelSerializer


class BloodNeededListAPIView(ListAPIView):
    queryset = BloodNeeded.objects.filter(is_visible=True).order_by("-id")
    serializer_class = BloodNeededModelSerializer


class BloodNeededCreateAPIView(CreateAPIView):
    queryset = BloodNeeded.objects.all().order_by("-id")
    serializer_class = BloodNeededModelSerializer


class BloodNeededUpdateAPIView(UpdateAPIView):
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwner,
    ]
    lookup_field = "id"
    lookup_url_kwarg = "id"
    queryset = BloodNeeded.objects.all().order_by("-id")
    serializer_class = BloodNeededModelSerializer


class BloodDonnerDonateListView(ListAPIView):
    serializer_class = UserBloodDonateSerializer

    def get_queryset(self):
        queryset = UserBloodDonate.objects.filter(
            blood_donner__email=self.kwargs["email"]
        ).order_by("-id")
        return queryset


class UserBloodDonateAPIView(CreateAPIView):
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserBloodDonateAddSerializer
    lookup_field = "email"

    def getNextDate(self):
        return datetime.now() + timedelta(days=90)

    def perform_create(self, serializer):
        blood_donner = self.request.user
        """
        in `UserBloodDonateAddSerializer` serializers `blood_donner`
        is read_only that's why there is need to pass `blood_donner`
        instance for create `UserBloodDonate`.
        like `serializer.save(blood_donner=blood_donner)`
        """
        _ = serializer.save(blood_donner=blood_donner)
        blood_donner.next_donation_remaining_days = self.getNextDate()

        if blood_donner.is_ready_to_donate:
            blood_donner.is_ready_to_donate = False
        blood_donner.save()

    def create(self, request, *args, **kwargs):
        request_data = request.data
        request_data._mutable = True
        blood_recipients_email = request_data.pop("bloodRecipients", None)

        if blood_recipients_email is not None:
            try:
                bloodRecipients = MyUser.objects.get(
                    email=blood_recipients_email[0],
                )
            except MyUser.DoesNotExist:
                return Response(
                    {"bloodRecipients": "bloodRecipients not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            request_data["bloodRecipients"] = bloodRecipients.pk
        request_data._mutable = False
        """
        in `UserBloodDonateAddSerializer` serializer `bloodDonner` is
        the read_only field, that's why self.get_serializer(data=request_data)
        takes write_only field exclude all read_only fields. In default
        self.perform_create() function when trying to create a UserBloodDonate
        object without bloodDonner field it raises an error. Because creating
        a UserBloodDonate object there is required all fields.
        """
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class DeviceTokenAPIView(APIView):
    serializer_class = UserDeviceTokenModelSerializer
    model = UserDeviceToken
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_device_token(self, user):
        return get_object_or_404(self.model, user=user)

    def get(self, request, *args, **kwargs):
        user_device_token = self.get_device_token(request.user)
        serializer = self.serializer_class(instance=user_device_token).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data={
                "device_token": request.data.get("device_token"),
                "user": request.user.pk,
            },
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request, *args, **kwargs):
        user_device_token = self.get_device_token(request.user)
        serializer = self.serializer_class(
            instance=user_device_token,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
